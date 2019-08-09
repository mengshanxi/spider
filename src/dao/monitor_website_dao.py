# coding:utf-8
import datetime

from dao.db import session


class MonitorWebsiteDao(object):

    @staticmethod
    def add(monitor_website):
        monitor_website.create_time = datetime.datetime.now()
        session.add(monitor_website)
