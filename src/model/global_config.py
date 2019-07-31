# coding:utf-8
from sqlalchemy import Column, String, Integer, DateTime

from dao.db import Base


class Global(Base):
    __tablename__ = 'global'
    id = Column(Integer(), primary_key=True)
    level = Column(String(100))
    freq = Column(String(100))
    create_time = Column(DateTime())
