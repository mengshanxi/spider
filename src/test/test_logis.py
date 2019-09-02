import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        url = "https://www.trackingmore.com/choose-cn-70634105326416.html?"
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
    try:
        driver.get(url)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        logis_list = soup.find_all(attrs={'class': 'ulliselect'})
        driver.quit()
        if logis_list is not None and logis_list.__len__() > 0:
            for logis in logis_list:
                href = logis.get("href")
                name = logis.get_text()
                print(name)
                driver = webdriver.Remote(command_executor='http://172.17.161.230:8912/wd/hub',
                                          desired_capabilities=DesiredCapabilities.CHROME)
                driver.implicitly_wait(60)
                driver.maximize_window()
                try:
                    print(href)
                    url = "https:"+href
                    driver.get(url)
                    driver.save_screenshot("D:/" + name + ".jpg")
                except Exception as e:
                    logger.error(e)
                    driver.execute_script('window.stop()')
                    driver.save_screenshot("D:/" + name + ".jpg")
                    driver.quit()
    except Exception as e:
        logger.error(e)
        driver.quit()
