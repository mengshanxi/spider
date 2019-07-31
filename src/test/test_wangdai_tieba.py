import time
from config.mylog import logger
from bs4 import BeautifulSoup
from service.senti_util import SentiUtil
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver
import urllib.request
from service.monitor_tieba_service import MonitorTiebaService


class TestWangdaitianyan(object):
    if __name__ == "__main__":
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")
        driver.get("http://tieba.baidu.com/f?fr=wwwt&kw=" + urllib.parse.quote("京东"))
        """
        MonitorTiebaService = MonitorTiebaService()
        MonitorTiebaService.monitor_tieba("京东", "", 1)
