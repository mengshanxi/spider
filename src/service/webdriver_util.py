# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config.config_load import chromedriver_path
from config.config_load import phantomjs_path
from dao.third_config_dao import ThirdConfigDao


class WebDriver:
    @staticmethod
    def get_phantomJS():
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
        driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap,
                                     service_args=['--ignore-ssl-errors=true'])
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_phantomJS_withcookie():
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        third_config_dao = ThirdConfigDao()
        cookie = third_config_dao.get("qichacha")
        headers = {
            'cookie': cookie}
        for key, value in headers.items():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(executable_path=phantomjs_path,
                                     desired_capabilities=desired_capabilities,
                                     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_chrome():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=chromedriver_path)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        return driver
