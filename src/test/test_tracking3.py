import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


class TestMysql(object):
    if __name__ == "__main__":
        chrome_options = Options()
        #chrome_options.add_argument('--proxy-server=http://218.63.76.41:47868')
        # 更换头部
        driver = webdriver.Remote(command_executor='http://172.17.161.226:8913/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME, options=chrome_options)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.maximize_window()
        try:
            driver.get("https://www.trackingmore.com/cn/1ZE1314V0389515183?ram=" + str(time.time()))
            driver.save_screenshot("D:/物流公司3.png")
        except Exception as e:
            print(e)
        finally:
            driver.quit()
