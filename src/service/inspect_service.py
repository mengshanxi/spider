# -*- coding:utf-8 -*-
import json

from dao.keyword_dao import KeywordDao
from manager.ims_api import ImsApi
from config.mylog import logger


class InspectService:

    @staticmethod
    def get_websites(task_id):
        try:
            ims_api = ImsApi()
            logger.info("get websites by ims api,taskId:%s", str(task_id))
            json_data = ims_api.get_websites(task_id)
            websites = json.loads(json_data)
            return websites["websiteList"]
        except Exception as e:
            logger.info(e)
            return None

    @staticmethod
    def get_keywords(level):
        keyword_dao = KeywordDao()
        return keyword_dao.get_keywords(level)
