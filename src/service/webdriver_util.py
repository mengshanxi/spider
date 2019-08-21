# -*- coding:utf-8 -*-

import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebDriver:

    @staticmethod
    def get_chrome():
        browser = os.environ['browser']
        port = os.environ['port']
        driver = webdriver.Remote(command_executor='http://' + browser + ':' + port + '/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(30)
        driver.set_script_timeout(10)
        driver.maximize_window()
        return driver
