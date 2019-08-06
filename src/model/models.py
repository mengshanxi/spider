# coding:utf-8
from sqlalchemy import Column, String, Integer, DateTime, Text

from dao.db import Base


class Strategy(Base):
    __tablename__ = 'strategy'
    id = Column(Integer(), primary_key=True)
    task_overtime = Column(Integer())
    cache_days = Column(Integer())
    gather_percent = Column(Integer())


class InspectDetail(Base):
    __tablename__ = 'inspect_detail'
    id = Column(Integer(), primary_key=True)
    tmpl_id = Column(Integer())
    platform_name = Column(String(255))
    website_name = Column(String(255))
    checked = Column(Integer())
    create_time = Column(DateTime())


class TaskItem(Base):
    __tablename__ = 'task_item'
    id = Column(Integer(), primary_key=True)
    title = Column(String(255))
    task_id = Column(Integer())
    batch_num = Column(String(255))
    url = Column(String(255))
    website_id = Column(Integer())
    website_name = Column(String(255))
    merchant_name = Column(String(255))
    type = Column(String(255))
    status = Column(String(255))
    processor = Column(String(255))
    create_time = Column(DateTime())
    last_update = Column(DateTime())


class InspectTask(Base):
    __tablename__ = 'inspect_task'
    id = Column(Integer(), primary_key=True)
    task_name = Column(String(255))
    mode = Column(String(255))
    cause = Column(String(255))
    website_is_open = Column(Integer())
    website_is_forward = Column(Integer())
    website_is_deadlink = Column(Integer())
    website_is_mislead = Column(Integer())
    website_is_stock = Column(Integer())
    website_is_badwords = Column(Integer())
    bc_is_dishonest = Column(Integer())
    bc_is_abn = Column(Integer())
    bc_is_logout = Column(Integer())
    bc_is_moveout = Column(Integer())
    bc_name_chg = Column(Integer())
    bc_legalperson_chg = Column(Integer())
    freq = Column(Integer())
    points = Column(String(255))
    source = Column(String(255))
    industry = Column(String(255))
    industry2 = Column(String(255))
    attention = Column(String(255))
    filename = Column(String(255))
    start_time = Column(DateTime())
    end_time = Column(DateTime())
    last_update = Column(DateTime())


class MonitorThird(Base):
    __tablename__ = 'monitor_third'
    id = Column(Integer(), primary_key=True)
    batch_num = Column(String(255))
    type = Column(String(100))
    website_name = Column(String(255))
    url = Column(String(255))
    outline = Column(String(100))
    snapshot = Column(String(100))
    is_normal = Column(String(100))
    level = Column(String(100))
    create_time = Column(DateTime())


class MonitorWebsite(Base):
    __tablename__ = 'monitor_website'
    id = Column(Integer(), primary_key=True)
    batch_num = Column(String(255))
    merchant_name = Column(String(100))
    website_name = Column(String(255))
    domain_name = Column(String(100))
    access = Column(String(255))
    pageview = Column(String(255))
    outline = Column(String(100))
    snapshot = Column(String(100))
    is_normal = Column(String(100))
    kinds = Column(String(100))
    level = Column(String(100))
    create_time = Column(DateTime())
    last_update = Column(DateTime())


class MonitorUrl(Base):
    __tablename__ = 'monitor_url'
    id = Column(Integer(), primary_key=True)
    batch_num = Column(String(255))
    website_name = Column(String(255))
    title = Column(String(255))
    url = Column(Text())
    outline = Column(String(100))
    snapshot = Column(String(100))
    is_normal = Column(String(100))
    kinds = Column(String(100))
    level = Column(String(100))
    create_time = Column(DateTime())


class MonitorBc(Base):
    __tablename__ = 'monitor_bc'
    id = Column(Integer(), primary_key=True)
    batch_num = Column(String(255))
    merchant_name = Column(String(100))
    outline = Column(String(100))
    snapshot = Column(String(100))
    is_normal = Column(String(100))
    kinds = Column(String(100))
    level = Column(String(100))
    create_time = Column(DateTime())


class BcPerson(Base):
    __tablename__ = 'bc_person'
    id = Column(Integer(), primary_key=True)
    batch_num = Column(String(255))
    merchant_name = Column(String(100))
    fullname = Column(String(50))
    job = Column(String(50))
    create_time = Column(DateTime())


class BcBenefit(Base):
    __tablename__ = 'bc_benefit'
    id = Column(Integer(), primary_key=True)
    batch_num = Column(String(255))
    merchant_name = Column(String(100))
    fullname = Column(String(255))
    proportion = Column(String(255))
    invest_train = Column(String(255))
    create_time = Column(DateTime())


class ThirdConfig(Base):
    __tablename__ = 'third_config'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    cookie = Column(Text())
    last_update = Column(DateTime())


class Keyword(Base):
    __tablename__ = 'words'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    level = Column(String(100))
    create_time = Column(DateTime())


class Weburl(Base):
    __tablename__ = 'weburl'
    id = Column(Integer(), primary_key=True)
    title = Column(String(100))
    url = Column(String(100))
    website_id = Column(String(100))
    website_name = Column(String(100))
    type = Column(String(10))
    create_time = Column(DateTime())
    last_update = Column(DateTime())


class Global(Base):
    __tablename__ = 'global'
    id = Column(Integer(), primary_key=True)
    level = Column(String(100))
    freq = Column(String(100))


class Website(Base):
    __tablename__ = 'website'
    id = Column(Integer(), primary_key=True)
    merchant_name = Column(String(100))
    website_name = Column(String(100))
    domain_name = Column(String(100))
    legal_person = Column(String(100))
    industry = Column(String(100))
    industry2 = Column(String(100))
    attention = Column(String(100))
    username = Column(String(100))
    password = Column(String(100))
    last_gather_time = Column(DateTime())
    create_time = Column(DateTime())
    last_update = Column(DateTime())
