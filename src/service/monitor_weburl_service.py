# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup

from config.mylog import logger
from dao.keyword_dao import KeywordDao
from dao.monitor_weburl_dao import MonitorWeburlDao
from model.models import MonitorUrl
from service.accessible_service import AccessibleService
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver


class MonitorWeburlService:
    @staticmethod
    def monitor_website(weburl, batch_num):
        # 內容监控
        keyword_dao = KeywordDao()
        keywords = keyword_dao.get_all()
        access = AccessibleService()

        monitor_weburl_dao = MonitorWeburlDao()
        monitor_weburl = MonitorUrl()
        monitor_weburl.website_name = weburl.website_name
        monitor_weburl.domain_name = weburl.domain_name
        monitor_weburl.url = weburl.url
        monitor_weburl.batch_num = batch_num
        monitor_weburl.title = weburl.title
        # 监测死链接
        reachable, current_url = access.get_access_res(weburl.url)
        use_proxy = False
        if reachable is None:
            logger.info("使用代理重试访问： %s", weburl.url)
            reachable, current_url = access.get_proxy_access_res(weburl.url)
        else:
            use_proxy = True
            logger.info("使用代理可以访问: %s", weburl.url)
        if reachable is None:
            logger.info("检测到误404 : %s", weburl.url)
            monitor_weburl.outline = '检测到误404'
            monitor_weburl.is_normal = '异常'
            monitor_weburl.level = '高'
            monitor_weburl.snapshot = ''
            monitor_weburl.kinds = '死链接'
            monitor_weburl_dao.add(monitor_weburl)
            return
            #  截图
        if use_proxy:
            driver = WebDriver.get_proxy_chrome()
        else:
            driver = WebDriver.get_chrome()
        try:
            driver.get(weburl.url)
            snapshot = SnapshotService.snapshot_weburl(driver, batch_num, weburl, '网站内容')
            print(snapshot)
            print(monitor_weburl)
            monitor_weburl.outline = '网页打开正常'
            monitor_weburl.is_normal = '正常'
            monitor_weburl.level = '-'
            monitor_weburl.snapshot = snapshot
            monitor_weburl.kinds = '是否能打开'
            monitor_weburl_dao.add(monitor_weburl)

            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            # 监测页面敏感词
            for keyword in keywords:
                index = soup.find(keyword.name)
                if index is not None:
                    logger.info("senti url alert,there is : %s", str(keyword.name))
                    monitor_weburl.outline = '检测到敏感词:' + str(keyword.name)
                    monitor_weburl.is_normal = '异常'
                    monitor_weburl.level = '低'
                    monitor_weburl.snapshot = snapshot
                    monitor_weburl.kinds = '命中敏感词'

                    monitor_weburl_dao.add(monitor_weburl)
            # 监测 非金融平台包含充值、提现、钱包功能
            illegal_fun = soup.find("充值")
            if illegal_fun is not None:
                logger.info("senti url alert,there is : %s", str("充值"))
                monitor_weburl.outline = '检测到包含充值、提现、钱包功能'
                monitor_weburl.is_normal = '异常'
                monitor_weburl.level = '低'
                monitor_weburl.snapshot = snapshot
                monitor_weburl.kinds = '非法功能'

                monitor_weburl_dao.add(monitor_weburl)
            # 监测 误导宣传
            mislead1 = soup.find("融宝资金担保")
            mislead2 = soup.find("融宝托管")
            if mislead1 is not None or mislead2 is not None:
                monitor_weburl.outline = '检测到误导宣传'
                monitor_weburl.is_normal = '异常'
                monitor_weburl.level = '中'
                monitor_weburl.snapshot = snapshot
                monitor_weburl.kinds = '误导宣传'

                monitor_weburl_dao.add(monitor_weburl)
        except Exception as e:
            logger.error(e)
            return
        finally:
            driver.quit()
