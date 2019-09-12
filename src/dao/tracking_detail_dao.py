# coding:utf-8

from dao.db import session
from model.models import TrackingDetail


class TrackingDetailDao(object):

    @staticmethod
    def get_by_task(task_id, status):
        tracking_details = session.query(TrackingDetail).filter(TrackingDetail.task_id == task_id,
                                                                TrackingDetail.status == status).all()
        return tracking_details

    @staticmethod
    def update(tracking_detail):
        session.query(TrackingDetail).filter(TrackingDetail.id == tracking_detail.id).update(
            {TrackingDetail.status: tracking_detail.status,
             TrackingDetail.start_time: tracking_detail.start_time,
             TrackingDetail.end_time: tracking_detail.end_time,
             TrackingDetail.url: tracking_detail.url,
             TrackingDetail.snapshot: tracking_detail.snapshot,
             TrackingDetail.result: tracking_detail.result,
             TrackingDetail.retry: tracking_detail.retry + 1})
