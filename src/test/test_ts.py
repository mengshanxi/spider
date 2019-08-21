import time
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        url = "http://ts.21cn.com/home/search?keyword=%E4%BA%AC%E4%B8%9C"
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8912/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
    try:
        driver.get(url)
        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        items = soup.find_all(attrs={'class': 'blackcat-con'})
        if items.__len__() > 0:
            for item in items:
                href = item.find_all('a')[0].get("href")
                content = item.find_all('h1')[0].get_text()
        else:
            logger.info("黑猫投诉没有搜索到数据:")
        driver.quit()
    except Exception as e:
        logger.error(e)
        driver.quit()
