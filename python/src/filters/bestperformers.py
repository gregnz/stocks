import logging
import traceback
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
from filters.filter import Filter


class BestPerformers(Filter):
    def __init__(self):
        super().__init__()
        self.analyse = True

    def calcExtraData(self, data):
        cagrPeriod = 2  # years

        extraData = super().calcExtraData(data)
        extraData['cagr_close'] = (data['close_last'] / data['close_last'].fillna(method='bfill').shift(cagrPeriod * 4)) ** (1 / cagrPeriod) - 1
        return extraData

    def setClauses(self):
        self.clauses = [
            (lambda x: self.clause('cagr_close', x.tail(1), 0.2, '>=')),
            # (lambda x: self.clause('revenue_yoy_qchange_growth_change', x.tail(6).mean(), 0, '>=')),
        ]
