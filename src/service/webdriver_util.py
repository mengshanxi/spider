# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from dao.third_config_dao import ThirdConfigDao


class WebDriver:

    @staticmethod
    def get_phantomjs():
        browser = os.environ['browser']
        port = os.environ['port']
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
        # driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap,
        #                              service_args=['--ignore-ssl-errors=true'])
        driver = webdriver.Remote(command_executor='http://' + browser + ':' + port,
                                  desired_capabilities=dcap)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_phantomjs_with_cookie():
        browser = os.environ['browser']
        port = os.environ['port']
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        third_config_dao = ThirdConfigDao()
        cookie = third_config_dao.get_by_name("qichacha")
        headers = {
            'cookie': cookie}
        for key, value in headers.items():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        # driver = webdriver.PhantomJS(executable_path=phantomjs_path,
        #                              desired_capabilities=desired_capabilities,
        #                              service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        driver = webdriver.Remote(command_executor='http://' + browser + ':' + port,
                                  desired_capabilities=desired_capabilities)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_chrome():
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # driver = webdriver.Chrome(chrome_options=chrome_options,
        #                           executable_path=chromedriver_path)
        # driver.set_page_load_timeout(10)
        # driver.set_script_timeout(10)
        # driver.maximize_window()
        driver = webdriver.Remote(
            command_executor='http://phantomjs:8910',
            desired_capabilities=DesiredCapabilities.FIREFOX)
        return driver
