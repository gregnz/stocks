import logging
import traceback
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from filters.filter import Filter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)




class HighGrowth(Filter):
    def __init__(self):
        super().__init__()
        self.analyse = True

    def setClauses(self):
        self.clauses = [
            (lambda x: self.clause('revenue_ttm_yoy_change_pct', x.tail(1), .3, '>')),
            (lambda x: self.clause('revenue_yoy_qchange_growth_change', x.tail(6).mean(), 0, '>=')),
            (lambda x: self.clause('revenue_ttm', x.tail(1), 1e7, '>')),
            (lambda x: self.clause('rule_of_40', x.tail(1), 0.4, '>')),
            (lambda x: self.clause('fcf_ttm', x.tail(1), 1e7, '>')),
            (lambda x: self.clause('p/fcf_ttm', x.tail(1), 5, '<')),
            (lambda x: self.clause('grossmargin', x.tail(1), 0.3, '>')),

            # (lambda x: x['ttm_revenue'] < 1e9),
            # (lambda x: x['marketcap'] < 15e9),
            # (lambda x: x['revenue_ttm_yoy_change_pct'].tail(1).iloc[0] > .30),
            (lambda x: x['ev/sales'].tail(1).iloc[0] < 10),
            # (lambda x: x['eps'].tail(1).iloc[0] > 0),
            # (lambda x: x['rule_of_40'].tail(1).iloc[0] > 0.4),
            # (lambda x: x['fcf_ttm'].tail(1).iloc[0] > 1e7),
            # (lambda x: x['p/fcf_ttm'].tail(1).iloc[0] < 5),
            # (lambda x: x['grossmargin'].tail(1).iloc[0] > 0.3),
            # (lambda x: x['samequarter_ttmrevenue_pct_change'] > 0.1),
            # (lambda x: x['samequarter_ttmrevenue_pct_change'] >= 0.1)
        ]


