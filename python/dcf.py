import numpy as np
import moment as moment
import pandas as pd

class DCF:
    def __init__(self, mrqData, cagr=0.3, targetEbitMargin=0.3):
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
        df.loc[0, 'nol'] = 0
        df.loc[0, 'investedCapital'] = d.investedCapital

        df.loc[0, 'roic'] = df.loc[0, 'ebitAfterTax'] / df.loc[0, 'investedCapital']
        df.loc[0, 'wacc'] = d.initialCostOfCapital
        df.loc[0, 'cumDiscountFactor'] = 1 / (1 + d.initialCostOfCapital)

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
            df.loc[i, 'ebitMargin'] = self.constantEndConvergence(c.yearOfEbitConvergence, i, d.ebit / d.revenue,
                                                                  d.targetEbitMargin)
            df.loc[i, 'taxRate'] = self.constantStartConvergence(c.yearsToTaxConvergence, i, d.effectiveTaxRate,
                                                                 d.marginalTaxRate)

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
                df.loc[i, 'ebitAfterTax'] = df.loc[i, 'ebit'] if df.loc[i, 'ebit'] < df.loc[i, 'nol'] else (df.loc[
                                                                                                                i, 'ebit'] -
                                                                                                            df.loc[
                                                                                                                i, 'nol']) * (
                                                                                                               1 -
                                                                                                               df.loc[
                                                                                                                   i, 'taxRate'])

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

        print(df.to_string())
        print(discountFactor)
        print("terminalCashFlow", terminalCashFlow)
        print("terminalCostOfCapital", terminalCostOfCapital)
        print("terminalRevenueGrowth", terminalRevenueGrowth)
        print("terminalValue", terminalValue)
        print("pvTerminalValue", pvTerminalValue)
        print("WACC", d.initialCostOfCapital, d.targetCostOfCapital)
        print("pvFcff", pvFcff)

        def calcOperatingAssets(presentValues, probabilityOfFailure=0.0, proceedsIfFirmFails=0):
            return presentValues * (1 - probabilityOfFailure) + proceedsIfFirmFails * probabilityOfFailure

        valueOfOperatingAssets = calcOperatingAssets(pvFcff + pvTerminalValue)
        valueOfEquity = valueOfOperatingAssets - d.debt
        valueOfEquity = valueOfEquity - d.minorityInterests
        valueOfEquity = valueOfEquity + d.cash
        valueOfEquity = valueOfEquity + d.nonOpAssets
        valueOfEquityInCommon = valueOfEquity - d.optionsValue
        valuePerShare = valueOfEquityInCommon / d.numberShares

        print("valueOfOperatingAssets", valueOfOperatingAssets)
        print("Value of equity", valueOfEquity)
        print("Value per share", valuePerShare)
        return valuePerShare


class DcfParameters:
    def __init__(self, mrqData, cagr, targetEbitMargin):
        self.riskFreeRate = .0225
        self.stockPrice = 34
        self.cagr = cagr
        self.targetCagr = self.riskFreeRate
        self.targetEbitMargin = targetEbitMargin
        self.salesToCapitalRatio = 1.5
        self.initialCostOfCapital = .09
        self.targetCostOfCapital = self.riskFreeRate + 0.045
        self.effectiveTaxRate = .15
        self.marginalTaxRate = .25

        # self.revenue = 145.883
        self.revenue = mrqData['revenue'][-4:].sum() / 1000000
        # self.ebit = -17.967
        self.ebit = mrqData['ebit'][-4:].sum() / 1000000
        # self.numberShares = 60.05
        self.numberShares = mrqData['shareswadil'][-1:].sum() / 1000000
        # self.cash = 59
        self.cash = mrqData['cashnequsd'][-1:].sum() / 1000000
        # =IF('Input sheet'!B15="Yes",IF('Input sheet'!B14="Yes",'Input sheet'!B12+'Input sheet'!B13-'Input sheet'!B16+'Operating lease converter'!F33+'R& D converter'!D35,'Input sheet'!B12+'Input sheet'!B13-'Input sheet'!B16+'Operating lease converter'!F33),IF('Input sheet'!B14="Yes",'Input sheet'!B12+'Input sheet'!B13-'Input sheet'!B16+'R& D converter'!D35,'Input sheet'!B12+'Input sheet'!B13-'Input sheet'!B16))
        self.debt = mrqData['debtusd'][-1:].sum() / 1000000

        self.bookValueEquity = mrqData['equity'][-1:].sum() / 1000000
        print("Equity: %s", self.bookValueEquity)
        print("Debt: %s", self.debt)
        print("Cash: %s", self.cash)
        self.investedCapital = self.bookValueEquity + self.debt - self.cash
        # investedCapital2 = mrqData['invcap'][-1:].sum() / 1000000
        self.minorityInterests = 0
        self.optionsValue = 0
        self.nonOpAssets = 0


class ConvergenceParameters:
    def __init__(self):
        self.yearsToTaxConvergence = 5
        self.taxConvergenceStartsAfterXYears = 5
        self.yearOfEbitConvergence = 3
        self.constantYearsOfWaccBeforeConvergence = 5
        self.yearOfRevenueGrowthConvergence = 5


class DcfAdjustments:
    def __init__(self):
        pass

    def researchAndDevelopment(self, mrqData):
        yearsToAmortise = 3
        rndValues = np.array([])
        print("Len", len(mrqData['rnd']))
        print("Len", mrqData['rnd'])
        if ((yearsToAmortise * 4) > len(mrqData)):
            print("Warning: not enough data to complete amortisation schedule. Years to amortise is:", yearsToAmortise,
                  "but only ", len(mrqData),
                  "quarters available. Only available data will be used.")

        for i in range(0, yearsToAmortise):
            startIndex = (i + 1) * 4
            endIndex = i * 4
            rndValues = np.append(rndValues, mrqData['rnd'][-startIndex:-endIndex].sum())

    def operatingLeases(self):
        pass


