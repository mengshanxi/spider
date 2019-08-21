import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


class TestCookie(object):
    if __name__ == "__main__":
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)
        driver.get("https://www.qichacha.com/firm_84c17a005a759a5e0d875c1ebb6c9846.html")
        time.sleep(3)
        driver.find_element_by_partial_link_text("经营风险").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_partial_link_text("经营异常").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        driver.save_screenshot("D:/cc.jpg")
        driver.quit()
