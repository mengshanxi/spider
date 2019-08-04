# coding:utf-8
from dao.db import session
from model.models import InspectTask


class InspectTaskDao(object):
    @staticmethod
    def get_task(task_id):
        inspect_task = session.query(InspectTask).filter(InspectTask.id == task_id).one()
        return inspect_task
