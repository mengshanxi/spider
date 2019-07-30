import time

from bs4 import BeautifulSoup

from src.service.snapshot_service import SnapshotService
from src.service.webdriver_util import WebDriver
import urllib.request

class TestWangdaitianyan(object):
    if __name__ == "__main__":
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")
        driver.get("http://tieba.baidu.com/f?fr=wwwt&kw=" + urllib.parse.quote("京东"))
        """
        driver = WebDriver.get_phantomJS()
        driver.set_page_load_timeout(60)
        #driver.get("https://tieba.baidu.com/f?ie=utf-8&&fr=search&kw=" + urllib.parse.quote("国商易贸"))
        driver.get("https://tieba.baidu.com/p/3990631710?red_tag=1663266479")
        SnapshotService.create_snapshot(driver)


        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        news = soup.find_all("div", attrs={'class': 'threadlist_title pull_left j_th_tit '})
        if news.__len__() > 0:
            for new in news:
                href = new.find_all('a')[0].get("href")
                content = new.find_all('a')[0].get_text()
                a = content.find("方针文产商城")
                print(new.find_all('a')[0].get_text())
        # 关闭浏览器
        driver.quit()
