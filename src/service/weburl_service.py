# -*- coding:utf-8 -*-
import time
from bs4 import BeautifulSoup

from config.mylog import logger
from dao.website_dao import WebsiteDao
from dao.weburl_dao import WeburlDao
from manager.ims_api import ImsApi
from model.models import Weburl
from service.strategy_service import StrategyService
from service.webdriver_util import WebDriver


class WeburlService:
    count = 0

    def gather_urls_by_website(self, website_id):
        ims_api = ImsApi()
        website_dao = WebsiteDao()
        if website_id is not None:
            website = website_dao.get_by_id(website_id)
            logger.info("gather url for website: %s  ", website)
            if len(website.domain_name) == 0 or website.domain_name is None:
                logger.info("gather url for %s,but website.domain_name is None,ignored! ", website.merchant_name)
            else:
                if str(website.domain_name).startswith('http'):
                    uri = website.domain_name
                    self.gather_urls(website.id, uri, website.website_name, website.domain_name,
                                     website.merchant_name,
                                     website.merchant_num, website.saler, 0)
                else:
                    uri = 'http://' + website.domain_name
                    self.gather_urls(website.id, uri, website.website_name, website.domain_name,
                                     website.merchant_name,
                                     website.merchant_num, website.saler, 0)
                ims_api.done_url_gather(website)

        else:
            websites = website_dao.get_overtime()
            logger.info("需要采集url的商户网站供 %s 个 ", websites.__len__())
            for website in websites:
                if len(website.domain_name) == 0 or website.domain_name is None:
                    logger.info("gather url for %s,but website.domain_name is None,ignored! ", website.merchant_name)
                else:
                    if str(website.domain_name).startswith('http'):
                        uri = website.domain_name
                        self.gather_urls(website.id, uri, website.website_name, website.domain_name,
                                         website.merchant_name,
                                         website.merchant_num, website.saler, 0)
                    else:
                        uri = 'http://' + website.domain_name
                        self.gather_urls(website.id, uri, website.website_name, website.domain_name,
                                         website.merchant_name,
                                         website.merchant_num, website.saler, 0)
                    ims_api.done_url_gather(website)

    def gather_urls(self, website_id, uri, website_name, domain_name, merchant_name, merchant_num, saler, level):
        strategy_service = StrategyService()
        strategy = strategy_service.get_strategy()
        frequency = strategy.frequency
        if strategy.frequency == 0 or strategy.frequency is None:
            logger.info("未设置爬取频率限制,继续执行任务..")
        else:
            logger.info("爬取频率限制为:%s 秒", strategy.frequency)
            time.sleep(frequency)
        if level == 1:
            logger.info("gather url just to 3 level: %s ", domain_name)
            return
        logger.info("gather url for website: %s ", uri)
        weburl_service = WeburlDao()
        try:
            driver = WebDriver.get_chrome_for_urlgather()
            driver.get(uri)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            for k in soup.find_all('a'):
                href = str(k.get('href'))
                logger.info("origin href: %s", href)
                if href.endswith(".jpg") or href.endswith(".jpeg") or href.endswith(".bmp") or href.endswith(
                        ".png") or href.endswith(
                    ".swf") or href == '/' or href == 'http://' or href == '#' or href.startswith(
                    'javascript') or href == 'None' or href.startswith('tencent://'):
                    continue
                elif href.startswith('http://') or href.startswith('https://'):
                    href = href
                elif href.startswith('/'):
                    href = uri + href
                elif href.startswith('./'):
                    href = uri + href[1:]
                else:
                    href = uri + "/" + href
                url = href.replace("//", "/").replace("/../", "/").replace(":/", "://")
                logger.info("href %s", href)
                logger.info("url %s", url)
                title = soup.find('title').string
                weburl = Weburl(website_id=website_id,
                                website_name=website_name,
                                merchant_name=merchant_name,
                                merchant_num=merchant_num,
                                saler=saler,
                                title=title,
                                type='page',
                                parent=uri,
                                url=href.replace("//", "/").replace("/../", "/").replace(":/", "://"))
                weburl_service.add(weburl)
                # self.gather_urls(website_id, href, website_name, domain_name, level + 1)
        except Exception as e:
            logger.error(e)
