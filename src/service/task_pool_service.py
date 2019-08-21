# -*- coding:utf-8 -*-

from dao.db import session
from model.models import Website, TaskItem, Weburl
import config.global_val as gl
import os


class TaskPoolService:

    @staticmethod
    def get_pending_task(batch_num):
        task_pool = session.query(TaskItem).filter(TaskItem.batch_num == batch_num).filter(
            TaskItem.status == 'pending').first()
        if task_pool is None:
            #  没有pending状态的任务
            gl.set_value('STATUS', False)
            return None, None, None, None
        session.query(TaskItem).filter(TaskItem.id == task_pool.id).update({"status": "processing"})
        if task_pool.type == "website":
            website = session.query(Website).filter(Website.id == task_pool.website_id).one()
            return website, task_pool.task_id, task_pool.type, task_pool.id
        elif task_pool.type == "weburl":
            weburl = session.query(Weburl).filter(Weburl.url == task_pool.url).one()
            return weburl, task_pool.task_id, task_pool.type, task_pool.id

    @staticmethod
    def close_task(task_pool_id):
        browser = os.environ['browser']
        session.query(TaskItem).filter(TaskItem.id == task_pool_id).update({"status": "done", "processor": browser})
