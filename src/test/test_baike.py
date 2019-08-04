import time
import urllib.request

from bs4 import BeautifulSoup

from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver


class TestWangdaitianyan(object):
    if __name__ == "__main__":
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")
        url = 'https://baike.baidu.com/item/%s' % urllib.parse.quote("猫小贷")
        """
        driver = WebDriver.get_phantomjs()
        driver.get('https://baike.baidu.com/item/%s' % urllib.parse.quote("方针文产商城"))
        SnapshotService.create_snapshot(driver)
        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        plants_string = soup.find(text="plants")

        description = soup.find(attrs={"name": "description"})['content']
        # keywords = soup.find(attrs={"name": "keywords"})['content']
        if str(description).startswith("百度百科是一部内容开放"):
            #print("百科没有搜索到词条:%s" % "猫小贷")
            pass
        else:
            #print("百科没有搜索到词条:%s" % "猫小贷")
            pass
