# coding:utf-8
from dao.db import session
from model.models import InspectDetail


class InspectDetailDao(object):

    @staticmethod
    def get_inspect_platform(task_id):
        inspect_details = session.query(InspectDetail).filter(InspectDetail.tmpl_id == task_id).filter(
            InspectDetail.checked == 1).all()
        return inspect_details
