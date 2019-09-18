# -*- coding:utf-8 -*-
import socket

import config.global_val as gl
from config.mylog import logger
from dao.db import session
from model.models import Website, TaskItem, Weburl


class TaskPoolService:

    @staticmethod
    def get_pending_task(batch_num):
        task_pools = session.query(TaskItem).filter(TaskItem.batch_num == batch_num).filter(
            TaskItem.status == 'pending')
        if task_pools.count() == 0:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            logger.info("没有待巡检任务，Agent切换为waiting状态: %s", ip)
            #  没有pending状态的任务
            gl.set_value('STATUS', False)
            return None, None
        else:
            logger.info("准备执行巡检子任务...")
        task_pool = task_pools.first()
        session.query(TaskItem).filter(TaskItem.id == task_pool.id).update({"status": "processing"})
        if task_pool.type == "website":
            website = session.query(Website).filter(Website.id == task_pool.website_id).one()
            return website, task_pool
        elif task_pool.type == "weburl":
            weburl = session.query(Weburl).filter(Weburl.url == task_pool.url).one()
            return weburl, task_pool

    @staticmethod
    def close_task(task_pool_id):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        session.query(TaskItem).filter(TaskItem.id == task_pool_id).update(
            {"status": "done", "processor": ip})
