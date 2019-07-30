# coding=gbk
from src.config.mylog import logger
from src.dao.monitor_website_dao import MonitorWebsiteDao
from src.dao.website_dao import WebsiteDao
from src.service.monitor_baike_service import MonitorBaikeService
from src.service.monitor_website_service import MonitorWebsiteService
from src.service.weburl_service import UrlService


class TestEs(object):
    if __name__ == "__main__":
        # 百科舆情
        test = '中视好食品科技(北京)有限公司'
        print(test.replace("(", "（").replace(")","）"))
        service = MonitorBaikeService()
        service.monitor_baike('中视好食品科技(北京)有限公司',27)
