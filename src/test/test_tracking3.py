import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


class TestMysql(object):
    if __name__ == "__main__":
        chrome_options = Options()
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument("--disk-cache-size=0")
        driver = webdriver.Remote(command_executor='http://172.19.27.54:8912/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME, options=chrome_options)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.maximize_window()
        try:
            driver.get("https://www.trackingmore.com/cn/AGSIPNJ0067608744?ram=" + str(time.time()))
            driver.save_screenshot("D:/物流公司3.png")
        except Exception as e:
            print(e)
        finally:
            driver.quit()
