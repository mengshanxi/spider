import json
import urllib

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from dao.db import session
from model.models import TaskItem
from service.monitor_tracking_service import MonitorTrackingService
from service.task_pool_service import TaskPoolService

#https://www.xicidaili.com/nt/
class TestMysql(object):
    if __name__ == "__main__":
        chrome_options = Options()
        chrome_options.add_argument("--proxy-server=https://115.200.251.158:8118")
        # 禁止图片和css加载
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME,
                                  options=chrome_options)

        driver.set_page_load_timeout(30)
        driver.set_script_timeout(10)
        driver.maximize_window()
        driver.get("https://www.qichacha.com/firm_b40ecf6c3e7e4e0414c501f6ce53dd37.html#fengxian")
        driver.save_screenshot("D:/cc.jpg")
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        # req = urllib.request.Request("http://www.melaleuca.com.cn", headers=headers )
        # web_page = urllib.request.urlopen(req, timeout=10)
        # html = web_page.read()
        # soup = BeautifulSoup(html, 'html.parser', from_encoding="gb18030")
        # for k in soup.find_all('a'):
        #     href = str(k.get('href'))
        #     print(href)
        # task_pools = session.query(TaskItem).filter(TaskItem.batch_num == '11').filter(
        #     TaskItem.status == 'pending')
        # if task_pools is None:
        #     print()
        # task_pool_service = TaskPoolService()
        # entity, task_pool = task_pool_service.get_pending_task("11111")
        # if entity is None:
        #     print()
        # check_item = json.loads(task_pool.check_item)
        # if task_pool.type == "weburl" and check_item["websiteIsBadwords"] is 1:
        #     print()
        # elif task_pool.type == "website":
        #     if check_item["websiteIsForward"] is 1 or check_item["websiteIsOpen"] is 1:
        #         # 网站监控
        #         print()
        #     else:
        #         print()

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
