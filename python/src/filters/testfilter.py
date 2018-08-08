import logging
import traceback
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from filters.filter import Filter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestFilter(Filter):
    def __init__(self):
        super().__init__()
        self.analyse = True

    def calcExtraData(self, data):
        extraData = super().calcExtraData(data)
        # print(extraData.to_string())
        # extraData['opMargin_change'] = extraData['opmargin'].pct_change(4)
        # extraData['average revenue_ttm yoy quarterly change (6 years)'] = extraData['revenue_ttm_yoy_change_pct'].rolling(6).mean()
        # extraData['meanEpsChange_4quarters'] = extraData['eps_ttm_yoy_change_pct'].rolling(4).mean()
        extraData['grossmargin_avg'] = data['grossmargin'].rolling(4, min_periods=4).mean()

        # print(extraData[
        #           ['revenue', 'revenue_ttm', 'revenue_ttm_yoy_change_pct', 'revenue_yoy_qchange_pct', 'eps', 'eps_ttm', 'eps_ttm_yoy_change_pct', 'meanEpsChange_4quarters']].to_string())
        return extraData

    def setClauses(self):
        self.clauses = [
            (lambda x: self.clause('revenue_ttm_yoy_change_pct', x.tail(1), .4, '>')), # revenue increasing - customers like it
            # (lambda x: self.clause('eps_ttm', x.tail(1), 0, '>')), # Earnings are positive
            (lambda x: self.clause('fcf_ttm', x.tail(1), 0, '>')), # FCF are positive
            (lambda x: self.clause('deferredrev', x.tail(1), 0, '>')), # FCF are positive
            (lambda x: self.clause('eps_ttm_yoy_change_pct', x.tail(1), .2, '>')), # EPS is increasing (average over TTM is > .2)
            (lambda x: self.clause('grossmargin_avg', x.tail(1), 0.5, '>')), # High gross margin gives ability to actually make money
            # (lambda x: self.clause('average revenue_ttm yoy quarterly change (6 years)', x.tail(1), .1, '>')),
            # (lambda x: self.clause('is growth accelerating', x.tail(1), 0, '>')),
            # (lambda x: self.clause('revenue_yoy_qchange_growth_change', x.tail(1), 0, '>=')),
            # (lambda x: self.clause('revenue_ttm', x.tail(1), 1e7, '>')),
            # (lambda x: self.clause('rule_of_40', x.tail(1), 0.4, '>')),
            # (lambda x: self.clause('fcf_ttm', x.tail(1), 1e7, '>')),
            # (lambda x: self.clause('ev/sales', x.tail(1), 1, '<')),
            # (lambda x: self.clause('1YPEG_last', x.tail(1), 1, '<')),
            # (lambda x: self.clause('p/fcf_ttm', x.tail(1), 5, '<')),

            # (lambda x: x['ttm_revenue'] < 1e9),
            # (lambda x: x['marketcap'] < 15e9),
            # (lambda x: x['revenue_ttm_yoy_change_pct'].tail(1).iloc[0] > .30),
            # (lambda x: x['ev/sales'].tail(1).iloc[0] < 10),
            # (lambda x: x['eps'].tail(1).iloc[0] > 0),
            # (lambda x: x['rule_of_40'].tail(1).iloc[0] > 0.4),
            # (lambda x: x['fcf_ttm'].tail(1).iloc[0] > 1e7),
            # (lambda x: x['p/fcf_ttm'].tail(1).iloc[0] < 5),
            # (lambda x: x['grossmargin'].tail(1).iloc[0] > 0.3),
            # (lambda x: x['samequarter_ttmrevenue_pct_change'] > 0.1),
            # (lambda x: x['samequarter_ttmrevenue_pct_change'] >= 0.1)
        ]
