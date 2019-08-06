# -*- coding:utf-8 -*-

from dao.strategy_dao import StrategyDao


class StrategyService:
    @staticmethod
    def get_strategy():
        strategy_dao = StrategyDao()
        return strategy_dao.get_strategy()
