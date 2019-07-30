import time
import urllib.request

from selenium import webdriver


class TestQichachaService(object):
    # get_script(str) -> str
    def get_script(_type):
        if _type == "body_height":
            return """
                        // get body_height
                        return document.getElementsByTagName("body")[0].clientHeight;
                """

    if __name__ == "__main__":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver2.38.exe")


    """
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    headers = {
    }
    for key, value in headers.items():
        desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
    driver = webdriver.PhantomJS(executable_path=phantomjs_path,
                                 desired_capabilities=desired_capabilities,
                                 service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    
    """

    # 设置最长的超时时间
    driver.set_page_load_timeout(10)
    driver.maximize_window()
    driver.get("https://www.p2peye.com/search.php?mod=zonghe&srchtxt=" + urllib.parse.quote("京东"))
    time.sleep(5)
    # body_height = driver.execute_script(get_script("body_height"))


    # driver.set_window_size(375, body_height)
    driver.save_screenshot('D:/3.png')
    # 将页面滚动条拖到底部
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(3)
    driver.save_screenshot('D:/buttom.png')

    # 将滚动条移动到页面的顶部
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    time.sleep(3)
    driver.save_screenshot('D:/4.png')

    # 将滚动条移动到页面的任意位置
    js = "var q=document.documentElement.scrollTop=900"
    driver.execute_script(js)
    time.sleep(3)
    print(driver.page_source)
    driver.save_screenshot('D:/5.png')

    # 将滚动条移动到页面的任意位置
    js = "var q=document.documentElement.scrollTop=1800"
    driver.execute_script(js)
    time.sleep(3)
    driver.save_screenshot('D:/6.png')

    driver.quit()

    # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    # headers = {
    # }
    # for key, value in headers.items():
    #     desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
    # driver = webdriver.PhantomJS(executable_path=phantomjs_path,
    #                              desired_capabilities=desired_capabilities,
    #                              service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    # driver.get("https://www.jianshu.com/p/7ed519854be7")
    # driver.save_screenshot("D:/2.png")
    # driver.quit()
