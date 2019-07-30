# coding:utf-8
from src.dao.mysql_util import MysqldbHelper


class MonitorThirdDao(object):

    @staticmethod
    def add(monitor_third):
        mysql = MysqldbHelper()
        sql = "insert into monitor_third(batch_num,type,website_name,outline,snapshot,is_normal,level,url)values('" + str(
            monitor_third.batch_num) + "','" + str(
            monitor_third.type) + "','" + str(
            monitor_third.website_name) + "','" + str(
            monitor_third.outline) + "','" + str(
            monitor_third.snapshot) + "','" + str(
            monitor_third.is_normal) + "','" + str(
            monitor_third.level) + "','" + str(
            monitor_third.url) + "')"
        mysql.executeCommit(sql)
