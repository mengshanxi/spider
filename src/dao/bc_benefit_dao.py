# coding:utf-8
from dao.mysql_util import MysqldbHelper


class BcBenifitDao(object):

    @staticmethod
    def add(bc_benefit):
        mysql = MysqldbHelper()
        """
        delete_sql = "delete from bc_benefit where merchant_name='" + str(
        bc_benefit.merchant_name) + "' and fullname='" + str(
        bc_benefit.fullname) + "'"
        mysql.executeCommit(delete_sql)
        """

        sql = "insert into bc_benefit(batch_num,merchant_name,fullname,proportion,invest_train)values('" + str(
            bc_benefit.batch_num) + "','" + str(
            bc_benefit.merchant_name) + "','" + str(
            bc_benefit.fullname) + "','" + str(
            bc_benefit.proportion) + "','" + str(
            bc_benefit.invest_train) + "')"
        mysql.executeCommit(sql)
