import urllib.request

from bs4 import BeautifulSoup

from config.mylog import logger
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver

"""
黑猫投诉监控服务
"""


class MonitorTousuService:

    @staticmethod
    def monitor(website_name, merchant_name, batch_num):
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "https://tousu.sina.com.cn/index/search/?keywords=" + urllib.parse.quote(website_name) + "&t=0"
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("黑猫投诉", merchant_name, url,
                                     batch_num, driver)
            soup = BeautifulSoup(source, 'html.parser')
            items = soup.find_all(attrs={'class': 'blackcat-con'})
            if items.__len__() > 0:
                for item in items:
                    href = item.find_all('a')[0].get("href")
                    content = item.find_all('h1')[0].get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("黑猫投诉", merchant_name, content, href,
                                                      batch_num)
            else:
                logger.info("黑猫投诉没有搜索到数据: %s", merchant_name)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
