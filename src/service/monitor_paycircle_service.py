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
    def monitor(keyword, batch_num, website):
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "http://www.paycircle.cn/company/search.php?kw=" + urllib.parse.quote(
                keyword) + "&c=SearchList&"
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("支付圈", url,
                                     batch_num, website,
                                     driver)
            soup = BeautifulSoup(source, 'html.parser')
            div_list = soup.find_all(attrs={'class': 'list'})
            if div_list.__len__() > 0:
                news = div_list[0].find_all('tr')
                for new in news:
                    href = new.find_all('td')[2].find_all('a')[0].get("href")
                    content = new.find_all('td')[2].find_all('li')[1].get_text()
                    if content.find(keyword) != -1:
                        senti_util.senti_process_text("支付圈", content, href,
                                                      batch_num, website)
            else:
                logger.info("支付圈没有搜索到数据: %s", keyword)

        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
