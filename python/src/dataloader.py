import json
import csv

import pandas as pd
import requests
from io import StringIO

batchSize = 200

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')


class DataLoader():
    def __init__(self):
        pass

    def loadBatchCompanyDataLive(self, tickers):
        dfAll = pd.read_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_company_data.pkl')
        return dfAll

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
                print(df.to_string())

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

        print("All data as dataframe")
        print(dfAll.to_string())
        print("Writing pickle")
        dfAll =  dfAll.rename(columns={'symbol': 'ticker'})
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

    def loadPriceDataLive(self, ticker):
        # TODO: Modify this to append historic data. Note that this must be 5years, otherwise the subsequent code will fail with TTM calcs etc.
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

        if (len(df['quarterString'].unique()) < 8):
            print("******\n"
                  "Warning: Only %d quarters of price data. This probably won't be enough, are you sure you're getting at least 5 years of data? This may be a recent IPO."
                  "\n*******" % len(df['quarterString'].unique()))
        self.priceData = df
        return df

    def loadPriceData(self, ticker):
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
        self.priceData = df
        return df

    def loadDataLive(self, ticker='FOSL', adjustments=None):
        if adjustments is None:
            adjustments = {}
        r = requests.get('https://www.quandl.com/api/v3/datatables/SHARADAR/SF1.csv?ticker=%s&api_key=CqV_AndpG4zhPcAPCoTN' % ticker)
        data = StringIO(r.text)
        with open('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_historical-2.csv' % ticker, 'w') as outputFile:
            outputFile.write(r.text)
        return self.loadData(csvSource=data, ticker=ticker, adjustments=adjustments)

    def loadData(self, csvSource=None, ticker='FOSL', adjustments=None):
        """Load the data for a single letter label."""
        if adjustments is None:
            adjustments = {}
        if csvSource == None:
            csvSource = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_historical.csv' % ticker
            print("No source data supplied. Loading from file: %s" % csvSource)
        else:
            print("Reading from live csv data")

        df = pd.read_csv(
            csvSource,
            delimiter=',',
            parse_dates=['calendardate', 'lastupdated', 'reportperiod', 'datekey'], date_parser=dateparse)
        df['quarterString'] = df['calendardate'].map(lambda x: pd.Period(x, 'Q'))
        df['quarter'] = df['calendardate'].map(lambda x: x.quarter)
        df['year'] = df['calendardate'].map(lambda x: x.year)
        df.set_index(pd.DatetimeIndex(df['calendardate']), inplace=True)
        # df.dropna(subset=['revenue', 'equity'], inplace=True)

        adjustmentsForTicker = adjustments[ticker] if ticker in adjustments else None
        if (adjustmentsForTicker != None):
            df = adjustmentsForTicker(df)

        self.tickerData = df
        return (df[(df.dimension == 'MRQ')]), (df[(df.dimension == 'MRY')]), (df[(df.dimension == 'ARQ')])

    def loadAllData(self):
        df = pd.DataFrame()
        try:
            print("Reading pickle")
            df = pd.read_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_data.pkl')
        except:
            print("Reading CSV")
            df = pd.read_csv(
                '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/SHARADAR_SF1_b4f396bf12b7322892a876eb11353fb7-3.csv',
                delimiter=',',
                parse_dates=['calendardate', 'lastupdated', 'reportperiod', 'datekey'], date_parser=dateparse)
            print("Dataframe loaded")
            df['quarterString'] = df['calendardate'].map(lambda x: pd.Period(x, 'Q'))
            df['quarter'] = df['calendardate'].map(lambda x: x.quarter)
            df['year'] = df['calendardate'].map(lambda x: x.year)
            # df.set_index(pd.DatetimeIndex(df['calendardate']), inplace=True)
            print("Writing pickle")
            df.to_pickle('/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/all_data.pkl')
        return (df[(df.dimension == 'MRQ')]), (df[(df.dimension == 'MRY')]), (df[(df.dimension == 'ARQ')]), (df[(df.dimension == 'ARY')])
