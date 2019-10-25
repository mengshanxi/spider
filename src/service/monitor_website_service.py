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
        monitor_website = MonitorWebsite()
        monitor_website.website_name = website.website_name
        monitor_website.merchant_name = website.merchant_name
        monitor_website.merchant_num = website.merchant_num
        monitor_website.domain_name = website.domain_name
        monitor_website.saler = website.saler
        monitor_website.batch_num = batch_num
        monitor_website.kinds = "首页是否可打开"
        monitor_website.level = '高'
        monitor_website.access = '异常'
        monitor_website.is_normal = '异常'
        monitor_website.pageview = '-'
        if len(website.domain_name) == 0:
            logger.info("website_domain is None! merchant_name: %s ", website.merchant_name)
            monitor_website.outline = '商户网址为空。'
            monitor_website_dao.add(monitor_website)
            return
        else:
            logger.info("domain_name is %s! Go to inspect... ", website.domain_name)
        # 首页监控
        domain_names = str(website.domain_name)
        domain_name_list = domain_names.split(",")
        for domain_name in domain_name_list:
            logger.info("-------------------")
            domain_name_rich = domain_name
            if str(domain_name).startswith("http"):
                pass
            else:
                domain_name_rich = "http://" + domain_name
            try:
                resp = urlopen(domain_name_rich, timeout=10)
                code = resp.getcode()
                logger.info("code:  %s", code)
                if code == 200:
                    logger.info("使用webdriver进行截图:  %s ... ", domain_name_rich)
                    try:
                        driver = WebDriver.get_phantomjs()
                        driver.get(domain_name_rich)
                        current_url = driver.current_url
                        title = driver.title
                        source = driver.page_source
                        snapshot = SnapshotService.create_snapshot(driver, batch_num, website, '网站')
                        logger.info("title:  %s", title)
                        logger.info("current_url:  %s", current_url)
                        if str(current_url) == "about:blank" and str(
                                source) == "<html><head></head><body></body></html>" and str(title) == "":
                            logger.info("检测到about:blank :  %s", current_url)
                            monitor_website.outline = "网站疑似无法访问"
                            monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                            monitor_website_dao.add(monitor_website)
                            driver.quit()
                            continue
                        else:
                            pass
                        if str(current_url).index(domain_name_rich[7:]) == -1:
                            logger.info("疑似跳转...:  %s", current_url)
                            monitor_website.outline = "疑似跳转，检测到首页地址为:" + current_url
                            monitor_website.snapshot = snapshot
                            monitor_website_dao.add(monitor_website)
                            driver.quit()
                            continue
                        else:
                            pass
                        monitor_website.snapshot = snapshot
                        logger.info("check title和source...")
                        if title.__contains__('404'):
                            monitor_website.outline = "疑似异常，检测到404"
                        elif source.__contains__(
                                'ERR_NAME_NOT_RESOLVED'):
                            monitor_website.outline = "疑似异常，Title信息:" + title
                        elif source.__contains__(
                                'ERR_CONNECTION_REFUSED'):
                            monitor_website.outline = "疑似异常，检测到 ERR_CONNECTION_REFUSED"
                        elif source.__contains__(
                                'ERR_CONNECTION_TIMED_OUT'):
                            monitor_website.outline = "疑似异常，检测到 ERR_CONNECTION_TIMED_OUT"
                        elif source.__contains__(
                                'ERR_NAME_NOT_RESOLVED'):
                            monitor_website.outline = "疑似异常，检测到 ERR_NAME_NOT_RESOLVED"
                        elif source.__contains__(
                                'ERR_NAME_RESOLUTION_FAILED'):
                            monitor_website.outline = "疑似异常，检测到 ERR_NAME_RESOLUTION_FAILED"
                        elif source.__contains__(
                                'DNS_PROBE_FINISHED_NXDOMAIN'):
                            monitor_website.outline = "疑似异常，检测到 DNS_PROBE_FINISHED_NXDOMAIN"
                        elif source.__contains__(
                                'ERR_EMPTY_RESPONSE'):
                            monitor_website.outline = "疑似异常，检测到 ERR_EMPTY_RESPONSE"
                        elif source.__contains__(
                                '主机开设成功'):
                            monitor_website.outline = "疑似异常，检测到类似网站在建信息"
                        elif source.__contains__(
                                '非法阻断'):
                            monitor_website.outline = "疑似异常，检测到非法阻断"
                        elif source.__contains__(
                                'Bad Request'):
                            monitor_website.outline = "疑似异常，检测到 Bad Request"
                        elif source.__contains__(
                                '404 page not found'):
                            monitor_website.outline = "疑似异常，检测到 404 page not found"
                        elif source.__contains__(
                                'https://wanwang.aliyun.com/domain/parking'):
                            monitor_website.outline = "疑似异常，检测到阻断拦截"
                        elif source.__contains__('没有找到站点'):
                            monitor_website.outline = "疑似异常，没有找到站点"
                        elif source.__contains__(
                                '未备案提示'):
                            monitor_website.outline = "疑似异常，未备案提示"
                        elif str(source) == "<html><head></head><body></body></html>" and str(title) == "":
                            monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                            monitor_website.outline = "疑似无法访问"
                        else:
                            monitor_website.outline = '检测正常'
                            monitor_website.access = '正常'
                            monitor_website.is_normal = '正常'
                            monitor_website.level = '-'
                        logger.info("outline:  %s", monitor_website.outline)
                        monitor_website_dao.add(monitor_website)
                    except Exception as e:
                        logger.error(e)
                        monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                        monitor_website.outline = '访问超时，可能被目标网站屏蔽，建议手动验证！'
                        monitor_website_dao.add(monitor_website)
                    finally:
                        driver.quit()
                else:
                    logger.info("确定无法访问!")
                    monitor_website.outline = '检测到网站异常'
                    monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                    monitor_website_dao.add(monitor_website)
            except Exception as e:
                logger.error(e)
                logger.info("urlopen 无法打开页面..")
                monitor_website.outline = 'urlopen无法打开网站。'
                monitor_website.snapshot = SnapshotService.simulation_404(domain_name_rich)
                monitor_website_dao.add(monitor_website)
