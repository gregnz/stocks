import logging
import multiprocessing
import os
import threading
import traceback
import pickle

import matplotlib
import numpy as np
import pandas as pd
from multiprocessing import Process
from sklearn.metrics.pairwise import cosine_similarity

from dataloader import DataLoader
from filters.bestperformers import BestPerformers
from filters.highgrowth import HighGrowth
from filters.testfilter import TestFilter

matplotlib.use('TkAgg')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Screen:
    pd.set_option('display.max_colwidth', -1)

    def __init__(self):
        self.DATA_PKL = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data'
        self.mrq, _, _, _ = DataLoader().loadAllFundamentalData()
        self.priceSummary = DataLoader().loadPriceSummary()

    def readPickles(self):
        print("Reading pickle")
        fundamentalArray = []
        priceArray = []
        for file in os.listdir(self.DATA_PKL):
            if file.endswith("_all-data.pkl"):
                if file.startswith('DLTH'):
                    path = os.path.join(self.DATA_PKL, file)
                    pickle = pd.read_pickle(path)

                    fundamentalArray.append(pickle)
                    priceArray.append(pickle)

        print('%d pickles read...' % len(fundamentalArray))
        fundamentalDF = pd.concat(fundamentalArray)
        priceDF = pd.concat(fundamentalArray)

        return fundamentalDF, priceDF

    def loadBaseData(self):
        print('Loading base data...')
        mrq, mry, arq, ary = DataLoader().loadDataFromCSV(ticker='DLTH')
        print('Processing base data...')
        df = mrq

        def sortOutTicker(ticker_, tickerData):
            print('------------ %s ------------' % ticker_)
            print(tickerData.to_string())

            # Add in price data, and map the price data to the fundamental data in the previous quarter. For example, if the price data is in February, the ratios etc should
            # be calculated on the Q4 (Dec 31) fundamental data.
            priceData = DataLoader().loadPriceDataLive(ticker_)
            if (priceData is None):
                print("No price data")
                return
            priceData['quarterEnd'] = priceData['date'].map(lambda x: x + pd.offsets.QuarterEnd(n=0))
            priceSummary = priceData.groupby('quarterEnd')['high', 'low', 'close', 'date'].agg(['max', 'min', 'last'])
            priceSummary.reset_index(inplace=True)
            priceSummary.columns = priceSummary.columns.map('_'.join)

            try:
                priceSummary['quarterPrev'] = priceSummary['quarterEnd_'].shift(1)
                priceSummary = priceSummary[1:]
            except Exception as e:
                print('Error shifting...returning', e)
                return

            # Note here that the last line (possibly 2) will duplicate the last reported fundamental data, as the price data wins in the merge_asof. 
            # So quarter comparisons might be a bit screwed unless you ignore that.
            try:
                fundamentalAndPriceData = pd.merge_asof(tickerData, priceSummary, right_on='quarterPrev', left_on='calendardate')
            except Exception as e:
                print("Error merge_asof. This could be because the price summary (length: %d) or the tickerData (length: %d) is insufficient. Reasons"
                      " include a delisted company (eg: ARMO) or... something else. Returning.")
                return

            mostRecentCalendarDate = tickerData['calendardate'].max()
            self.writePickle(fundamentalAndPriceData, '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_all-data.pkl' % ticker_)

        adt_ = df  # [df['ticker'] > 'UFS']
        for i, g in adt_.groupby('ticker'):
            sortOutTicker(i, g)

    def writePickle(self, df, filename):
        print("Writing pickle")
        df.to_pickle(filename)

    def similarityMatrix(self):
        # Workaround from: https://github.com/pandas-dev/pandas/issues/21200
        df = self.df[0:100].copy()
        df['revenue_ttm'] = [0] * len(df)
        g = df.groupby('ticker')
        for i, ticker in g:
            print(i)
            ticker['ttm_revenue'] = ticker['revenue']
            ticker['ttm_eps'] = ticker['eps'].rolling(4).sum()
            df.update(ticker)
            break

        print(df['revenue_ttm'])
        exit(1)
        # df['ttm_revenue'] = g['revenue'].apply(lambda x: x.rolling(4).sum())
        print('Adding extra data...TTM EPS')
        df['ttm_fcf'] = g['fcf'].apply(lambda x: pd.np.random.rand())

        df['prevquarter_revenue_pct_change'] = g['revenue'].apply(lambda x: x.pct_change(periods=1))
        df['samequarter_revenue_pct_change'] = g['revenue'].apply(lambda x: x.pct_change(periods=4))
        df['revenue_ttm_yoy_change'] = g['ttm_revenue'].apply(lambda x: x.diff(periods=1))
        df['revenue_ttm_same_change_pct'] = g['ttm_revenue'].apply(lambda x: x.pct_change(periods=1))
        df['revenue_ttm_yoy_change_pct'] = g['ttm_revenue'].apply(lambda x: x.pct_change(periods=4))

        # df['prevquarter_eps_pct_change'] = g['eps'].apply(lambda x: x.pct_change(periods=1))
        # df['samequarter_eps_pct_change'] = g['eps'].apply(lambda x: x.pct_change(periods=4))
        # df['prevquarter_ttmeps_pct_change'] = g['ttm_eps'].apply(lambda x: x.pct_change(periods=1))
        # df['samequarter_ttmeps_pct_change'] = g['ttm_eps'].apply(lambda x: x.pct_change(periods=4))

        # df['prevquarter_fcf_pct_change'] = g['fcf'].apply(lambda x: x.pct_change(periods=1))
        # df['samequarter_fcf_pct_change'] = g['fcf'].apply(lambda x: x.pct_change(periods=4))
        # df['prevquarter_ttmfcf_pct_change'] = g['ttm_fcf'].apply(lambda x: x.pct_change(periods=1))
        # df['samequarter_ttmfcf_pct_change'] = g['ttm_fcf'].apply(lambda x: x.pct_change(periods=4))

        print('Starting similarity...')
        similarity = self.df[['revenue_ttm', 'grossmargin', 'marketCap_last', 'revenue_ttm_yoy_change_pct']]
        print(cosine_similarity(similarity))

    def filter(self):
        passed = []
        passedDataframes = []

        # reportOnTickers = ['MIDD', 'SWKS']
        reportOnTickers = ['ZYME', 'ZYNE']
        # reportOnTickers = ['AYX', 'TWLO', 'NTNX', 'SQ', 'MDB', 'OKTA', 'PVTL', 'ZS', 'NEWR', 'PSTG']
        # reportOnTickers = ['ADBE', 'DLTH,''TREX', 'SKX', 'AAPL', 'ABMD', 'ADBE', 'ALGN', 'AMZN', 'ANET', 'APPN', 'ATVI', 'BB', 'BIDU', 'CELG', 'CMG', 'CTRP', 'DBX', 'DDD', 'DIS',
        #                    'EA', 'FB', 'FOSL', 'GME', 'GOOG', 'GOOGL', 'HUBS', 'ILMN', 'INST', 'INTC', 'INTU', 'IRBT', 'LFUS', 'LGIH', 'MA', 'MDB', 'MELI', 'MIDD', 'MSFT',
        #                    'MZOR', 'NCR', 'NEWR', 'NFLX', 'NKTR', 'NTNX', 'NVDA', 'NYT', 'OKTA', 'OLED', 'PAYC', 'PSTG', 'PVTL', 'PYPL', 'SBUX', 'SFIX', 'SHOP', 'SKX', 'SQ',
        #                    'SWIR', 'SWKS', 'TENB', 'TLND', 'TPR', 'TREX', 'TRIP', 'TSLA', 'TTD', 'TWTR', 'UBNT', 'ULTA', 'ULTA', 'ULTI', 'VEEV', 'VIX', 'WIX', 'Z',
        #                    ]

        print("Screening %d tickers" % len(self.mrq['ticker'].unique()))
        print("\t %d ticker price data" % len(self.priceSummary['ticker_'].unique()))

        p = multiprocessing.Pool(4)
        data = []
        priceSummaryGroups = self.priceSummary.groupby('ticker_')
        restrictToReportOnTickers = False

        try:
            with open('blacklist.pkl', 'rb') as f:
                blacklist = pickle.load(f)
        except FileNotFoundError as e:
            blacklist = []

        print("%d tickers blacklisted" % len(blacklist))

        for ticker, tickerFundamentalData in self.mrq.groupby('ticker'):
            if (ticker in blacklist): continue
            if (restrictToReportOnTickers == False or ticker in reportOnTickers):
                try:
                    priceData = priceSummaryGroups.get_group(ticker)
                    data.append((ticker, tickerFundamentalData, priceData, (ticker in reportOnTickers)))
                except Exception as e:
                    logger.error('Error processing ticker (%s), possibly missing price data. Adding to blacklist...' % ticker)
                    logger.error(e)
                    blacklist.append(ticker)

        with open('blacklist.pkl', 'wb') as f:
            pickle.dump(blacklist, f)

        print("Data collated. Allocating to workers...")

        results = p.starmap(mp_worker, data)
        for ticker, passed, clauseResults, df in results:
            print(ticker, end='', flush=False)
            if clauseResults is not None:
                for cr in clauseResults:
                    print("\t%s (%s) \t\t %s" % (cr['name'], cr['string'], cr['passed']))

            if (passed == True):
                passedDataframes.append(df)

        if (len(passedDataframes) == 0):
            print("No companies passed filtering. Check the filter and try again")
            return
        filtered = pd.concat(passedDataframes)
        # print(filtered.to_string())
        dfCompany = pd.read_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_company_data.pkl')
        print(dfCompany['ticker'].unique().tolist())
        filtered = filtered.merge(dfCompany, how='inner', on=['ticker'])
        print(filtered['ticker'].unique())
        print("Removing tickers based on industry...")
        filtered = filtered[filtered['industry'] != 'Banks']
        filtered = filtered[filtered['industry'] != 'REITs']
        filtered = filtered[filtered['industry'] != 'Oil & Gas - Midstream']
        filtered = filtered[filtered['industry'] != 'Oil & Gas - E&P']
        filtered = filtered[filtered['industry'] != 'Oil & Gas - E&P']
        filtered = filtered[filtered['industry'] != 'Oil & Gas - Integrated']
        filtered = filtered[filtered['industry'] != 'Insurance - Property & Casualty']
        filtered = filtered[filtered['industry'] != 'Insurance']
        filtered = filtered[filtered['industry'] != 'Biotechnology']

        # filtered['company'] = filtered['ticker'].apply(DataLoader().loadCompanyDataLive)


        summary = filtered.groupby('ticker').tail(1)
        # print(summary.to_string())
        print(summary[
                  ['ticker', 'calendardate', 'revenue_yoy_qchange_growth_change', 'grossmargin', 'p/fcf_ttm',
                   'revenue_ttm', 'revenue_ttm_yoy_change_pct', 'revenue_yoy_qchange_growth_change',
                   'industry', 'eps_x', 'deferredrev',
                   'description',
                   'ev/sales']].to_string())


def mp_worker(i, g, priceData, analyse):
    filter = TestFilter()
    tickerPass, tickerData, clauseResults = filter.filter(i, g, priceData, analyse=analyse)
    # print('%s %s...' % ('' if analyse == False else i,'' if analyse == False else tickerPass))

    if (tickerPass == False):
        return (i, False, clauseResults, None)
    if (tickerPass == True):
        return i, True, clauseResults, tickerData


# dfCompany = DataLoader().loadBatchCompanyDataLive(tickers=[])
# print(dfCompany[dfCompany['ticker']=='AMP'].to_string())
# exit(1)
#

# t = threading.Thread(target=DataLoader().loadAllPriceData, args=([True]))
# t2 = threading.Thread(target=DataLoader().loadAllPriceData, args=([False]))
# if not t.isAlive():
#     t.start()
# t2.start()

if (__name__ == '__main__'):
    screen = Screen()
    screen.filter()
# screen.similarityMatrix()
# df = pd.DataFrame({'col1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16], 'col2': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]})
# print(df.to_string())
# df2 = screen.periodChange(['col1', 'col2'], df)
# print(df2.to_string())
# print(screen.last[screen.last.index == 'CLCT'].apply(screen.filterFn, args=(True,), axis=1))
#
