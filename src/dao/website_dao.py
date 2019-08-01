# coding:utf-8
from dao.db import session
from model.models import Website


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
