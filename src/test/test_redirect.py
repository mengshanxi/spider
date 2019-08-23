from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
    try:
        driver.get("http://en.ly.com")
        driver.save_screenshot("D:/bb.jpg")
        print(driver.current_url)
        driver.quit()
    except Exception as e:
        logger.error(e)