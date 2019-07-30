# -*- coding:utf-8 -*-
import urllib.request

from bs4 import BeautifulSoup

from config.mylog import logger
from dao.weburl_dao import WeburlDao
from model.weburl import Weburl


class UrlService:

    @staticmethod
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

    @staticmethod
    def gather_urls(website):
        logger.info("gather url for website: %s ", website["websiteName"])
        weburls = []
        weburl_service = WeburlDao
        try:
            req = urllib.request.Request(website["domainName"])
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
                    href = website["domainName"] + href
                elif href.startswith('./'):
                    href = website["domainName"] + href[1:]
                else:
                    href = website["domainName"] + "/" + href

                title = soup.find('title').string
                weburl = Weburl()
                weburl.url = href
                weburl.website_name = website["websiteName"]
                weburl.title = title
                weburls.append(weburl)
                weburl_service.add(weburl)

            for k in soup.find_all('img'):
                src = str(k.get('src'))
                logger.info("origin src: %s", src)
                if endswith(".jpg") or endswith(".jpeg") or endswith(".bmp") or endswith(
                        ".png"):
                    if startswith('http://') or startswith('https://'):
                        pass
                    elif startswith('/'):
                        src = website["domainName"] + src
                    else:
                        src = website["domainName"] + "/" + src

                    weburl = Weburl()
                    weburl.url = src
                    weburl.website_name = website["websiteName"]
                    weburl.title = "图片识别"
                    weburls.append(weburl)
                    weburl_service.add(weburl)
                else:
                    pass
            return weburls

        except Exception as e:
            logger.error(e)
