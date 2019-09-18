import json

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from dao.db import session
from model.models import TaskItem
from service.monitor_tracking_service import MonitorTrackingService
from service.task_pool_service import TaskPoolService


class TestMysql(object):
    if __name__ == "__main__":
        task_pools = session.query(TaskItem).filter(TaskItem.batch_num == '11').filter(
            TaskItem.status == 'pending')
        if task_pools is None:
            print()
        #task_pool_service = TaskPoolService()
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
