# coding:utf-8
import datetime

from config.mylog import logger
from dao.db import session


class MonitorWeburlDao(object):

    @staticmethod
    def add(monitor_url):
        try:
            monitor_url.create_time = datetime.datetime.now()
            session.add(monitor_url)
        except Exception as e:
            logger.info(e)
