# coding:utf-8
from src.dao.mysql_util import MysqldbHelper
from src.model.website import Website


class WebsiteDao(object):

    @staticmethod
    def getwebsite_by_name(website_name):
        mysql = MysqldbHelper()
        cond_dict = {}
        cond_dict['website_name'] = website_name
        website = Website()
        rtn = mysql.selectOne('website', cond_dict=cond_dict,
                              fields=["id", "merchant_name", "domain_name", "website_name"])
        website.id = rtn[0]
        website.merchant_name = rtn[1]
        website.domain_name = rtn[2]
        website.website_name = rtn[3]
        return website

    @staticmethod
    def getwebsite_by_merchant(merchant_name):
        mysql = MysqldbHelper()
        cond_dict = {}
        cond_dict['merchant_name'] = merchant_name
        website = Website()
        rtn = mysql.selectOne('website', cond_dict=cond_dict,
                              fields=["id", "merchant_name", "domain_name", "website_name"])
        website.id = rtn[0]
        website.merchant_name = rtn[1]
        website.domain_name = rtn[2]
        website.website_name = rtn[3]
        return website

    @staticmethod
    def add(monitor_website):
        mysql = MysqldbHelper()
        sql = "insert into monitor_website(website_id,access,is_normal,outline)values('" + str(
            monitor_website.website_id) + "','" + str(
            monitor_website.access) + "','" + str(monitor_website.outline) + "','" + str(
            monitor_website.is_normal) + "')"
        mysql.executeCommit(sql)
