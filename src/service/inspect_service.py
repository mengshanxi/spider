# -*- coding:utf-8 -*-
import json

from src.dao.keyword_dao import KeywordDao
from src.manager.ims_api import ImsApi
from src.config.mylog import logger


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
