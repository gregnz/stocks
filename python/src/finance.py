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
from dcf import DcfParameters
import logging
import tabulate as tabulate

from screen import Screen

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
            df[column + '_ttm_yoy_change'] = df[column + '_ttm'].diff(periods=4)
            df[column + '_ttm_yoy_change_pct'] = df[column + '_ttm_yoy_change'].pct_change(periods=4)
            df[column + '_qchange'] = source[column].diff()
            df[column + '_qchange_pct'] = source[column].pct_change(periods=1)
            df[column + '_yoy_qchange'] = source[column].diff(periods=4)
            df[column + '_yoy_qchange_pct'] = source[column].pct_change(periods=4)
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
        self.report(mrqData, priceData, start, end)
        self.financials(mrqData)

        opMargin = (mrqData[-8:]['opinc'] / mrqData[-8:]['revenue']).describe()
        revenueChangeData = self.calculator.periodChange(['revenue'], mrqData[-8:])
        cagr = revenueChangeData['revenue_yoy_qchange_pct'].describe()
        # print(opMargin.to_string())
        # print(cagr.to_string())
        return cagr, opMargin

    def financials(self, df):
        fmt = TMF1000Analyser.fmt
        hasDeferredRevenue = df['deferredrev'].sum() > 0
        hasRnd = df['rnd'].sum() > 0

        df['quarterString'] = df['calendardate'].map(lambda x: pd.Period(x, 'Q'))

        # Remove the last row because its the current quarter trading row, which is a duplicate of the last reported quarter.
        # What if the last row is data from an 8K?
        revenueData = self.calculator.periodChange(['revenue', 'deferredrev', 'netinc', 'eps', 'workingcapital', 'fcf', 'revenue_ttm'], df[-8:])
        revenueData['billings'] = revenueData['deferredrev_qchange'] + revenueData['revenue']
        revenueData['revenue'] = revenueData['revenue'].map(fmt.number_formatter)
        revenueData['revenue_ttm'] = revenueData['revenue_ttm'].map(fmt.number_formatter)
        revenueData['revenue_qchange_pct'] = revenueData['revenue_qchange_pct'].map(fmt.percent_formatter)
        revenueData['revenue_yoy_qchange_pct'] = revenueData['revenue_yoy_qchange_pct'].map(fmt.percent_formatter)
        revenueData['revenue_ttm_yoy_qchange_pct'] = revenueData['revenue_ttm_yoy_qchange_pct'].map(fmt.percent_formatter)
        revenueData['quarterString'] = df['quarterString']
        print("\n### Revenue\n")

        # This data may have up to 2? extra duplicated rows in order to get trading range data for the current quarter. This data shouldnt be here.
        print(
            tabulate.tabulate(revenueData[['quarterString', 'revenue', 'revenue_ttm', 'revenue_qchange_pct', 'revenue_yoy_qchange_pct', 'revenue_ttm_yoy_qchange_pct']],
                              headers=['Quarter', 'Revenue', 'TTM', '𝝳 (q-1)', '𝝳 (YoY)', '𝝳 (TTM)'],
                              tablefmt='pipe', showindex=False))
        print("\n### Deferred revenue\n")
        if (hasDeferredRevenue == False):
            print("No deferred revenue.")
        else:
            revenueData['deferredrev'] = revenueData['deferredrev'].map(fmt.number_formatter)
            revenueData['billings'] = revenueData['billings'].map(fmt.number_formatter)
            revenueData['deferredrev_qchange_pct'] = revenueData['deferredrev_qchange_pct'].map(fmt.percent_formatter)
            revenueData['deferredrev_yoy_qchange_pct'] = revenueData['deferredrev_yoy_qchange_pct'].map(fmt.percent_formatter)
            print(tabulate.tabulate(revenueData[['quarterString', 'deferredrev', 'deferredrev_qchange_pct', 'deferredrev_yoy_qchange_pct', 'billings']],
                                    headers=['Quarter', 'Def.Revenue', '𝝳 (q-1)', '𝝳 (YoY)', 'Billings(Rev + 𝝳 def. rev)'],
                                    tablefmt='pipe', showindex=False))
        print("\n### Margins\n")
        # tabulate.tabulate(lastEightQuarters[['currentratio']], headers="firstrow", tablefmt="pipe"))
        # print(df[-8:].to_string())
        reinvestment = df[-12:][['revenue', 'ebit', 'taxexp', 'depamor', 'intexp', 'capex', 'workingcapital']]
        reinvestment['changerev'] = (reinvestment['revenue'].diff(1))
        reinvestment['changewc'] = (reinvestment['workingcapital'].diff(1))
        reinvestment['capex'] = abs(reinvestment['capex'])
        reinvestment['reinvestment'] = reinvestment['capex'] - reinvestment['depamor'] + reinvestment['changewc']
        reinvestment['earningsToEquityAfterTax'] = reinvestment['ebit'] + reinvestment['intexp'] - reinvestment['taxexp']
        reinvestment['reinvestmentRate'] = reinvestment['reinvestment'] / reinvestment['earningsToEquityAfterTax']

        print(reinvestment.to_string())

        capitalStructureData = df[-8:][
            ['quarterString', 'grossmargin', 'ebitdamargin', 'inventory', 'ncfdiv', 'netmargin', 'opinc', 'revenue', 'fcf', 'debtusd', 'equity', 'cashnequsd',
             'workingcapital', 'intexp', 'investmentsc', 'intangibles']].reset_index()
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
        print(tabulate.tabulate(capitalStructureData[['quarterString', 'fcf', 'ncfdiv']], headers=['Quarter', 'FCF', 'Dividends'],
                                tablefmt='pipe', showindex=False))
        print("\n### Capital structure\n")
        capitalStructureData['debtEquity'] = (capitalStructureData['debtusd'] / capitalStructureData['equity'])
        capitalStructureData['cashAndInvestment'] = (
            capitalStructureData['cashnequsd'] + capitalStructureData['investmentsc'])
        capitalStructureData['cashnequsd'] = capitalStructureData['cashnequsd'].map(fmt.number_formatter)
        capitalStructureData['investmentsc'] = capitalStructureData['investmentsc'].map(fmt.number_formatter)
        capitalStructureData['cashAndInvestment'] = capitalStructureData['cashAndInvestment'].map(fmt.number_formatter)
        capitalStructureData['inventory'] = capitalStructureData['inventory'].map(fmt.number_formatter)
        capitalStructureData['workingcapital'] = capitalStructureData['workingcapital'].map(fmt.number_formatter)
        capitalStructureData['debtusd'] = capitalStructureData['debtusd'].map(fmt.number_formatter)
        capitalStructureData['intexp'] = capitalStructureData['intexp'].map(fmt.number_formatter)
        capitalStructureData['debtEquity'] = capitalStructureData['debtEquity'].map(fmt.number_formatter)
        print(tabulate.tabulate(
            capitalStructureData[
                ['quarterString', 'cashnequsd', 'investmentsc', 'cashAndInvestment', 'workingcapital', 'debtusd',
                 'debtEquity', 'intexp', 'inventory']].dropna(),
            headers=['Cash', 'Investments', 'Cash and investments', 'Working Capital', 'Debt', 'Debt to Equity',
                     'Interest', 'Inventory'], tablefmt='pipe', showindex=False))
        print("\n### Expenses\n")
        expensesData = self.calculator.periodChange(['sgna', 'gp', 'rnd'], df[-16:])
        # How much SGNA changed (in dollars) / How much GP changed in dollars
        expensesData['sgna 𝝳/gp 𝝳'] = expensesData['gp_ttm_yoy_change'] / expensesData['sgna_ttm_yoy_change']
        expensesData['sgna 𝝳/gp 𝝳'] = expensesData['sgna 𝝳/gp 𝝳'].map(fmt.number_formatter)

        expensesData['quarterString'] = df['quarterString']
        expensesData['rnd'] = expensesData['rnd'].map(fmt.number_formatter)
        expensesData['rnd_ttm'] = expensesData['rnd_ttm'].map(fmt.number_formatter)
        expensesData['sgna'] = expensesData['sgna'].map(fmt.number_formatter)
        expensesData['rnd_qchange_pct'] = expensesData['rnd_qchange_pct'].map(fmt.percent_formatter)
        expensesData['rnd_yoy_qchange_pct'] = expensesData['rnd_yoy_qchange_pct'].map(fmt.percent_formatter)
        expensesData['sgna_qchange'] = expensesData['sgna_qchange'].map(fmt.number_formatter)
        expensesData['sgna_yoy_qchange'] = expensesData['sgna_yoy_qchange'].map(fmt.number_formatter)
        if hasRnd == True:
            print(tabulate.tabulate(
                expensesData[
                    ['quarterString', 'rnd', 'rnd_ttm', 'rnd_qchange_pct', 'rnd_yoy_qchange_pct', 'sgna', 'sgna_qchange_pct',
                     'sgna_yoy_qchange_pct', 'sgna 𝝳/gp 𝝳']].dropna(subset=['rnd', 'sgna']),
                headers=['Quarter', 'R and D', 'rnd(ttm)', 'Change (q-1)', 'Change (YoY)', 'Sales, General, Admin',
                         '𝝳 (q-1)',
                         '𝝳 (YoY)', 'SG&A 𝝳/GP 𝝳'], tablefmt='pipe', showindex=False))

        else:
            print(tabulate.tabulate(
                expensesData[
                    ['quarterString', 'sgna', 'sgna_qchange', 'sgna_yoy_qchange', 'gp_yoy_qchange', 'sgna 𝝳/gp 𝝳']].dropna(subset=['sgna']),
                headers=['Quarter', 'Sales, General, Admin', '𝝳 (q-1)', '𝝳 (YoY)', 'GP 𝝳 (yoy)', 'SG&A 𝝳/GP 𝝳'], tablefmt='pipe', showindex=False))

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

        # The 0.0000001 is a hack to get around DivisionByZero errors
        quarterData['1YPEG_min'] = pd.np.where(quarterData['eps_ttm_growth'] > 0, quarterData['ttmPE_min'] / (quarterData['eps_ttm_growth'] + 0.0000001 * 100), np.NAN)
        quarterData['1YPEG_max'] = pd.np.where(quarterData['eps_ttm_growth'] > 0, quarterData['ttmPE_max'] / (quarterData['eps_ttm_growth'] + 0.0000001 * 100), np.NAN)
        quarterData['1YPEG_last'] = pd.np.where(quarterData['eps_ttm_growth'] > 0, quarterData['ttmPE_last'] / (quarterData['eps_ttm_growth'] + 0.0000001 * 100), np.NAN)
        # quarterData['1YPEG_max'] = quarterData['ttmPE_max'] / (quarterData['eps_ttm_growth'] + 0.0000001 * 100)
        # quarterData['1YPEG_last'] = quarterData['ttmPE_last'] / (quarterData['eps_ttm_growth'] + 0.0000001 * 100)

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
        relevantPriceData = priceData  # [(priceData['date'] >= start) & (priceData['date'] < end)][['date', 'high', 'low', 'close', 'quarterEnd']]
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
        mrqData['rps_ttm'] = mrqData['revenue_ttm'] / mrqData['shareswadil']
        mrqData['eps_ttm_same'] = mrqData['eps_ttm'].shift(4)

        # This line adds NaN where previous ttm_eps is negative
        mrqData['eps_ttm_growth'] = pd.np.where(mrqData['eps_ttm_same'] > 0, mrqData['eps_ttm'].pct_change(periods=4), np.NAN)

        # These two lines add in duplicate data for the 'current' period (ie, the period [potentially multiple quarters] where we have no reported results). This data should not be
        # utilised subsequently, its only useful for reporting value and trading ranges.
        # fundamentalData = dates.join(mrqData, lsuffix='_date', rsuffix='_mrq')
        fundamentalData = mrqData
        # priceSummary.set_index('date_max', inplace=True)
        # Join works as a left join on the indexes by default
        fundamentalData['calendardate'] = fundamentalData.index
        # left join, but match on closest rather than exact key (date-max -> calendardate) - so priceSummary 'wins' - ie, indexed by previous quarter
        fundamentalAndPriceData = pd.merge_asof(priceSummary, fundamentalData, left_on='quarterEnd', right_on='calendardate')

        print('\n### Basic data (TMF1000)')
        fundamentalAndPriceData.reset_index(inplace=True)
        # There will be duplicated rows for fundamentals, because we group price data on quarters, and will match the prices to quarters that have already been reported.
        # For example, we have july prices (ie, Q3) but only have reported Q1 fundamentals.

        # Note: This also means that fundamental based prices are no longer valid (there will be duplicates)
        fundamentalsReported = []
        for indexValue, row in fundamentalAndPriceData.iterrows():
            if not ((row['date_max'] >= start) and (row['date_min'] < end)):
                continue

            previousMonthRow = fundamentalAndPriceData.iloc[(indexValue - 1)]
            previousYearRow = fundamentalAndPriceData.iloc[(indexValue - 5)]

            if (row['calendardate'] not in fundamentalsReported):
                self.reportedFundamentals(fmt, row, previousMonthRow, previousYearRow)
                fundamentalsReported.append(row['calendardate'])
            self.priceBasedMetrics(row)

        return fundamentalAndPriceData


def analyse(ticker, start, end, liveData=False, adjustments=None, dcfProfile=None):
    if dcfProfile == None:
        dcfProfile = {
            "cagr": np.arange(0.1, 0.4, 0.05),
            "opMargin": np.arange(0.1, 0.4, 0.05),
            "salesToCapital": 1.0,
        }

    if not isinstance(ticker, list):
        ticker = [ticker]
    results = {}
    for t in ticker:
        if (liveData == True):
            priceData = DataLoader().loadPriceDataLive(ticker=t)
            mrqData, mryData, arqData = DataLoader().loadDataLive(ticker=t, adjustments=adjustments)
        else:
            priceData = DataLoader().loadPriceData(t)
            mrqData, mryData, arqData = DataLoader().loadData(ticker=t, adjustments=adjustments)
        # peerData = DataLoader().loadPeerDataLive(ticker)
        # graphs.graph(ticker, mrqData, 'calendardate', 'assets')
        close = priceData[-1:]['close'][0]
        print(t, close)
        try:
            cagr, opMargin = TMF1000Analyser().analyse(mrqData, mryData, priceData, start=start, end=end)
        except Exception:
            continue

        dcfProfile['opMargin'] = np.linspace(opMargin['mean'] - 2 * opMargin['std'], opMargin['mean'] + 2 * opMargin['std'], num=5)
        dcfProfile['cagr'] = np.linspace(cagr['mean'] - 2 * cagr['std'], cagr['mean'] + 2 * cagr['std'], num=5)
        dcfProfile['salesToCapitalRatio'] = np.linspace(0.7, 1.75, num=5)
        # dcfProfile["cagr"] = np.linspace(0.05, 0.3, num=5)

        # i = pd.MultiIndex.from_product([dcfProfile["opMargin"], dcfProfile['salesToCapitalRatio']], names=['opMargin', 'salesToCapitalRatio'])

        revDf = pd.DataFrame(index=['Year 10 Revenue'], columns=dcfProfile["cagr"])
        dataframeArray = []
        currentDf = pd.DataFrame(index=dcfProfile["opMargin"], columns=dcfProfile["cagr"], dtype=float)
        print("\n### DCF \n")
        print("Warning: Have you adjusted the inputs to the DCF? In particular, sales to capital ratio and tax rates?")
        for z in dcfProfile["salesToCapitalRatio"]:
            for x in dcfProfile["cagr"]:
                for y in dcfProfile["opMargin"]:
                    dcfParams = DcfParameters(mrqData, cagr=x, targetEbitMargin=y, salesToCapitalRatio=z)
                    d = DCF(mrqData, dcfParams)

                    dcfParams.salesToCapitalRatio = z
                    # pool.apply(d.calc, args=())
                    revenueAtEnd, calc = d.calc()
                    currentDf.at[y, x] = float(calc)
                    revDf.at['Year 10 Revenue', x] = float(revenueAtEnd)

            dataframeArray.append(currentDf.copy())

        print(tabulate.tabulate(revDf, headers=revDf.columns, tablefmt='pipe', showindex=True, floatfmt='.1f'))

        for d in dataframeArray:
            print(d.to_string())

        df = pd.concat(dataframeArray, keys=dcfProfile['salesToCapitalRatio'])

        groupby = df.groupby(level=1).mean()

        print('\n#### Discounted cash flow estimates (rows=OperatingMargin, cols = Revenue growth)\n')
        print(tabulate.tabulate(groupby, headers=df.columns, tablefmt='pipe', showindex=True, floatfmt='.1f'))


        numberOfCellsOverClose = groupby.applymap(lambda x: 1 if x > close else 0).sum(axis=1).sum()
        if (numberOfCellsOverClose > 15):
            print("%s has %d cells over the last close price. May be worth investigating..." % (t, numberOfCellsOverClose))
        results[t] = {'numberOfCellsOverClose': numberOfCellsOverClose, 'ticker': t}

    df = pd.DataFrame.from_dict(results, orient='index', columns=['numberOfCellsOverClose', 'ticker'])
    print(df.to_string())
    dfCompany = DataLoader().loadBatchCompanyDataLive([])
    filtered = df.merge(dfCompany, on=['ticker']).groupby(['ticker']).tail(1)

    print(results)
    print(filtered.to_string())
    end = time.time()
    # revDf.rename(lambda x: '{:.1f}%'.format(x * 100), inplace=True, axis=1)
    # df.rename(lambda x: '{:.1f}%'.format(x * 100), inplace=True)
    # df.rename(lambda x: '{:.1f}%'.format(x * 100), inplace=True, axis=1)

    exit(1)


def ntnxAdjustments(df):
    # This data is from morningstar/iex
    df.loc[(df.dimension == 'MRQ') & (df.calendardate == '2017-06-30'), 'revenue'] = 173424000
    return df


def SKX_adjustments(df):
    calendardate_ = moment.Moment('2018-06-30').datetime
    index = (calendardate_, 'MRQ')
    # Income statement
    df.loc[index, 'calendardate'] = calendardate_
    df.loc[index, 'ticker'] = 'SKX'
    df.loc[index, 'dimension'] = 'MRQ'
    df.loc[index, 'revenue'] = 1134797000
    df.loc[index, 'gp'] = 560957000 + 5350000
    df.loc[index, 'sgna'] = 370927000 + 114022000
    df.loc[index, 'ebit'] = 81358000
    df.loc[index, 'intexp'] = 1054000
    df.loc[index, 'ebt'] = 74939000
    df.loc[index, 'taxexp'] = 14080000
    df.loc[index, 'netinc'] = 60859000 - 15575000
    df.loc[index, 'sharesbas'] = 156518000
    df.loc[index, 'shareswadil'] = 157091000
    df.loc[index, 'eps'] = df.loc[index, 'netinc'] / df.loc[index, 'sharesbas']
    df.loc[index, 'epsusd'] = df.loc[index, 'netinc'] / df.loc[index, 'sharesbas']
    df.loc[index, 'epsdil'] = df.loc[index, 'netinc'] / df.loc[index, 'shareswadil']

    df.loc[index, 'cashneq'] = 844847000
    df.loc[index, 'cashnequsd'] = 844847000
    df.loc[index, 'investmentsc'] = 42895000
    df.loc[index, 'receivables'] = 547497000 + 26938000
    df.loc[index, 'inventory'] = 822423000
    # Prepaid expenses and other current assets			77,290
    df.loc[index, 'assetsc'] = 2361890000
    df.loc[index, 'ppnenet'] = 553574000
    df.loc[index, 'taxassets'] = 26209000
    df.loc[index, 'investmentsnc'] = 23954000
    df.loc[index, 'assetsc'] = 2361890000
    df.loc[index, 'assetsnc'] = 643775000
    df.loc[index, 'assets'] = 3005665000

    df.loc[index, 'payables'] = 577783000
    # Current installments of long-term borrowings		$	1,810
    df.loc[index, 'debtc'] = 11179000
    # Accrued expenses			128,783
    df.loc[index, 'liabilitiesc'] = 719555000
    df.loc[index, 'debtnc'] = 70181000
    df.loc[index, 'taxliabilities'] = 161000
    # Other long-term liabilities			102,306
    df.loc[index, 'liabilitiesnc'] = 172648000
    df.loc[index, 'liabilities'] = 892203000
    df.loc[index, 'equityusd'] = 2113462000

    df.loc[index, 'debt'] = df.loc[index, 'debtc'] - df.loc[index, 'debtnc']
    df.loc[index, 'debtusd'] = df.loc[index, 'debt']
    df.loc[index, 'workingcapital'] = df.loc[index, 'assetsc'] - df.loc[index, 'liabilitiesc']
    df.loc[index, 'grossmargin'] = df.loc[index, 'gp'] / df.loc[index, 'revenue']
    df.loc[index, 'opmargin'] = df.loc[index, 'opinc'] / df.loc[index, 'revenue']
    df.loc[index, 'netmargin'] = df.loc[index, 'netinc'] / df.loc[index, 'revenue']

    return df


"""
"""
quandl = {"revenue": ["Revenues"],
          "cor": ["Cost of Revenue"],
          "sgna": ["Selling, General and Administrative Expense"],
          "rnd": ["Research and Development Expense"],
          "opex": ["Operating Expenses"],
          "intexp": ["Interest Expense"],
          "taxexp": ["Income Tax Expense"],
          "netincdis": ["Net Income from Discontinued Operations"],
          "consolinc": ["Consolidated Income"],
          "netincnci": ["Net Income to Non-Controlling Interests"],
          "netinc": ["Net Income"],
          "prefdivis": ["Preferred Dividends Income Statement Impact"],
          "netinccmn": ["Net Income Common Stock"],
          "eps": ["Earnings per Basic Share"],
          "epsdil": ["Earnings per Diluted Share"],
          "shareswa": ["Weighted Average Shares"],
          "shareswadil": ["Weighted Average Shares Diluted"],
          "capex": ["Capital Expenditure"],
          "ncfbus": ["Net Cash Flow - Business Acquisitions and Disposals"],
          "ncfinv": ["Net Cash Flow - Investment Acquisitions and Disposals"],
          "ncff": ["Net Cash Flow from Financing"],
          "ncfdebt": ["Issuance (Repayment) of Debt Securities "],
          "ncfcommon": ["Issuance (Purchase) of Equity Shares"],
          "ncfdiv": ["Payment of Dividends & Other Cash Distributions   "],
          "ncfi": ["Net Cash Flow from Investing"],
          "ncfo": ["Net Cash Flow from Operations"],
          "ncfx": ["Effect of Exchange Rate Changes on Cash "],
          "ncf": ["Net Cash Flow / Change in Cash & Cash Equivalents"],
          "sbcomp": ["Share Based Compensation"],
          "depamor": ["Depreciation, Amortization & Accretion"],
          # -------------------------------------------------------------------------------------
          "assets": ["Total Assets"],
          "cashneq": ["Cash and Equivalents"],
          "investments": ["Investments"],
          "investmentsc": ["Investments Current"],
          "investmentsnc": ["Investments Non-Current"],
          "deferredrev": ["Deferred Revenue"],
          "deposits": ["Deposit Liabilities"],
          "ppnenet": ["Property, Plant & Equipment Net"],
          "inventory": ["Inventory"],
          "taxassets": ["Tax Assets"],
          "receivables": ["Trade and Non-Trade Receivables"],
          "payables": ["Trade and Non-Trade Payables"],
          "intangibles": ["Goodwill and Intangible Assets"],
          "liabilities": ["Total Liabilities"],
          "equity": ["Shareholders Equity"],
          "retearn": ["Accumulated Retained Earnings (Deficit)"],
          "accoci": ["Accumulated Other Comprehensive Income"],
          "assetsc": ["Current Assets"],
          "assetsnc": ["Assets Non-Current"],
          "liabilitiesc": ["Current Liabilities"],
          "liabilitiesnc": ["Liabilities Non-Current"],
          "taxliabilities": ["Tax Liabilities"],
          "debt": ["Total Debt"],
          "debtc": ["Debt Current"],
          "debtnc": ["Debt Non-Current"],

          "ebt": ["Earnings before Tax"],
          "ebit": ["Earning Before Interest & Taxes (EBIT)"],
          "ebitda": ["Earnings Before Interest, Taxes & Depreciation Amortization (EBITDA)"],
          "fxusd": ["Foreign Currency to USD Exchange Rate"],
          "equityusd": ["Shareholders Equity (USD)"],
          "epsusd": ["Earnings per Basic Share (USD)"],
          "revenueusd": ["Revenues (USD)"],
          "netinccmnusd": ["Net Income Common Stock (USD)"],
          "cashnequsd": ["Cash and Equivalents (USD)"],
          "debtusd": ["Total Debt (USD)"],
          "ebitusd": ["Earning Before Interest & Taxes (USD)"],
          "ebitdausd": ["Earnings Before Interest, Taxes & Depreciation Amortization (USD)"],
          "sharesbas": ["Shares (Basic)"],
          "dps": ["Dividends per Basic Common Share"],
          "sharefactor": ["Share Factor"],
          "marketcap": ["Market Capitalization"],
          "ev": ["Enterprise Value"],
          "invcap": ["Invested Capital"],
          "equityavg": ["Average Equity"],
          "assetsavg": ["Average Assets"],
          "invcapavg": ["Invested Capital Average"],
          "tangibles": ["Tangible Asset Value"],
          "roe": ["Return on Average Equity"],
          "roa": ["Return on Average Assets"],
          "fcf": ["Free Cash Flow"],
          "roic": ["Return on Invested Capital"],
          "gp": ["Gross Profit"],
          "opinc": ["Operating Income"],
          "grossmargin": ["Gross Margin"],
          "netmargin": ["Profit Margin"],
          "ebitdamargin": ["EBITDA Margin"],
          "ros": ["Return on Sales"],
          "assetturnover": ["Asset Turnover"],
          "payoutratio": ["Payout Ratio"],
          "evebitda": ["Enterprise Value over EBITDA"],
          "evebit": ["Enterprise Value over EBIT"],
          "pe": ["Price Earnings (Damodaran Method)"],
          "pe1": ["Price to Earnings Ratio"],
          "sps": ["Sales per Share"],
          "ps1": ["Price to Sales Ratio"],
          "ps": ["Price Sales (Damodaran Method)"],
          "pb": ["Price to Book Value"],
          "de": ["Debt to Equity Ratio"],
          "divyield": ["Dividend Yield"],
          "currentratio": ["Current Ratio"],
          "workingcapital": ["Working Capital"],
          "fcfps": ["Free Cash Flow per Share"],
          "bvps": ["Book Value per Share"],
          "tbvps": ["Tangible Assets Book Value per Share"],
          "price": ["Share Price (Adjusted Close)"],
          "ticker": ["Ticker Symbol"],
          "dimension": ["Dimension"],
          "calendardate": ["Calendar Date"],
          "datekey": ["Date Key"],
          "reportperiod": ["Report Period"]
          }

# analyse(['AYX', 'MDB', 'NTNX', 'OKTA', 'PVTL', 'PSTG', 'SHOP', 'SQ', 'TWLO', 'ZS'])
# analyse(Screen().filter(), start=pd.Timestamp(year=2010, month=2, day=7), end=pd.Timestamp.now(), liveData=True)
analyse('PYPL', start=pd.Timestamp(year=2010, month=2, day=7), end=pd.Timestamp.now(), liveData=True)
# analyse('PYPL', start=pd.Timestamp(year=2016, month=2, day=7), end=pd.Timestamp(year=2018, month=8, day=1), adjustments=SKX_adjustments)
# analyse('PVTL', start=pd.Timestamp(year=2012, month=2, day=7), end=pd.Timestamp.now(), liveData=True)
# analyse('ADBE', start=pd.Timestamp(year=2016, month=2, day=7), end=pd.Timestamp.now(), liveData=True)
# analyse('AAPL', start=pd.Timestamp(year=2016, month=2, day=7), end=pd.Timestamp.now())
# analyse('SKX', start=pd.Timestamp(year=2015, month=2, day=7), end=pd.Timestamp.now(), liveData=True)
# analyse('CAKE', start=pd.Timestamp(year=2017, month=2, day=21), end=pd.Timestamp(year=2018, month=4, day=25))
# analyse('ANET', start=pd.Timestamp(year=2017, month=2, day=15), end=pd.Timestamp(year=2018, month=5, day=3))
# analyse('LGIH', start=pd.Timestamp(year=2017, month=2, day=15), end=pd.Timestamp(year=2018, month=7, day=20))
# analyse('NTNX', start=pd.Timestamp(year=2016, month=2, day=15), end=pd.Timestamp(year=2018, month=7, day=20), adjustments=ntnxAdjustments)




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
