# coding:utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

from service.snapshot_service import SnapshotService


def editUserAgent():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
    driver = webdriver.PhantomJS(executable_path="D:/software/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                                 desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                               '--load-images=false'],
                                 service_log_path="D:/a.log")
    try:
        url = "www.365zfpay.com"
        if str(url).startswith("http"):
            print()
        else:
            url = "http://" + url
        driver.get(url)
        weburl=We
        SnapshotService.snapshot_weburl(driver, "22", weburl, '网站内容')
        time.sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        driver.save_screenshot("D:/333.png")
        print()
    except Exception as e:
        print(e)
        driver.quit()


if __name__ == '__main__':
    editUserAgent()
