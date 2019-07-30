# coding:utf-8
from src.dao.mysql_util import MysqldbHelper
from src.model.keyword import Keyword


class KeywordDao(object):

    @staticmethod
    def get_keywords():
        mysql = MysqldbHelper()
        sql = "select name, level from words ORDER  BY level desc"
        rtn = mysql.executeSql(sql)
        keywords = []
        for data in rtn:
            keyword = Keyword()
            keyword.name = data[0]
            keyword.level = data[1]
            keywords.append(keyword)
        return keywords

    """
        def get_keywords(level):
        mysql = MysqldbHelper()
        sql = "select name from words where level='" + str(level) + "'"
        rtn = mysql.executeSql(sql)
        keywords = []
        for data in rtn:
            keywords.append(data[0])
        return keywords
    """
