from datetime import datetime
import time
from multiprocessing.pool import Pool

import matplotlib
import moment as moment
import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np
import pandas as pd

import graphs
from dataloader import DataLoader
from dcf import DCF
import logging
import tabulate as tabulate

matplotlib.use('TkAgg')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Quandl headings
quandl_headings = ['ticker', 'dimension', 'calendardate', 'datekey', 'reportperiod', 'lastupdated', 'accoci', 'assets',
                   'assetsavg', 'assetsc', 'assetsnc', 'assetturnover', 'bvps',
                   'capex', 'cashneq', 'cashnequsd', 'cor', 'consolinc', 'currentratio', 'de', 'debt', 'debtc',
                   'debtnc', 'debtusd', 'deferredrev', 'depamor', 'deposits',
                   'divyield', 'dps', 'ebit', 'ebitda', 'ebitdamargin', 'ebitdausd', 'ebitusd', 'ebt', 'eps', 'epsdil',
                   'epsusd', 'equity', 'equityavg', 'equityusd', 'ev',
                   'evebit', 'evebitda', 'fcf', 'fcfps', 'fxusd', 'gp', 'grossmargin', 'intangibles', 'intexp',
                   'invcap', 'invcapavg', 'inventory', 'investments', 'investmentsc',
                   'investmentsnc', 'liabilities', 'liabilitiesc', 'liabilitiesnc', 'marketcap', 'ncf', 'ncfbus',
                   'ncfcommon', 'ncfdebt', 'ncfdiv', 'ncff', 'ncfi', 'ncfinv',
                   'ncfo', 'ncfx', 'netinc', 'netinccmn', 'netinccmnusd', 'netincdis', 'netincnci', 'netmargin', 'opex',
                   'opinc', 'payables', 'payoutratio', 'pb', 'pe', 'pe1',
                   'ppnenet', 'prefdivis', 'price', 'ps', 'ps1', 'receivables', 'retearn', 'revenue', 'revenueusd',
                   'rnd', 'roa', 'roe', 'roic', 'ros', 'sbcomp', 'sgna',
                   'sharefactor', 'sharesbas', 'shareswa', 'shareswadil', 'sps', 'tangibles', 'taxassets', 'taxexp',
                   'taxliabilities', 'tbvps', 'workingcapital']


class Calculator:
    def __init__(self):
        pass

    def periodChange(self, columns, source):
        df = pd.DataFrame()
        for column in columns:
            df[column] = source[column]
            df[column + '_ttm'] = source[column].rolling(4).sum()
            df[column + '_qchange'] = source[column].diff()
            df[column + '_qchange_pct'] = source[column].pct_change(periods=1)
            df[column + '_yoy_qchange'] = source[column].diff(periods=4)
            df[column + '_yoy_qchange_pct'] = source[column].pct_change(periods=4)
            df['quarterString'] = source['quarterString']
            df['quarter'] = source['quarter']
            df['year'] = source['year']


            # df.set_index(source['calendardate'], inplace=True)
        return df

    def valuePoints(self, source):
        df = pd.DataFrame()
        # How the various PEs are calculate in Quandl
        df['pe_calc'] = source['price'] / (source['eps'].rolling(4).sum())
        df['pe1_calc'] = source['marketcap'] / (source['netinccmnusd'].rolling(4).sum())
        df['pe'] = source['pe']
        df['pe1'] = source['pe1']
        df['ev_revenue'] = source['ev'] / source['revenue']
        return df


class Formatter:
    def number_formatter(self, num, m=1000000):
        if (np.isnan(num)):
            return ''

        if (abs(num) > 1e6 and abs(num) < 1e9):
            return '{0:.2f}m'.format(num / 1000000)
        elif (abs(num) > 1000000000):
            return '{0:.3f}b'.format(num / 1000000000)
        elif (abs(num) > 10000):
            return '{0:.0f}k'.format(num / 1000)
        else:
            return '{0:.2f}'.format(num)

    def percent_formatter(self, num):
        if (np.isnan(num)):
            return 'NaN'
        return '{0:.1f}%'.format(num * 100)

    def constructSentence(self, key, current, previous, suffix=''):
        if (previous == 0):
            percentChange = '\u221e'
        else:
            percentChange = '{0:.1f}%'.format(abs((current - previous) * 100 / previous))
        currentStr = self.number_formatter(current)
        previousStr = self.number_formatter(previous)
        return "* " + key + " was " + str(currentStr) + (" up" if current > previous else " down") + " (" + str(
            percentChange) + ")" + " from " + str(previousStr) + suffix

    def constructMinMaxSentence(self, key, min, max):
        # ** Trading range between April 25, 2018 and the present May 29, 2018 was $49.64 to $54.48: PE ratio range was 15.91 to 17.46: PS ratio range was 1.01 to 1.11: Cash flow yield range was 5.3% to 5.8%
        # Non-GAAP PE ratio range was 21.12 to 23.18

        return key + " was " + str(self.number_formatter(min)) + " to " + str(self.number_formatter(max))


#
# def trendline(data, order=1):
#     revenue = [87756000, 102697000, 114690000, 139785000, 188561000, 199214000, 191763000, 226102000]
#     revenue = [0.85, 0.99, 1.01, 1.12, 1.25, 1.36, 1.28, 1.44]
#     revenue = [0, 100, 200, 300, 400, 500, 600, 700]
#     year = [1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000]
#     data = pd.DataFrame({'year': year, 'revenue': revenue})
#     data['revenue'] = data['revenue'] / 100
#     data_ = [i for i in range(len(data))]
#     print(data)
#
#     coeffs = np.polyfit(data_, list(data['revenue']), order)
#     print(coeffs)
#     slope = coeffs[-2]
#     return float(slope)


class Analyser:
    def __init__(self):
        pass


class TMF1000Analyser(Analyser):
    fmt = Formatter()

    def __init__(self):
        super().__init__()
        self.calculator = Calculator()

    def analyse(self, mrqData, mryData, priceData, start, end):
        fullDataSet = self.report(mrqData, priceData, start, end)
        # self.financials(fullDataSet)

        df = pd.DataFrame()
        df['opmargin'] = (mrqData['opinc'] / mrqData['revenue']).describe()
        # df['cagr'] = mrqData['revenue_yoy_qchange'].describe()
        return df

    def financials(self, df):
        fmt = TMF1000Analyser.fmt
        hasDeferredRevenue = df['deferredrev'].sum() > 0
        hasRnd = df['rnd'].sum() > 0

        # Remove the last row because its the current quarter trading row, which is a duplicate of the last reported quarter.
        # What if the last row is data from an 8K?
        revenueData = self.calculator.periodChange(['revenue', 'deferredrev', 'netinc', 'eps', 'workingcapital', 'fcf', 'revenue_ttm'], df[-8:])
        revenueData['billings'] = revenueData['deferredrev_qchange'] + revenueData['revenue']
        revenueData['revenue'] = revenueData['revenue'].map(fmt.number_formatter)
        revenueData['revenue_ttm'] = revenueData['revenue_ttm'].map(fmt.number_formatter)
        revenueData['revenue_qchange_pct'] = revenueData['revenue_qchange_pct'].map(fmt.percent_formatter)
        revenueData['revenue_yoy_qchange_pct'] = revenueData['revenue_yoy_qchange_pct'].map(fmt.percent_formatter)
        print("\n### Revenue\n")

        # This data may have up to 2? extra duplicated rows in order to get trading range data for the current quarter. This data shouldnt be here.
        print(
            tabulate.tabulate(revenueData[['quarterString', 'revenue', 'revenue_ttm', 'revenue_qchange_pct', 'revenue_yoy_qchange_pct']],
                              headers=['Quarter', 'Revenue', 'TTM', '𝝳 (q-1)', '𝝳 (YoY)'],
                              tablefmt='pipe', showindex=False))
        print("\n### Deferred revenue\n")
        if (hasDeferredRevenue == False):
            print("No deferred revenue.")
        else:
            revenueData['deferredrev'] = revenueData['deferredrev'].map(fmt.number_formatter)
            revenueData['billings'] = revenueData['billings'].map(fmt.number_formatter)
            revenueData['deferredrev_qchange_pct'] = revenueData['deferredrev_qchange_pct'].map(fmt.percent_formatter)
            revenueData['deferredrev_yoy_qchange_pct'] = revenueData['deferredrev_yoy_qchange_pct'].map(fmt.percent_formatter)
            print(tabulate.tabulate(revenueData[['quarterString', 'deferredrev', 'deferredrev_qchange', 'deferredrev_yoy_qchange', 'billings']],
                                    headers=['Quarter', 'Def.Revenue', '𝝳 (q-1)', '𝝳 (YoY)', 'Billings(Rev + 𝝳 def. rev)'],
                                    tablefmt='pipe', showindex=False))
        print("\n### Margins\n")
        # tabulate.tabulate(lastEightQuarters[['currentratio']], headers="firstrow", tablefmt="pipe"))
        capitalStructureData = df[-8:][
            ['quarterString', 'grossmargin', 'ebitdamargin', 'netmargin', 'opinc', 'revenue', 'fcf', 'debtusd', 'equity', 'cashnequsd',
             'workingcapital', 'intexp', 'investments', 'intangibles']].reset_index()
        capitalStructureData['grossmargin'] = capitalStructureData['grossmargin'].map(fmt.percent_formatter)
        capitalStructureData['ebitdamargin'] = capitalStructureData['ebitdamargin'].map(fmt.percent_formatter)
        capitalStructureData['opmargin'] = (capitalStructureData['opinc'] / capitalStructureData['revenue']).map(fmt.percent_formatter)
        capitalStructureData['netmargin'] = capitalStructureData['netmargin'].map(fmt.percent_formatter)
        capitalStructureData['fcf'] = capitalStructureData['fcf'].map(fmt.number_formatter)
        print(tabulate.tabulate(capitalStructureData[['quarterString', 'grossmargin', 'ebitdamargin', 'opmargin', 'netmargin']],
                                headers=['Quarter', 'Gross margin', 'ebitdamargin', 'opmargin', 'netmargin'],
                                tablefmt='pipe'))
        # print(tabulate.tabulate(mryData[-4:][['year', 'grossmargin', 'ebitdamargin', 'netmargin']], tablefmt='pipe'))
        print("\n### Free cash flow\n")
        print(tabulate.tabulate(capitalStructureData[['quarterString', 'fcf', ]], headers=['Quarter', 'FCF'],
                                tablefmt='pipe', showindex=False))
        print("\n### Capital structure\n")
        capitalStructureData['debtEquity'] = (capitalStructureData['debtusd'] / capitalStructureData['equity'])
        capitalStructureData['cashAndInvestment'] = (
            capitalStructureData['cashnequsd'] + capitalStructureData['investments'])
        capitalStructureData['cashnequsd'] = capitalStructureData['cashnequsd'].map(fmt.number_formatter)
        capitalStructureData['investments'] = capitalStructureData['investments'].map(fmt.number_formatter)
        capitalStructureData['cashAndInvestment'] = capitalStructureData['cashAndInvestment'].map(fmt.number_formatter)
        capitalStructureData['workingcapital'] = capitalStructureData['workingcapital'].map(fmt.number_formatter)
        capitalStructureData['debtusd'] = capitalStructureData['debtusd'].map(fmt.number_formatter)
        capitalStructureData['intexp'] = capitalStructureData['intexp'].map(fmt.number_formatter)
        capitalStructureData['debtEquity'] = capitalStructureData['debtEquity'].map(fmt.number_formatter)
        print(tabulate.tabulate(
            capitalStructureData[
                ['quarterString', 'cashnequsd', 'investments', 'cashAndInvestment', 'workingcapital', 'debtusd',
                 'debtEquity', 'intexp']].dropna(),
            headers=['Cash', 'Investments', 'Cash and investments', 'Working Capital', 'Debt', 'Debt to Equity',
                     'Interest'], tablefmt='pipe', showindex=False))
        print("\n### Expenses\n")
        expensesData = df[-8:][['quarterString', 'quarter', 'year', 'rnd', 'sgna']]
        expensesData = self.calculator.periodChange(['sgna', 'rnd'], expensesData)
        expensesData['rnd'] = expensesData['rnd'].map(fmt.number_formatter)
        expensesData['rnd_ttm'] = expensesData['rnd_ttm'].map(fmt.number_formatter)
        expensesData['sgna'] = expensesData['sgna'].map(fmt.number_formatter)
        expensesData['rnd_qchange'] = expensesData['rnd_qchange'].map(fmt.percent_formatter)
        expensesData['rnd_yoy_qchange_pct'] = expensesData['rnd_yoy_qchange_pct'].map(fmt.percent_formatter)
        expensesData['sgna_qchange_pct'] = expensesData['sgna_qchange_pct'].map(fmt.percent_formatter)
        expensesData['sgna_yoy_qchange_pct'] = expensesData['sgna_yoy_qchange_pct'].map(fmt.percent_formatter)

        if hasRnd == True:
            print(tabulate.tabulate(
                expensesData[
                    ['quarterString', 'rnd', 'rnd_ttm', 'rnd_qchange', 'rnd_yoy_qchange', 'sgna', 'sgna_qchange_pct',
                     'sgna_yoy_qchange_pct']].dropna(subset=['rnd', 'sgna']),
                headers=['Quarter', 'R and D', 'rnd(ttm)', 'Change (q-1)', 'Change (YoY)', 'Sales, General, Admin',
                         'Change (q-1)',
                         'Change (YoY)'], tablefmt='pipe', showindex=False))

        else:
            print(tabulate.tabulate(
                expensesData[
                    ['quarterString', 'sgna', 'sgna_qchange_pct', 'sgna_yoy_qchange_pct']].dropna(subset=['sgna']),
                headers=['Quarter', 'Sales, General, Admin', 'Change (q-1)', 'Change (YoY)'], tablefmt='pipe', showindex=False))

    def reportedFundamentals(self, fmt, row, previousQuarter, sameQuarterLastYear):
        """ Row, previousQuarter, sameQuarerLastYear needs to have price and fundamental data associated with it."""
        quarterDateFmt = moment.Moment(row['calendardate']).format('MMM D, YYYY')

        print("\n#### Quarter ended %s" % (quarterDateFmt))
        print(fmt.constructSentence("Revenue", row['revenue'], previousQuarter['revenue'],
                                    "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(sameQuarterLastYear['revenue'])))

        print(fmt.constructSentence("TTM Revenue", row['revenue_ttm'], previousQuarter['revenue_ttm']),
              "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(sameQuarterLastYear['revenue_ttm']))
        print(fmt.constructSentence("TTM Revenue per share (diluted)", row['rps_ttm'], previousQuarter['rps_ttm'],
                                    "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(sameQuarterLastYear['rps_ttm'])))
        print(fmt.constructSentence("EPS (diluted):", row['epsdil'], previousQuarter['epsdil'], "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(
            sameQuarterLastYear['epsdil'])))  # Previous quarter, -5 for same quarter last year
        print(fmt.constructSentence("TTM EPS (diluted)", row['eps_ttm'], previousQuarter['eps_ttm'],
                                    "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(
                                        sameQuarterLastYear['eps_ttm'])))
        # print(fmt.constructSentence("Diluted share count", row['shareswadil'],  "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(
        #     sameQuarterLastYear['shareswadil'])))
        print(
            fmt.constructSentence("Cash and short-term investments ", row['cashnequsd'] + row['investmentsc'], previousQuarter['cashnequsd'] + previousQuarter['investmentsc'],
                                  suffix=' (prev quarter)'))
        print(fmt.constructSentence("Debt (prev quarter)", row['debtusd'], previousQuarter['debtusd'], suffix=' (prev quarter)'))
        print(fmt.constructSentence("Free cash flow for quarter", row['fcf'], previousQuarter['fcf'],
                                    " from the previous quarter (%s same quarter last year)" % fmt.number_formatter(sameQuarterLastYear['fcf'])))
        print(fmt.constructSentence("TTM free cash flow", row['fcf_ttm'], row['fcf_ttm']))
        print("* TTM cash flow per share was $%s" % fmt.number_formatter(row['fcf_ttm'] / row['shareswadil']))
        print(fmt.constructSentence("Gross margins", row['grossmargin'], previousQuarter['grossmargin']))
        print(fmt.constructSentence("CapExp", abs(row['capex']), abs(previousQuarter['capex'])))

    def priceBasedMetrics(self, row):
        """ Row needs to have price and fundamental data associated with it."""
        fmt = TMF1000Analyser.fmt
        quarterData = row
        startDateFmt = moment.Moment(quarterData['date_min']).format('MMM D, YYYY')
        endDateFmt = moment.Moment(quarterData['date_max']).format('MMM D, YYYY')
        quarterDateFmt = moment.Moment(quarterData['quarterEnd']).format('MMM D, YYYY')
        quarterData['marketCap_max'] = quarterData['sharesbas'] * quarterData['high_max']
        quarterData['marketCap_min'] = quarterData['sharesbas'] * quarterData['low_min']
        quarterData['marketCap_last'] = quarterData['sharesbas'] * quarterData['close_last']
        quarterData['ev_min'] = quarterData['marketCap_min'] + quarterData['debt'] - quarterData['cashnequsd']
        quarterData['ev_max'] = quarterData['marketCap_max'] + quarterData['debt'] - quarterData['cashnequsd']
        quarterData['ev_last'] = quarterData['marketCap_last'] + quarterData['debt'] - quarterData['cashnequsd']

        quarterData['ttmPE_min'] = quarterData['low_min'] / quarterData['eps_ttm']
        quarterData['ttmPE_max'] = quarterData['high_max'] / quarterData['eps_ttm']
        quarterData['ttmPE_last'] = quarterData['close_last'] / quarterData['eps_ttm']
        quarterData['1YPEG_min'] = quarterData['ttmPE_min'] / (quarterData['eps_ttm_growth'] * 100)
        quarterData['1YPEG_max'] = quarterData['ttmPE_max'] / (quarterData['eps_ttm_growth'] * 100)
        quarterData['1YPEG_last'] = quarterData['ttmPE_last'] / (quarterData['eps_ttm_growth'] * 100)

        print('\n#### Trading data (%s - %s)' % (startDateFmt, endDateFmt))
        print("* Trading range was %s to %s [%s]" % (quarterData['low_min'], quarterData['high_max'], quarterData['close_last']))
        print("* Market cap  was %s to %s [%s]" % (
            fmt.number_formatter(quarterData['marketCap_min']), fmt.number_formatter(quarterData['marketCap_max']),
            fmt.number_formatter(quarterData['marketCap_last'])))

        lastTtmEps = quarterData['eps_ttm']
        rps = quarterData['rps_ttm']
        lastFreeCashFlow = quarterData['fcf_ttm']
        ttmRevenue = quarterData['revenue_ttm']

        if lastTtmEps < 0:
            print("* PE range not applicable (earnings < 0)")
        else:
            print("* PE range was %s to %s [%s]" % (
                fmt.number_formatter(quarterData['low_min'] / lastTtmEps), fmt.number_formatter(quarterData['low_max'] / lastTtmEps),
                fmt.number_formatter(quarterData['close_last'] / lastTtmEps)))

        print("* PS ratio range was %s to %s [%s]" % (
            fmt.number_formatter((quarterData['low_min']) / rps), fmt.number_formatter((quarterData['high_max'] / rps)),
            fmt.number_formatter(quarterData['close_last'] / rps)))

        print("* Free cash flow (TTM) yield range was %s to %s [%s]" % (
            fmt.number_formatter(lastFreeCashFlow * 100 / quarterData['marketCap_max']),
            fmt.number_formatter(lastFreeCashFlow * 100 / quarterData['marketCap_min']),
            fmt.number_formatter(lastFreeCashFlow * 100 / quarterData['marketCap_last'])))
        print("* EV/Sales was %s to %s [%s]" % (
            fmt.number_formatter(quarterData['ev_min'] / ttmRevenue), fmt.number_formatter(quarterData['ev_max'] / ttmRevenue),
            fmt.number_formatter(quarterData['ev_last'] / ttmRevenue)))
        print("* TTM EPS growth was %s [EPS: %s versus %s]" % (
            fmt.percent_formatter(quarterData['eps_ttm_growth']), fmt.number_formatter(quarterData['eps_ttm']),
            fmt.number_formatter(quarterData['eps_ttm_same'])))
        print("* 1YPEG (under 1.0 desirable) was %s to %s [%s]" % (
            fmt.number_formatter(quarterData['1YPEG_min']), fmt.number_formatter(quarterData['1YPEG_max']),
            fmt.number_formatter(quarterData['1YPEG_last'])))
        pass

    def report(self, mrqData, priceData, start, end):
        fmt = Formatter()
        # Subtract a year from start to make sure we have enough for TTM
        # dataRange = pd.date_range(start=start - pd.offsets.QuarterBegin() - pd.DateOffset(years=1), end=end + pd.offsets.QuarterEnd(), freq='Q')
        dataRange = pd.date_range(start=start - pd.offsets.QuarterBegin() - pd.DateOffset(years=5), end=end + pd.offsets.QuarterEnd(), freq='Q')
        dates = pd.DataFrame(dataRange, columns=['date'])
        dates['quarterEnd'] = dates['date'].map(lambda x: x + pd.offsets.QuarterEnd(n=0))
        # dates['prev_quarter'] = dates['quarterEnd'].shift(1)
        dates['quarterString'] = dates['quarterEnd'].map(lambda x: pd.Period(x, 'Q'))
        dates['quarterInt'] = dates['quarterEnd'].map(lambda x: x.quarter)
        dates['year'] = dates['quarterEnd'].map(lambda x: x.year)

        # At this point, we have per-day price data. When we group by, we need to have pruned the price data appropriately.
        # (in order to get correct max and min dates.
        priceData['quarterEnd'] = priceData['date'].map(lambda x: x + pd.offsets.QuarterEnd(n=0))
        relevantPriceData = priceData #[(priceData['date'] >= start) & (priceData['date'] < end)][['date', 'high', 'low', 'close', 'quarterEnd']]
        priceSummary = relevantPriceData.groupby('quarterEnd')['high', 'low', 'close', 'date'].agg(['max', 'min', 'last'])

        # These next two lines flatten out the hierarchical indexValue caused by the multicolumn groupby above.
        priceSummary.columns = priceSummary.columns.map('_'.join)
        priceSummary = priceSummary.reset_index()
        # Add in the prev_quarter data - 'dates' is the canonical source of all relevant dates.
        priceSummary = priceSummary.merge(dates, on=['quarterEnd'])

        dates.set_index(['quarterEnd'], inplace=True)

        # populate ttm/max/min/last figures
        mrqData.set_index(['calendardate'], inplace=True)
        mrqData['fcf_ttm'] = mrqData['fcf'].rolling(4).sum()
        mrqData['eps_ttm'] = mrqData['epsusd'].rolling(4).sum()
        mrqData['revenue_ttm'] = mrqData['revenue'].rolling(4).sum()
        mrqData['rpsdil'] = mrqData['revenue_ttm'] / mrqData['shareswadil']
        mrqData['rps_ttm'] = mrqData['revenue_ttm'] / mrqData['shareswadil']
        mrqData['eps_ttm_same'] = mrqData['eps_ttm'].shift(4)

        # This line adds NaN where previous ttm_eps is negative
        mrqData['eps_ttm_growth'] = pd.np.where(mrqData['eps_ttm_same'] > 0, mrqData['eps_ttm'].pct_change(periods=4), np.NAN)

        # These two lines add in duplicate data for the 'current' period (ie, the period [potentially multiple quarters] where we have no reported results). This data should not be
        # utilised subsequently, its only useful for reporting value and trading ranges.
        # fundamentalData = dates.join(mrqData, lsuffix='_date', rsuffix='_mrq')
        fundamentalData = mrqData
        priceSummary.set_index('date_max', inplace=True)
        # Join works as a left join on the indexes by default
        fundamentalData['calendardate'] = fundamentalData.index

        # left join, but match on closest rather than exact key (date-max -> calendardate) - so priceSummary 'wins' - ie, indexed by previous quarter
        fundamentalAndPriceData = pd.merge_asof(priceSummary, fundamentalData, left_index=True, right_index=True)

        print('\n### Basic data (TMF1000)')
        fundamentalAndPriceData.reset_index(inplace=True)

        # There will be duplicated rows for fundamentals, because we group price data on quarters, and will match the prices to quarters that have already been reported.
        # For example, we have july prices (ie, Q3) but only have reported Q1 fundamentals.
        fundamentalsReported = []
        for indexValue, row in fundamentalAndPriceData.iterrows():
            if not ((row['date_max'] >= start) and (row['date_min'] < end)):
                continue

            previousMonthRow = fundamentalAndPriceData.iloc[(indexValue - 1)]
            previousYearRow = fundamentalAndPriceData.iloc[(indexValue - 4)]

            if (row['calendardate'] not in fundamentalsReported):
                self.reportedFundamentals(fmt, row, previousMonthRow, previousYearRow)
                fundamentalsReported.append(row['calendardate'])
            self.priceBasedMetrics(row)

        return mrqData


def analyse(ticker, start, end, adjustments=None, dcfProfile=None):
    if dcfProfile == None:
        dcfProfile = {
            "cagr": np.arange(0.1, 0.4, 0.05),
            "opMargin": np.arange(0.1, 0.4, 0.05),
            "salesToCapital": 1.0,
        }

    if not isinstance(ticker, list):
        ticker = [ticker]

    for t in ticker:
        # priceData = DataLoader().loadPriceDataLive(ticker=t)
        priceData = DataLoader().loadPriceData(t)
        # peerData = DataLoader().loadPeerDataLive(ticker)
        # mrqData, mryData, arqData = DataLoader().loadDataLive(ticker=t, adjustments=adjustments)
        mrqData, mryData, arqData = DataLoader().loadData(ticker=t, adjustments=adjustments)
        # graphs.graph(ticker, mrqData, 'calendardate', 'assets')
        print(t)
        changeData = TMF1000Analyser().analyse(mrqData, mryData, priceData, start=start, end=end)
        # , end=pd.Timestamp.now())

    exit(1)
    dcfProfile["opMargin"] = np.arange(changeData.loc['min'], changeData.loc['max'], (changeData.loc['max'] - changeData.loc['min']) / 5)
    dcfProfile["cagr"] = np.arange(changeData.loc['min'], changeData.loc['max'], (changeData.loc['max'] - changeData.loc['min']) / 5)
    print(dcfProfile)
    exit(1)
    # return
    # pool = Pool(processes=8)
    # cagr = np.arange(0.05, 0.2, 0.02)
    # opMargin = np.arange(0.05, 0.15, 0.02)

    df = pd.DataFrame(index=dcfProfile["opMargin"], columns=dcfProfile["cagr"])
    for x in dcfProfile["cagr"]:
        for y in dcfProfile["opMargin"]:
            d = DCF(mrqData, x, y)
            # pool.apply(d.calc, args=())
            df.at[y, x] = float(d.calc())
            pass

    end = time.time()
    print("\n### DCF \n")
    print("Warning: Have you adjusted the inputs to the DCF? In particular, sales to capital ratio and tax rates?")
    print(tabulate.tabulate(df, headers=df.columns, tablefmt='pipe', showindex=True))

    exit(1)


def ntnxAdjustments(df):
    # This data is from morningstar/iex
    df.loc[(df.dimension == 'MRQ') & (df.calendardate == '2017-06-30'), 'revenue'] = 173424000
    return df


def SKX_adjustments(df):
    # This data is from morningstar/iex
    calendardate_ = moment.Moment('2018-06-30').datetime
    index = (calendardate_, 'MRQ')
    df.loc[index, 'calendardate'] = calendardate_
    df.loc[index, 'dimension'] = 'MRQ'
    df.loc[index, 'revenue'] = 1134797000
    # df.loc[calendardate_, 'cogs'] = ???
    df.loc[index, 'gp'] = 560957000
    # df.loc[calendardate_, 'royaties'] = ???
    df.loc[index, 'sgna'] = 484949000
    df.loc[index, 'ebit'] = 81358000
    # TODO: Deal with interest
    df.loc[index, 'ebt'] = 74939000

    df.loc[index, 'intexp'] = 1054000
    # df.loc[calendardate_, 'otherexp'] = (7, 473)???
    df.loc[index, 'taxexp'] = 14080000
    df.loc[index, 'netinc'] = 60859000 - 15575000
    df.loc[index, 'sharesbas'] = 156518000
    df.loc[index, 'shareswadil'] = 157091000
    df.loc[index, 'eps'] = df.loc[index, 'netinc'] / df.loc[index, 'sharesbas']
    df.loc[index, 'epsdil'] = df.loc[index, 'netinc'] / df.loc[index, 'shareswadil']

    # print(df.loc[(df.dimension == 'MRQ')].to_string())
    return df


# Screen()
# analyse(['AYX', 'MDB', 'NTNX', 'OKTA', 'PVTL', 'PSTG', 'SHOP', 'SQ', 'TWLO', 'ZS'])
# analyse('SKX', start=pd.Timestamp(year=2016, month=2, day=7), end=pd.Timestamp(year=2018, month=7, day=25), adjustments=SKX_adjustments)
# analyse('ADBE', start=pd.Timestamp(year=2016, month=2, day=7), end=pd.Timestamp(year=2018, month=7, day=25))
analyse('AAPL', start=pd.Timestamp(year=2018, month=2, day=7), end=pd.Timestamp(year=2018, month=7, day=16))
# analyse('CAKE', start=pd.Timestamp(year=2018, month=2, day=21), end=pd.Timestamp(year=2018, month=4, day=25))
# analyse('ANET', start=pd.Timestamp(year=2017, month=2, day=15), end=pd.Timestamp(year=2018, month=5, day=3))
# analyse('LGIH', start=pd.Timestamp(year=2017, month=2, day=15), end=pd.Timestamp(year=2018, month=7, day=20))

quandl_headings = ['ticker', 'dimension', 'calendardate', 'datekey', 'reportperiod', 'lastupdated', 'accoci', 'assets',
                   'assetsavg', 'assetsc', 'assetsnc', 'assetturnover', 'bvps',
                   'capex', 'cashneq', 'cashnequsd', 'cor', 'consolinc', 'currentratio', 'de', 'debt', 'debtc',
                   'debtnc', 'debtusd', 'deferredrev', 'depamor', 'deposits',
                   'divyield', 'dps', 'ebit', 'ebitda', 'ebitdamargin', 'ebitdausd', 'ebitusd', 'ebt', 'eps', 'epsdil',
                   'epsusd', 'equity', 'equityavg', 'equityusd', 'ev',
                   'evebit', 'evebitda', 'fcf', 'fcfps', 'fxusd', 'gp', 'grossmargin', 'intangibles', 'intexp',
                   'invcap', 'invcapavg', 'inventory', 'investments', 'investmentsc',
                   'investmentsnc', 'liabilities', 'liabilitiesc', 'liabilitiesnc', 'marketcap', 'ncf', 'ncfbus',
                   'ncfcommon', 'ncfdebt', 'ncfdiv', 'ncff', 'ncfi', 'ncfinv',
                   'ncfo', 'ncfx', 'netinc', 'netinccmn', 'netinccmnusd', 'netincdis', 'netincnci', 'netmargin', 'opex',
                   'opinc', 'payables', 'payoutratio', 'pb', 'pe', 'pe1',
                   'ppnenet', 'prefdivis', 'price', 'ps', 'ps1', 'receivables', 'retearn', 'revenue', 'revenueusd',
                   'rnd', 'roa', 'roe', 'roic', 'ros', 'sbcomp', 'sgna',
                   'sharefactor', 'sharesbas', 'shareswa', 'shareswadil', 'sps', 'tangibles', 'taxassets', 'taxexp',
                   'taxliabilities', 'tbvps', 'workingcapital']


# iexApiFinancials = {"symbol": "NTNX", "financials": [
#     {"reportDate": "2018-04-30", "grossProfit": 193798000, "costOfRevenue": 95615000, "operatingRevenue": 289413000, "totalRevenue": 289413000, "operatingIncome": -82282000,
#      "netIncome": -85674000, "researchAndDevelopment": 81291000, "operatingExpense": 276080000, "currentAssets": 1184676000, "totalAssets": 1475398000, "totalLiabilities": null,
#      "currentCash": 376789000, "currentDebt": null, "totalCash": 923464000, "totalDebt": null, "shareholderEquity": 354581000, "cashChange": -233657000, "cashFlow": 13308000,
#      "operatingGainsLosses": null},
#     {"reportDate": "2018-01-31", "grossProfit": 178216000, "costOfRevenue": 108528000, "operatingRevenue": 286744000, "totalRevenue": 286744000, "operatingIncome": -59857000,
#      "netIncome": -62631000, "researchAndDevelopment": 70924000, "operatingExpense": 238073000, "currentAssets": 1162551000, "totalAssets": 1345196000,
#      "totalLiabilities": 1044717000, "currentCash": 610446000, "currentDebt": null, "totalCash": 918255000, "totalDebt": null, "shareholderEquity": 300479000,
#      "cashChange": 477987000, "cashFlow": 46395000, "operatingGainsLosses": null},
#     {"reportDate": "2017-10-31", "grossProfit": 166930000, "costOfRevenue": 108622000, "operatingRevenue": 275552000, "totalRevenue": 275552000, "operatingIncome": -59039000,
#      "netIncome": -61487000, "researchAndDevelopment": 64512000, "operatingExpense": 225969000, "currentAssets": 592901000, "totalAssets": 764910000, "totalLiabilities": 548330000,
#      "currentCash": 132459000, "currentDebt": null, "totalCash": 365945000, "totalDebt": null, "shareholderEquity": 216580000, "cashChange": -5900000, "cashFlow": 10107000,
#      "operatingGainsLosses": null},
# ]}
