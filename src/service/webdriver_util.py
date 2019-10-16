# -*- coding:utf-8 -*-
from random import choice

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config.mylog import logger
from dao.third_config_dao import ThirdConfigDao
from service.strategy_service import StrategyService


class WebDriver:
    # @staticmethod
    # def get_chrome():
    #     chrome_options = Options()
    #     # 禁止图片和css加载
    #     # prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    #     # chrome_options.add_experimental_option("prefs", prefs)
    #     dcap = dict(DesiredCapabilities.PHANTOMJS)
    #     dcap['phantomjs.page.settings.userAgent'] = (
    #         'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
    #     headers = {
    #         'cookie': "_uab_collina=152905475626038564211156; zg_did=%7B%22did%22%3A%20%2216402c3dd9f1a3-048c8f157b8bef-62101875-15f900-16402c3dda240e%22%7D; _umdata=65F7F3A2F63DF020E71AEDA6F30593EA2A3D12D925F079E1C3AD72E105725A3834473AB8A6F2708CCD43AD3E795C914CDE7897677D443EB4C388E3204FFBF1CF; saveFpTip=true; UM_distinctid=16c2cc5326d31c-0c9a87f30aaef5-3f385c06-15f900-16c2cc5326ee7; QCCSESSID=lajs6k2n011qdt4muhp6pvpvu6; acw_tc=8bd7c0a715688745163558521e01768ca3582d4469d3fedb6973ead086; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568874516,1568958347,1569310892; hasShow=1; CNZZDATA1254842228=2046742533-1539154952-https%253A%252F%252Fwww.baidu.com%252F%7C1569311470; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201569316566287%2C%22updated%22%3A%201569316567763%2C%22info%22%3A%201568874515460%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22211a877f4df3307566603a3b5918bf6e%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1569316569"}
    #     for key, value in headers.items():
    #         dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
    #     driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs",
    #                                  desired_capabilities=dcap)
    #     driver.set_page_load_timeout(30)
    #     driver.set_script_timeout(10)
    #     driver.maximize_window()
    #     return driver

    @staticmethod
    def get_chrome():
        chrome_options = Options()
        # 禁止图片和css加载
        # prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME,
                                  options=chrome_options)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_chrome_by_local():
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                                  desired_capabilities=DesiredCapabilities.CHROME,
                                  options=chrome_options)
        driver.set_page_load_timeout(20)
        driver.set_script_timeout(20)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_chrome_with_cookie():
        dcap = dict(DesiredCapabilities.PHANTOMJS.copy())
        third_config_dao = ThirdConfigDao()
        cookie = third_config_dao.get_by_name("qichacha")
        logger.info("cookie: %s", cookie)
        headers = {
            'cookie': cookie,
            'Host': 'www.qichacha.com',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        for key, value in headers.items():
            dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs",
                                     desired_capabilities=dcap,
                                     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'],
                                     service_log_path="/home/seluser/logs/phantomjs.log")

        driver.set_page_load_timeout(10)
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
    def get_chrome_for_urlgather():
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
    def get_chrome_for_access():
        chrome_options = Options()
        # 禁止图片和css加载
        # prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME,
                                  options=chrome_options)

        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        driver.maximize_window()
        return driver
