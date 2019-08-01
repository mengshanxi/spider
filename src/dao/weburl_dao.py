# coding:utf-8
from dao.db import session
from dao.mysql_util import MysqldbHelper
from model.models import Weburl


class WeburlDao(object):

    @staticmethod
    def get_all():
        weburl = session.query(Weburl).all()
        return weburl

    @staticmethod
    def add(weburl):
        exist_weburl = session.query(Weburl).filter(Weburl.url == weburl.url).all()
        if len(exist_weburl):
            pass
        else:
            session.add(weburl)
