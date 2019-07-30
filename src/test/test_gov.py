import time

from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup


class TestWangdaitianyan(object):
    if __name__ == "__main__":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")
        driver.get(
            "http://www.gsxt.gov.cn/corp-query-search-advancetest.html?tab=excep_tab&cStatus=0&eYear=0&area=0&filter=0&province=100000&searchword=%E4%BA%AC%E4%B8%9C" + urllib.parse.quote(
                "京东"))
        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        # 关闭浏览器
        driver.quit()
