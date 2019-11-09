# coding:utf-8
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config_load import database
from config.config_load import host
from config.config_load import password
from config.config_load import username
from config.mylog import logger
from dao.db import session
from model.models import Weburl


class WeburlDao(object):

    @staticmethod
    def get_all():
        weburl = session.query(Weburl).all()
        return weburl

    @staticmethod
    def add(weburl):
        logger.info("add weburl to db: %s", weburl.url)
        engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8&autocommit=true' %
                               (username, password, host, database),
                               encoding='utf-8', echo=False,
                               pool_size=100, pool_recycle=10)
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            exist_weburl = session.query(Weburl).filter(Weburl.url == weburl.url).filter(
                Weburl.website_id == weburl.website_id).all()
            if len(exist_weburl):
                pass
            else:
                weburl.create_time = datetime.datetime.now()
                weburl.last_update = datetime.datetime.now()
                session.add(weburl)
                session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()
        # logger.info("weburl add..")
        # exist_weburl = session.query(Weburl).filter(Weburl.url == weburl.url).filter(
        #     Weburl.website_id == weburl.website_id).all()
        # logger.info("exist_weburl")
        # if len(exist_weburl):
        #     logger.info("weburl is exist!")
        #     pass
        # else:
        #     logger.info("add to db!")
        #     weburl.create_time = datetime.datetime.now()
        #     weburl.last_update = datetime.datetime.now()
        #     session.add(weburl)
        #     session.commit()
        # conn = DB_Session()
        # try:
        #     exist_weburl = conn.query(Weburl).filter(Weburl.url == weburl.url).filter(
        #         Weburl.website_id == weburl.website_id).all()
        #     if len(exist_weburl):
        #         pass
        #     else:
        #         weburl.create_time = datetime.datetime.now()
        #         weburl.last_update = datetime.datetime.now()
        #         conn.add(weburl)
        # except Exception as e:
        #     print(e)
        #     conn.rollback()
        #     raise
        # finally:
        #     conn.close()
