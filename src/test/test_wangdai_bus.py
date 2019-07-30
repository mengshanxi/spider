import time

from bs4 import BeautifulSoup

from config.mylog import logger
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver


class TestWangdaitianyan(object):
    if __name__ == "__main__":
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")  
        driver.get("http://www.wangdaibus.com/search.php?mod=forum")
        driver.find_element_by_id("scform_srchtxt").send_keys(u"京东")
        driver.find_element_by_id("scform_submit").click()     
        """
        driver = WebDriver.get_phantomJS()
        try:
            driver.get("http://www.wangdaibus.com/search/list?subject=%E4%BA%AC%E4%B8%9C")
            aaa="京东"
            #lement_by_xpath('//input[@name="subject"]').send_keys(aaa)
            #driver.find_element_by_xpath('//input[@name="subject"]').send_keys(Keys.ENTER)
            time.sleep(10)

        except Exception as e:  # 异常处理
            logger.error(e)
            pass
        SnapshotService.create_snapshot(driver)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        news = soup.find_all("h3", attrs={'class': 'xs3'})
        if news.__len__() > 0:
            for new in news:
                href = new.find_all('a')[0].get("href")
                logger.info("http://www.wangdaibus.com/" + href)
                logger.info(new.get_text())
        # 关闭浏览器
        driver.quit()
        '''
        forum.php?mod=viewthread&tid=181410&highlight=%BE%A9%B6%AB

中国企业报：京东总部现维权人群：0元购破灭 京东是否要担责？

forum.php?mod=viewthread&tid=180234&highlight=%BE%A9%B6%AB

金蛋理财，平台耍赖，投资人的京东卡一个多月了迟迟不发

        '''
