# coding:utf-8
from src.dao.mysql_util import MysqldbHelper


class MonitorBcDao(object):

    @staticmethod
    def add(monitor_bc):
        mysql = MysqldbHelper()
        sql = "insert into monitor_bc(batch_num,merchant_name,outline,snapshot,is_normal,kinds,level)values('" + str(
            monitor_bc.batch_num) + "','" + str(
            monitor_bc.merchant_name) + "','" + str(
            monitor_bc.outline) + "','" + str(
            monitor_bc.snapshot) + "','" + str(
            monitor_bc.is_normal) + "','" + str(
            monitor_bc.kinds) + "','" + str(
            monitor_bc.level) + "')"
        mysql.executeCommit(sql)
