import time
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        url = "http://www.zhifujie.com/search/search"
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
    try:
        driver.get(url)
        search_text_blank = driver.find_element_by_id("searchbox")
        search_text_blank.send_keys('移动支付')
        driver.find_element_by_xpath('//button[contains(text(), "搜索")]').click()

        time.sleep(5)
        driver.save_screenshot("D:/bb.jpg")
        driver.quit()
    except Exception as e:
        logger.error(e)
