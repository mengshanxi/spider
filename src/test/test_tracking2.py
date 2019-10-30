from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options



class TestMysql(object):
    if __name__ == "__main__":
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", prefs)
        url = "https://www.trackingmore.com/yunda-tracking/cn.html?number=4300688044377"
        #查不到
        #url = "https://www.trackingmore.com/zto-tracking/cn.html?number=430068804437"
        #快递公司列表
        #url="https://www.trackingmore.com/cn/430068804437"
        # driver = webdriver.Remote(command_executor='http://172.19.27.54:8912/wd/hub',
        #                           desired_capabilities=DesiredCapabilities.CHROME,
        #                           options=chrome_options)
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        driver = webdriver.PhantomJS(executable_path="D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                                     desired_capabilities=dcap,
                                     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                                   '--load-images=false'],
                                     service_log_path="D:/a.log")
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(10)
        driver.maximize_window()

        try:
            driver.get("http://www.trackingmore.com/usps-tracking/cn.html?number=9374889697090677379574")
            # source = driver.page_source
            # soup = BeautifulSoup(source, 'html.parser')
            # trackings = soup.find_all("a", attrs={'class': 'ulliselect'})
            # if trackings.__len__() > 0:
            #     for tracking in trackings:
            #         print(tracking.get_text())
            #         print("http:"+tracking.get("href"))
            #Not Found
            driver.save_screenshot("D:/gggg.png")
        except Exception as e:
            print(e)
        finally:
            driver.quit()
