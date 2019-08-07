import datetime
import time
import urllib

from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome import webdriver
import os
from config.config_load import chromedriver_path, phantomjs_path
from config.mylog import logger
from service.inspect_task_service import InspectTaskService
from service.monitor_bc_service import MonitorBcService
from service.webdriver_util import WebDriver
from service.weburl_service import WeburlService


class TestMysql(object):
    if __name__ == "__main__":
        os.environ['browser'] = "172.17.161.230"
        os.environ['port'] = '8912'
        webdriver = WebDriver()
        driver = webdriver.get_phantomjs()
        driver.set_window_size(1920, 1080)
        # 打开登录页面
        driver.get('https://www.qichacha.com/user_login')
        # 单击用户名密码登录的标签
        tag = driver.find_element_by_xpath('//*[@id="normalLogin"]')
        tag.click()
        # 将用户名、密码注入
        driver.find_element_by_id('nameNormal').send_keys('13811668973')
        driver.find_element_by_id('pwdNormal').send_keys('Abcd1234')
        time.sleep(10)  # 休眠，人工完成验证步骤，等待程序单击“登录”
        # 单击登录按钮
        btn = driver.find_element_by_xpath('//*[@id="user_login_normal"]/button')
        btn.click()
        time.sleep(10)
        source = driver.page_source
        driver.find_element_by_id("searchkey").send_keys("京东")
        driver.find_element_by_id("V3_Search_bt").click()
        source = driver.page_source
        print(source)
