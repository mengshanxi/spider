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
        driver.get("https://www.baidu.com/")
        driver.find_element_by_id("kw").send_keys(u"京东")
        driver.find_element_by_id("su").click()
        """
        driver = WebDriver.get_phantomjs()
        try:
            driver.get("https://www.baidu.com/")
            driver.find_element_by_xpath('//input[@name="wd"]').send_keys(u"京东")

        except Exception as e:  # 异常处理
            print(e)
            pass
        SnapshotService.create_snapshot(driver)
        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        for result_table in soup.find_all('h3', class_='t'):
            a_click = result_table.find("a");
            print(a_click.get_text())  # 标题
            print(str(a_click.get("href")))  # 链接
        '''
        京东、盒马鲜生入驻重庆财富购物中心_凤凰资讯
        http://www.baidu.com/link?url=CV-k6a_vPNU_Y4uczGPGvuldDzwkbK2UaDoCVavtVp88Iete-1kkBj-6SC29fMZmygPNUz0hduJShHwPVPyJDa
        '''
