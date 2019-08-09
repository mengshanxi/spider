# coding:utf-8
import datetime

from dao.db import session


class MonitorThirdDao(object):

    @staticmethod
    def add(monitor_third):
        monitor_third.create_time = datetime.datetime.now()
        session.add(monitor_third)
