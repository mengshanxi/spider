import urllib.request

from bs4 import BeautifulSoup

import util.globalvar as gl
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver
from config.mylog import logger

"""
网贷之家监控服务
"""


class MonitorWdzjService:

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
            url = "https://www.wdzj.com/front/search/index?key=" + urllib.parse.quote(website_name)
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("网贷之家", merchant_name, url,
                                     batch_num, driver)
            soup = BeautifulSoup(source, 'html.parser')
            tzbox = soup.find_all("ul", attrs={'class': 'so-tzbox'})
            if tzbox.__len__() == 0:
                return
            news = tzbox[0].find_all("li")
            if news.__len__() > 0:
                for new in news:
                    if not gl.check_by_batch_num(batch_num):
                        break
                    href = new.find_all('a')[0].get("href")
                    content = new.get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("网贷之家", merchant_name, content, "http://" + href[2:],
                                                      batch_num)
            else:
                logger.info("网贷之家没有搜索到数据: %s", merchant_name)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
