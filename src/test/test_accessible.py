from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from model.models import Weburl
from service.accessible_service import AccessibleService
from service.monitor_bc_service import MonitorBcService
from service.monitor_weburl_service import MonitorWeburlService
from service.webdriver_util import WebDriver


class TestEs(object):
    if __name__ == "__main__":
        # service = MonitorBcService()
        # url = service.get_merchant_url(str(1), merchant_name='河北纷橙电子商务有限公司')
        # if url is not None:
        #     try:
        #         service.inspect(str(1), "https://www.qichacha.com" + url, '河北纷橙电子商务有限公司',
        #                         '靳建通')
        #     except Exception as e:
        #         pass
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(5)
        driver.set_script_timeout(5)
        driver.maximize_window()
    try:
        driver.get("http://www.aa.com")
        driver.save_screenshot("D:/bb.jpg")
        driver.quit()
    except Exception as e:
        print(e)