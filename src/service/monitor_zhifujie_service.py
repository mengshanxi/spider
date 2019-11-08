import time

from bs4 import BeautifulSoup

from config.mylog import logger
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver

"""
支付界监控服务
"""


class MonitorZhifujieService:

    @staticmethod
    def monitor(keyword, batch_num, website):
        url = "http://www.zhifujie.com/search/search"
        try:
            driver = WebDriver.get_chrome()
            senti_util = SentiUtil()
            driver.get(url)
            search_text_blank = driver.find_element_by_id("searchbox")
            search_text_blank.send_keys(keyword)
            driver.find_element_by_xpath('//button[contains(text(), "搜索")]').click()
            time.sleep(5)
            source = driver.page_source
            senti_util.snapshot_home("支付界", url,
                                     batch_num, website, driver)
            soup = BeautifulSoup(source, 'html.parser')
            items = soup.find_all(attrs={'class': 'main-news-content-item'})
            if items.__len__() > 0:
                for item in items:
                    href = item.find_all('a')[1].get("href")
                    content = item.find_all('a')[1].get_text()
                    if content.find(keyword) != -1:
                        senti_util.senti_process_text("支付界", content,
                                                      "http://www.paycircle.cn" + href[1:],
                                                      batch_num, website)
            else:
                logger.info("支付界没有搜索到数据: %s", keyword)
        except Exception as e:
            logger.error(e)
            senti_util.snapshot_home("支付界", url,
                                     batch_num, website, driver)
            return
        finally:
            driver.quit()
