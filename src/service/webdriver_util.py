# -*- coding:utf-8 -*-
from random import choice

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config.mylog import logger
from service.strategy_service import StrategyService


class WebDriver:

    @staticmethod
    def get_chrome():
        chrome_options = Options()
        # 禁止图片和css加载
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME,
                                  options=chrome_options)

        driver.set_page_load_timeout(30)
        driver.set_script_timeout(10)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_proxy_chrome():
        chrome_options = Options()
        strategy_service = StrategyService()
        strategy = strategy_service.get_strategy()
        if strategy.proxy_server is None or strategy.proxy_server == '':
            logger.info("proxy_server is none!")
            return None

        else:
            proxy_servers = strategy.proxy_server.split(",")
            chrome_options.add_argument("--proxy-server=" + choice(proxy_servers))
            # 禁止图片和css加载
            prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
            chrome_options.add_experimental_option("prefs", prefs)
            driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                      desired_capabilities=DesiredCapabilities.CHROME,
                                      options=chrome_options)

            driver.set_page_load_timeout(30)
            driver.set_script_timeout(10)
            driver.maximize_window()
            return driver

    @staticmethod
    def get_chrome_for_access():
        chrome_options = Options()
        # 禁止图片和css加载
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME,
                                  options=chrome_options)

        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.maximize_window()
        return driver
