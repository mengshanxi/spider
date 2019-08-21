import urllib.request

from bs4 import BeautifulSoup

from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver
from config.mylog import logger

"""
支付产业网监控服务
"""


class MonitorPaynewsService:

    @staticmethod
    def monitor_paynews(website_name, merchant_name, batch_num):
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "http://paynews.net/search.php?mod=forum"
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("支付产业网", merchant_name, url,
                                     batch_num, driver)
            soup = BeautifulSoup(source, 'html.parser')
            # soup.find_all(attrs={'class': 'slst mtw'}).__len__()
            # soup.find_all(attrs={'class': 'slst mtw'})[0].find_all('li')[0].find_all('a')[0].get("href")
            # soup.find_all(attrs={'class': 'slst mtw'})[0].find_all('li')[0].find_all('a')[0].get_text()
            div_list = soup.find_all(attrs={'class': 'slst mtw'})
            if div_list.__len__() > 0:
                news = div_list.find_all('li')
                for new in news:
                    href = new.find_all('a')[0].get("href")
                    content = new.find_all('a')[0].get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("支付产业网", merchant_name, content, "http://paynews.net/" + href,
                                                      batch_num)
            else:
                logger.info("支付产业网没有搜索到数据: %s", merchant_name)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
