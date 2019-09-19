import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from config.mylog import logger
from service.IMonitor import IMonitor
from service.senti_util import SentiUtil
from service.webdriver_util import WebDriver

"""
裁判文书网
"""


class MonitorWenshuService(IMonitor):

    @staticmethod
    def monitor(keyword, batch_num, website):
        driver = WebDriver.get_chrome()
        senti_util = SentiUtil()
        try:
            url = "http://wenshu.court.gov.cn/"
            driver.get(url)
            search_text_blank = driver.find_element_by_xpath("//*[@class='searchKey search-inp']")
            search_text_blank.send_keys(keyword)
            search_text_blank.send_keys(Keys.RETURN)
            time.sleep(3)
            source = driver.page_source
            senti_util.snapshot_home("裁判文书网", url, batch_num, website, driver)
            soup = BeautifulSoup(source, 'html.parser')
            for a_tag in soup.find_all('a', class_='caseName'):
                href = a_tag.get("href")
                title = a_tag.get_text()
                if title.find(keyword) != -1:
                    senti_util.senti_process_text("裁判文书网", title,
                                                  "http://wenshu.court.gov.cn/website/wenshu" + href[2:],
                                                  batch_num, website)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
