import time

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
        driver.get("https://www.wdzj.com/front/search/index?key=" + urllib.parse.quote("猫小贷"))
        """
        try:
            driver = WebDriver.get_phantomJS()
            driver.get("http://www.wdzj.com/news/yc/2934681.html")

        except Exception as e:  # 异常处理
            print(e)
            pass
        SnapshotService.create_snapshot(driver)
        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        print(soup.find_all("ul", attrs={'class': 'so-tzbox'}))
        news = soup.find_all("ul", attrs={'class': 'so-tzbox'})[0].find_all("li")
        if news.__len__() > 0:
            for new in news:
                href = new.find_all('a')[0].get("href")
                print(href[2:])
                #print(new.get_text())
