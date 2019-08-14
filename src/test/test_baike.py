import urllib.request

import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


class TestWangdaitianyan(object):
    if __name__ == "__main__":
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")
        url = 'https://baike.baidu.com/item/%s' % urllib.parse.quote("猫小贷")
        """
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        driver = webdriver.Remote(command_executor="http://172.17.161.230:8913/wd/hub",
                desired_capabilities=DesiredCapabilities.CHROME)
        driver.set_page_load_timeout(5)
        driver.set_script_timeout(5)
        driver.maximize_window()
        url = "https://www.p2peye.com/search.php?mod=zonghe&srchtxt=" + urllib.parse.quote('上海菁厘信息科技有限公司')
        #driver.get('https://baike.baidu.com/item/%s' % urllib.parse.quote("京东"))
        driver.get(url)
        time.sleep(3)
        driver.save_screenshot("ff.png")

        driver.quit()
        # SnapshotService.create_snapshot(driver)
        # time.sleep(3)
        # source = driver.page_source
        # soup = BeautifulSoup(source, 'html.parser')
        #
        # plants_string = soup.find(text="plants")
        #
        # description = soup.find(attrs={"name": "description"})['content']
        # # keywords = soup.find(attrs={"name": "keywords"})['content']
        # if str(description).startswith("百度百科是一部内容开放"):
        #     #print("百科没有搜索到词条:%s" % "猫小贷")
        #     pass
        # else:
        #     #print("百科没有搜索到词条:%s" % "猫小贷")
        #     pass
