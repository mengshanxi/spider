# coding:utf-8
from src.model.weburl import Weburl
from src.dao.mysql_util import MysqldbHelper


class WeburlDao(object):

    @staticmethod
    def get_all():
        mysql = MysqldbHelper()
        sql = "select id,url from weburl"
        rtn = mysql.executeSql(sql)
        weburls = []
        for data in rtn:
            weburl = Weburl()
            weburl.id = data[0]
            weburl.url = data[1]
            weburls.append(data)
        return weburls

    @staticmethod
    def add(weburl):
        mysql = MysqldbHelper()
        records = mysql.executeSql("select count(id) as count from weburl where url='" + str(weburl.url).strip() + "'")
        if records[0][0] == 0:
            sql = "insert into weburl(url,title,website_name)values('" + str(weburl.url).strip() + "','" + str(
                weburl.title).strip() + "','" + str(weburl.website_name).strip() + "')"
        else:
            sql = "update  weburl set title='" + str(weburl.title).strip() + "', website_name='" + str(
                weburl.website_name).strip() + "' where url = '" + weburl.url + "'"
        mysql.executeCommit(sql)
