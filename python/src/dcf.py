import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DcfParameters:
    def __init__(self, mrqData, cagr, targetEbitMargin):
        self.adjustments = DcfAdjustments(mrqData)
        self.riskFreeRate = .0225
        self.stockPrice = 25
        self.cagr = cagr
        self.targetCagr = self.riskFreeRate
        self.targetEbitMargin = targetEbitMargin
        self.salesToCapitalRatio = 1.5
        self.initialCostOfCapital = .09
        self.targetCostOfCapital = self.riskFreeRate + 0.045
        self.effectiveTaxRate = .15
        self.marginalTaxRate = .24
        opinc__sum = mrqData['opinc'].sum()
        self.nol = abs(opinc__sum) if opinc__sum < 0 else 0

        self.revenue = mrqData['revenue'][-4:].sum() / 1000000

        opExpAdjustment, debtAdjustment = self.adjustments.operatingLeases([])
        rndAdjustment = self.adjustments.researchAndDevelopment()
        self.ebit = mrqData['ebit'][-4:].sum() / 1000000 + opExpAdjustment + rndAdjustment

        self.numberShares = mrqData['shareswadil'][-1:].sum() / 1000000
        self.cash = mrqData['cashnequsd'][-1:].sum() / 1000000
        self.investmentsc = mrqData['investmentsc'][-1:].sum() / 1000000
        self.debt = mrqData['debtusd'][-1:].sum() / 1000000

        self.bookValueEquity = mrqData['equity'][-1:].sum() / 1000000
        logger.debug("Equity: %s:" % self.bookValueEquity)
        logger.debug("Debt: %s:" % self.debt)
        logger.debug("Cash: %s:" % self.cash)
        logger.debug("Short term investments: %s:" % self.investmentsc)
        self.investedCapital = self.bookValueEquity + self.debt + debtAdjustment - self.cash - self.investmentsc

        # investedCapital2 = mrqData['invcap'][-1:].sum() / 1000000
        self.minorityInterests = 0
        self.optionsValue = 0
        self.nonOpAssets = 0


class DCF:
    def __init__(self, mrqData, cagr=0.3, targetEbitMargin=0.3):
        logger.debug("Warning: Have you adjusted the inputs to the DCF? In particular, sales to capital ratio and tax rates?")
        self.dcfParameters = DcfParameters(mrqData, cagr, targetEbitMargin)
        self.convergenceParameters = ConvergenceParameters()
        self.totalYears = 10  # This probably shouldnt be changed much

    def constantStartConvergence(self, constantYears, i, initial, target):
        adjustment = (target - initial) / (self.totalYears - constantYears)
        if i > constantYears:
            if (target < initial):
                return max(target, initial + (i - constantYears) * adjustment)
            else:
                return min(target, initial + (i - constantYears) * adjustment)
        else:
            return initial

    def constantEndConvergence(self, yearsToConverge, i, initial, target):
        adjustment = (target - initial) / yearsToConverge
        if i < yearsToConverge:
            return initial + i * adjustment
        else:
            return target

    def calc(self):
        d = self.dcfParameters
        c = self.convergenceParameters
        df = self.initialiseInitialParameters(d)

        for i in range(df.index.size):
            if i == 0:
                continue
            df.loc[i, 'revenueGrowth'] = self.constantStartConvergence(c.yearOfRevenueGrowthConvergence, i, d.cagr,
                                                                       d.targetCagr)
            df.loc[i, 'wacc'] = self.constantStartConvergence(c.constantYearsOfWaccBeforeConvergence, i,
                                                              d.initialCostOfCapital, d.targetCostOfCapital)
            df.loc[i, 'cumDiscountFactor'] = (
                df.loc[i - 1, 'cumDiscountFactor'] * (1 / (1 + df.loc[i, 'wacc']))) if i > 1 else (
                1 / (1 + df.loc[i, 'wacc']))
            df.loc[i, 'ebitMargin'] = self.constantEndConvergence(c.yearOfEbitConvergence, i, d.ebit / d.revenue, d.targetEbitMargin)
            df.loc[i, 'taxRate'] = self.constantStartConvergence(c.yearsToTaxConvergence, i, d.effectiveTaxRate, d.marginalTaxRate)

            df.loc[i, 'revenue'] = (df.loc[i - 1, 'revenue']) * (1 + df.loc[i, 'revenueGrowth'])
            df.loc[i, 'ebit'] = df.loc[i, 'revenue'] * df.loc[i, 'ebitMargin']

            # TODO: Reinvestment for terminal year is different
            df.loc[i, 'reinvestment'] = (df.loc[i, 'revenue'] - df.loc[i - 1, 'revenue']) / d.salesToCapitalRatio
            df.loc[i, 'investedCapital'] = (df.loc[i - 1, 'investedCapital'] + df.loc[i, 'reinvestment'])

            # Net Operating Loss
            if df.loc[i, 'ebit'] < 0:
                df.loc[i, 'nol'] = (df.loc[i - 1, 'nol'] - df.loc[i, 'ebit'])
            else:
                df.loc[i, 'nol'] = max(df.loc[i - 1, 'nol'] - df.loc[i, 'ebit'], 0)

            if df.loc[i, 'ebit'] < 0:
                df.loc[i, 'ebitAfterTax'] = df.loc[i, 'ebit']  # No tax paid
            else:
                df.loc[i, 'ebitAfterTax'] = df.loc[i, 'ebit'] if df.loc[i, 'ebit'] < df.loc[i - 1, 'nol'] \
                    else df.loc[i, 'ebit'] - (df.loc[i, 'ebit'] - df.loc[i - 1, 'nol']) * (df.loc[i, 'taxRate'])

            df.loc[i, 'fcff'] = df.loc[i, 'ebitAfterTax'] - df.loc[i, 'reinvestment']

        df['roic'] = df['ebitAfterTax'] / df['investedCapital']
        df['pvFcff'] = df['cumDiscountFactor'] * df['fcff']

        def calculateTerminalYear(df):
            useEffectiveTaxRateAsTerminal = False
            i = self.totalYears + 1
            terminalRoic = df.loc[i, 'wacc']

            df.loc[i, 'roic'] = terminalRoic
            df.loc[i, 'taxRate'] = d.marginalTaxRate if useEffectiveTaxRateAsTerminal == False else d.effectiveTaxRate
            df.loc[i, 'ebitAfterTax'] = df.loc[i, 'ebit'] * (1 - df.loc[i, 'taxRate'])
            df.loc[i, 'reinvestment'] = 0 if df.loc[i, 'revenueGrowth'] < 0 else \
                df.loc[i, 'revenueGrowth'] / df.loc[i, 'roic'] * df.loc[i, 'ebitAfterTax']
            df.loc[i, 'fcff'] = df.loc[i, 'ebitAfterTax'] - df.loc[i, 'reinvestment']

        calculateTerminalYear(df)

        # TODO: ROIC for terminal year is different

        terminalCashFlow = df[-1:]['fcff']
        terminalCostOfCapital = df[-1:]['wacc']
        terminalRevenueGrowth = df[-1:]['revenueGrowth']
        terminalValue = terminalCashFlow / (terminalCostOfCapital - terminalRevenueGrowth)
        discountFactor = df[-2:-1]['cumDiscountFactor'].sum()
        pvTerminalValue = terminalValue * discountFactor
        pvFcff = df[:-1]['pvFcff'].sum()

        logger.debug(df.to_string())
        logger.debug(discountFactor)
        logger.debug("terminalCashFlow: %s" % terminalCashFlow)
        logger.debug("terminalCostOfCapital: %s" % terminalCostOfCapital)
        logger.debug("terminalRevenueGrowth: %s" % terminalRevenueGrowth)
        logger.debug("terminalValue: %s" % terminalValue)
        logger.debug("pvTerminalValue: %s" % pvTerminalValue)
        logger.debug("WACC: %s -> %s" % (d.initialCostOfCapital, d.targetCostOfCapital))
        logger.debug("pvFcff: %s" % pvFcff)

        def calcOperatingAssets(presentValues, probabilityOfFailure=0.0, proceedsIfFirmFails=0):
            return presentValues * (1 - probabilityOfFailure) + proceedsIfFirmFails * probabilityOfFailure

        valueOfOperatingAssets = calcOperatingAssets(pvFcff + pvTerminalValue)
        valueOfEquity = valueOfOperatingAssets - d.debt
        valueOfEquity = valueOfEquity - d.minorityInterests
        valueOfEquity = valueOfEquity + d.cash
        valueOfEquity = valueOfEquity + d.nonOpAssets
        valueOfEquityInCommon = valueOfEquity - d.optionsValue
        valuePerShare = valueOfEquityInCommon / d.numberShares

        logger.debug("valueOfOperatingAssets: %s" % valueOfOperatingAssets)
        logger.debug("Value of equity: %s" % valueOfEquity)
        logger.debug("Value per share: %s" % valuePerShare)
        return valuePerShare

    def initialiseInitialParameters(self, d):
        df = pd.DataFrame(index=[i for i in range(self.totalYears + 2)],  # 2 extras for the inital and terminal years
                          columns=['i', 'revenueGrowth', 'revenue', 'ebitMargin', 'ebit', 'taxRate', 'ebitAfterTax',
                                   'reinvestment', 'fcff', 'nol', 'wacc', 'cumDiscountFactor',
                                   'pvFcff', 'investedCapital'])

        df['i'] = df.index
        df['salesToCapitalRatio'] = d.salesToCapitalRatio
        df.loc[0, 'revenue'] = d.revenue

        df.loc[0, 'ebit'] = d.ebit
        df.loc[0, 'ebitMargin'] = d.ebit / d.revenue  # ebit / revenue
        df.loc[0, 'taxRate'] = d.effectiveTaxRate
        df.loc[0, 'ebitAfterTax'] = d.ebit if d.ebit < 0 else d.ebit * (1 - d.effectiveTaxRate)
        df.loc[0, 'nol'] = d.nol
        df.loc[0, 'investedCapital'] = d.investedCapital
        df.loc[0, 'roic'] = df.loc[0, 'ebitAfterTax'] / df.loc[0, 'investedCapital']
        df.loc[0, 'wacc'] = d.initialCostOfCapital
        df.loc[0, 'cumDiscountFactor'] = 1 / (1 + d.initialCostOfCapital)
        return df




class ConvergenceParameters:
    def __init__(self):
        self.yearsToTaxConvergence = 5
        self.taxConvergenceStartsAfterXYears = 5
        self.yearOfEbitConvergence = 6
        self.constantYearsOfWaccBeforeConvergence = 5
        self.yearOfRevenueGrowthConvergence = 5


class DcfAdjustments:
    def __init__(self, mrqData):
        # iloc[::-1] reverses the dataframe
        logger.debug(mrqData.to_string())
        self.rnd = mrqData['rnd'].iloc[::-1].fillna(0).reset_index()
        self.rnd = mrqData['rnd'].iloc[::-1].fillna(0).reset_index()
        logger.debug(self.rnd)
        pass

    def researchAndDevelopment(self):
        yearsToAmortise = 3
        if ((yearsToAmortise * 4) > len(self.rnd)):
            logger.debug("Warning: not enough data to complete amortisation schedule. Years to amortise is: %d "
                         "but only %d quarters available. Only available data will be used." % (yearsToAmortise, len(self.rnd)))

        rndValues = self.rnd.groupby(self.rnd.index // 4 * 4).sum().reset_index()
        logger.debug(rndValues)
        rndValues['unamortised'] = 1 - (rndValues['index'] / 4) * 1 / yearsToAmortise
        rndValues['unamortisedAmt'] = rndValues['unamortised'] * rndValues['rnd']
        rndValues['amortisation'] = rndValues['rnd'] / yearsToAmortise
        logger.debug(rndValues)
        amortisationOfResearchAssetForCurrentYear = rndValues['amortisation'][1:].sum()
        currentYearRandD = rndValues['rnd'][0:1].sum()
        logger.debug(amortisationOfResearchAssetForCurrentYear)
        logger.debug(currentYearRandD)
        adjustmentToOperatingIncome = currentYearRandD - amortisationOfResearchAssetForCurrentYear
        logger.debug(adjustmentToOperatingIncome)
        # =IF('Input sheet'!B14="Yes",'Input sheet'!B10+'R& D converter'!D39,'Input sheet'!
        return adjustmentToOperatingIncome / 1000000

    def operatingLeases(self, operatingLeaseExpenses):
        if len(operatingLeaseExpenses) == 0: return 0, 0
        preTaxCostOfDebt = .2085
        additionalYearsToDepreciate = 0

        def pv(i, v):
            pow1 = pow((1 + preTaxCostOfDebt), i)
            logger.debug("PV: %s" % i, v, pow1, v / pow1)
            return v / pow1

        presentValues = [pv(i, val) for i, val in enumerate(operatingLeaseExpenses) if True]
        presentValue = sum(presentValues[1:])
        straightLineDepn = presentValue / len(operatingLeaseExpenses) + additionalYearsToDepreciate
        adjustmentToOperatingEarnings = operatingLeaseExpenses[0] - straightLineDepn

        logger.debug(presentValues, presentValue, adjustmentToOperatingEarnings)

        return adjustmentToOperatingEarnings, presentValue
