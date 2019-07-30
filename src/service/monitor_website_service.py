# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup

from src.config.mylog import logger
from src.dao.keyword_dao import KeywordDao
from src.dao.monitor_website_dao import MonitorWebsiteDao
from src.dao.monitor_weburl_dao import MonitorWeburlDao
from src.model.monitor_website import MonitorWebsite
from src.model.monitor_weburl import MonitorWeburl
from src.service.accessible_service import AccessibleService
from src.service.snapshot_service import SnapshotService
from src.service.traffic_service import TrafficService
from src.service.webdriver_util import WebDriver
from src.service.weburl_service import UrlService
import src.util.globalvar as gl
from src.service.pic_recg_service import PicRecgService


class MonitorWebsiteService:
    @staticmethod
    def monitor_website(website, batch_num):
        #   首页监控
        website_dao = MonitorWebsiteDao
        service = TrafficService()
        access = AccessibleService()

        domain_names = str(website["domainName"])
        domain_name_list = domain_names.split(",")
        for domain_name in domain_name_list:
            try:
                logger.info("check whether website available : %s", website["websiteName"])
                #  截图
                monitor_website = MonitorWebsite()
                monitor_website.website_name = website["websiteName"]
                monitor_website.merchant_name = website["merchantName"]
                monitor_website.domain_name = domain_name
                monitor_website.batch_num = batch_num
                monitor_website.kinds = "首页是否可打开"
                monitor_website.level = 0
                monitor_website.snapshot = ""
                domain_name_rich = access.get_access_res(domain_name)
                logger.info("domain_name: %s", domain_name)
                logger.info("domain_name_rich: %s", domain_name_rich)
                driver = WebDriver.get_phantomJS()
                if domain_name_rich is not None:
                    logger.info("2: %s", domain_name_rich)
                    logger.info("domain : %s", str(domain_name_rich))
                    monitor_website.access = '正常'
                    monitor_website.is_normal = '正常'
                    monitor_website.outline = '正常'
                    monitor_website.level = 0
                    pageview = service.get_traffic(domain_name=domain_name_rich)
                    monitor_website.pageview = pageview.reach_rank[0]
                    try:
                        driver.get(domain_name_rich)
                        snapshot = SnapshotService.create_snapshot(driver)
                        monitor_website.snapshot = snapshot
                        website_dao.add(monitor_website, batch_num)
                    except Exception as e:
                        logger.info(e)
                        monitor_website.access = '异常'
                        monitor_website.is_normal = '异常'
                        monitor_website.outline = '首页访问检测到异常'
                        monitor_website.level = 3
                        monitor_website.pageview = '-'
                        monitor_website.snapshot = SnapshotService.simulation_404()
                        website_dao.add(monitor_website, batch_num)
                    driver.quit()
                else:
                    logger.info("domain_name: %s", domain_name)
                    monitor_website.access = '异常'
                    monitor_website.is_normal = '异常'
                    monitor_website.outline = '首页访问检测到异常'
                    monitor_website.level = 3
                    monitor_website.pageview = '-'
                    monitor_website.snapshot = SnapshotService.simulation_404()
                    website_dao.add(monitor_website, batch_num)
                    logger.info("website is not available : %s return!", domain_name)
                    driver.quit()
                    return
            except Exception as e:
                driver.quit()
                logger.info("check whether website available : %s ,there is exception", domain_name)
                logger.info(e)
                return

            # 內容监控
            keyword_dao = KeywordDao()
            keywords = keyword_dao.get_keywords()

            monitor_weburl_dao = MonitorWeburlDao()

            url_service = UrlService()
            website["domainName"] = domain_name_rich
            weburls = url_service.gather_urls(website)
            """
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=chrome_options,
                                      executable_path=chromedriver_path)

            """
            if weburls is None:
                return
            driver = WebDriver.get_phantomJS()
            if weburls.__len__() > 2:
                del weburls[2:]
            for weburl in weburls:
                if not gl.check_by_batch_num(batch_num):
                    break

                url = weburl.url
                if url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".bmp") or url.endswith(
                        ".png"):
                    src = SnapshotService.download(url)
                    pic_service = PicRecgService()
                    text = pic_service.tran2text(src)
                    logger.info("pic 2 text,text: %s", text)
                    if text is not None:
                        logger.info("text is not None,url: %s", url)
                        try:
                            for keyword in keywords:
                                index = text.find(keyword.name)
                                if index is not -1:
                                    logger.info("senti url alert,there is : %s", str(keyword.name))
                                    monitor_weburl = MonitorWeburl()
                                    monitor_weburl.website_name = website["websiteName"]
                                    monitor_weburl.outline = "[" + weburl.url + '] 图片检测到敏感词:' + str(keyword.name)
                                    monitor_weburl.is_normal = '异常'
                                    monitor_weburl.url = url
                                    monitor_weburl.level = 2
                                    monitor_weburl.snapshot = ""
                                    monitor_weburl.kinds = '异常图片'
                                    monitor_weburl.batch_num = batch_num
                                    monitor_weburl.title = weburl.title

                                    monitor_weburl_dao.add(monitor_weburl)
                        except Exception as e:
                            logger.error(e)
                else:
                    logger.info("check url : %s", weburl.url)

                    monitor_weburl = MonitorWeburl()
                    monitor_weburl.website_name = website["websiteName"]
                    monitor_weburl.url = weburl.url
                    monitor_weburl.batch_num = batch_num
                    monitor_weburl.title = weburl.title

                    # 监测死链接
                    reachable = access.get_access_res(weburl.url)
                    logger.info("rtn url : %s", str(reachable))
                    #  截图
                    snapshot = SnapshotService.create_snapshot(driver)

                    if reachable is None:
                        monitor_weburl.outline = '检测到误404'
                        monitor_weburl.is_normal = '异常'
                        monitor_weburl.level = 2
                        monitor_weburl.snapshot = ''
                        monitor_weburl.kinds = '死链接'
                        monitor_weburl_dao.add(monitor_weburl)
                        continue
                    else:
                        monitor_weburl.outline = '网页打开正常'
                        monitor_weburl.is_normal = '正常'
                        monitor_weburl.level = 0
                        monitor_weburl.snapshot = snapshot
                        monitor_weburl.kinds = '是否能打开'
                        monitor_weburl_dao.add(monitor_weburl)

                    try:
                        driver.get(weburl.url)
                    except Exception as e:
                        logger.error(e)
                        continue
                    source = driver.page_source
                    soup = BeautifulSoup(source, 'html.parser')

                    # 监测页面敏感词
                    for keyword in keywords:
                        index = soup.find(keyword.name)
                        if index is not None:
                            logger.info("senti url alert,there is : %s", str(keyword.name))
                            monitor_weburl.outline = '检测到敏感词:' + str(keyword.name)
                            monitor_weburl.is_normal = '异常'
                            monitor_weburl.level = 2
                            monitor_weburl.snapshot = snapshot
                            monitor_weburl.kinds = '命中敏感词'

                            monitor_weburl_dao.add(monitor_weburl)
                    # 监测 非金融平台包含充值、提现、钱包功能
                    illegal_fun = soup.find("充值")
                    if illegal_fun is not None:
                        logger.info("senti url alert,there is : %s", str("充值"))
                        monitor_weburl.outline = '检测到包含充值、提现、钱包功能'
                        monitor_weburl.is_normal = '异常'
                        monitor_weburl.level = 2
                        monitor_weburl.snapshot = snapshot
                        monitor_weburl.kinds = '非法功能'

                        monitor_weburl_dao.add(monitor_weburl)
                    # 监测 误导宣传
                    mislead1 = soup.find("融宝资金担保")
                    mislead2 = soup.find("融宝托管")
                    if mislead1 is not None or mislead2 is not None:
                        monitor_weburl.outline = '检测到误导宣传'
                        monitor_weburl.is_normal = '异常'
                        monitor_weburl.level = 2
                        monitor_weburl.snapshot = snapshot
                        monitor_weburl.kinds = '误导宣传'

                        monitor_weburl_dao.add(monitor_weburl)
            # 关闭浏览器
            driver.quit()
