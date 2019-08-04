# -*- coding:utf-8 -*-

from dao.keyword_dao import KeywordDao


class KeywordService:

    @staticmethod
    def get_keywords(level):
        keyword_dao = KeywordDao()
        return keyword_dao.get_all(level)
