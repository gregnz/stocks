import json

import pandas as pd
import requests

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

class DataLoader():
    def __init__(self):
        pass

    def loadPriceDataLive(self, ticker):
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

    def loadDataLive(self, ticker='FOSL'):
        r = requests.get('https://www.quandl.com/api/v3/datatables/SHARADAR/SF1.csv?ticker=%s&api_key=CqV_AndpG4zhPcAPCoTN' % ticker)
        file = '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_historical.csv' % ticker
        w = csv.writer(file)
        # w.writerow(r.)
        # spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        #     csv.dump(r.json(), file)
        df = pd.DataFrame.from_dict(r.json())
        df['date'] = pd.to_datetime(df['date'])
        df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
        df['quarterString'] = df['date'].map(lambda x: pd.Period(x, 'Q'))
        df['quarter'] = df['date'].map(lambda x: x.quarter)
        df['year'] = df['date'].map(lambda x: x.year)
        self.tickerData = df
        return df

    def loadData(self, ticker='FOSL', adjustments={}):
        """Load the data for a single letter label."""
        df = pd.read_csv(
            '/Users/gregday/Library/Mobile Documents/com~apple~CloudDocs/stock research/data/%s_historical.csv' % ticker,
            delimiter=',',
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
