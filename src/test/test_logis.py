from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        url = "https://www.trackingmore.com/choose-cn-70634105326416.html?"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")

        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        driver.maximize_window()
    try:
        driver.get(url)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        logis_list = soup.find_all(attrs={'class': 'ulliselect'})
        if logis_list is not None and logis_list.__len__() > 0:
            for logis in logis_list:
                try:
                    href = logis.get("href")
                    name = logis.get_text()
                    print(name)
                    driver.set_page_load_timeout(20)
                    driver.set_script_timeout(20)
                    driver.maximize_window()
                    driver.get("https:"+href)
                    driver.save_screenshot("D:/" + name + ".jpg")
                except Exception as e:
                    logger.error(e)
                    driver.execute_script('window.stop()')
                    driver.save_screenshot("D:/" + "ddd" + ".jpg")
        driver.quit()
    except Exception as e:
        logger.error(e)
