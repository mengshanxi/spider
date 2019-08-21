import urllib.request

from bs4 import BeautifulSoup

from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver
from config.mylog import logger

"""
支付圈监控服务
"""


class MonitorPaycircleService:

    @staticmethod
    def monitor_paycircle(website_name, merchant_name, batch_num):
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "http://www.paycircle.cn/company/search.php?kw=" + urllib.parse.quote(website_name) + "&c=SearchList&"
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("支付圈", merchant_name, url,
                                     batch_num, driver)
            soup = BeautifulSoup(source, 'html.parser')
            news = soup.find_all(attrs={'class': 'result-t'})
            if news.__len__() > 0:
                for new in news:
                    href = new.find_all('a')[0].get("href")
                    content = new.get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("支付圈", merchant_name, content, "http://" + href[2:],
                                                      batch_num)
            else:
                logger.info("支付圈没有搜索到数据: %s", merchant_name)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
