from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class TestEs(object):
    if __name__ == "__main__":
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        headers = {
            'cookie': ''}
        for key, value in headers.items():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(executable_path='/agent/phantomjs',desired_capabilities=DesiredCapabilities.PHANTOMJS)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        driver.get("www.baidu.com")
        driver.save_screenshot("/usr/local/snapshots/aa.png")
        driver.quit()
