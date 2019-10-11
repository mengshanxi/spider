# coding:utf-8
import datetime

from dao.db import session
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
            weburl.create_time = datetime.datetime.now()
            weburl.last_update = datetime.datetime.now()
            session.add(weburl)
            session.commit()
