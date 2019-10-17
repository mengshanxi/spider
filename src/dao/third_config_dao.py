# coding:utf-8
from config.mylog import logger
from dao.db import session
from model.models import ThirdConfig


class ThirdConfigDao(object):

    @staticmethod
    def get_by_name(name):
        third_config = session.query(ThirdConfig).filter(ThirdConfig.name == name).all()
        if len(third_config):
            return third_config[0].cookie
        else:
            return "nocookie"
