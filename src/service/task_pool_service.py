# -*- coding:utf-8 -*-

import os

import datetime

import config.global_val as gl
from config.mylog import logger
from dao.db import session
from model.models import Website, TaskItem, Weburl


class TaskPoolService:

    @staticmethod
    def get_pending_task(batch_num):
        agent_name = os.environ['agent_name']
        job = os.environ['job']
        if job == "bc":
            task_pools = session.query(TaskItem).filter(TaskItem.batch_num == batch_num).filter(
                TaskItem.status == 'pending', TaskItem.type == 'bc')
        else:
            task_pools = session.query(TaskItem).filter(TaskItem.batch_num == batch_num).filter(
                TaskItem.status == 'pending', TaskItem.type != 'bc')
        if task_pools.count() == 0:
            logger.info("本Agent没有待巡检任务，Agent切换为waiting状态: %s", agent_name)
            #  没有pending状态的任务
            gl.set_value('STATUS', False)
            return None, None
        else:
            logger.info("%s 准备执行可以处理的任务,倒数第：%s 个...", agent_name, str(task_pools.count()))
        task_pool = task_pools.first()
        session.query(TaskItem).filter(TaskItem.id == task_pool.id).update({"status": "processing"})
        if task_pool.type == "weburl":
            logger.info("task_pool.website_id：%s", task_pool.website_id)
            weburl = session.query(Weburl).filter(Weburl.url == task_pool.url).filter(
                Weburl.website_id == task_pool.website_id).all()
            if len(weburl):
                return weburl[0], task_pool
            else:
                logger.info("task_pool.website_id：%s", task_pool.website_id)
                logger.info("task_pool.id：%s", task_pool.id)
                session.query(TaskItem).filter(TaskItem.id == task_pool.id).update({"status": "done"})
                return None, None
        else:
            website = session.query(Website).filter(Website.id == task_pool.website_id).one()
            return website, task_pool

    @staticmethod
    def close_task(task_pool_id):
        agent_name = os.environ['agent_name']
        current_time = datetime.datetime.now()
        session.query(TaskItem).filter(TaskItem.id == task_pool_id).update(
            {TaskItem.status: "done",
             TaskItem.processor: agent_name,
             TaskItem.last_update: current_time})
