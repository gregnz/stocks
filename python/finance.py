from datetime import datetime

import csv
import numpy as np
import moment as moment
import pandas as pd
import json
import requests
import matplotlib

from dcf import DCF
from dataloader import DataLoader

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
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
        print(df)
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

    def analyse(self, mrqData, mryData, priceData, startDate='2017-11-01', endDate='2018-07-25'):
        print('\n### Basic data (TMF1000)\n')

        fmt = self.formatter
        print(fmt.constructSentence("Revenue", mrqData['revenue'][-1:].values[0], mrqData['revenue'][-2:-1].values[0]),
              "from the previous quarter" + " (%s same quarter last year)" % fmt.number_formatter(
                  mrqData['revenue'][-5:-4].values[0]))
        print(fmt.constructSentence("TTM Revenue", mrqData['revenue'][-4:].sum(), mrqData['revenue'][-9:-5].sum()), "")

        rps = mrqData['revenue'] / mrqData['shareswadil']
        print(fmt.constructSentence("TTM Revenue per share", rps[-4:].sum(), rps[-9:-5].sum()))
        print(fmt.constructSentence("Earnings (prev quarter):", mrqData['epsdil'][-1:].sum(),
                                    mrqData['epsdil'][-2:-1].sum()))  # Previous quarter, -5 for same quarter last year
        print(fmt.constructSentence("Earnings (same quarter prev year):", mrqData['epsdil'][-1:].sum(),
                                    mrqData['epsdil'][-5:-4].sum()))  # Previous quarter, -5 for same quarter last year
        print(fmt.constructSentence("TTM eps", mrqData['epsdil'][-4:].sum(), mrqData['epsdil'][-9:-5].sum()))

        print(fmt.constructSentence("Diluted share count", mrqData['shareswadil'][-1:].sum(),
                                    mrqData['shareswadil'][-5:-4].sum()))
        cash = mrqData['cashnequsd'][-1:].sum()
        print(fmt.constructSentence("Cash ", cash, mrqData['cashnequsd'][-2:-1].sum(), suffix=' (prev quarter)'))
        debt = mrqData['debtusd'][-1:].sum()
        print(fmt.constructSentence("Debt (prev quarter)", debt, mrqData['debtusd'][-2:-1].sum(), suffix=' (prev quarter)'))
        print(fmt.constructSentence("Cash flow for quarter", mrqData['fcf'][-1:].sum(), mrqData['fcf'][-2:].sum()))
        print(fmt.constructSentence("Cash flow for TTM", mrqData['fcf'][-4:].sum(), mrqData['fcf'][-9:-5].sum()))
        print("* Cash flow per share for TTM was $%s" % fmt.number_formatter(
            mrqData['fcf'][-4:].sum() / mrqData['shareswadil'][-1:].sum()))
        print(fmt.constructSentence("Gross margins", mrqData['grossmargin'][-1:].sum(), mrqData['grossmargin'][-2:-1].sum()))
        print(fmt.constructSentence("CapExp", abs(mrqData['capex'][-1:].sum()), abs(mrqData['capex'][-2:-1].sum())))
        # print("1YPEG %d %d", 1, 1)

        # totalQuarterlyData = mrqData
        startDate = moment.date(startDate)
        endDate = moment.date(endDate)

        priceData2 = priceData.groupby(['year', 'quarter'])['close'].agg(['mean', 'max', 'min', 'last']).reset_index()
        totalQuarterlyData = priceData2.merge(mrqData, on=['year', 'quarter'])
        totalQuarterlyData['fcf_ttm'] = totalQuarterlyData['fcf'].rolling(4).sum()
        totalQuarterlyData['eps_ttm'] = totalQuarterlyData['epsusd'].rolling(4).sum()
        totalQuarterlyData['rev_ttm'] = totalQuarterlyData['revenue'].rolling(4).sum()
        totalQuarterlyData['rpsdil'] = totalQuarterlyData['rev_ttm'] / totalQuarterlyData['shareswadil']
        totalQuarterlyData['rps_ttm'] = totalQuarterlyData['rev_ttm'] / totalQuarterlyData['shareswadil']
        totalQuarterlyData['marketCap_max'] = totalQuarterlyData['sharesbas'] * totalQuarterlyData['max']
        totalQuarterlyData['marketCap_min'] = totalQuarterlyData['sharesbas'] * totalQuarterlyData['min']
        totalQuarterlyData['marketCap_last'] = totalQuarterlyData['sharesbas'] * totalQuarterlyData['last']
        totalQuarterlyData['evMin'] = totalQuarterlyData['marketCap_min'] + totalQuarterlyData['debt'] - totalQuarterlyData['cashnequsd']
        totalQuarterlyData['evMax'] = totalQuarterlyData['marketCap_max'] + totalQuarterlyData['debt'] - totalQuarterlyData['cashnequsd']
        totalQuarterlyData['evLast'] = totalQuarterlyData['marketCap_last'] + totalQuarterlyData['debt'] - totalQuarterlyData['cashnequsd']

        def calc1YPEG(ttmEps, ttmEpsPrevYear, currentPrice):
            # ttmEps = 4.71
            # ttmEpsPrevYear = 1.82
            # currentPrice = 151.35
            ttmPe = currentPrice / ttmEps
            # if((P124-O124)/if(P124>0, if(O124<=0, 0.01, O124), abs(O124))>2, 2, (P124-O124)/if(P124>0, if(O124<=0, 0.01, O124), abs(O124)))
            epsGrowth = (ttmEps - ttmEpsPrevYear) / ttmEpsPrevYear
            oneYearPEG = ttmPe / (epsGrowth * 100)
            print(oneYearPEG)

        print("\n### Last reported quarter ranges min, max [last]\n")
        filteredDateData = totalQuarterlyData[(totalQuarterlyData['calendardate'] > startDate.date) & (totalQuarterlyData['calendardate'] < endDate.date)]
        self.reportRangeData(filteredDateData, mrqData)

        print("\n### Most recent quarter ranges min, max [last] (uses more recent price data with last reported results)\n")
        self.sortOutMostRecentQuarterPrice(totalQuarterlyData, priceData)

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
        change['deferredrev'] = change['deferredrev'].map(fmt.number_formatter)
        change['billings'] = change['billings'].map(fmt.number_formatter)
        change['deferredrev_qchange'] = change['deferredrev_qchange'].map(fmt.percent_formatter)
        change['deferredrev_yoy_qchange'] = change['deferredrev_yoy_qchange'].map(fmt.percent_formatter)
        print(tabulate.tabulate(change[['quarterString', 'deferredrev', 'deferredrev_qchange', 'deferredrev_yoy_qchange', 'billings']],
                                headers=['Quarter', 'Def.Revenue', '𝝳 (q-1)', '𝝳 (YoY)', 'Billings\n(Rev + 𝝳 def. rev)'],
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
            headers=['Quarter', 'R and D', 'rnd', 'Change (q-1)', 'Change (YoY)', 'Sales, General, Admin',
                     'Change (q-1)',
                     'Change (YoY)'], tablefmt='pipe', showindex=False))

        return self.calculator.periodChange(['revenue', 'deferredrev', 'netinc', 'eps', 'workingcapital', 'fcf'], mrqData)

    def reportRangeData(self, df, mrqData):
        fmt = self.formatter

        calendardate_ = df.at[df.index[0], 'calendardate']
        startDate = calendardate_ - pd.offsets.QuarterBegin() - pd.offsets.QuarterBegin()
        endDate = df.at[df.index[-1], 'calendardate']
        if (endDate > datetime.now()):
            endDate = datetime.now()
        startDateFmt = moment.Moment(startDate).format('MMM D, YYYY')
        endDateFmt = moment.Moment(endDate).format('MMM D, YYYY')

        maxPrice = df['max'].max()
        minPrice = df['min'].min()

        lastTtmEps = df['eps_ttm'][-1:].sum()
        lastRps = df['rps_ttm'][-1:].sum()
        lastShareCount = df['sharesbas'][-1:].sum()

        lastFreeCashFlow = df['fcf_ttm'][-1:].sum()
        maxMarketCap = df['marketCap_max'].max()
        minMarketCap = df['marketCap_min'].min()
        evMax = df['evMax'].max()
        evMin = df['evMin'].min()
        evLast = df['evLast'][-1:].sum()
        # Note: Last price is the last price for the data contained in filteredDateDate
        lastPrice = df[-1:]['last'].sum()
        lastMarketCap = lastPrice * lastShareCount
        ttmRevenue = mrqData['revenue'][-4:].sum()
        print(
            "* Trading range between %s - %s was %s to %s [%s]" % (startDateFmt, endDateFmt, minPrice, maxPrice, lastPrice))
        print("* Market cap between %s - %s was %s to %s [%s]" % (
            startDateFmt, endDateFmt, fmt.number_formatter(minMarketCap), fmt.number_formatter(maxMarketCap),
            fmt.number_formatter(lastMarketCap)))
        if lastTtmEps < 0:
            print("* PE range (%s - %s) not applicable (earnings < 0)" % (startDateFmt, endDateFmt))
        else:
            print("* PE range (%s - %s) was %s to %s [%s]" % (
                startDateFmt, endDateFmt, minPrice['close'] / lastTtmEps, maxPrice['close'] / lastTtmEps, lastPrice / lastTtmEps))
        print("* PS ratio range (%s - %s) was %s to %s [%s]" % (
            startDateFmt, endDateFmt, fmt.number_formatter((minPrice) / lastRps), fmt.number_formatter((maxPrice / lastRps)),
            fmt.number_formatter(lastPrice / lastRps)))
        print("* Free cash flow yield range (%s - %s) was %s to %s [%s]" % (
            startDateFmt, endDateFmt, fmt.number_formatter(lastFreeCashFlow * 100 / maxMarketCap),
            fmt.number_formatter(lastFreeCashFlow * 100 / minMarketCap),
            fmt.number_formatter(lastFreeCashFlow * 100 / lastMarketCap)))
        print("* EV/Sales between %s - %s was %s to %s [%s]" % (
            startDateFmt, endDateFmt, fmt.number_formatter(evMin / ttmRevenue), fmt.number_formatter(evMax / ttmRevenue),
            fmt.number_formatter(evLast / ttmRevenue)))

    def sortOutMostRecentQuarterPrice(self, mrqData, priceData):
        mostRecentData = mrqData[-1:]
        end_ = mostRecentData.at[mostRecentData.index[-1], 'calendardate'] + pd.offsets.QuarterEnd()
        mostRecentData.at[mostRecentData.index[-1], 'quarterString'] = pd.Period(end_, 'Q')
        mostRecentData.at[mostRecentData.index[-1], 'quarter'] = end_.quarter
        mostRecentData.at[mostRecentData.index[-1], 'year'] = end_.year
        mostRecentData.at[mostRecentData.index[-1], 'calendardate'] = end_
        priceData2 = priceData.groupby(['year', 'quarter'])['close'].agg(['mean', 'max', 'min', 'last']).reset_index()
        mostRecentData = priceData2.merge(mostRecentData, on=['year', 'quarter'], suffixes=('', '_y'))
        del mostRecentData['max_y']
        del mostRecentData['min_y']
        del mostRecentData['mean_y']
        del mostRecentData['last_y']
        mostRecentData.at[mostRecentData.index[-1], 'marketCap_max'] = mostRecentData['shareswadil'] * mostRecentData['max']
        mostRecentData.at[mostRecentData.index[-1], 'marketCap_min'] = mostRecentData['shareswadil'] * mostRecentData['min']
        mostRecentData.at[mostRecentData.index[-1], 'marketCap_last'] = mostRecentData['shareswadil'] * mostRecentData['last']
        mostRecentData.at[mostRecentData.index[-1], 'evMin'] = mostRecentData['marketCap_min'] + mostRecentData['debt'] - mostRecentData['cashnequsd']
        mostRecentData.at[mostRecentData.index[-1], 'evMax'] = mostRecentData['marketCap_max'] + mostRecentData['debt'] - mostRecentData['cashnequsd']
        mostRecentData.at[mostRecentData.index[-1], 'evLast'] = mostRecentData['marketCap_last'] + mostRecentData['debt'] - mostRecentData['cashnequsd']
        self.reportRangeData(mostRecentData, mrqData)
        return mostRecentData

def ntnxAdjustments(df):
    # This data is from morningstar/iex
    df.loc[(df.dimension == 'MRQ') & (df.calendardate == '2017-06-30'), 'revenue'] = 173424000
    return df


# priceData = loadPriceDataLive(ticker='NTNX')
priceData = DataLoader().loadPriceData(ticker='NTNX')
adjustments = {
    'NTNX': ntnxAdjustments
}
mrqData, mryData, arqData = DataLoader().loadData(ticker='NTNX', adjustments=adjustments)
# print(mrqData.to_string())
changeData = TMF1000Analyser().analyse(mrqData, mryData, priceData)
DCF(mrqData).calc()
df = pd.read_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_data.pkl')

# mrq, mry_, arq, ary = loadAllData()
# tickerData = mrq[(mrq['ticker'] == 'AAPL') | (mrq['ticker'] == 'AMZN')]
# mrq.to_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_data.pkl')
g = df.groupby(['ticker'])
df['ttm_revenue'] = g['revenue'].transform(lambda x: x.rolling(4).sum())
df['revenue_qchange'] = g['revenue'].pct_change(periods=1)
df['revenue_yoy_qchange'] = g['revenue'].pct_change(periods=4)

# print(df.groupby(['ticker']).agg(lambda x: x.iloc[-1]).to_string())
last = g.last()
sum_ = last[(last['ttm_revenue'] > changeData['revenue_ttm'][-1:].sum()) & (last['revenue_qchange'] > changeData['revenue_qchange'][-1:].sum()) & (
    last['revenue_yoy_qchange'] > changeData['revenue_yoy_qchange'][-1:].sum())]
print(sum_[['ttm_revenue', 'revenue_qchange', 'revenue_yoy_qchange']])



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
