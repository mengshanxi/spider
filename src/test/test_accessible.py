import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from service.accessible_service import AccessibleService

if __name__ == "__main__":
    chrome_options = Options()
    # 禁止图片和css加载
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Remote(command_executor='http://172.17.161.230:8912/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME,
                              options=chrome_options)

    driver.set_page_load_timeout(60)
    driver.set_script_timeout(30)
    driver.maximize_window()
    try:
        driver.get("http:/www.tubuyla.com/#buttons")
        print()
    except Exception as e:
        print()
    finally:
        driver.quit()
