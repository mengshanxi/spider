# coding:utf-8
import datetime

from dao.db import session
from dao.website_dao import WebsiteDao


class MonitorThirdDao(object):

    @staticmethod
    def add(monitor_third):
        website_dao = WebsiteDao()
        website = website_dao.get_by_merchant(monitor_third.merchant_name)
        monitor_third.create_time = datetime.datetime.now()
        monitor_third.merchant_name = website.merchant_name
        session.add(monitor_third)
