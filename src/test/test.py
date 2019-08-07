import datetime
import time
import urllib

from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome import webdriver
import os
from config.config_load import chromedriver_path, phantomjs_path
from config.mylog import logger
from service.inspect_task_service import InspectTaskService
from service.monitor_bc_service import MonitorBcService
from service.webdriver_util import WebDriver
from service.weburl_service import WeburlService


class TestMysql(object):
    if __name__ == "__main__":
        os.environ['browser'] = "172.17.161.230"
        os.environ['port'] = '8912'
        # monitor_bc_service = MonitorBcService
        # monitor_bc_service.get_merchant_url("1",'北京京东世纪贸易有限公司')
        service = MonitorBcService()
        url = service.get_merchant_url(str(1), merchant_name='深圳市腾讯计算机系统有限公司')
        url='https://www.qichacha.com/firm_f1c5372005e04ba99175d5fd3db7b8fc.html'
        logger.info("get qichacha url  : %s", str(url))
        if url is not None:
            try:
                service.inspect(str(1), url, '北京京东世纪贸易有限公司',
                                '刘强东')
            except Exception as e:
                logger.info(e)
                pass
        logger.info("qichacha monitor  done!merchantName : %s", '北京京东世纪贸易有限公司')
