# coding:utf-8
from dao.mysql_util import MysqldbHelper
from config.mylog import logger

class MonitorWebsiteDao(object):

    @staticmethod
    def add(monitor_website, batch_num):
        mysql = MysqldbHelper()
        sql = "insert into monitor_website(batch_num,merchant_name,website_name,domain_name,access,snapshot,is_normal,kinds,level,outline,pageview)values('" + str(
            batch_num) + "','" + str(
            monitor_website.merchant_name) + "','" + str(
            monitor_website.website_name) + "','" + str(
            monitor_website.domain_name) + "','" + str(
            monitor_website.access) + "','" + str(
            monitor_website.snapshot) + "','" + str(
            monitor_website.is_normal) + "','" + str(
            monitor_website.kinds) + "','" + str(
            monitor_website.level) + "','" + str(
            monitor_website.outline) + "','" + str(
            monitor_website.pageview) + "')"
        try:
            mysql.executeCommit(sql)
        except Exception as e:
            logger.error(e)
