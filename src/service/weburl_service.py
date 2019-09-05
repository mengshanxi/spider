# -*- coding:utf-8 -*-
import urllib.request

from bs4 import BeautifulSoup

from config.mylog import logger
from dao.website_dao import WebsiteDao
from dao.weburl_dao import WeburlDao
from manager.ims_api import ImsApi
from model.models import Weburl
from service.inspect_task_service import InspectTaskService


class WeburlService:
    count = 0

    def gather_urls_by_task(self, task_id):
        ims_api = ImsApi()
        if task_id is not None:
            inspect_service = InspectTaskService()
            websites = inspect_service.get_websites(task_id)
            for website in websites:
                uri = 'http://' + website.domain_name
                self.gather_urls(website.id, uri, website.website_name, website.domain_name, website.merchant_name,
                                 website.merchant_num, 0)
                ims_api.done_url_gather(website)
        else:
            website_dao = WebsiteDao()
            websites = website_dao.get_overtime()
            for website in websites:
                uri = 'http://' + website.domain_name
                self.gather_urls(website.id, uri, website.website_name, website.domain_name, website.merchant_name,
                                 website.merchant_num, 0)
                ims_api.done_url_gather(website)

    def gather_urls(self, website_id, uri, website_name, domain_name, merchant_name, merchant_num, level):
        if level == 1:
            logger.info("gather url just to 3 level: %s ", domain_name)
            return
        logger.info("gather url for website: %s ", domain_name)
        weburl_service = WeburlDao()
        try:
            req = urllib.request.Request(uri)
            web_page = urllib.request.urlopen(req, timeout=10)
            html = web_page.read()
            soup = BeautifulSoup(html, 'html.parser', from_encoding="gb18030")
            # 不做图片的处理
            # for k in soup.find_all('img'):
            #     src = str(k.get('src'))
            #     logger.info("origin src: %s", src)
            #     if src.endswith(".jpg") or src.endswith(".jpeg") or src.endswith(".bmp") or src.endswith(
            #             ".png"):
            #         if src.startswith('http://') or src.startswith('https://'):
            #             pass
            #         elif src.startswith('/'):
            #             src = "http://" + domain_name + src
            #         else:
            #             src = uri + "/" + src
            #         weburl = Weburl(url=src.replace("//", "/").replace("/../", "/"),
            #                         website_id=website_id,
            #                         website_name=website_name,
            #                         title=soup.find('title').string,
            #                         type='pic',
            #                         parent=uri)
            #         weburl_service.add(weburl)
            #     else:
            #         pass
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
                    href = "http://" + domain_name + href
                elif href.startswith('./'):
                    href = uri + href[1:]
                else:
                    href = uri + "/" + href

                title = soup.find('title').string
                weburl = Weburl(website_id=website_id,
                                website_name=website_name,
                                merchant_name=merchant_name,
                                merchant_num=merchant_num,
                                title=title,
                                type='page',
                                parent=uri,
                                url=href.replace("//", "/").replace("/../", "/"))
                weburl_service.add(weburl)
                # self.gather_urls(website_id, href, website_name, domain_name, level + 1)

        except Exception as e:
            logger.error(e)
