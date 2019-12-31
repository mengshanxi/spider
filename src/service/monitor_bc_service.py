import json
from urllib import parse, request

from config.config_load import ims_rest_base
from config.mylog import logger
from dao.monitor_bc_dao import MonitorBcDao
from model.models import MonitorBc
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver

"""
企查查监控服务
url = "https://www.qichacha.com/company_getinfos?unique="+url[30:62]+"&companyname="+urllib.parse.quote(merchant_name)+"&tab=fengxian"
"""


class MonitorBcService:

    @staticmethod
    def inspect(batch_num, url, website, task_id):
        monitor_bc_dao = MonitorBcDao()
        monitor_bc = MonitorBc()
        monitor_bc.batch_num = batch_num
        monitor_bc.domain_name = website.domain_name
        monitor_bc.merchant_num = website.merchant_num
        monitor_bc.website_name = website.website_name
        monitor_bc.merchant_name = website.merchant_name
        monitor_bc.saler = website.saler
        monitor_bc.is_normal = '正常'
        monitor_bc.kinds = '工商巡检'
        monitor_bc.outline = '企业工商信息检查正常'
        monitor_bc.level = '-'
        url = ims_rest_base + "open/api/v1/agent/monitor_bc"
        data_json = {"merchantNum": website.merchant_num, "merchantName": website.merchant_name, "taskId": task_id,
                     "batchNum": batch_num}
        data = bytes(parse.urlencode(data_json), encoding="utf8")
        new_url = request.Request(url, data)
        res = request.urlopen(new_url).read().decode('utf-8')
        bc_response = json.loads(res)
        if bc_response['status'] == "正常":
            monitor_bc.status = bc_response['businessInfo']['enterpriseBase']['entStatus']
            logger.info("企业工商信息检测正常：%s", website.merchant_name)
        elif bc_response['status'] == "无法获取":
            logger.info("企业工商信息检测无法获取：%s", website.merchant_name)
            monitor_bc.is_normal = '无法获取'
            monitor_bc.outline = '企业工商信息无法获取,跳过巡检。'
        else:
            logger.info("企业工商信息检测异常：%s", website.merchant_name)
            monitor_bc.is_normal = '异常'
            monitor_bc.kinds = '企业工商信息'
            monitor_bc.outline = bc_response['msg']
            monitor_bc.status = bc_response['businessInfo']['enterpriseBase']['entStatus']
            monitor_bc.level = '高'
        url = ims_rest_base + "views/system/enterprise.jsp?merchantNum=" + website.merchant_num
        driver = WebDriver.get_phantomjs()
        try:
            logger.info("企业工商信息截图：%s", website.merchant_name)
            driver.get(url)
            snapshot = SnapshotService.create_snapshot(driver, batch_num, website, "工商巡检")
            monitor_bc.snapshot = snapshot
            monitor_bc_dao.add(monitor_bc)
        except Exception as e:
            print(e)
            monitor_bc_dao.add(monitor_bc)
        finally:
            driver.quit()

    @staticmethod
    def get_merchant_url(batch_num, website):
        return "URL"
