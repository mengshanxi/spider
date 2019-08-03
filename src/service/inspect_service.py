# -*- coding:utf-8 -*-

from dao.db import session
from dao.inspect_task_dao import InspectTaskDao
from dao.keyword_dao import KeywordDao
from model.models import Website


class InspectService:

    @staticmethod
    def get_websites(task_id):
        inspect_dao = InspectTaskDao()
        inspect_task = inspect_dao.get_task(task_id)
        websites = session.query(Website).filter(Website.attention == inspect_task.attention).filter(
            Website.industry.contains(inspect_task.industry)).filter(
            Website.industry2.contains(inspect_task.industry2)).all()
        return websites

    @staticmethod
    def get_keywords(level):
        keyword_dao = KeywordDao()
        return keyword_dao.get_all(level)
