# coding:utf-8
from dao.db import session
from dao.mysql_util import MysqldbHelper
from model.models import InspectTask


class InspectTaskDao(object):
    @staticmethod
    def get_task(task_id):
        inspect_task = session.query(InspectTask).filter(InspectTask.id == task_id).one()
        return inspect_task

    @staticmethod
    def get_inspect_platform(task_id):
        mysql = MysqldbHelper()
        sql = "SELECT DISTINCT(platform_name) from inspect_task INNER JOIN inspect_detail " \
              "on inspect_task.id=inspect_detail.tmpl_id " \
              "and inspect_task.id='" + str(
            task_id) + "' " \
                       "and platform_name is not NULL and checked=1"
        rtn = mysql.executeSql(sql)
        platforms = []
        for data in rtn:
            platforms.append(data[0])
        return platforms

    @staticmethod
    def get_inspect_website(tmpl_id):
        mysql = MysqldbHelper()
        sql = "SELECT DISTINCT(website_name) from inspect_tmpl INNER JOIN inspect_detail " \
              "on inspect_tmpl.id=inspect_detail.tmpl_id " \
              "and inspect_tmpl.id='" + str(
            tmpl_id) + "' " \
                       "and website_name is not NULL and checked=1"
        rtn = mysql.executeSql(sql)
        websites = []
        for data in rtn:
            websites.append(data[0])
        return websites
