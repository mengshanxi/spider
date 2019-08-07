# coding:utf-8
from dao.db import session


class MonitorBcDao(object):

    @staticmethod
    def add(monitor_bc):
        try:
            session.add(monitor_bc)
            session.commit()
        except Exception  as e:
            print(e)
