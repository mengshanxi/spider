# coding:utf-8
from dao.db import session


class BcPersonDao(object):

    @staticmethod
    def add(bc_person):
        session.add(bc_person)
