import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


if __name__ == "__main__":
    driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(10)
    url = "http://www.jixiangshxl.com/"
    try:
        if str(url).startswith("http"):
            http_url = str(url)
        else:
            http_url = "http://" + str(url)
        driver.get(http_url)
        title = driver.title
        if title is '没有找到站点':
            print(title)
    except Exception as e:
        print(e)
    finally:
        driver.quit()

