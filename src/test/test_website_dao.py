import datetime
import time
import urllib

from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome import webdriver

from config.config_load import chromedriver_path, phantomjs_path
from config.mylog import logger
from service.inspect_task_service import InspectTaskService
from service.monitor_bc_service import MonitorBcService
from service.weburl_service import WeburlService

from selenium import webdriver


class TestMysql(object):
    if __name__ == "__main__":
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # driver = webdriver.Chrome(chrome_options=chrome_options,
        #                           executable_path=chromedriver_path)
        user_agent = (
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"
             )
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = user_agent
        # url = "https://www.qichacha.com/search?key=" + urllib.parse.quote("京东")
        url = "https://www.qichacha.com/"
        driver = webdriver.PhantomJS(executable_path=phantomjs_path,
                                     desired_capabilities=dcap,
                                     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])

        driver.set_window_size(1920, 1080)
    try:
        driver.get(url)
    except Exception as e:
        logger.error(e)
    driver.find_element_by_id("searchkey").send_keys("京东")
    driver.find_element_by_id("V3_Search_bt").click()
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')

    title = soup.find(name="title").get_text()
    logger.info("qichacha res title :%s", str(title))
    tbodys = soup.find_all(id="search-result")
    trs = tbodys[0].find_all('tr')
    tds = trs[0].find_all('td')
    a = tds[2].find_all('a')
    name = a[0].get_text().strip()
    print(name)
    # driver.set_page_load_timeout(10)
    # driver.set_script_timeout(10)
    # driver.maximize_window()
    # weburl_service = WeburlService()
    # weburl_service.gather_urls(1, "http://rczhiyun.com", "财新联合汽车租赁（北京）有限公司","rczhiyun.com", 0)
    # insepect_task_service =  InspectTaskService()
    # insepect_task_service.get_websites(34)
    # test='/usr/local/snapshots'
    # print(test[:10])
    # website_dao = WebsiteDao()
    # website = website_dao.get_by_name("威海紫光科技园有限公司")
    #  print(website.merchant_name)
    # spider_manager = GatherCenter()
    # spider_manager.gather('', '')
    # weburl = WeburlService()
    # weburl.gather_urls(website)
    # service = MonitorBcService()
    # batch_num = '1'
    # # url = service.get_merchant_url('1', merchant_name='威海紫光科技园有限公司')
    # url = '/firm_6d1f03aac2ffea7e98592821fe618a62.html'
    # if url is not None:
    #     try:
    #         service.inspect(str(batch_num), "https://www.qichacha.com" + url, '威海紫光科技园有限公司','')
    #         print()
    #     except Exception as e:
    #         pass
