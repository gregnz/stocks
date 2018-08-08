import logging
import traceback
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Filter(ABC):
    def __init__(self):
        super().__init__()
        self.analyse = False
        self.setClauses()

    @abstractmethod
    def setClauses(self):
        pass

    def periodChange(self, columns, source):
        df = pd.DataFrame()
        for column in columns:
            df[column] = source[column]
            df[column + '_ttm'] = source[column].rolling(4).sum()
            df[column + '_ttm_yoy_change'] = df[column + '_ttm'].diff(periods=4)
            df[column + '_ttm_yoy_change_pct'] = df[column + '_ttm'].pct_change(periods=4)
            df[column + '_qchange'] = source[column].diff()
            df[column + '_qchange_pct'] = source[column].pct_change(periods=1)
            df[column + '_yoy_qchange'] = source[column].diff(periods=4)
            df[column + '_yoy_qchange_pct'] = source[column].pct_change(periods=4)
        return df

    def calcExtraData(self, data):
        logger.debug("Calculating extra data...")
        extraData = self.periodChange(['revenue', 'ebitda', 'eps', 'opinc', 'fcf'], data)

        extraData['revenue_yoy_qchange_growth_change'] = extraData['revenue_yoy_qchange_pct'].diff()
        # print(extraData[['revenue','revenue_ttm','revenue_ttm_yoy_change_pct','revenue_yoy_qchange_pct','revenue_yoy_qchange_growth_change']].to_string())
        extraData['ev/sales'] = data['ev'] / data['revenue']
        extraData['eps_ttm_same'] = extraData['eps_ttm'].shift(4)

        extraData['fcf_ps'] = extraData['fcf_ttm'] / data['shareswadil']
        extraData['fcf_margin_ttm'] = extraData['fcf_ttm'] / extraData['revenue_ttm']
        extraData['opMargin_ttm'] = (extraData['opinc_ttm'] / extraData['revenue_ttm'])
        extraData['ebitdaMargin_ttm'] = (extraData['ebitda_ttm'] / extraData['revenue_ttm'])
        extraData['p/fcf_ttm'] = data['close_last'] / extraData['fcf_ps']
        extraData['calendar_date2'] = data['calendardate']
        extraData['marketCap_max'] = data['sharesbas'] * data['high_max']
        extraData['marketCap_min'] = data['sharesbas'] * data['low_min']
        extraData['marketCap_last'] = data['sharesbas'] * data['close_last']
        extraData['ev_min'] = extraData['marketCap_min'] + data['debt'] - data['cashnequsd']
        extraData['ev_max'] = extraData['marketCap_max'] + data['debt'] - data['cashnequsd']
        extraData['ev_last'] = extraData['marketCap_last'] + data['debt'] - data['cashnequsd']
        extraData['ttmPE_min'] = data['low_min'] / extraData['eps_ttm']
        extraData['ttmPE_max'] = data['high_max'] / extraData['eps_ttm']
        extraData['ttmPE_last'] = data['close_last'] / extraData['eps_ttm']

        # exit()
        # This line adds NaN where previous ttm_eps is negative
        extraData['eps_ttm_growth'] = pd.np.where(extraData['eps_ttm_same'] > 0, extraData['eps_ttm'].pct_change(periods=4), np.NAN)

        # The 0.0000001 is a hack to get around DivisionByZero errors
        extraData['1YPEG_min'] = pd.np.where(extraData['eps_ttm_growth'] > 0,
                                             extraData['ttmPE_min'] / (extraData['eps_ttm_growth'] + 0.0000001 * 100), np.NAN)
        extraData['1YPEG_max'] = pd.np.where(extraData['eps_ttm_growth'] > 0,
                                             extraData['ttmPE_max'] / (extraData['eps_ttm_growth'] + 0.0000001 * 100), np.NAN)
        extraData['1YPEG_last'] = pd.np.where(extraData['eps_ttm_growth'] > 0,
                                              extraData['ttmPE_last'] / (extraData['eps_ttm_growth'] + 0.0000001 * 100), np.NAN)

        extraData['rule_of_40'] = extraData['revenue_ttm_yoy_change_pct'] + extraData['opMargin_ttm']
        # Bessemer “Efficiency Score
        extraData['bessemer'] = extraData['ebitda_ttm_yoy_change_pct'] + extraData['fcf_margin_ttm']
        # print(extraData[['calendar_date2', 'revenue_ttm', 'opinc_ttm', 'ebitda_ttm','ebitdaMargin_ttm','ebitda_ttm_yoy_change_pct', 'opMargin_ttm', 'revenue_ttm_yoy_change_pct', 'rule_of_40', 'bessemer']].to_string())
        return extraData

    def clause(self, name, values, target, comparison):
        if isinstance(values, np.float64):
            value = values
        elif isinstance(values[name], np.float64):
            value = values[name]
        else:
            value = values[name].iloc[0]
        target_ = '%f %s %.2f' % (value, comparison, target)

        if (np.isnan(value)):
            if (self.analyse == True): logger.debug("\tValue NAN: %s %s" % (name, target_))
            return False, name, target_

        # Theoretically, this logic is incorrect, but indicates a zero somewhere in the mix.
        if (np.isinf(value)):
            if (self.analyse == True): logger.debug("\tValue infinite: %s %s" % (name, target_))
            return False, name, target_
        expression = eval(target_)
        return expression, name, target_

    def filter(self, ticker, data, priceData, analyse=False):
        self.analyse = analyse
        if (len(data) == 0):
            logger.debug("Empty dataframe, returning false")
            return False, None, None

        try:
            data = pd.merge_asof(data, priceData[1:], right_on='quarterPrev', left_on='calendardate')
        except Exception as e:
            logger.error("Error in merging ticker %s. Returning" % ticker)
            # traceback.print_exc()
            return False, None, None

        extraData = self.calcExtraData(data)

        df = pd.merge(data, extraData, how='inner', left_index=True, right_index=True)

        isValid = True
        clauseResults = [False] * len(self.clauses)
        for i, clause in enumerate(self.clauses):
            passed, name, target = clause(df)
            if (passed == False):
                isValid = False
            clauseResults[i] = {'passed': passed, 'name': name, 'string': target}
        return isValid, df, clauseResults



