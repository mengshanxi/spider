import time

import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        url = "https://www.trackingmore.com/choose-cn-70634105326416.html?"
        # 实例化一个启动参数对象
        chrome_options = Options()
        # 禁止图片和css加载
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME,
                                  options=chrome_options)
        driver.maximize_window()
        driver.set_page_load_timeout(60)
    try:
        driver.get(url)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        logis_list = soup.find_all(attrs={'class': 'ulliselect'})
        start = datetime.datetime.now()
        if logis_list is not None and logis_list.__len__() > 0:
            for logis in logis_list:
                href = logis.get("href")
                name = logis.get_text()
                print(name)
                try:
                    print(href)
                    url = "https:" + href
                    driver.get(url)
                    driver.save_screenshot("D:/" + name + ".png")
                    end = datetime.datetime.now()
                    print(end - start)
                except Exception as e:
                    logger.error(e)
                    print('time out after 30 seconds when loading page')
                    driver.execute_script('window.stop()')
                    print('111')
                    driver.save_screenshot("D:/" + href + ".png")
                    print('超时后截图完毕')
            end = datetime.datetime.now()
            print(end - start)
    except Exception as e:
        print('3333')
        logger.error(e)
        print('2222')
        driver.quit()
