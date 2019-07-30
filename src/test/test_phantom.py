# coding:utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config.config_load import phantomjs_path
import urllib.request
import time

def editUserAgent():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
    driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true'])
    driver.get("https://www.p2peye.com/search.php?mod=zonghe&srchtxt=" + urllib.parse.quote("京东"))
    time.sleep(5)
    driver.save_screenshot('D:/11.png')

    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    user_agent = soup.find_all('td', attrs={
        'style': 'height:40px;text-align:center;font-size:16px;font-weight:bolder;color:red;'})
    for u in user_agent:
        print(u.get_text().replace('\n', '').replace(' ', ''))
    driver.close()


if __name__ == '__main__':
    editUserAgent()
