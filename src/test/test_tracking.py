from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class TestMysql(object):
    if __name__ == "__main__":
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2, 'javascript': 2}
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", prefs)
        url = "https://www.trackingmore.com/yunda-tracking/cn.html?number=4300688044377"
        #查不到
        #url = "https://www.trackingmore.com/zto-tracking/cn.html?number=430068804437"
        #快递公司列表
        #url="https://www.trackingmore.com/cn/430068804437"

        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME,
                                  options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(10)
        driver.maximize_window()
        try:
            driver.get("https://www.trackingmore.com/cn/75168858039903")
            driver.find_element_by_link_text("中通快递").click()
            # 将滚动条移动到页面的顶部
            driver.implicitly_wait(3)
            #Not Found
            driver.save_screenshot("D:/nnnn.png")
        except Exception as e:
            print(e)
        finally:
            driver.quit()
