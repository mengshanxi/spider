from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from config.mylog import logger
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver

"""
支付产业网监控服务
"""


class MonitorPaynewsService:

    @staticmethod
    def monitor(keyword, batch_num, website):
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        url = "http://paynews.net/search.php?mod=forum"
        if driver is None:
            senti_util.log_error("支付产业网", url, batch_num, website)
            return
        else:
            pass
        try:
            driver.get(url)
            search_text_blank = driver.find_element_by_id("scform_srchtxt")
            search_text_blank.send_keys(keyword)
            search_text_blank.send_keys(Keys.RETURN)
            senti_util.snapshot_home("支付产业网", url,
                                     batch_num, website,
                                     driver)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            div_list = soup.find(attrs={'class': 'slst mtw'})
            if div_list is not None and div_list.__len__() > 0:
                news = div_list.find_all('li')
                for new in news:
                    href = new.find_all('a')[0].get("href")
                    content = new.find_all('a')[0].get_text()
                    if content.find(keyword) != -1:
                        senti_util.senti_process_text("支付产业网", content, "http://paynews.net/" + href,
                                                      batch_num, website)
            else:
                logger.info("支付产业网没有搜索到数据: %s", keyword)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
