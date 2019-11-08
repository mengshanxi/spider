from bs4 import BeautifulSoup

from service.IMonitor import IMonitor
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver
from config.mylog import logger
from selenium.webdriver.common.keys import Keys
import time

"""
百度监控服务
"""


class MonitorBaiduService(IMonitor):

    @staticmethod
    def monitor(keyword, batch_num, website):
        try:
            driver = WebDriver.get_chrome()
            senti_util = SentiUtil()
            url = "https://www.baidu.com/"
            driver.get(url)
            search_text_blank = driver.find_element_by_id("kw")
            search_text_blank.send_keys(keyword)
            search_text_blank.send_keys(Keys.RETURN)
            time.sleep(5)
            # driver.find_element_by_xpath('//input[@name="wd"]').send_keys(website_name)
            senti_util.snapshot_home("百度搜索", url, batch_num, website, driver)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            for result_table in soup.find_all('h3', class_='t'):
                a_click = result_table.find("a")
                title = a_click.get_text()
                if title.find(keyword) != -1:
                    senti_util.senti_process_text("百度搜索", title, str(a_click.get("href")),
                                                  batch_num, website)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
