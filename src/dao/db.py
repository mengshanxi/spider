from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config_load import database
from config.config_load import host
from config.config_load import password
from config.config_load import username

Base = declarative_base()
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8&autocommit=true' %
                       (username, password, host, database),
                       encoding='utf-8', echo=False,
                       pool_size=100, pool_recycle=10)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
