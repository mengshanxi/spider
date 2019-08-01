# coding:utf-8
from dao.db import session


class MonitorWeburlDao(object):

    @staticmethod
    def add(monitor_url):
        session.add(monitor_url)
