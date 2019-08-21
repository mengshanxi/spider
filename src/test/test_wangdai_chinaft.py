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
        driver.get("http://www.chinaft.com.cn/news/search/_1.shtml?key=" + urllib.parse.quote("京东"))
        """
        driver = WebDriver.get_chrome()
        try :
            driver.get("http://www.chinaft.com.cn/news/search/_1.shtml?key=" + urllib.parse.quote("京东"))
        except Exception as e:
            print("error")
            pass

        print("e")
        SnapshotService.create_snapshot(driver)
        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        news = soup.find_all("div", attrs={'class': 'xixi_ChinaFT_left_news_box'})
        if news.__len__() > 0:
            for new in news:
                href = new.find_all('a')[1].get("href")
                print("http://www.chinaft.com.cn"+href)
                print(new.find_all('a')[1].get_text())
