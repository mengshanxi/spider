# coding:utf-8
import datetime

from dao.db import session
from model.models import TrackingTask


class TrackingTaskDao(object):

    @staticmethod
    def close_task(task_id):
        current_time = datetime.datetime.now()
        session.query(TrackingTask).filter(TrackingTask.id == task_id).update(
            {TrackingTask.status: 'done',
             TrackingTask.end_time: current_time,
             TrackingTask.last_update: current_time
             })
