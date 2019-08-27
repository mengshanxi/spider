import urllib.request

from bs4 import BeautifulSoup

from config.mylog import logger
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver

"""
聚投诉监控服务
"""


class MonitorTsService:

    @staticmethod
    def monitor(keyword, website_name, batch_num, merchant_name, merchant_num):
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "http://ts.21cn.com/home/search?keyword=" + urllib.parse.quote(keyword)
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("聚投诉", website_name, url,
                                     batch_num, merchant_name, merchant_num,
                                     driver)
            soup = BeautifulSoup(source, 'html.parser')
            items = soup.find_all(attrs={'class': 'complain-item'})
            if items.__len__() > 0:
                for item in items:
                    href = item.find_all('a')[1].get("href")
                    content = item.find_all('a')[1].get_text()
                    if content.find(keyword) != -1:
                        senti_util.senti_process_text("聚投诉", website_name, content,
                                                      "http://www.paycircle.cn" + href[1:],
                                                      batch_num, merchant_name,
                                                      merchant_num)
            else:
                logger.info("聚投诉没有搜索到数据: %s", keyword)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
