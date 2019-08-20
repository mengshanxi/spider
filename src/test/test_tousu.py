import time
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        url = "https://tousu.sina.com.cn/index/search/?keywords=%E4%BA%AC%E4%B8%9C&t=0"
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8912/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
    try:
        driver.get(url)
        time.sleep(5)
        driver.save_screenshot("D:/bb.jpg")
        driver.quit()
    except Exception as e:
        logger.error(e)
