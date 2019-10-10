#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.mylog import logger
from service.webdriver_util import WebDriver


class AccessibleService:
    @staticmethod
    def get_access_res(url):
        driver = WebDriver.get_chrome_for_access()
        try:
            if str(url).startswith("http"):
                http_url = str(url)
            else:
                http_url = "http://" + str(url)
            logger.info("http_url: %s", http_url)
            driver.get(http_url)
            title = driver.title
            if title.__contains__('404') or driver.page_source.__contains__(
                    'ERR_NAME_NOT_RESOLVED') or driver.page_source.__contains__(
                'ERR_CONNECTION_REFUSED') or driver.page_source.__contains__(
                'ERR_CONNECTION_TIMED_OUT') or driver.page_source.__contains__(
                'ERR_NAME_NOT_RESOLVED') or driver.page_source.__contains__(
                'ERR_NAME_RESOLUTION_FAILED') or driver.page_source.__contains__('DNS_PROBE_FINISHED_NXDOMAIN'):
                return None, None
            else:
                return http_url, driver.current_url
        except Exception as e:
            logger.error(e)
            return None, None
        finally:
            driver.quit()

    @staticmethod
    def get_proxy_access_res(url):
        driver = WebDriver.get_proxy_chrome()
        if driver is None:
            return None, None
        else:
            try:
                if str(url).startswith("http"):
                    http_url = str(url)
                else:
                    http_url = "http://" + str(url)
                logger.info("http_url: %s", http_url)
                driver.get(http_url)
                title = driver.title
                if title.__contains__('404') or driver.page_source.__contains__(
                        'ERR_NAME_NOT_RESOLVED') or driver.page_source.__contains__(
                    'ERR_CONNECTION_REFUSED') or driver.page_source.__contains__('ERR_CONNECTION_TIMED_OUT'):
                    return None, None
                else:
                    return http_url, driver.current_url
            except Exception as e:
                logger.error(e)
                return None, None
            finally:
                driver.quit()
