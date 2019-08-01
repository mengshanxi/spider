# coding:utf-8

from dao.db import session
from model.models import Keyword


class KeywordDao(object):

    @staticmethod
    def get_all():
        keywords = session.query(Keyword).all()
        return keywords
