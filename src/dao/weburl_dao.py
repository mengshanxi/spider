# coding:utf-8
import datetime

from config.mylog import logger
from dao.db import session, DB_Session
from model.models import Weburl


class WeburlDao(object):

    @staticmethod
    def get_all():
        weburl = session.query(Weburl).all()
        return weburl

    @staticmethod
    def add(weburl):
        exist_weburl = session.query(Weburl).filter(Weburl.url == weburl.url).filter(
            Weburl.website_id == weburl.website_id).all()
        if len(exist_weburl):
            logger.info("weburl is exist!")
            pass
        else:
            logger.info("add to db!")
            weburl.create_time = datetime.datetime.now()
            weburl.last_update = datetime.datetime.now()
            session.add(weburl)
        # conn = DB_Session()
        # try:
        #     exist_weburl = conn.query(Weburl).filter(Weburl.url == weburl.url).all()
        #     if len(exist_weburl):
        #         pass
        #     else:
        #         weburl.create_time = datetime.datetime.now()
        #         weburl.last_update = datetime.datetime.now()
        #         conn.add(weburl)
        #         session.commit()
        # except Exception as e:
        #     print(e)
        #     conn.rollback()
        #     raise
        # finally:
        #     conn.close()
