# -*- coding:utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from src.service.senti_util import SentiUtil
from src.service.webdriver_util import WebDriver
from src.config.mylog import logger


class MonitorBaikeService:
    @staticmethod
    def monitor_baike(website_name,merchant_name, batch_num):
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=chromedriver_path)
        """
        driver = WebDriver.get_phantomJS()
        senti_util = SentiUtil()
        url = 'https://baike.baidu.com/item/%s' % urllib.parse.quote(website_name.replace("(", "（").replace(")", "）"))
        try:
            driver.get(url)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            check_exist = soup.find_all(name='p', attrs={'class': re.compile('sorryCont')})
            if check_exist.__len__() == 0:
                description = soup.find(attrs={"name": "description"})['content']
                senti_util.senti_process_text("百度百科", merchant_name, description, url,
                                              batch_num)
            else:
                senti_util.snapshot_home("百度百科", merchant_name, url,
                                         batch_num, driver)
                logger.info("百度百科没有搜索到数据: %s", merchant_name)
            driver.quit()

        except Exception as e:
            logger.error(e)
            driver.quit()
            return
