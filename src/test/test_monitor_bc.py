import re
import time

from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from config.config_load import phantomjs_path
from dao.third_config_dao import ThirdConfigDao
from service.monitor_bc_service import MonitorBcService


class TestQichachaService(object):
    if __name__ == "__main__":
        service = MonitorBcService()
        # url = "https://www.qichacha.com/search?key=%E4%BA%AC%E4%B8%9C"
        # url = "https://www.qichacha.com/firm_cf2dcea7ed6c31269ccda79df6ba064a.html"

        # url = service.get_merchant_url(merchant_name='天津融宝支付网络有限公司')
        ##service.add_monitor_bc(merchant_name='天津融宝支付网络有限公司 ', url=url)
        # print("https://www.qichacha.com" + url)
        url = "/firm_877d32d9f838380236fd48630dcecea0.shtml"
        # if url != 'NONE':
        # service.parase_bc_module("https://www.qichacha.com" + url,
        #                          merchant_name="天津融宝支付网络有限公司 ")
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        third_config_dao = ThirdConfigDao
        cookie = third_config_dao.get("qichacha")
        headers = {
            'cookie': cookie}
        for key, value in headers.items():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(executable_path=phantomjs_path,
                                     desired_capabilities=desired_capabilities,
                                     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        driver.get("https://www.qichacha.com/firm_b40ecf6c3e7e4e0414c501f6ce53dd37.html#fengxian")
        time.sleep(10)
        driver.maximize_window()
        driver.save_screenshot("D://1.png")
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        cminfo = driver.find_element_by_xpath('//div[@class="company-nav-tab"]')[3]
        locations = cminfo.location
        sizes = cminfo.size
        rangle = (int(locations['x']), int(locations['y']), int(locations['x'] + sizes['width']),
                  int(locations['y'] + sizes['height']))
        img = Image.open("D://1.png")
        jpg = img.crop(rangle)
        jpg.save("D://2.png")

        print(legalmans.__len__() == 0)
        print(legalmans[0].get_text())

        cminfo = soup.find_all(name='section', id=re.compile('Cominfo'))
        tables = cminfo[0].find_all(name='table', class_='ntable')
        tds = tables[1].find_all(name='td')
        state = tds[5].get_text().strip()
        print(state)

        driver.get("https://www.qichacha.com" + url + "#fengxian")
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        companys = soup.find_all(name='div', class_='company-nav-tab')
        risks = companys[3].find_all(name='span')
        manage_abn = risks[2].get_text()
        serious_illegal = risks[4].get_text()
        print("经营异常:" + manage_abn)
        print("严重违法:" + serious_illegal)
