import urllib.request

from bs4 import BeautifulSoup

from config.mylog import logger
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver

"""
贴吧监控服务
"""


class MonitorTiebaService:

    @staticmethod
    def monitor_tieba(website_name, merchant_name, batch_num):
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=chromedriver_path)
        """
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "http://tieba.baidu.com/f?fr=wwwt&kw=" + urllib.parse.quote(website_name)
            driver.get(url)
            senti_util.snapshot_home("百度贴吧", merchant_name, url,
                                     batch_num, driver)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            news = soup.find_all("div", attrs={'class': 'threadlist_title pull_left j_th_tit '})
            if news.__len__() > 0:
                for new in news:
                    href = new.find_all('a')[0].get("href")
                    content = new.find_all('a')[0].get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("百度贴吧", merchant_name, content,
                                                      "http://tieba.baidu.com" + href, batch_num)
            else:
                logger.info("百度贴吧没有搜索到数据: %s", merchant_name)
        except Exception as e:
            logger.error(e)
            return
