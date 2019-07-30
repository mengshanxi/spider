#!/usr/bin/python
# -*- coding: UTF-8 -*-
from dao.mysql_util import MysqldbHelper

aaa = "32,33";
aa = str.split(',')
mysql = MysqldbHelper()

sql = "select website_name from report where id in(" + str(aaa) + ")"
rtn = mysql.executeSql(str(sql))
website_names = []
for data in rtn:
    website_names.append(data[0])
print(website_names)

