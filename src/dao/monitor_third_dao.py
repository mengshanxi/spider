# coding:utf-8
from dao.db import session


class MonitorThirdDao(object):

    @staticmethod
    def add(monitor_third):
        session.add(monitor_third)
