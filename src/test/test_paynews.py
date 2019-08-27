import time
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        url = "http://paynews.net/search.php?mod=forum"
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
    try:
        driver.get(url)
        search_text_blank = driver.find_element_by_id("scform_srchtxt")
        search_text_blank.send_keys('京东')
        search_text_blank.send_keys(Keys.RETURN)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        driver.save_screenshot("D:/a.png")
        div_list = soup.find(attrs={'class': 'slst mtw'})
        if div_list.__len__() > 0:
            news = div_list.find_all('li')
            for new in news:
                href = new.find_all('a')[0].get("href")
                content = new.find_all('a')[0].get_text()
                print(content)
        else:
            logger.info("支付产业网没有搜索到数据: %s")
        driver.quit()
    except Exception as e:
        logger.error(e)
        driver.quit()
