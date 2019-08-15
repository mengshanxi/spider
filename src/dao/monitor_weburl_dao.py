# coding:utf-8
import datetime

from dao.db import session


class MonitorWeburlDao(object):

    @staticmethod
    def add(monitor_url):
        monitor_url.create_time = datetime.datetime.now()
        session.add(monitor_url)
        session.commit()
