# coding:utf-8
from dao.db import session


class BcBenefitDao(object):

    @staticmethod
    def add(bc_benefit):
        session.add(bc_benefit)
