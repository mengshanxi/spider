# -*- coding:utf-8 -*-
from dao.db import session
from dao.inspect_detail_dao import InspectDetailDao
from dao.inspect_task_dao import InspectTaskDao
from model.models import Website


class InspectTaskService(object):
    @staticmethod
    def get_inspect_platforms(task_id):
        dao = InspectDetailDao()
        inspect_details = dao.get_inspect_platform(task_id)
        platforms = []
        for inspect_detail in inspect_details:
            list.append(inspect_detail.platform_name)
        return platforms

    @staticmethod
    def get_websites(task_id):
        inspect_dao = InspectTaskDao()
        inspect_task = inspect_dao.get_task(task_id)
        websites = session.query(Website).filter(Website.attention == inspect_task.attention).filter(
            Website.industry.contains(inspect_task.industry)).filter(
            Website.industry2.contains(inspect_task.industry2)).all()
        return websites
