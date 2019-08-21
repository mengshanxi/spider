import urllib.request

import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from config.mylog import logger
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver

"""
支付快讯监控服务，10s一次
"""


class MonitorZfzjService:

    @staticmethod
    def monitor_tousu(website_name, merchant_name, batch_num):
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "http://www.zfzj.cn/search.php"
            driver.get(url)
            source = driver.page_source
            search_text_blank = driver.find_element_by_id("scform_srchtxt")
            search_text_blank.send_keys(merchant_name)
            search_text_blank.send_keys(Keys.RETURN)
            time.sleep(5)
            senti_util.snapshot_home("支付快讯", merchant_name, url,
                                     batch_num, driver)
            soup = BeautifulSoup(source, 'html.parser')
            items = soup.find_all(attrs={'class': 'slst mtw'})
            if items.__len__() > 0:
                for item in items.find_all('li'):
                    href = item.find_all('a')[0].get("href")
                    content = item.find_all('a')[0].get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("支付快讯", merchant_name, content,
                                                      "http://www.paycircle.cn" + href[1:],
                                                      batch_num)
            else:
                logger.info("支付快讯没有搜索到数据: %s", merchant_name)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
