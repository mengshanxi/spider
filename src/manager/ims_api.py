#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib import request, parse

import os

from config.mylog import logger
from config.config_load import ims_rest_base
import config.global_val as gl
import socket


class ImsApi(object):

    @staticmethod
    def register():
        try:
            agent_name = os.environ['agent_name']
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            url = ims_rest_base + "open/api/v1/agent/register"
            data_json = {"ip": ip, "job": agent_name}
            data = bytes(parse.urlencode(data_json), encoding="utf8")
            new_url = request.Request(url, data)
            logger.info("agent register ip: %s" % str(ip))
            request.urlopen(new_url)
        except Exception as e:
            logger.info("register fail")
            logger.info(e)

    @staticmethod
    def heartbeat():
        try:
            agent_name = os.environ['agent_name']
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            url = ims_rest_base + "open/api/v1/agent/heartbeat"
            status = gl.get_value('STATUS')
            data_json = {"ip": ip, "status": status, "job": agent_name}
            data = bytes(parse.urlencode(data_json), encoding="utf8")
            new_url = request.Request(url, data)
            request.urlopen(new_url)
        except Exception as e:
            logger.info(e)
            logger.info("heartbeat fail")

    @staticmethod
    def done_url_gather(website):
        try:
            url = ims_rest_base + "open/api/v1/agent/done_url_gather"
            data_json = {"websiteId": website.id}
            data = bytes(parse.urlencode(data_json), encoding="utf8")
            new_url = request.Request(url, data)
            logger.info("done url gather: %s" % str(website.domain_name))
            request.urlopen(new_url)
        except Exception as e:
            logger.info(e)
            logger.info("url gather res fail!")

    @staticmethod
    def done_tracking(task_id):
        try:
            url = ims_rest_base + "open/api/v1/agent/done_tracking"
            data_json = {"taskId": task_id}
            data = bytes(parse.urlencode(data_json), encoding="utf8")
            new_url = request.Request(url, data)
            logger.info("done tricking: %s" % str(task_id))
            request.urlopen(new_url)
        except Exception as e:
            logger.info(e)
            logger.info("tracking  fail")
