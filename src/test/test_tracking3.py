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
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        # 更换头部
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
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
