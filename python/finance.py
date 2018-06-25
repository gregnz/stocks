from datetime import datetime

import moment as moment
import numpy as np
import pandas as pd
import json
import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tabulate as tabulate

matplotlib.use('TkAgg')

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')


def loadPriceDataLive(ticker):
    r = requests.get('https://api.iextrading.com/1.0/stock/%s/chart/5y' % ticker)
    file = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_price.json' % ticker
    with open(file, 'w') as jsonData:
        json.dump(r.json(), jsonData)
    df = pd.DataFrame.from_dict(r.json())
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
    df['quarterString'] = df['date'].map(lambda x: pd.Period(x, 'Q'))
    df['quarter'] = df['date'].map(lambda x: x.quarter)
    df['year'] = df['date'].map(lambda x: x.year)
    return df


def loadPriceData(ticker):
    # curl -XGET 'https://api.iextrading.com/1.0/stock/ntnx/chart/5y' > NTNX_price.json

    file = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_price.json' % ticker
    with open(file) as jsonData:
        dict_train = json.load(jsonData)
    df = pd.DataFrame.from_dict(dict_train)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
    df['quarterString'] = df['date'].map(lambda x: pd.Period(x, 'Q'))
    df['quarter'] = df['date'].map(lambda x: x.quarter)
    df['year'] = df['date'].map(lambda x: x.year)
    return df


def loadData(ticker='FOSL', adjustments={}):
    """Load the data for a single letter label."""
    df = pd.read_csv('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_historical.csv' % ticker, delimiter=',',
                     parse_dates=['calendardate', 'lastupdated', 'reportperiod', 'datekey'], date_parser=dateparse)
    df['quarterString'] = df['calendardate'].map(lambda x: pd.Period(x, 'Q'))
    df['quarter'] = df['calendardate'].map(lambda x: x.quarter)
    df['year'] = df['calendardate'].map(lambda x: x.year)
    df.set_index(pd.DatetimeIndex(df['calendardate']), inplace=True)
    # df.dropna(subset=['revenue', 'equity'], inplace=True)

    # TODO: Update for FCF?
    # Net Income
    # + Depreciation/Amortization + (Interest Expense - Interest Income) * (1 - Tax Rate)
    # - Changes in Working Capital
    # - Capital expenditure
    # = Free Cash Flow
    adjustmentsForTicker = adjustments[ticker] if ticker in adjustments else None
    if (adjustmentsForTicker != None):
        df = adjustmentsForTicker(df)

    return (df[(df.dimension == 'MRQ')]), (df[(df.dimension == 'MRY')])


# Quandl headings
quandl_headings = ['ticker', 'dimension', 'calendardate', 'datekey', 'reportperiod', 'lastupdated', 'accoci', 'assets', 'assetsavg', 'assetsc', 'assetsnc', 'assetturnover', 'bvps',
                   'capex', 'cashneq', 'cashnequsd', 'cor', 'consolinc', 'currentratio', 'de', 'debt', 'debtc', 'debtnc', 'debtusd', 'deferredrev', 'depamor', 'deposits',
                   'divyield', 'dps', 'ebit', 'ebitda', 'ebitdamargin', 'ebitdausd', 'ebitusd', 'ebt', 'eps', 'epsdil', 'epsusd', 'equity', 'equityavg', 'equityusd', 'ev',
                   'evebit', 'evebitda', 'fcf', 'fcfps', 'fxusd', 'gp', 'grossmargin', 'intangibles', 'intexp', 'invcap', 'invcapavg', 'inventory', 'investments', 'investmentsc',
                   'investmentsnc', 'liabilities', 'liabilitiesc', 'liabilitiesnc', 'marketcap', 'ncf', 'ncfbus', 'ncfcommon', 'ncfdebt', 'ncfdiv', 'ncff', 'ncfi', 'ncfinv',
                   'ncfo', 'ncfx', 'netinc', 'netinccmn', 'netinccmnusd', 'netincdis', 'netincnci', 'netmargin', 'opex', 'opinc', 'payables', 'payoutratio', 'pb', 'pe', 'pe1',
                   'ppnenet', 'prefdivis', 'price', 'ps', 'ps1', 'receivables', 'retearn', 'revenue', 'revenueusd', 'rnd', 'roa', 'roe', 'roic', 'ros', 'sbcomp', 'sgna',
                   'sharefactor', 'sharesbas', 'shareswa', 'shareswadil', 'sps', 'tangibles', 'taxassets', 'taxexp', 'taxliabilities', 'tbvps', 'workingcapital']


def periodChange(columns, source):
    df = pd.DataFrame()
    for column in columns:
        df[column] = source[column]
        df[column + '_ttm'] = source[column].rolling(4).sum()
        df[column + '_qchange'] = source[column].pct_change(periods=1)
        df[column + '_prev_qchg'] = source[column].pct_change(periods=4)
        df['quarterString'] = source['quarterString']
        df['quarter'] = source['quarter']
        df['year'] = source['year']

        df.set_index(source['calendardate'], inplace=True)
    return df


def valuePoints(source):
    df = pd.DataFrame()
    # How the various PEs are calculate in Quandl
    df['pe_calc'] = source['price'] / (source['eps'].rolling(4).sum())
    df['pe1_calc'] = source['marketcap'] / (source['netinccmnusd'].rolling(4).sum())
    df['pe'] = source['pe']
    df['pe1'] = source['pe1']
    df['ev_revenue'] = source['ev'] / source['revenue']
    print(df)
    return df


def number_formatter(num, m=1000000):
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


def percent_formatter(num):
    if (np.isnan(num)):
        return ''
    return '{0:.0f}%'.format(num * 100)


def constructSentence(key, current, previous, suffix=''):
    if (previous == 0):
        percentChange = '\u221e'
    else:
        percentChange = '{0:.1f}%'.format(abs((current - previous) * 100 / previous))
    current = number_formatter(current)
    previous = number_formatter(previous)
    return "* " + key + " was " + str(current) + (" up" if current > previous else " down") + " (" + str(percentChange) + ")" + " from " + str(previous) + suffix


def constructMinMaxSentence(key, min, max):
    # ** Trading range between April 25, 2018 and the present May 29, 2018 was $49.64 to $54.48: PE ratio range was 15.91 to 17.46: PS ratio range was 1.01 to 1.11: Cash flow yield range was 5.3% to 5.8%
    # Non-GAAP PE ratio range was 21.12 to 23.18

    return key + " was " + str(number_formatter(min)) + " to " + str(number_formatter(max))


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

    startDateFmt = startDate.format('MMM D, YYYY')
    endDateFmt = endDate.format('MMM D, YYYY')

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
    # print(constructSentence("Fiscal 20XX Revenue", source['revenue'][-4:].sum(),source['revenue'][-9:-5].sum()))
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
    print(lastEightQuarters[['cashnequsd', 'workingcapital', 'debtusd', 'equity', 'debtEquity']].dropna().transpose().to_string())
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

pass


def TMF1000(mrqData, mryData, priceData, startDate='2018-05-08', endDate='2018-06-19'):
    print('\n### Basic data (TMF1000)\n')

    print(constructSentence("Revenue", mrqData['revenue'][-1:].values[0], mrqData['revenue'][-2:-1].values[0]),
          "from the previous quarter" + " (%s same quarter last year)" % number_formatter(mrqData['revenue'][-5:-4].values[0]))
    print(constructSentence("TTM Revenue", mrqData['revenue'][-4:].sum(), mrqData['revenue'][-9:-5].sum()), "")

    rps = mrqData['revenue'] / mrqData['shareswadil']
    print(constructSentence("TTM Revenue per share", rps[-4:].sum(), rps[-9:-5].sum()))
    print(constructSentence("Earnings (prev quarter):", mrqData['epsdil'][-1:].sum(), mrqData['epsdil'][-2:-1].sum()))  # Previous quarter, -5 for same quarter last year
    print(constructSentence("Earnings (same quarter prev year):", mrqData['epsdil'][-1:].sum(), mrqData['epsdil'][-5:-4].sum()))  # Previous quarter, -5 for same quarter last year
    print(constructSentence("TTM eps", mrqData['epsdil'][-4:].sum(), mrqData['epsdil'][-9:-5].sum()))

    print(constructSentence("Diluted share count", mrqData['shareswadil'][-1:].sum(), mrqData['shareswadil'][-5:-4].sum()))
    print(constructSentence("Cash ", mrqData['cashnequsd'][-1:].sum(), mrqData['cashnequsd'][-2:-1].sum(), suffix=' (prev quarter)'))
    print(constructSentence("Debt (prev quarter)", mrqData['debtusd'][-1:].sum(), mrqData['debtusd'][-2:-1].sum(), suffix=' (prev quarter)'))
    print(constructSentence("Cash flow for quarter", mrqData['fcf'][-1:].sum(), mrqData['fcf'][-2:].sum()))
    print(constructSentence("Cash flow for TTM", mrqData['fcf'][-4:].sum(), mrqData['fcf'][-9:-5].sum()))
    print("* Cash flow per share for TTM was $%s" % number_formatter(mrqData['fcf'][-4:].sum() / mrqData['shareswadil'][-1:].sum()))
    print(constructSentence("Gross margins", mrqData['grossmargin'][-1:].sum(), mrqData['grossmargin'][-2:-1].sum()))
    print(constructSentence("CapExp", abs(mrqData['capex'][-1:].sum()), abs(mrqData['capex'][-2:-1].sum())))



    print("\n### Ranges min, max [last]\n")
    # maxMonthPrice = priceData.groupby(['year', 'quarter'])['close'].agg(['mean', 'max', 'min', 'last']).reset_index()
    totalQuarterlyData = mrqData  # .merge(maxMonthPrice, on=['year', 'quarter'])
    totalQuarterlyData['fcf_ttm'] = totalQuarterlyData['fcf'].rolling(4).sum()
    totalQuarterlyData['eps_ttm'] = totalQuarterlyData['epsusd'].rolling(4).sum()
    totalQuarterlyData['rev_ttm'] = totalQuarterlyData['revenue'].rolling(4).sum()
    totalQuarterlyData['rpsdil'] = totalQuarterlyData['rev_ttm'] / totalQuarterlyData['shareswadil']
    totalQuarterlyData['rps'] = totalQuarterlyData['rev_ttm'] / totalQuarterlyData['shareswadil']

    lastEps = totalQuarterlyData['eps_ttm'][-1:].sum()
    lastRps = totalQuarterlyData['rps'][-1:].sum()
    freeCashFlow = totalQuarterlyData['fcf_ttm'][-1:].sum()
    sharesbas_ = totalQuarterlyData['sharesbas'][-1:].sum()

    startDate = moment.date(startDate)
    endDate = moment.date(endDate)
    maxPrice = priceData.loc[startDate.date:endDate.date].max()['close']
    maxMarketCap = maxPrice * sharesbas_
    minPrice = priceData.loc[startDate.date:endDate.date].min()['close']
    minMarketCap = minPrice * sharesbas_
    lastPrice = priceData.iloc[-1:]['close'].sum()
    lastMarketCap = lastPrice * sharesbas_
    ev = mrqData['ev'][-1:].sum() + (lastMarketCap - mrqData.iloc['marketcap'][-1:].sum())
    print("* Enterprise value(EV) %s" % (number_formatter(ev)))
    print("* EV/Sales %s" % (number_formatter(ev / mrqData['revenue'][-1:].values[0])))


    startDateFmt = startDate.format('MMM D, YYYY')
    endDateFmt = endDate.format('MMM D, YYYY')
    print("* Trading range between %s - %s was %s to %s [%s]" % (startDateFmt, endDateFmt, minPrice, maxPrice, lastPrice))
    print("* Market cap between %s - %s was %s to %s [%s]" % (
        startDateFmt, endDateFmt, number_formatter(minMarketCap), number_formatter(maxMarketCap), number_formatter(lastMarketCap)))

    if lastEps < 0:
        print("* PE range (%s - %s) not applicable (earnings < 0)" % (startDateFmt, endDateFmt))
    else:
        print("* PE range (%s - %s) was %s to %s [%s]" % (
            startDateFmt, endDateFmt, minPrice['close'] / lastEps, maxPrice['close'] / lastEps, lastPrice / lastEps))

    print("* PS ratio range (%s - %s) was %s to %s [%s]" % (
        startDateFmt, endDateFmt, number_formatter((minPrice) / lastRps), number_formatter((maxPrice / lastRps)), number_formatter((lastPrice) / lastRps)))
    # Cash flow yield range was 6.98% to 12.99%
    print("* Free cash flow yield range (%s - %s) was %s to %s [%s]" % (
        startDateFmt, endDateFmt, number_formatter(freeCashFlow * 100 / maxMarketCap), number_formatter(freeCashFlow * 100 / minMarketCap),
        number_formatter(freeCashFlow * 100 / lastMarketCap)))


    # print(totalQuarterlyData[
    #           ['max', 'min', 'last', 'fcfyield_last', 'fcfyield_max', 'fcfyield_min', 'fcf', 'mc_max', 'mc_min', 'mc_last', 'marketcap', 'fcf_ttm', 'calendardate']].to_string())
    change = periodChange(['revenue', 'deferredrev', 'netinc', 'eps', 'workingcapital', 'fcf'], mrqData)

    change['revenue'] = change['revenue'].map(number_formatter)
    change['revenue_ttm'] = change['revenue_ttm'].map(number_formatter)
    change['revenue_qchange'] = change['revenue_qchange'].map(percent_formatter)
    change['revenue_prev_qchg'] = change['revenue_prev_qchg'].map(percent_formatter)
    print("\n### Revenue\n")
    print(tabulate.tabulate(change[['quarterString', 'revenue', 'revenue_ttm', 'revenue_qchange', 'revenue_prev_qchg']],
                            headers=['Quarter', 'Revenue', 'TTM', 'Change (q-1)', 'Change (YoY)'],
                            tablefmt='pipe', showindex=False))
    print("\n### Deferred revenue\n")
    change['deferredrev'] = change['deferredrev'].map(number_formatter)
    change['deferredrev_qchange'] = change['deferredrev_qchange'].map(percent_formatter)
    change['deferredrev_prev_qchg'] = change['deferredrev_prev_qchg'].map(percent_formatter)
    print(tabulate.tabulate(change[['quarterString', 'deferredrev', 'deferredrev_qchange', 'deferredrev_prev_qchg']],
                            headers=['Quarter', 'Def.Revenue', 'Change (q-1)', 'Change (YoY)'],
                            tablefmt='pipe', showindex=False))

    print("\n### Margins\n")
    # tabulate.tabulate(lastEightQuarters[['currentratio']], headers="firstrow", tablefmt="pipe"))
    lastEightQuarters = mrqData[-8:][['quarterString', 'grossmargin', 'ebitdamargin', 'netmargin', 'fcf', 'debtusd', 'equity', 'cashnequsd', 'workingcapital']].reset_index()
    lastEightQuarters['grossmargin'] = lastEightQuarters['grossmargin'].map(percent_formatter)
    lastEightQuarters['ebitdamargin'] = lastEightQuarters['ebitdamargin'].map(percent_formatter)
    lastEightQuarters['netmargin'] = lastEightQuarters['netmargin'].map(percent_formatter)
    lastEightQuarters['fcf'] = lastEightQuarters['fcf'].map(number_formatter)
    print(tabulate.tabulate(lastEightQuarters[['quarterString', 'grossmargin', 'ebitdamargin', 'netmargin']], headers=['Quarter', 'Gross margin', 'ebitdamargin', 'netmargin'],
                            tablefmt='pipe'))
    # print(tabulate.tabulate(mryData[-4:][['year', 'grossmargin', 'ebitdamargin', 'netmargin']], tablefmt='pipe'))
    print("\n### Free cash flow\n")
    print(tabulate.tabulate(lastEightQuarters[['quarterString', 'fcf', ]], headers=['Quarter', 'FCF'], tablefmt='pipe'))

    print("Capital structure")
    lastEightQuarters['debtEquity'] = (lastEightQuarters['debtusd'] / lastEightQuarters['equity'])

    print(lastEightQuarters[['cashnequsd', 'workingcapital', 'debtusd', 'equity', 'debtEquity']].dropna().to_string())



pass


# quandl_headings = ['ticker', 'dimension', 'calendardate', 'datekey', 'reportperiod', 'lastupdated', 'accoci', 'assets', 'assetsavg', 'assetsc', 'assetsnc', 'assetturnover', 'bvps',
#                    'capex', 'cashneq', 'cashnequsd', 'cor', 'consolinc', 'currentratio', 'de', 'debt', 'debtc', 'debtnc', 'debtusd', 'deferredrev', 'depamor', 'deposits',
#                    'divyield', 'dps', 'c', 'ebitda', 'ebitdamargin', 'ebitdausd', 'ebitusd', 'ebt', 'eps', 'epsdil', 'epsusd', 'equity', 'equityavg', 'equityusd', 'ev',
#                    'evebit', 'evebitda', 'fcf', 'fcfps', 'fxusd', 'gp', 'grossmargin', 'intangibles', 'intexp', 'invcap', 'invcapavg', 'inventory', 'investments', 'investmentsc',
#                    'investmentsnc', 'liabilities', 'liabilitiesc', 'liabilitiesnc', 'marketcap', 'ncf', 'ncfbus', 'ncfcommon', 'ncfdebt', 'ncfdiv', 'ncff', 'ncfi', 'ncfinv',
#                    'ncfo', 'ncfx', 'netinc', 'netinccmn', 'netinccmnusd', 'netincdis', 'netincnci', 'netmargin', 'opex', 'opinc', 'payables', 'payoutratio', 'pb', 'pe', 'pe1',
#                    'ppnenet', 'prefdivis', 'price', 'ps', 'ps1', 'receivables', 'retearn', 'revenue', 'revenueusd', 'rnd', 'roa', 'roe', 'roic', 'ros', 'sbcomp', 'sgna',
#                    'sharefactor', 'sharesbas', 'shareswa', 'shareswadil', 'sps', 'tangibles', 'taxassets', 'taxexp', 'taxliabilities', 'tbvps', 'workingcapital']

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
            print("Warning: not enough data to complete amortisation schedule. Years to amortise is:", yearsToAmortise, "but only ", len(mrqData),
                  "quarters available. Only available data will be used.")

        for i in range(0, yearsToAmortise):
            startIndex = (i + 1) * 4
            endIndex = i * 4
            rndValues = np.append(rndValues, mrqData['rnd'][-startIndex:-endIndex].sum())

    def operatingLeases(self):
        pass


class dcf:
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
                          columns=['i', 'revenueGrowth', 'revenue', 'ebitMargin', 'ebit', 'taxRate', 'ebitAfterTax', 'reinvestment', 'fcff', 'nol', 'wacc', 'cumDiscountFactor',
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
            df.loc[i, 'revenueGrowth'] = self.constantStartConvergence(c.yearOfRevenueGrowthConvergence, i, d.cagr, d.targetCagr)
            df.loc[i, 'wacc'] = self.constantStartConvergence(c.constantYearsOfWaccBeforeConvergence, i, d.initialCostOfCapital, d.targetCostOfCapital)
            df.loc[i, 'cumDiscountFactor'] = (df.loc[i - 1, 'cumDiscountFactor'] * (1 / (1 + df.loc[i, 'wacc']))) if i > 1 else (1 / (1 + df.loc[i, 'wacc']))
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
                df.loc[i, 'ebitAfterTax'] = df.loc[i, 'ebit'] if df.loc[i, 'ebit'] < df.loc[i, 'nol'] else (df.loc[i, 'ebit'] - df.loc[i, 'nol']) * (1 - df.loc[i, 'taxRate'])

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

        # print(df.to_string())
        # print(discountFactor)
        # print("terminalCashFlow", terminalCashFlow)
        # print("terminalCostOfCapital", terminalCostOfCapital)
        # print("terminalRevenueGrowth", terminalRevenueGrowth)
        # print("terminalValue", terminalValue)
        # print("pvTerminalValue", pvTerminalValue)
        # print("WACC", d.initialCostOfCapital, d.targetCostOfCapital)
        # print("pvFcff", pvFcff)

        def calcOperatingAssets(presentValues, probabilityOfFailure=0.0, proceedsIfFirmFails=0):
            return presentValues * (1 - probabilityOfFailure) + proceedsIfFirmFails * probabilityOfFailure

        valueOfOperatingAssets = calcOperatingAssets(pvFcff + pvTerminalValue)
        valueOfEquity = valueOfOperatingAssets - d.debt
        valueOfEquity = valueOfEquity - d.minorityInterests
        valueOfEquity = valueOfEquity + d.cash
        valueOfEquity = valueOfEquity + d.nonOpAssets
        valueOfEquityInCommon = valueOfEquity - d.optionsValue
        valuePerShare = valueOfEquityInCommon / d.numberShares

        # print("valueOfOperatingAssets", valueOfOperatingAssets)
        # print("Value of equity", valueOfEquity)
        print("Value per share", valuePerShare)
        return valuePerShare


def ntnxAdjustments(df):
    # This data is from morningstar/iex
    df.loc[(df.dimension == 'MRQ') & (df.calendardate == '2017-06-30'), 'revenue'] = 173424000
    return df


priceData = loadPriceDataLive(ticker='NTNX')
# priceData = loadPriceData('NTNX')
adjustments = {
    'NTNX': ntnxAdjustments
}
mrqData, mryData = loadData('NTNX', adjustments)
print(mrqData.to_string())

TMF1000(mrqData, mryData, priceData)

# DcfAdjustments().researchAndDevelopment(mrqData)

# cagrRange = np.linspace(0.2, 0.4, num=5)
# ebitMarginRange = np.linspace(0.2, 0.4, num=5)
# df = pd.DataFrame(index=cagrRange, columns=ebitMarginRange)
# print(df)
# for cagr in cagrRange:
#     values = np.array([])
#     for targetEbitMargin in ebitMarginRange:
#         value = dcf(mrqData, cagr, targetEbitMargin).calc()
#         values = np.append(values, value)
#     df._setitem_array(cagr, values)
#
# print(df.to_string())



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
