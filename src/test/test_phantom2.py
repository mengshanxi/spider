# coding:utf-8

import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config.config_load import phantomjs_path
from config.mylog import logger


def execute():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
    driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true'])
    time.sleep(5)
    try:
        driver.get("http://omniaccou1nt.com/home/info.html")
    except Exception as e:
        logger.error(e)
    driver.save_screenshot('D:/11.png')
    time.sleep(5)
    source = driver.page_source
    print(source)
    driver.close()


if __name__ == '__main__':
    execute()
