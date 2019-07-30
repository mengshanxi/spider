#!/usr/bin/env python
import urllib.request
import re
from src.model.traffic import Traffic
from src.config.mylog import logger

'''
help:
#http://outofmemory.cn/code-snippet/1812/usage-python-get-web-site-alexa-paiming
#http://alexa.chinaz.com/default.html
'''


class TrafficService:
    def get_traffic(self, domain_name):
        header = {
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        try:
            req = urllib.request.Request('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (domain_name),
                                         headers=header)
            res = urllib.request.urlopen(req, timeout=10).read()
            res = res.decode('UTF-8')
            reach_rank = re.findall("REACH[^\d]*(\d+)", res)

            ##访客排名
            if not reach_rank:
                reach_rank = "-"
            ##全球排名
            popularity_rank = re.findall("POPULARITY[^\d]*(\d+)", res)
            if not popularity_rank:
                popularity_rank = "-"
            traffic = Traffic(reach_rank, popularity_rank)
            # print(res)
            return traffic
        except Exception as  e:
            logger.info(e)
            traffic = Traffic([0, 0], 0)
            # print(res)
            return traffic
