#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib import request, parse
from config.mylog import logger
from config.config_load import ims_rest_base
import socket


class ImsApi(object):

    @staticmethod
    def register():
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            url = ims_rest_base + "open/api/v1/agent/register"
            data_json = {"ip": ip}
            data = bytes(parse.urlencode(data_json), encoding="utf8")
            new_url = request.Request(url, data)
            logger.info("agent register ip: %s" % str(ip))
            request.urlopen(new_url)
        except Exception as e:
            logger.info("register fail")
            logger.info(e)
            pass

    @staticmethod
    def heartbeat():
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            url = ims_rest_base + "open/api/v1/agent/heartbeat"
            data_json = {"ip": ip}
            data = bytes(parse.urlencode(data_json), encoding="utf8")
            new_url = request.Request(url, data)
            request.urlopen(new_url)
        except Exception as e:
            logger.info("register fail")
            logger.info(e)
            pass

    @staticmethod
    def done_url_gather(website):
        try:
            url = ims_rest_base + "open/api/v1/agent/done_url_gather"
            data_json = {"websiteId": website.id}
            data = bytes(parse.urlencode(data_json), encoding="utf8")
            new_url = request.Request(url, data)
            logger.info("done url gather: %s." % str(website.website_name))
            request.urlopen(new_url)
        except Exception as e:
            logger.info("register fail")
            logger.info(e)
            pass
