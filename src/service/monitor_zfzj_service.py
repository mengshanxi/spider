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
    def monitor(keyword, batch_num, website):
        try:
            driver = WebDriver.get_chrome()
            senti_util = SentiUtil()
            url = "http://www.zfzj.cn/search.php"
            driver.get(url)
            source = driver.page_source
            search_text_blank = driver.find_element_by_id("scform_srchtxt")
            search_text_blank.send_keys(keyword)
            search_text_blank.send_keys(Keys.RETURN)
            time.sleep(5)
            senti_util.snapshot_home("支付快讯", url,
                                     batch_num, website, driver)
            soup = BeautifulSoup(source, 'html.parser')
            items = soup.find_all(attrs={'class': 'slst mtw'})
            if items.__len__() > 0:
                for item in items.find_all('li'):
                    href = item.find_all('a')[0].get("href")
                    content = item.find_all('a')[0].get_text()
                    if content.find(keyword) != -1:
                        senti_util.senti_process_text("支付快讯", content,
                                                      "http://www.paycircle.cn" + href[1:],
                                                      batch_num, website)
            else:
                logger.info("支付快讯没有搜索到数据: %s", keyword)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
