import urllib.request

from bs4 import BeautifulSoup

import util.globalvar as gl
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver
from config.mylog import logger

"""
中国监控服务
"""


class MonitorChinaftService:

    @staticmethod
    def monitor(website_name, merchant_name, batch_num):
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=chromedriver_path)
        """
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "http://www.chinaft.com.cn/news/search/_1.shtml?key=" + urllib.parse.quote(website_name)
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("交易中国", merchant_name, url,
                                     batch_num, driver)
            soup = BeautifulSoup(source, 'html.parser')
            news = soup.find_all("div", attrs={'class': 'xixi_ChinaFT_left_news_box'})
            if news.__len__() > 0:
                for new in news:
                    if not gl.check_by_batch_num(batch_num):
                        break
                    href = new.find_all('a')[1].get("href")
                    content = new.find_all('a')[1].get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("交易中国", merchant_name, content,
                                                      "http://www.chinaft.com.cn" + href, batch_num)
            else:
                logger.info("交易中国没有搜索到数据: %s", merchant_name)
        except Exception as e:
            logger.error(e)
        finally:
            driver.quit()
