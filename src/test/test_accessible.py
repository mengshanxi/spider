import time
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from dao.monitor_weburl_dao import MonitorWeburlDao
from model.models import Weburl, MonitorUrl
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
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8912/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)
        driver.get("http:/ziguangkeji.com.cn/product.php?pid=1&cid=4&nid=37&id=28")
        monitor_weburl_dao = MonitorWeburlDao()
        monitor_weburl = MonitorUrl()
        monitor_weburl.website_name = weburl.website_name
        monitor_weburl.url = weburl.url
        monitor_weburl.batch_num = batch_num
        monitor_weburl.title = weburl.title
        monitor_weburl.outline = '网页打开正常'
        monitor_weburl.is_normal = '正常'
        monitor_weburl.level = 0
        monitor_weburl.snapshot = snapshot
        monitor_weburl.kinds = '是否能打开'
        monitor_weburl_dao.add(monitor_weburl)

        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        # 监测页面敏感词
        for keyword in keywords:
            index = soup.find(keyword.name)
            if index is not None:
                monitor_weburl.outline = '检测到敏感词:' + str(keyword.name)
                monitor_weburl.is_normal = '异常'
                monitor_weburl.level = 2
                monitor_weburl.snapshot = snapshot
                monitor_weburl.kinds = '命中敏感词'

                monitor_weburl_dao.add(monitor_weburl)
        # 监测 非金融平台包含充值、提现、钱包功能
        illegal_fun = soup.find("充值")
        if illegal_fun is not None:
            monitor_weburl.outline = '检测到包含充值、提现、钱包功能'
            monitor_weburl.is_normal = '异常'
            monitor_weburl.level = 2
            monitor_weburl.snapshot = snapshot
            monitor_weburl.kinds = '非法功能'

            monitor_weburl_dao.add(monitor_weburl)
        # 监测 误导宣传
        mislead1 = soup.find("融宝资金担保")
        mislead2 = soup.find("融宝托管")
        if mislead1 is not None or mislead2 is not None:
            monitor_weburl.outline = '检测到误导宣传'
            monitor_weburl.is_normal = '异常'
            monitor_weburl.level = 2
            monitor_weburl.snapshot = snapshot
            monitor_weburl.kinds = '误导宣传'

            monitor_weburl_dao.add(monitor_weburl)
    except Exception as e:
        print(e)
    finally:
        driver.quit()

