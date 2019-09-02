import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from model.models import Weburl
from service.accessible_service import AccessibleService
from service.monitor_bc_service import MonitorBcService
from service.monitor_weburl_service import MonitorWeburlService
from service.webdriver_util import WebDriver


def take_screenshot(browser):
    browser.set_window_size(1200, 900)
    # 以下代码是将浏览器页面拉到最下面。
    browser.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);
            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }
            setTimeout(f, 1000);
        })();
    """)
    time.sleep(1)


if __name__ == "__main__":
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")
        driver.get('https://www.trackingmore.com/bestex-tracking/cn.html?number=70634105326416')
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        driver.maximize_window()
        take_screenshot(driver)
        driver.save_screenshot('1' + '.png')
        driver.quit()
    except Exception as e:
        driver.quit()
