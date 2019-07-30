from bs4 import BeautifulSoup
import urllib.request
import src.util.globalvar as gl
from src.service.senti_util import SentiUtil
from src.service.webdriver_util import WebDriver
from src.config.mylog import logger
import time

"""
网贷巴士监控服务
"""


class MonitorBusService:

    @staticmethod
    def monitor_bus(website_name,merchant_name, batch_num):
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=chromedriver_path)
        """
        driver = WebDriver.get_phantomJS()
        senti_util = SentiUtil()
        try:
            url = "http://www.wangdaibus.com/search/list?subject=" + urllib.parse.quote(website_name)
            driver.get(url)
            time.sleep(10)
            senti_util.snapshot_home("网贷巴士", merchant_name, url,
                                     batch_num, driver)
            # driver.find_element_by_xpath('//input[@name="srchtxt"]').send_keys(website_name)
            # driver.find_element_by_xpath('//input[@name="srchtxt"]').send_keys(Keys.ENTER)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            news = soup.find_all("h3", attrs={'class': 'xs3'})
            if news.__len__() > 0:
                for new in news:
                    if not gl.check_by_batch_num(batch_num):
                        break
                    href = new.find_all('a')[0].get("href")
                    content = new.get_text()
                    if content.find(website_name) != -1:
                        senti_util.senti_process_text("网贷巴士", merchant_name,content,
                                                      "http://www.wangdaibus.com/" + href,
                                                      batch_num)
            else:
                logger.info("网贷巴士没有搜索到数据: %s", merchant_name)
            driver.quit()
        except Exception as e:
            logger.error(e)
            driver.quit()
            return
