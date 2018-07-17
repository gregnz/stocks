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

matplotlib.use('TkAgg')
import tabulate as tabulate

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
            df[column + '_qchange_actual'] = source[column].diff()
            df[column + '_qchange'] = source[column].pct_change(periods=1)
            df[column + '_yoy_qchange'] = source[column].pct_change(periods=4)
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
            return ''
        return '{0:.0f}%'.format(num * 100)

    def constructSentenceNew(self, key, data, suffix=''):
        totalDataLength = len(mrqData[key])
        print(mrqData[key].to_string())
        current = mrqData[key][-1:].values[0]
        previous = mrqData[key][-2:-1].values[0]
        if (totalDataLength >= 5):
            data_revenue__values_ = mrqData[key][-5:-4].values[0]
        else:
            data_revenue__values_ = np.NaN

        # print(fmt.constructSentence("Revenue", mrqData['revenue'][-1:].values[0], mrqData['revenue'][-2:-1].values[0]),
        #       "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(
        #           mrqData['revenue'][-5:-4].values[0]))
        print(current, previous)

        if (previous == 0):
            percentChange = '\u221e'
        else:
            percentChange = '{0:.1f}%'.format(abs((current - previous) * 100 / previous))
        currentStr = self.number_formatter(current)
        previousStr = self.number_formatter(previous)
        return "* " + key + " was " + str(currentStr) + (" up" if current > previous else " down") + " (" + str(percentChange) + ")" + " from " + str(previousStr) + suffix

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


def trendline(data, order=1):
    revenue = [87756000, 102697000, 114690000, 139785000, 188561000, 199214000, 191763000, 226102000]
    revenue = [0.85, 0.99, 1.01, 1.12, 1.25, 1.36, 1.28, 1.44]
    revenue = [0, 100, 200, 300, 400, 500, 600, 700]
    year = [1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000]
    data = pd.DataFrame({'year': year, 'revenue': revenue})
    data['revenue'] = data['revenue'] / 100
    data_ = [i for i in range(len(data))]
    print(data)

    coeffs = np.polyfit(data_, list(data['revenue']), order)
    print(coeffs)
    slope = coeffs[-2]
    return float(slope)


def imuafool(priceData, mrqData, dfMry=None, startDate='2018-05-08', endDate='2018-06-11'):
    print('---------------------------- Imuafool ---------------------------------')
    maxMonthPrice = priceData.groupby(['year', 'quarter'])['close'].agg(['mean', 'max', 'min', 'last']).reset_index()
    totalQuarterlyData = mrqData.merge(maxMonthPrice, on=['year', 'quarter'])
    totalQuarterlyData['fcf_ttm'] = totalQuarterlyData['fcf'].rolling(4).sum()
    totalQuarterlyData['mc_max'] = totalQuarterlyData['max'] * totalQuarterlyData['sharesbas']
    totalQuarterlyData['mc_min'] = totalQuarterlyData['min'] * totalQuarterlyData['sharesbas']
    totalQuarterlyData['mc_last'] = totalQuarterlyData['last'] * totalQuarterlyData['sharesbas']

    # Right now data - relies on up-to-date price data
    startDate = moment.date(startDate)
    endDate = moment.date(endDate)
    maxPrice = priceData.loc[startDate.date:endDate.date].max()['close']
    sharesbas_ = mrqData['sharesbas'][-1:].sum()
    maxMarketCap = maxPrice * sharesbas_
    minPrice = priceData.loc[startDate.date:endDate.date].min()['close']
    minMarketCap = minPrice * sharesbas_
    lastPrice = priceData['close'].iat[-1]
    lastMarketCap = lastPrice * sharesbas_
    lastEightQuarters = mrqData[-8:]

    change = periodChange(['revenue', 'netinc', 'eps', 'workingcapital'], lastEightQuarters)
    print(change.to_string())

    # print("Market Cap (min, max, last):", minMarketCap, maxMarketCap, lastMarketCap)
    # print("Current share price", lastPrice)
    print("52 week low/high", "???")
    ev = mrqData['ev'].iat[-1]
    print("EV/EBITDA (mrq)", ev / mrqData['ebitdausd'].iat[-1])
    print("EV/Sales (ttm)", ev / change['revenue_ttm'].iat[-1])
    print("Fwd P/E", "???")  # needs estimates
    print("Revenue. Net Income and Earnings")

    # print(source[['quarter','revenue']].to_string(formatters={'revenue':'${:,.0f}'.format}))
    # print(constructSentence("Fiscal 20XX Revenue", source['revenue'][-4:].sum(),source['revenue'][-8:-4].sum()))
    print("Revenue")
    print(lastEightQuarters[['quarter', 'grossmargin', 'ebitdamargin', 'netmargin']].to_string())
    print("Margins")
    print(lastEightQuarters[['quarter', 'grossmargin', 'ebitdamargin', 'netmargin']].to_string())
    print(lastEightQuarters[['year', 'grossmargin', 'ebitdamargin', 'netmargin']].to_string())
    # print("TrendLine",trendline(source['revenue']))
    print("Free Cash Flow")
    print(lastEightQuarters[['year', 'fcf']].to_string())

    print("Capital structure")
    lastEightQuarters['debtEquity'] = (lastEightQuarters['debtusd'] / lastEightQuarters['equity'])
    print(lastEightQuarters[
              ['cashnequsd', 'workingcapital', 'debtusd', 'equity', 'debtEquity']].dropna().transpose().to_string())
    # print(lastEightQuarters[['marketcap']].transpose().to_string())
    # print((lastEightQuarters['debtusd'] / mrqData['marketcap']).transpose().to_string())
    # print(lastEightQuarters['currentratio'].transpose().to_string())
    # print(tabulate.tabulate(lastEightQuarters[['currentratio']], headers="firstrow", tablefmt="pipe"))


# Return on Invested Capital (ROIC)-Weighted Average Cost of Capital (WACC) Spreads
# Date	   ROIC	   WACC	    EVA
#
# 6/8/18    45.5%	  13.6%   31.9%
# Q1 ‘18	  54.8%	  13.4%   41.5%
#
# FY 2017   60.4%	  14.1%	  46.3%
# FY 2016	  58.9%	  15.2%	  43.7%
# FY 2015	  43.8%	  18.2%	  25.7%
# FY 2014	  40.7%	  18.3%	  22.4%
# FY 2013	  35.5%	  16.0%	  19.5%

# Stock-based Compensation
#
# SBC/revenue ratios are favorably low.
#
# FY/QTR	  SBC	SBC/Revenue
# ($ M)
#
# Q1 ‘18	  2.30	  1.3%
#
# FY 2017   5.19	  0.9%
# FY 2016	  4.79	  1.0%
# FY 2015	  4.86	  1.1%
# FY 2014	  4.81	  1.2%
# FY 2013	  3.81	  1.1%

class Analyser:
    def __init__(self):
        pass


class TMF1000Analyser(Analyser):
    def __init__(self):
        super().__init__()
        self.formatter = Formatter()
        self.calculator = Calculator()

    def analyse(self, mrqData, mryData, priceData, start, end):
        fmt = self.formatter
        self.basics(fmt, mrqData)
        self.report(mrqData, priceData, start, end)
        # self.financials(fmt, mrqData)

        return self.calculator.periodChange(['revenue', 'deferredrev', 'netinc', 'eps', 'workingcapital', 'fcf'], mrqData)

    def financials(self, fmt, mrqData):
        hasDeferredRevenue = mrqData['deferredrev'].sum() > 0


        change = self.calculator.periodChange(['revenue', 'deferredrev', 'netinc', 'eps', 'workingcapital', 'fcf'], mrqData)
        change['billings'] = change['deferredrev_qchange_actual'] + change['revenue']
        change['revenue'] = change['revenue'].map(fmt.number_formatter)
        change['revenue_ttm'] = change['revenue_ttm'].map(fmt.number_formatter)
        change['revenue_qchange'] = change['revenue_qchange'].map(fmt.percent_formatter)
        change['revenue_yoy_qchange'] = change['revenue_yoy_qchange'].map(fmt.percent_formatter)
        print("\n### Revenue\n")
        print(
            tabulate.tabulate(change[['quarterString', 'revenue', 'revenue_ttm', 'revenue_qchange', 'revenue_yoy_qchange']],
                              headers=['Quarter', 'Revenue', 'TTM', '𝝳 (q-1)', '𝝳 (YoY)'],
                              tablefmt='pipe', showindex=False))
        print("\n### Deferred revenue\n")
        if (hasDeferredRevenue == False):
            print("No deferred revenue.")
        else:
            change['deferredrev'] = change['deferredrev'].map(fmt.number_formatter)
            change['billings'] = change['billings'].map(fmt.number_formatter)
            change['deferredrev_qchange'] = change['deferredrev_qchange'].map(fmt.percent_formatter)
            change['deferredrev_yoy_qchange'] = change['deferredrev_yoy_qchange'].map(fmt.percent_formatter)
            print(tabulate.tabulate(change[['quarterString', 'deferredrev', 'deferredrev_qchange', 'deferredrev_yoy_qchange', 'billings']],
                                    headers=['Quarter', 'Def.Revenue', '𝝳 (q-1)', '𝝳 (YoY)', 'Billings(Rev + 𝝳 def. rev)'],
                                    tablefmt='pipe', showindex=False))
        print("\n### Margins\n")
        # tabulate.tabulate(lastEightQuarters[['currentratio']], headers="firstrow", tablefmt="pipe"))
        capitalStructureData = mrqData[-8:][
            ['quarterString', 'grossmargin', 'ebitdamargin', 'netmargin', 'fcf', 'debtusd', 'equity', 'cashnequsd',
             'workingcapital', 'intexp', 'investments', 'intangibles']].reset_index()
        capitalStructureData['grossmargin'] = capitalStructureData['grossmargin'].map(fmt.percent_formatter)
        capitalStructureData['ebitdamargin'] = capitalStructureData['ebitdamargin'].map(fmt.percent_formatter)
        capitalStructureData['netmargin'] = capitalStructureData['netmargin'].map(fmt.percent_formatter)
        capitalStructureData['fcf'] = capitalStructureData['fcf'].map(fmt.number_formatter)
        print(tabulate.tabulate(capitalStructureData[['quarterString', 'grossmargin', 'ebitdamargin', 'netmargin']],
                                headers=['Quarter', 'Gross margin', 'ebitdamargin', 'netmargin'],
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
            headers=['cash', 'Investments', 'Cash and investments', 'Working Capital', 'Debt', 'Debt to Equity',
                     'Interest'], tablefmt='pipe', showindex=False))
        print("\n### Expenses\n")
        expensesData = mrqData[-8:][
            ['quarterString', 'quarter', 'year', 'rnd', 'sgna']].reset_index()
        expensesData = self.calculator.periodChange(['sgna', 'rnd'], expensesData)
        expensesData['rnd'] = expensesData['rnd'].map(fmt.number_formatter)
        expensesData['rnd_ttm'] = expensesData['rnd_ttm'].map(fmt.number_formatter)
        expensesData['sgna'] = expensesData['sgna'].map(fmt.number_formatter)
        expensesData['rnd_qchange'] = expensesData['rnd_qchange'].map(fmt.percent_formatter)
        expensesData['rnd_yoy_qchange'] = expensesData['rnd_yoy_qchange'].map(fmt.percent_formatter)
        expensesData['sgna_qchange'] = expensesData['sgna_qchange'].map(fmt.percent_formatter)
        expensesData['sgna_yoy_qchange'] = expensesData['sgna_yoy_qchange'].map(fmt.percent_formatter)
        print(tabulate.tabulate(
            expensesData[
                ['quarterString', 'rnd', 'rnd_ttm', 'rnd_qchange', 'rnd_yoy_qchange', 'sgna', 'sgna_qchange',
                 'sgna_yoy_qchange']].dropna(),
            headers=['Quarter', 'R and D', 'rnd(ttm)', 'Change (q-1)', 'Change (YoY)', 'Sales, General, Admin',
                     'Change (q-1)',
                     'Change (YoY)'], tablefmt='pipe', showindex=False))

    # Todo: report on each quarter - fold into report?
    def basics(self, fmt, mrqData):
        print('\n### Basic data (TMF1000)\n')
        print(mrqData.to_string())

        print(fmt.constructSentence("Revenue", mrqData['revenue'][-1:].sum(), mrqData['revenue'][-2:-1].sum()),
              "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(mrqData['revenue'][-5:-4].sum()))
        print(fmt.constructSentence("TTM Revenue", mrqData['revenue'][-4:].sum(), mrqData['revenue'][-8:-4].sum()), "")
        rps = mrqData['revenue'] / mrqData['shareswadil']
        print(fmt.constructSentence("TTM Revenue per share (diluted)", rps[-4:].sum(), rps[-8:-4].sum()))
        print(fmt.constructSentence("EPS diluted (prev quarter):", mrqData['epsdil'][-1:].sum(),
                                    mrqData['epsdil'][-2:-1].sum()), "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(mrqData['epsdil'][-5:-4].sum()))  # Previous quarter, -5 for same quarter last year
        print(fmt.constructSentence("TTM EPS (diluted)", mrqData['epsdil'][-4:].sum(), mrqData['epsdil'][-8:-4].sum()))
        print(fmt.constructSentence("Diluted share count", mrqData['shareswadil'][-1:].sum(),
                                    mrqData['shareswadil'][-5:-4].sum()))
        cash = mrqData['cashnequsd'][-1:].sum() + mrqData['investmentsc'][-1:].sum()
        print(fmt.constructSentence("Cash and short-term investments ", cash, mrqData['cashnequsd'][-2:-1].sum() + mrqData['investmentsc'][-2:-1].sum(), suffix=' (prev quarter)'))
        debt = mrqData['debtusd'][-1:].sum()
        print(fmt.constructSentence("Debt (prev quarter)", debt, mrqData['debtusd'][-2:-1].sum(), suffix=' (prev quarter)'))
        print(fmt.constructSentence("Free cash flow for quarter", mrqData['fcf'][-1:].sum(), mrqData['fcf'][-2:-1].sum()))
        print(fmt.constructSentence("TTM free cash flow", mrqData['fcf'][-4:].sum(), mrqData['fcf'][-8:-4].sum()))
        print("* TTM cash flow per share was $%s" % fmt.number_formatter(
            mrqData['fcf'][-4:].sum() / mrqData['shareswadil'][-1:].sum()))
        print(fmt.constructSentence("Gross margins", mrqData['grossmargin'][-1:].sum(), mrqData['grossmargin'][-2:-1].sum()))
        print(fmt.constructSentence("CapExp", abs(mrqData['capex'][-1:].sum()), abs(mrqData['capex'][-2:-1].sum())))

    def report(self, mrqData, priceData, start, end):
        print("\n### Trading data \n")

        fmt = Formatter()
        # Subtract a year from start to make sure we have enough for TTM
        # dataRange = pd.date_range(start=start - pd.offsets.QuarterBegin() - pd.DateOffset(years=1), end=end + pd.offsets.QuarterEnd(), freq='Q')
        dataRange = pd.date_range(start=start - pd.offsets.QuarterBegin() - pd.DateOffset(years=5), end=end + pd.offsets.QuarterEnd(), freq='Q')
        dates = pd.DataFrame(dataRange, columns=['date'])
        dates['quarterEnd'] = dates['date'].map(lambda x: x + pd.offsets.QuarterEnd(n=0))
        dates['prev_quarter'] = dates['quarterEnd'].shift(1)
        dates['quarterString'] = dates['quarterEnd'].map(lambda x: pd.Period(x, 'Q'))
        dates['quarterInt'] = dates['quarterEnd'].map(lambda x: x.quarter)
        dates['year'] = dates['quarterEnd'].map(lambda x: x.year)
        # This method will do the quarter after the last reported quarter. Even if its being run in the quarter after
        # eg, running 3 July, it will do
        # print("Dates")
        # print(dates.to_string())

        # At this point, we have per-day price data. When we group by, we need to have pruned the price data appropriately.
        # (in order to get correct max and min dates.
        # However,
        priceData['quarterEnd'] = priceData['date'].map(lambda x: x + pd.offsets.QuarterEnd(n=0))
        relevantPriceData = priceData[(priceData['date'] >= start) & (priceData['date'] < end)][['date', 'high', 'low', 'close', 'quarterEnd']]
        priceSummary = relevantPriceData.groupby('quarterEnd')['high', 'low', 'close', 'date'].agg(['max', 'min', 'last'])

        # These next two lines flatten out the hierarchical index caused by the multicolumn groupby above.
        priceSummary.columns = priceSummary.columns.map('_'.join)
        priceSummary = priceSummary.reset_index()
        # Add in the prev_quarter data - 'dates' is the canonical source of all relevant dates.
        priceSummary = priceSummary.merge(dates, on=['quarterEnd'])
        mrqData.set_index(['calendardate'], inplace=True)
        dates.set_index(['quarterEnd'], inplace=True)

        # populate ttm/max/min/last figures
        mrqData['fcf_ttm'] = mrqData['fcf'].rolling(4).sum()
        mrqData['eps_ttm'] = mrqData['epsusd'].rolling(4).sum()
        mrqData['rev_ttm'] = mrqData['revenue'].rolling(4).sum()
        mrqData['rpsdil'] = mrqData['rev_ttm'] / mrqData['shareswadil']
        mrqData['rps_ttm'] = mrqData['rev_ttm'] / mrqData['shareswadil']
        mrqData['ttmEps_previous'] = mrqData['eps_ttm'].shift(-4)
        mrqData['ttmEpsGrowth'] = mrqData['eps_ttm'].pct_change(periods=4)

        mostRecentData = dates.join(mrqData, lsuffix='_date', rsuffix='_mrq')
        mostRecentData.fillna(method='ffill', inplace=True)

        # print(mostRecentData.to_string())
        priceSummary.set_index('prev_quarter', inplace=True)
        # print(priceSummary.to_string())
        # print(mostRecentData.to_string())
        # Join works as a left join on the indexes by default
        mostRecentData = priceSummary.join(mostRecentData, lsuffix='_caller', rsuffix='_other')

        # Share price dependent
        mostRecentData['marketCap_max'] = mostRecentData['sharesbas'] * mostRecentData['high_max']
        mostRecentData['marketCap_min'] = mostRecentData['sharesbas'] * mostRecentData['low_min']
        mostRecentData['marketCap_last'] = mostRecentData['sharesbas'] * mostRecentData['close_last']
        mostRecentData['ev_min'] = mostRecentData['marketCap_min'] + mostRecentData['debt'] - mostRecentData['cashnequsd']
        mostRecentData['ev_max'] = mostRecentData['marketCap_max'] + mostRecentData['debt'] - mostRecentData['cashnequsd']
        mostRecentData['ev_last'] = mostRecentData['marketCap_last'] + mostRecentData['debt'] - mostRecentData['cashnequsd']

        mostRecentData['ttmPE_min'] = mostRecentData['low_min'] / mostRecentData['eps_ttm']
        mostRecentData['ttmPE_max'] = mostRecentData['high_max'] / mostRecentData['eps_ttm']
        mostRecentData['ttmPE_last'] = mostRecentData['close_last'] / mostRecentData['eps_ttm']
        mostRecentData['1YPEG_min'] = mostRecentData['ttmPE_min'] / (mostRecentData['ttmEpsGrowth'] * 100)
        mostRecentData['1YPEG_max'] = mostRecentData['ttmPE_max'] / (mostRecentData['ttmEpsGrowth'] * 100)
        mostRecentData['1YPEG_last'] = mostRecentData['ttmPE_last'] / (mostRecentData['ttmEpsGrowth'] * 100)

        def report(quarterData):

            startDateFmt = moment.Moment(quarterData['date_min']).format('MMM D, YYYY')
            endDateFmt = moment.Moment(quarterData['date_max']).format('MMM D, YYYY')
            quarterDateFmt = moment.Moment(quarterData['quarterEnd']).format('MMM D, YYYY')
            print('--------------- Trading days for quarter ended: %s  (%s - %s) ------------------------------' % (quarterDateFmt, startDateFmt, endDateFmt))
            print("* Trading range was %s to %s [%s]" % (quarterData['low_min'], quarterData['high_max'], quarterData['close_last']))
            print("* Market cap  was %s to %s [%s]" % (
                fmt.number_formatter(quarterData['marketCap_min']), fmt.number_formatter(quarterData['marketCap_max']),
                fmt.number_formatter(quarterData['marketCap_last'])))

            lastTtmEps = quarterData['eps_ttm']
            rps = quarterData['rps_ttm']
            lastFreeCashFlow = quarterData['fcf_ttm']
            ttmRevenue = quarterData['rev_ttm']

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
                fmt.number_formatter(quarterData['ttmEpsGrowth']), fmt.number_formatter(quarterData['eps_ttm']),
                fmt.number_formatter(quarterData['ttmEps_previous'])))
            print("* 1YPEG (under 1.0 desirable) was %s to %s [%s]" % (
                fmt.number_formatter(quarterData['1YPEG_min']), fmt.number_formatter(quarterData['1YPEG_max']),
                fmt.number_formatter(quarterData['1YPEG_last'])))
            pass

        reportData = mostRecentData[(mostRecentData['date_min'] >= start) & (mostRecentData['date_min'] < end)]
        for index, row in reportData.iterrows():
            report(row)

        return mostRecentData


def ntnxAdjustments(df):
    # This data is from morningstar/iex
    df.loc[(df.dimension == 'MRQ') & (df.calendardate == '2017-06-30'), 'revenue'] = 173424000
    return df


def analyse(ticker, start, end):
    if not isinstance(ticker, list):
        ticker = [ticker]
    adjustments = {
        'NTNX': ntnxAdjustments
    }

    for t in ticker:
        priceData = DataLoader().loadPriceDataLive(ticker=t)
        # priceData = DataLoader().loadPriceData(t)
        # peerData = DataLoader().loadPeerDataLive(ticker)
        mrqData, mryData, arqData = DataLoader().loadDataLive(ticker=t)
        # mrqData, mryData, arqData = DataLoader().loadData(ticker=t)
        # graphs.graph(ticker, mrqData, 'calendardate', 'assets')
        print(t)
        changeData = TMF1000Analyser().analyse(mrqData, mryData, priceData, start=start, end=end)

        # , end=pd.Timestamp.now())

    return
    # pool = Pool(processes=8)
    cagr = np.arange(0.2, 0.4, 0.05)
    opMargin = np.arange(0.1, 0.4, 0.05)

    start = time.time()
    df = pd.DataFrame(index=opMargin, columns=cagr)
    for x in cagr:
        for y in opMargin:
            d = DCF(mrqData, x, y)
            # pool.apply(d.calc, args=())
            df.at[y, x] = float(d.calc())
            pass

    end = time.time()
    print("\n### DCF \n")
    print(tabulate.tabulate(df, headers=df.columns, tablefmt='pipe', showindex=True))

    exit(1)


class Screen:
    pd.set_option('display.max_colwidth', -1)

    def __init__(self):
        self.DATA_PKL = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_data-mod.pkl'
        self.df = self.loadBaseData()
        self.writePickle()
        # self.df = self.readPickle(self.DATA_PKL)
        self.filter()

    def readPickle(self, DATA_PKL):
        print("Reading pickle")
        return pd.read_pickle(DATA_PKL)

    def loadBaseData(self):
        mrq, mry_, arq, ary = DataLoader().loadAllData()
        df = mrq
        # Workaround from: https://github.com/pandas-dev/pandas/issues/21200
        g = df.groupby('ticker')
        df['ttm_revenue'] = g['revenue'].apply(lambda x: x.rolling(4).sum())
        df['ttm_eps'] = g['eps'].apply(lambda x: x.rolling(4).sum())
        df['ttm_fcf'] = g['fcf'].apply(lambda x: x.rolling(4).sum())

        df['prevquarter_revenue_pct_change'] = g['revenue'].apply(lambda x: x.pct_change(periods=1))
        df['samequarter_revenue_pct_change'] = g['revenue'].apply(lambda x: x.pct_change(periods=4))
        df['prevquarter_ttmrevenue_pct_change'] = g['ttm_revenue'].apply(lambda x: x.pct_change(periods=1))
        df['samequarter_ttmrevenue_pct_change'] = g['ttm_revenue'].apply(lambda x: x.pct_change(periods=4))

        df['prevquarter_eps_pct_change'] = g['eps'].apply(lambda x: x.pct_change(periods=1))
        df['samequarter_eps_pct_change'] = g['eps'].apply(lambda x: x.pct_change(periods=4))
        df['prevquarter_ttmeps_pct_change'] = g['ttm_eps'].apply(lambda x: x.pct_change(periods=1))
        df['samequarter_ttmeps_pct_change'] = g['ttm_eps'].apply(lambda x: x.pct_change(periods=4))

        df['prevquarter_fcf_pct_change'] = g['fcf'].apply(lambda x: x.pct_change(periods=1))
        df['samequarter_fcf_pct_change'] = g['fcf'].apply(lambda x: x.pct_change(periods=4))
        df['prevquarter_ttmfcf_pct_change'] = g['ttm_fcf'].apply(lambda x: x.pct_change(periods=1))
        df['samequarter_ttmfcf_pct_change'] = g['ttm_fcf'].apply(lambda x: x.pct_change(periods=4))
        # df['evrev'] = df['ev']  / df['ttm_revenue']


        # print(df[(df['ticker'] == 'NVDA')| (df['ticker'] == 'AAPL')].to_string())
        # exit(1)
        return df

    def writePickle(self):
        self.df.to_pickle(self.DATA_PKL)

    def filter(self):
        last = self.df.groupby(['ticker']).tail(8)
        last['ev/sales'] = last['ev'] / last['ttm_revenue']
        last['p/fcf'] = last['price'] / last['fcf']
        print(last['ttm_fcf'])
        filtered = last[
            (last['ttm_revenue'] > 1e8) & (last['ttm_revenue'] < 1e9) & (last['marketcap'] < 15e9) & (last['ev/sales'] < 10)
            & (last['deferredrev'] > 0)
            & (last['eps'] > 0)
            & (last['ttm_fcf'] > 0)
            & (last['grossmargin'] > 0.7)
            & (last['samequarter_ttmeps_pct_change'] > 0.1)
            & (last['samequarter_ttmrevenue_pct_change'] >= 0.3)]

        tolist = last['ticker'].tolist()
        dfCompany = DataLoader().loadBatchCompanyDataLive(tolist)
        filtered = filtered.merge(dfCompany, on=['ticker']).groupby(['ticker']).tail(1)
        # filtered['company'] = filtered['ticker'].apply(DataLoader().loadCompanyDataLive)
        print(filtered[
                  ['ticker', 'p/fcf', 'calendardate', 'industry', 'eps', 'deferredrev', 'description', 'ttm_revenue', 'samequarter_ttmrevenue_pct_change', 'ev/sales']].to_string())

        # sum_ = last[(last['ttm_revenue'] > changeData['revenue_ttm'][-1:].sum()) & (last['revenue_qchange'] > changeData['revenue_qchange'][-1:].sum()) & (
        #     last['revenue_yoy_qchange'] > changeData['revenue_yoy_qchange'][-1:].sum())]
        # print(sum_[['ttm_revenue', 'revenue_qchange', 'revenue_yoy_qchange']])


# Screen()
# analyse(['AYX', 'MDB', 'NTNX', 'OKTA', 'PVTL', 'PSTG', 'SHOP', 'SQ', 'TWLO', 'ZS'])
analyse('CAKE', start=pd.Timestamp(year=2018, month=4, day=25), end=pd.Timestamp(year=2018, month=7, day=17))

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
