# coding:utf-8
import datetime

from dao.db import session
from model.models import TrackingTask


class TrackingTaskDao(object):

    @staticmethod
    def close_task(task_id):
        end_time = datetime.datetime.now
        session.query(TrackingTask).filter(TrackingTask.id == task_id).update(
            {TrackingTask.status: 'done',
             TrackingTask.end_time: end_time,
             TrackingTask.last_update: end_time
             })
