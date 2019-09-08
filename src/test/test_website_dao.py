from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver

from dao.monitor_website_dao import MonitorWebsiteDao
from model.models import Website, MonitorWebsite
from service.accessible_service import AccessibleService
from service.snapshot_service import SnapshotService
from service.traffic_service import TrafficService


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
        # dcap["phantomjs.page.settings.userAgent"] = user_agent
        # url = "https://www.qichacha.com/search?key=" + urllib.parse.quote("京东")
        url = "https://www.baidu.com/"
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)
        website = Website(website_name='',domain_name='hauxidyy.cn',merchant_name='内蒙古宇航人高技术产业有限责任公司')
        batch_num = '1'
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.maximize_window()
        monitor_website_dao = MonitorWebsiteDao
        service = TrafficService()
        access = AccessibleService()

        domain_names = str(website.domain_name)
        domain_name_list = domain_names.split(",")
        for domain_name in domain_name_list:
            try:
                #  截图
                monitor_website = MonitorWebsite()
                monitor_website.website_name = website.website_name
                monitor_website.merchant_name = website.merchant_name
                monitor_website.merchant_num = website.merchant_num
                monitor_website.saler = website.saler
                monitor_website.domain_name = domain_name
                monitor_website.batch_num = batch_num
                monitor_website.kinds = "首页是否可打开"
                monitor_website.level = '-'
                monitor_website.snapshot = ""
                domain_name_rich = None
                if domain_name_rich is not None:
                    print(domain_name_rich)
                else:
                    monitor_website.access = '异常'
                    monitor_website.is_normal = '异常'
                    monitor_website.outline = '首页访问检测到异常'
                    monitor_website.level = '高'
                    monitor_website.pageview = '-'
                    monitor_website.snapshot = SnapshotService.simulation_404(domain_name)
                    monitor_website.batch_num = batch_num
            except Exception as e:
                print(e)
            finally:
                driver.quit()

    # driver.find_element_by_id("searchkey").send_keys("京东")
    # driver.find_element_by_id("V3_Search_bt").click()
    # source = driver.page_source
    # soup = BeautifulSoup(source, 'html.parser')

    # title = soup.find(name="title").get_text()
    # logger.info("qichacha res title :%s", str(title))
    # tbodys = soup.find_all(id="search-result")
    # trs = tbodys[0].find_all('tr')
    # tds = trs[0].find_all('td')
    # a = tds[2].find_all('a')
    # name = a[0].get_text().strip()
    # print(name)
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
