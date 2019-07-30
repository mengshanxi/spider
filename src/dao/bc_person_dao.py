# coding:utf-8
from dao.mysql_util import MysqldbHelper


class BcPersonDao(object):

    @staticmethod
    def add(bc_person):
        mysql = MysqldbHelper()
        """
        delete_sql = "delete from bc_person where merchant_name='" + str(
            bc_person.merchant_name) + "' and fullname='" + str(
            bc_person.fullname) + "'"
        mysql.executeCommit(delete_sql)       
        """
        sql = "insert into bc_person(batch_num,merchant_name,fullname,job)values('" + str(
            bc_person.batch_num) + "','" + str(
            bc_person.merchant_name) + "','" + str(
            bc_person.fullname) + "','" + str(
            bc_person.job) + "')"
        mysql.executeCommit(sql)
