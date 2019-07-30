# coding:utf-8
from dao.mysql_util import MysqldbHelper


class ThirdConfigDao(object):

    @staticmethod
    def get(name):
        mysql = MysqldbHelper()
        sql = "select cookie from third_config where name='" + name + "'"
        rtn = mysql.executeSql(sql)
        if rtn.__len__() == 1:
            return rtn[0][0]
        else:
            return "nocookie"
