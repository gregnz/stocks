import json
import csv
import logging
import threading
import traceback

import pandas as pd
import requests
from io import StringIO
import quandl

quandl.ApiConfig.api_key = 'CqV_AndpG4zhPcAPCoTN'
batchSize = 100

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
logger = logging.getLogger(__name__)


class DataLoader():
    def __init__(self):
        pass

    def loadBatchCompanyData(self):
        mrq, mry, arq, ary = self.loadAllFundamentalData()
        tickers = mrq['ticker'].unique()
        print(tickers.tolist())

        apiEndpoint = 'https://api.iextrading.com/1.0/stock/market/batch?symbols=%s&types=company'
        dfAll = pd.DataFrame(columns=['symbol'
            , 'companyName'
            , 'exchange'
            , 'industry'
            , 'website'
            , 'description'
            , 'CEO'
            , 'issueType'
            , 'sector'
            , 'tags'])

        def processCompanyResponse(r):
            data = r.json()
            # df = pd.DataFrame.from_dict(r.json(), orient='index')
            # dfAll.append(df)
            dfAll = pd.DataFrame(columns=['symbol'
                , 'companyName'
                , 'exchange'
                , 'industry'
                , 'website'
                , 'description'
                , 'CEO'
                , 'issueType'
                , 'sector'
                , 'tags'])
            for key in data:
                companyData = data[key]['company']
                companyData['tags'] = ",".join(companyData['tags'])
                df = pd.DataFrame.from_dict(companyData, orient='index')
                df = df.transpose()

                dfAll = dfAll.append(df, ignore_index=True)

            return dfAll

        for i in range(0, len(tickers), batchSize):
            endIndex = i + batchSize if i + batchSize < len(tickers) else len(tickers)
            print("Querying range %d-%d [%s]" % (i, endIndex, ",".join(tickers[i:endIndex])))
            tickerString = ",".join(tickers[i:endIndex])
            r = requests.get(apiEndpoint % tickerString)
            if (r.status_code != 200):
                print("Warning: Error in block. Not sure which one is wrong... trying them all")
                for ticker in tickers[i:endIndex]:
                    r = requests.get(apiEndpoint % ticker)
                    if (r.status_code != 200):
                        print("\t Error with ticker: %s, continuing..." % ticker)
                    dfAll = dfAll.append(processCompanyResponse(r))
                continue

            dfAll = dfAll.append(processCompanyResponse(r))

        print("Writing pickle")
        dfAll = dfAll.rename(columns={'symbol': 'ticker'})
        dfAll.to_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_company_data.pkl')
        return dfAll

    def loadCompanyDataLive(self, ticker):
        print("Ticker %s" % ticker)
        r = requests.get('https://api.iextrading.com/1.0/stock/%s/company' % ticker)
        print(r.text)
        print(r.status_code)
        if (r.status_code != 200): return None
        df = pd.DataFrame.from_dict(r.json())
        self.peers = df
        return df

    def loadPeerDataLive(self, ticker):
        r = requests.get('https://api.iextrading.com/1.0/stock/%s/peers' % ticker)
        df = pd.DataFrame.from_dict(r.json())
        self.peers = df
        print(self.peers.to_string())
        return df

    def loadPriceDataLive(self, tickers, existingDF=None):
        dfArray = []
        for i in range(0, len(tickers), batchSize):
            endIndex = i + batchSize if i + batchSize < len(tickers) else len(tickers)
            print("Querying range %d-%d [%s]" % (i, endIndex, ",".join(tickers[i:endIndex])))
            tickerString = ",".join(tickers[i:endIndex])

            if (existingDF is not None):
                rng = '5d'
            else:
                rng = '5y'

            r = requests.get('https://api.iextrading.com/1.0/stock/market/batch?symbols=%s&types=chart&range=%s' % (tickerString, rng))

            if (r.status_code != 200):
                logger.error("Failed to load price data for %s, continuing" % tickerString)
                return None
            json = r.json()
            print("Loaded price data for %d/%d tickers" % (len(json), endIndex - i))
            for ticker in tickers[i:endIndex]:
                try:
                    chart_ = json[ticker]['chart']
                except:
                    logger.error("No price data for %s" % ticker)
                    continue

                df = pd.DataFrame.from_dict(chart_)
                df['ticker'] = ticker

                dfArray.append(df)
                # if (len(df['quarterString'].unique()) < 8):
                #     print("******\n"
                #           "Warning: Only %d quarters of price data. This probably won't be enough, are you sure you're getting at least 5 years of data? This may be a recent IPO."
                #           "\n*******" % len(df['quarterString'].unique()))
        print("Total dataframes loaded:", len(dfArray))
        df = pd.concat(dfArray)
        df['date'] = pd.to_datetime(df['date'])
        df['quarterString'] = df['date'].map(lambda x: pd.Period(x, 'Q'))
        df['quarter'] = df['date'].map(lambda x: x.quarter)
        df['year'] = df['date'].map(lambda x: x.year)
        df['quarterEnd'] = df['date'].map(lambda x: x + pd.offsets.QuarterEnd(n=0))

        if (existingDF is not None):
            print("Combining first...")
            df = df.combine_first(existingDF)

        return df

    def loadPriceData(self, ticker):
        # curl -XGET 'https://api.iextrading.com/1.0/stock/ntnx/chart/5y' > NTNX_price.json
        file = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_price.json' % ticker
        try:
            with open(file) as jsonData:
                dict_train = json.load(jsonData)
            df = pd.DataFrame.from_dict(dict_train)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
            df['quarterString'] = df['date'].map(lambda x: pd.Period(x, 'Q'))
            df['quarter'] = df['date'].map(lambda x: x.quarter)
            df['year'] = df['date'].map(lambda x: x.year)
            self.priceData = df
            return df
        except Exception:
            return self.loadPriceDataLive(ticker)

    def loadDataFromCSV(self, csvSource=None):
        df = pd.read_csv(
            csvSource,
            delimiter=',',
            parse_dates=['calendardate', 'lastupdated', 'reportperiod', 'datekey'], date_parser=dateparse)
        df = df.sort_values(by=['ticker', 'dimension', 'calendardate'])
        df['quarterString'] = df['calendardate'].map(lambda x: pd.Period(x, 'Q'))
        df['quarter'] = df['calendardate'].map(lambda x: x.quarter)
        df['year'] = df['calendardate'].map(lambda x: x.year)
        df['quarterEnd'] = df['calendardate'].map(lambda x: x + pd.offsets.QuarterEnd(n=0))

        return df

    def loadFundamentalDataLive(self, tickers, existingDF=None):
        dfArray = []
        for i in range(0, len(tickers), batchSize):
            endIndex = i + batchSize if i + batchSize < len(tickers) else len(tickers)
            print("Querying range %d-%d [%s]" % (i, endIndex, ",".join(tickers[i:endIndex])))
            tickerString = ",".join(tickers[i:endIndex])

            r = requests.get('https://www.quandl.com/api/v3/datatables/SHARADAR/SF1.csv?ticker=%s&api_key=CqV_AndpG4zhPcAPCoTN' % (tickerString))

            if (r.status_code != 200):
                logger.error("Failed to load price data for %s, continuing" % tickerString)
                return None
            df = self.loadDataFromCSV(csvSource=(StringIO(r.text)))

            if (len(df) == 0): print("No fundamental data returned for tickers %s" % tickerString)

            for ticker, tickerFundamentalData in df.groupby('ticker'):
                if (len(tickerFundamentalData) == 0): print("No fundamental data returned for ticker %s" % ticker)

            print("Loaded fundamental data for %d/%d tickers" % (len(df['ticker'].unique()), endIndex - i))
            dfArray.append(df)
        print("Total dataframes loaded:", len(dfArray))
        df = pd.concat(dfArray)

        if (existingDF is not None):
            print("Combining first...")
            df = df.combine_first(existingDF)
        return df

    def loadDataLive(self, ticker='FOSL', adjustments=None):
        df = self.loadFundamentalDataLive(tickers=[ticker])
        print("Writing pickle")
        df.to_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_data.pkl' % ticker)
        return (df[(df.dimension == 'MRQ')]), (df[(df.dimension == 'MRY')]), (df[(df.dimension == 'ARQ')]), (df[(df.dimension == 'ARY')])

    def getAllTickers(self):
        tickerRequest = 'https://www.quandl.com/api/v3/datatables/SHARADAR/TICKERS?table=SF1&api_key=CqV_AndpG4zhPcAPCoTN&qopts.export=false&qopts.columns=ticker'
        df = quandl.get_table('SHARADAR/SF1', qopts={"columns": "ticker"}, calendardate={'gte': '2017-09-01', 'lte': '2018-01-10'}, paginate=True)
        tickers = df['ticker'].unique().tolist()
        print(tickers)
        return tickers

    def loadAllFundamentalData(self, forceLive=False):
        try:
            if (forceLive == True): raise Exception
            print("Reading fundamental pickle")

            df = pd.read_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_data.pkl')
        except:
            traceback.print_exc()
            tickers = self.getAllTickers()
            print("Querying fundamental data for %d tickers..." % len(tickers))
            df = self.loadFundamentalDataLive(tickers)
            print("Total fundamental data for %d tickers..." % len(df['ticker'].unique()))
            print("Writing pickle")
            df.to_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_data.pkl')

        return (df[(df.dimension == 'MRQ')]), (df[(df.dimension == 'MRY')]), (df[(df.dimension == 'ARQ')]), (df[(df.dimension == 'ARY')])

    def loadAllPriceData(self, readAll=False):
        print("Loading price data...")

        price_data_pkl = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_price_data.pkl'
        try:
            if (readAll == True): raise Exception
            print("Reading price pickle")
            df = pd.read_pickle(price_data_pkl)
            print("Total price data for %d tickers..." % len(df['ticker'].unique()))
            # df = self.loadPriceDataLive(tickers=df['ticker'].unique().tolist(), existingDF=df)

            return df
        except Exception as e:
            traceback.print_exc()
            mrq_, _, _, _ = self.loadAllFundamentalData()
            tickers = mrq_['ticker'].unique().tolist()
            print("Querying price data for %d tickers..." % len(tickers))
            df = self.loadPriceDataLive(tickers)
            print("Total price data for %d tickers..." % len(df['ticker'].unique()))

            print("Writing pickle")
            df.to_pickle(price_data_pkl)

        return df

    def createPriceSummary(self):
        print("Create price summary")
        price_data_summary_pkl = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/summary_price_data.pkl'
        df = self.loadAllPriceData(readAll=False)
        # df['quarterEnd'] = df['date'].map(lambda x: x + pd.offsets.QuarterEnd(n=0))
        priceSummary = df.groupby(['ticker', 'quarterEnd'])['high', 'low', 'close', 'date'].agg(['max', 'min', 'last'])
        priceSummary.reset_index(inplace=True)
        priceSummary.columns = priceSummary.columns.map('_'.join)

        priceSummary['quarterPrev'] = priceSummary['quarterEnd_'].shift(1)
        priceSummary.to_pickle(price_data_summary_pkl)
        return priceSummary

    def loadPriceSummary(self):
        print("Loading price summary")

        price_data_summary_pkl = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/summary_price_data.pkl'
        df = pd.read_pickle(price_data_summary_pkl)
        print("Loaded price summary data for %d tickers" % len(df['ticker_'].unique()))
        return df


if __name__ == '__main__':
    loader = DataLoader()
    # loader.loadBatchCompanyData()
    # loader.loadAllPriceData(readAll=True)
    # loader.createPriceSummary()
    mrq, _, _, _ = loader.loadAllFundamentalData()
    print(mrq['ticker'].to_string())
    # loader.loadFundamentalDataLive(tickers=['AAPL', 'MDB'])
