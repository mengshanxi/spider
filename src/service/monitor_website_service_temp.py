# -*- coding:utf-8 -*-
from urllib.request import urlopen

from config.mylog import logger
from dao.monitor_website_dao import MonitorWebsiteDao
from model.models import MonitorWebsite
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver


class MonitorWebsiteService:
    @staticmethod
    def monitor_website(website, batch_num):
        monitor_website_dao = MonitorWebsiteDao
        if len(website.domain_name) == 0:
            logger.info("website_domain is None! merchant_name: %s ", website.merchant_name)
            monitor_website = MonitorWebsite()
            monitor_website.website_name = website.website_name
            monitor_website.merchant_name = website.merchant_name
            monitor_website.merchant_num = website.merchant_num
            monitor_website.domain_name = website.domain_name
            monitor_website.saler = website.saler
            monitor_website.batch_num = batch_num
            monitor_website.kinds = "首页是否可打开"
            monitor_website.level = '-'
            monitor_website.access = '异常'
            monitor_website.is_normal = '异常'
            monitor_website.outline = '商户网址为空。'
            monitor_website.level = '-'
            monitor_website.pageview = '-'
            monitor_website_dao.add(monitor_website)
            return
        else:
            logger.info("domain_name is %s! Go to inspect... ", website.domain_name)
        # 首页监控
        domain_names = str(website.domain_name)
        domain_name_list = domain_names.split(",")
        for domain_name in domain_name_list:
            logger.info("-------------------")
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
            monitor_website.access = '正常'
            monitor_website.is_normal = '正常'
            monitor_website.level = '-'
            monitor_website.batch_num = batch_num
            monitor_website.pageview = "-"
            domain_name_rich = domain_name
            if str(domain_name).startswith("http"):
                pass
            else:
                domain_name_rich = "http://" + domain_name
            try:
                driver = WebDriver.get_phantomjs()
                driver.get(domain_name_rich)
                current_url = driver.current_url
                if len(str(current_url)) - len(str(domain_name_rich)) <= 2:
                    pass
                else:
                    monitor_website.access = '异常'
                    monitor_website.is_normal = '异常'
                    monitor_website.outline = "疑似跳转，检测到首页地址为:" + current_url
                    monitor_website.level = '高'
                    monitor_website_dao.add(monitor_website)
                title = driver.title
                source = driver.page_source
                snapshot = SnapshotService.create_snapshot(driver, batch_num, website, '网站')
                monitor_website.snapshot = snapshot
                if title.__contains__('404') or source.__contains__(
                        'ERR_NAME_NOT_RESOLVED') or source.__contains__(
                    'ERR_CONNECTION_REFUSED') or source.__contains__(
                    'ERR_CONNECTION_TIMED_OUT') or source.__contains__(
                    'ERR_NAME_NOT_RESOLVED') or source.__contains__(
                    'ERR_NAME_RESOLUTION_FAILED') or source.__contains__(
                    'DNS_PROBE_FINISHED_NXDOMAIN') or source.__contains__(
                    'ERR_EMPTY_RESPONSE') or source.__contains__(
                    '主机开设成功') or source.__contains__(
                    '非法阻断') or source.__contains__(
                    'Bad Request') or source.__contains__(
                    '404 page not found') or source.__contains__(
                    'https://wanwang.aliyun.com/domain/parking') or source.__contains__(
                    '没有找到站点') or source.__contains__(
                    '未备案提示'):
                    monitor_website.access = '异常'
                    monitor_website.is_normal = '异常'
                    monitor_website.outline = "疑似异常，Title信息:" + title
                    monitor_website.level = '高'
                    monitor_website_dao.add(monitor_website)
                else:
                    monitor_website_dao.add(monitor_website)
            except Exception as e:
                logger.error(e)
                # 重试
                try:
                    resp = urlopen(domain_name_rich, timeout=10)
                    code = resp.getcode()
                    if code == 200:
                        driver.set_page_load_timeout(180)
                        driver.set_script_timeout(180)
                        driver.get(domain_name_rich)
                        title = driver.title
                        snapshot = SnapshotService.create_snapshot(driver, batch_num, website, '网站')
                        monitor_website.snapshot = snapshot
                        if title.__contains__('404') or source.__contains__(
                                'ERR_NAME_NOT_RESOLVED') or source.__contains__(
                            'ERR_CONNECTION_REFUSED') or source.__contains__(
                            'ERR_CONNECTION_TIMED_OUT') or source.__contains__(
                            'ERR_NAME_NOT_RESOLVED') or source.__contains__(
                            'ERR_NAME_RESOLUTION_FAILED') or source.__contains__(
                            'DNS_PROBE_FINISHED_NXDOMAIN') or source.__contains__(
                            'ERR_EMPTY_RESPONSE') or source.__contains__(
                            '主机开设成功') or source.__contains__(
                            '非法阻断') or source.__contains__(
                            'Bad Request') or source.__contains__(
                            '404 page not found') or source.__contains__(
                            'https://wanwang.aliyun.com/domain/parking') or source.__contains__(
                            '没有找到站点') or source.__contains__(
                            '未备案提示'):
                            monitor_website.access = '异常'
                            monitor_website.is_normal = '异常'
                            monitor_website.outline = "疑似异常，Title信息:" + title
                            monitor_website.level = '高'
                            monitor_website_dao.add(monitor_website)
                        else:
                            monitor_website_dao.add(monitor_website)
                    else:
                        monitor_website.outline = '检测到网站异常'
                        monitor_website.access = '异常'
                        monitor_website.is_normal = '异常'
                        monitor_website.level = '高'
                        monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                        monitor_website_dao.add(monitor_website)
                except Exception as e:
                    logger.error(e)
                    monitor_website.outline = '检测到网站异常'
                    monitor_website.access = '异常'
                    monitor_website.is_normal = '异常'
                    monitor_website.level = '高'
                    monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                    monitor_website_dao.add(monitor_website)
            finally:
                driver.quit()
