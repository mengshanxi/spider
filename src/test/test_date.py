#! /usr/bin/python
# encoding:utf-8

import time
import os

day = time.strftime('%Y-%m-%d', time.localtime())
print(day)
millis = int(round(time.time() * 1000))
print(millis)
url = "http://asfas/dasdf/dd/1/dsf/da/a.jsp"
url_processed = url.replace("http://", "").replace("/", "_").replace(".", "_")
print(url_processed)
open("D:/" + url_processed + ".txt", 'w')
