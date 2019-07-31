from bs4 import BeautifulSoup

import util.globalvar as gl
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver
from config.mylog import logger
from selenium.webdriver.common.keys import Keys
import time

"""
百度监控服务
"""


class MonitorBaiduService:

    @staticmethod
    def monitor_baidu(website_name,merchant_name, batch_num):
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=chromedriver_path)
        """
        driver = WebDriver.get_phantomJS()
        senti_util = SentiUtil()
        try:
            url = "https://www.baidu.com/"
            driver.get(url)
            search_text_blank = driver.find_element_by_id("kw")
            search_text_blank.send_keys(website_name)
            search_text_blank.send_keys(Keys.RETURN)
            time.sleep(10)
            # driver.find_element_by_xpath('//input[@name="wd"]').send_keys(website_name)
            senti_util.snapshot_home("百度搜索", merchant_name, url,
                                     batch_num, driver)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            for result_table in soup.find_all('h3', class_='t'):
                if not gl.check_by_batch_num(batch_num):
                    break
                a_click = result_table.find("a")
                title = a_click.get_text()
                if title.find(website_name) != -1:
                    senti_util.senti_process_text("百度搜索", merchant_name, title, str(a_click.get("href")),
                                                  batch_num)
        except Exception as e:
            logger.error(e)
            return
