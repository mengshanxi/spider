#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request
from src.config.mylog import logger
from src.config.config_load import ims_rest_base


class ImsApi:
    def create_report(self, task_id, batch_num):
        try:
            url = ims_rest_base + "open/api/v1/report/%s/%s" % (task_id, batch_num)
            logger.info(url)
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=10).read()
        except Exception as e:
            logger.info("create report for %s fail" % str(batch_num))
            logger.info(e)
            pass

    def get_websites(self, task_id):
        try:
            url = ims_rest_base + "api/v1/inspect_task/%s" % (task_id)
            logger.info("get_websites url :%s " % str(url))
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=10).read()
            logger.info("get_websites res :%s " % str(res))
            return res
        except Exception as e:
            logger.error(e)

    def hands_report(self, report_id):
        try:
            url = "http://localhost/ims/open/api/v1/hands_report/%s" % report_id
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=10).read()
            logger.info(res)
        except:
            logger.info("create report for %s fail" % report_id)
            pass
