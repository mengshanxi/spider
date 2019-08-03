# -*- coding:utf-8 -*-
import urllib.request

from bs4 import BeautifulSoup

from config.mylog import logger
from dao.website_dao import WebsiteDao
from dao.weburl_dao import WeburlDao
from model.models import Weburl
from service.inspect_service import InspectService


class WeburlService:

    def get_urls(website):
        urls = set()
        try:
            req = urllib.request.Request(website)
            web_page = urllib.request.urlopen(req, timeout=10)
            html = web_page.read()
            soup = BeautifulSoup(html, 'html.parser')  # 文档对象
            for k in soup.find_all('a'):
                # print(k)
                # print(k.get('class'))#查a标签的class属性
                # print(k.get('id'))#查a标签的id值
                # print(k.get('href'))#查a标签的href值
                # print(k.string)#查a标签的string
                href = str(k.get('href'))
                logger.info("gather url href:%s" % str(href))
                if href.endswith(".jpg") or href.endswith(".jpeg") or href.endswith(".bmp") or href.endswith(
                        ".png") or href.endswith(".swf") or href == '/' or href == 'http://':
                    continue
                if href.startswith('http://'):
                    urls.add(href)
                elif href.startswith('/'):
                    urls.add(website + href)
        except Exception as e:
            logger.error(e)
            return urls
        return urls

    def gather_urls_by_task(self, task_id):
        if task_id != 'NONE':
            inspect_service = InspectService()
            websites = inspect_service.get_websites(task_id)
            for website in websites:
                self.gather_urls(website)
        else:
            website_dao = WebsiteDao()
            websites = website_dao.get_all()
            for website in websites:
                self.gather_urls(website)

    def gather_urls(self, website):
        logger.info("gather url for website: %s ", website.website_name)
        weburl_service = WeburlDao()
        try:
            uri = 'http://' + website.domain_name
            req = urllib.request.Request(uri)
            web_page = urllib.request.urlopen(req, timeout=10)
            html = web_page.read()
            soup = BeautifulSoup(html, 'html.parser', from_encoding="gb18030")  # 文档对象
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

                title = soup.find('title').string
                weburl = Weburl()
                weburl.url = href
                weburl.website_id = website.id
                weburl.website_name = website.website_name
                weburl.title = title
                weburl.type = 'page'
                weburl_service.add(weburl)

            for k in soup.find_all('img'):
                src = str(k.get('src'))
                logger.info("origin src: %s", src)
                if src.endswith(".jpg") or src.endswith(".jpeg") or src.endswith(".bmp") or src.endswith(
                        ".png"):
                    if src.startswith('http://') or src.startswith('https://'):
                        pass
                    elif src.startswith('/'):
                        src = uri + src
                    else:
                        src = uri + "/" + src
                    weburl = Weburl()
                    weburl.url = src
                    weburl.website_id = website.id
                    weburl.website_name = website.website_name
                    weburl.title = soup.find('title').string
                    weburl.type = 'pic'
                    weburl_service.add(weburl)
                else:
                    pass
        except Exception as e:
            logger.error(e)
