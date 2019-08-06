# -*- coding:utf-8 -*-
import time

from dao.db import session
from dao.inspect_detail_dao import InspectDetailDao
from dao.inspect_task_dao import InspectTaskDao
from model.models import Website
from service.strategy_service import StrategyService


class InspectTaskService(object):
    @staticmethod
    def get_inspect_platforms(task_id):
        dao = InspectDetailDao()
        inspect_details = dao.get_inspect_platform(task_id)
        platforms = []
        for inspect_detail in inspect_details:
            platforms.append(inspect_detail.platform_name)
        return platforms

    @staticmethod
    def get_websites(task_id):
        filterd = []
        inspect_dao = InspectTaskDao()
        inspect_task = inspect_dao.get_task(task_id)
        websites = session.query(Website).filter(Website.attention == inspect_task.attention).filter(
            Website.industry.contains(inspect_task.industry)).filter(
            Website.industry2.contains(inspect_task.industry2)).all()
        strategy_service = StrategyService()
        strategy = strategy_service.get_strategy()
        now = time.time()
        overtime = now - strategy.cache_days * 24 * 60 * 1000
        for website in websites:
            last_gather_time = website.last_gather_time
            if last_gather_time is None:
                continue
            elif time.mktime(time.strptime(str(last_gather_time), "%Y-%m-%d %H:%M:%S")) > overtime:
                continue
            else:
                filterd.append(website)
        return filterd
