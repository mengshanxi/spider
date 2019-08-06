# coding:utf-8

from dao.db import session
from model.models import Strategy


class StrategyDao(object):

    @staticmethod
    def get_strategy():
        strategy = session.query(Strategy).one()
        return strategy
