#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from config.mylog import logger


class AccessibleService:
    @staticmethod
    def get_access_res(url):
        try:
            if str(url).startswith("http"):
                resp = urlopen(url, timeout=10)
                resp.getcode()
                return str(url)
            else:
                http_url = "http://" + str(url)
                resp = urlopen(http_url, timeout=10)
                resp.getcode()
                return http_url
        except Exception as e:
            logger.error(e)
        try:
            https_url = "https://" + str(url)
            resp = urlopen(https_url, timeout=10)
            resp.getcode()
            return https_url
        except Exception as e:
            logger.error(e)
            return None
