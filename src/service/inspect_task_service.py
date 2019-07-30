# -*- coding:utf-8 -*-
from src.dao.inspect_task_dao import InspectTaskDao


class InspectTaskService:

    def get_inspect_paltforms(self, tmpl_id):
        dao = InspectTaskDao()
        return dao.get_inspect_platform(tmpl_id)

    def get_inspect_websites(self, tmpl_id):
        dao = InspectTaskDao()
        return dao.get_inspect_website(tmpl_id)
