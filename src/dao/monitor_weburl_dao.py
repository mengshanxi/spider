# coding:utf-8
from src.dao.mysql_util import MysqldbHelper


class MonitorWeburlDao(object):

    @staticmethod
    def add(monitor_url):
        mysql = MysqldbHelper()
        sql = "insert into monitor_url(batch_num,website_name,title,url,outline,snapshot,is_normal,kinds,level)values('" + str(
            monitor_url.batch_num) + "','" + str(
            monitor_url.website_name) + "','" + str(
            monitor_url.title) + "','" + str(
            monitor_url.url) + "','" + str(
            monitor_url.outline) + "','" + str(
            monitor_url.snapshot) + "','" + str(
            monitor_url.is_normal) + "','" + str(
            monitor_url.kinds) + "','" + str(
            monitor_url.level) + "')"
        mysql.executeCommit(sql)
