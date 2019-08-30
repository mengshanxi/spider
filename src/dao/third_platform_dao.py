# coding:utf-8

from dao.db import session
from model.models import ThirdPlatform


class ThirdPlatformDao(object):

    @staticmethod
    def get_all():
        platforms = session.query(ThirdPlatform).all()
        return platforms
