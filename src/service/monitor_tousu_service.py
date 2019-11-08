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
    def monitor(keyword, batch_num, website):
        try:
            driver = WebDriver.get_chrome()
            senti_util = SentiUtil()
            url = "https://tousu.sina.com.cn/index/search/?keywords=" + urllib.parse.quote(keyword) + "&t=0"
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("黑猫投诉", url, batch_num, website, driver)
            soup = BeautifulSoup(source, 'html.parser')
            items = soup.find_all(attrs={'class': 'blackcat-con'})
            if items.__len__() > 0:
                for item in items:
                    href = item.find_all('a')[0].get("href")
                    content = item.find_all('h1')[0].get_text()
                    if content.find(keyword) != -1:
                        senti_util.senti_process_text("黑猫投诉", content, href,
                                                      batch_num, website)
            else:
                logger.info("黑猫投诉没有搜索到数据: %s", keyword)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
