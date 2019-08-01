from dao.website_dao import WebsiteDao
from manager.gather_center import GatherCenter
from service.monitor_bc_service import MonitorBcService
from service.weburl_service import WeburlService


class TestMysql(object):
    if __name__ == "__main__":
        # test='/usr/local/snapshots'
        # print(test[:10])
        # website_dao = WebsiteDao()
        # website = website_dao.get_by_name("威海紫光科技园有限公司")
        #  print(website.merchant_name)
        # spider_manager = GatherCenter()
        # spider_manager.gather('', '')
        # weburl = WeburlService()
        # weburl.gather_urls(website)
        service = MonitorBcService()
        batch_num = '1'
        # url = service.get_merchant_url('1', merchant_name='威海紫光科技园有限公司')
        url = '/firm_6d1f03aac2ffea7e98592821fe618a62.html'
        if url is not None:
            try:
                service.inspect(str(batch_num), "https://www.qichacha.com" + url, '威海紫光科技园有限公司','')
                print()
            except Exception as e:
                pass
