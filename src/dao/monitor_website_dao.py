# coding:utf-8
from dao.db import session


class MonitorWebsiteDao(object):

    @staticmethod
    def add(monitor_website):
        session.add(monitor_website)
