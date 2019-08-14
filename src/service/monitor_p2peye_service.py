import urllib.request

from bs4 import BeautifulSoup

from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver
from config.mylog import logger

"""
网贷天眼监控服务
"""


class MonitorP2peyeService:

    @staticmethod
    def monitor_p2peye(website_name, merchant_name,batch_num):
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=chromedriver_path)
        """
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "https://www.p2peye.com/search.php?mod=zonghe&srchtxt=" + urllib.parse.quote(website_name)
            driver.get(url)
            source = driver.page_source
            senti_util.snapshot_home("网贷天眼", merchant_name, url,
                                     batch_num, driver)
            soup = BeautifulSoup(source, 'html.parser')
            news = soup.find_all(attrs={'class': 'result-t'})
            if news.__len__() > 0:
                for new in news:
                    href = new.find_all('a')[0].get("href")
                    content = new.get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("网贷天眼", merchant_name,content, "http://" + href[2:],
                                                      batch_num)
            else:
                logger.info("网贷天眼没有搜索到数据: %s", merchant_name)
        except Exception as e:
            logger.error(e)
            return
