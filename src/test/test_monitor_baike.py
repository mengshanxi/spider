# coding=gbk
from src.config.mylog import logger
from src.dao.monitor_website_dao import MonitorWebsiteDao
from src.dao.website_dao import WebsiteDao
from src.service.monitor_baike_service import MonitorBaikeService
from src.service.monitor_website_service import MonitorWebsiteService
from src.service.weburl_service import UrlService


class TestEs(object):
    if __name__ == "__main__":
        # �ٿ�����
        test = '���Ӻ�ʳƷ�Ƽ�(����)���޹�˾'
        print(test.replace("(", "��").replace(")","��"))
        service = MonitorBaikeService()
        service.monitor_baike('���Ӻ�ʳƷ�Ƽ�(����)���޹�˾',27)
