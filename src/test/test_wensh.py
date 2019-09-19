import json
import urllib

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from dao.db import session
from model.models import TaskItem
from service.monitor_tracking_service import MonitorTrackingService
from service.task_pool_service import TaskPoolService


class TestMysql(object):
    if __name__ == "__main__":
        url = "http://wenshu.court.gov.cn/"
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
    try:
        driver.get(url)
        search_text_blank = driver.find_element_by_xpath("//*[@class='searchKey search-inp']")
        search_text_blank.send_keys('京东')
        search_text_blank.send_keys(Keys.RETURN)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        for a_tag in soup.find_all('a', class_='caseName'):
            href = a_tag.get("href")
            title = a_tag.get_text()
            print("http://wenshu.court.gov.cn/website/wenshu" + href[2:])
            print(title)
        driver.save_screenshot("D:/111.png")
        driver.quit()
    except Exception as e:
        driver.quit()
