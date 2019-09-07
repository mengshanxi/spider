# -*- coding:utf-8 -*-

from config.mylog import logger
from dao.monitor_website_dao import MonitorWebsiteDao
from model.models import MonitorWebsite
from service.accessible_service import AccessibleService
from service.snapshot_service import SnapshotService
from service.traffic_service import TrafficService
from service.webdriver_util import WebDriver


class MonitorWebsiteService:
    @staticmethod
    def monitor_website(website, batch_num):
        #   首页监控
        driver = WebDriver.get_chrome()
        monitor_website_dao = MonitorWebsiteDao
        service = TrafficService()
        access = AccessibleService()

        domain_names = str(website.domain_name)
        domain_name_list = domain_names.split(",")
        for domain_name in domain_name_list:
            try:
                logger.info("check whether website available,domain_name : %s", website.domain_name)
                #  截图
                monitor_website = MonitorWebsite()
                monitor_website.website_name = website.website_name
                monitor_website.merchant_name = website.merchant_name
                monitor_website.merchant_num = website.merchant_num
                monitor_website.saler = website.saler
                monitor_website.domain_name = domain_name
                monitor_website.batch_num = batch_num
                monitor_website.kinds = "首页是否可打开"
                monitor_website.level = 0
                monitor_website.snapshot = ""
                domain_name_rich, current_url = access.get_access_res(domain_name)
                logger.info("domain_name: %s", domain_name)
                logger.info("domain_name_rich: %s", domain_name_rich)
                if domain_name_rich is not None:
                    logger.info("domain : %s", str(domain_name_rich))
                    monitor_website.access = '正常'
                    monitor_website.is_normal = '正常'
                    monitor_website.outline = '正常'
                    monitor_website.level = 0
                    pageview = service.get_traffic(domain_name=domain_name_rich)
                    monitor_website.pageview = pageview.reach_rank[0]
                    try:
                        driver.get(domain_name_rich)
                        title = driver.title
                        snapshot = SnapshotService.create_snapshot(driver, batch_num, website.merchant_name,
                                                                   website.merchant_num, '网站')
                        monitor_website.snapshot = snapshot
                        if title == '没有找到站点' or title == '未备案提示':
                            monitor_website.access = '异常'
                            monitor_website.is_normal = '异常'
                            monitor_website.outline = title
                            monitor_website.level = 3
                            monitor_website.pageview = '-'
                            monitor_website.batch_num = batch_num
                        monitor_website_dao.add(monitor_website)
                    except Exception as e:
                        logger.info(e)
                        monitor_website.access = '异常'
                        monitor_website.is_normal = '异常'
                        monitor_website.outline = '首页访问检测到异常'
                        monitor_website.level = 3
                        monitor_website.pageview = '-'
                        monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                        monitor_website.batch_num = batch_num
                        monitor_website_dao.add(monitor_website)
                else:
                    logger.info("domain_name: %s", domain_name)
                    monitor_website.access = '异常'
                    monitor_website.is_normal = '异常'
                    monitor_website.outline = '首页访问检测到异常'
                    monitor_website.level = 3
                    monitor_website.pageview = '-'
                    monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                    monitor_website.batch_num = batch_num
                    monitor_website_dao.add(monitor_website)
                    logger.info("website is not available : %s return!", domain_name)
                    return
            except Exception as e:
                logger.info("check whether website available : %s ,there is exception", domain_name)
                logger.info(e)
            finally:
                driver.quit()
