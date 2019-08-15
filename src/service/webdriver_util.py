# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from dao.third_config_dao import ThirdConfigDao


class WebDriver:

    @staticmethod
    def get_phantomjs():
        # browser = os.environ['browser']
        # port = os.environ['port']
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap['phantomjs.page.settings.userAgent'] = (
        #     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
        # driver = webdriver.Remote(command_executor='http://' + browser + ':' + port,
        #                           desired_capabilities=dcap)
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        headers = {
            'cookie': '_uab_collina=152905475626038564211156; zg_did=%7B%22did%22%3A%20%2216402c3dd9f1a3-048c8f157b8bef-62101875-15f900-16402c3dda240e%22%7D; _umdata=65F7F3A2F63DF020E71AEDA6F30593EA2A3D12D925F079E1C3AD72E105725A3834473AB8A6F2708CCD43AD3E795C914CDE7897677D443EB4C388E3204FFBF1CF; saveFpTip=true; UM_distinctid=16c2cc5326d31c-0c9a87f30aaef5-3f385c06-15f900-16c2cc5326ee7; acw_tc=3cdfd94715641192177182843e4c640ca42a017726eab6816193d1b6d1; QCCSESSID=bov0tfoco6terisv66up1hq5f3; CNZZDATA1254842228=2046742533-1539154952-https%253A%252F%252Fwww.baidu.com%252F%7C1565860922; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1564649135,1565146916,1565148967,1565863713; hasShow=1; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1565863730; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201565863712914%2C%22updated%22%3A%201565863737242%2C%22info%22%3A%201565863712919%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%22211a877f4df3307566603a3b5918bf6e%22%7D'}
        for key, value in headers.items():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8910',
                                  desired_capabilities=desired_capabilities)
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
        # chrome = os.environ['chrome']
        # port = '4444'
        # driver = webdriver.Remote(command_executor='http://' + chrome + ':' + port + '/wd/hub',
        #                           desired_capabilities=DesiredCapabilities.CHROME)
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8913/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        return driver
