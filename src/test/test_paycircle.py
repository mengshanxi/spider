import time
import urllib

from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config.mylog import logger


class TestMysql(object):
    if __name__ == "__main__":
        url = "http://www.paycircle.cn/company/search.php?kw=" + urllib.parse.quote('京东') + "&c=SearchList&"
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
    try:
        driver.get(url)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        div_list = soup.find_all(attrs={'class': 'list'})
        if div_list.__len__() > 0:
            news = div_list[0].find_all('tr')
            for new in news:
                href = new.find_all('td')[2].find_all('a')[0].get("href")
                content = new.find_all('td')[2].find_all('li')[1].get_text()
        else:
            logger.info("支付圈没有搜索到数据")
        driver.quit()
    except Exception as e:
        logger.error(e)
