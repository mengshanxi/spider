# coding:utf-8
import datetime

from dao.db import session


class MonitorBcDao(object):

    @staticmethod
    def add(monitor_bc):
        try:
            monitor_bc.create_time = datetime.datetime.now()
            session.add(monitor_bc)
            session.commit()
        except Exception  as e:
            print(e)
