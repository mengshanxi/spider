# coding:utf-8
import time

from dao.db import session
from model.models import Website
from service.strategy_service import StrategyService


class WebsiteDao(object):
    @staticmethod
    def get_all():
        websites = session.query(Website).all()
        return websites

    @staticmethod
    def get_by_name(website_name):
        website = session.query(Website).filter(Website.website_name == website_name).one()
        return website

    @staticmethod
    def get_by_merchant(merchant_name):
        website = session.query(Website).filter(Website.website_name == merchant_name).one()
        return website

    @staticmethod
    def get_overtime():
        filterd = []
        websites = session.query(Website).all()
        strategy_service = StrategyService()
        strategy = strategy_service.get_strategy()
        now = time.time()
        overtime = now - strategy.cache_days * 24 * 60 * 1000
        for website in websites:
            last_gather_time = website.last_gather_time
            if last_gather_time is None:
                continue
            elif time.mktime(time.strptime(str(last_gather_time), "%Y-%m-%d %H:%M:%S")) > overtime:
                continue
            else:
                filterd.append(website)
        return filterd
