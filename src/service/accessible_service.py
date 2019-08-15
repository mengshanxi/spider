#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.mylog import logger
from service.webdriver_util import WebDriver


class AccessibleService:
    @staticmethod
    def get_access_res(url):
        driver = WebDriver.get_phantomjs()
        try:
            if str(url).startswith("http"):
                http_url = str(url)
            else:
                http_url = "http://" + str(url)
            driver.get(http_url)
            title = driver.title
            if title.__contains__('404'):
                return None
            else:
                return http_url
        except Exception as e:
            logger.error(e)
        finally:
            driver.quit()
