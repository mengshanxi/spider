from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8&autocommit=true' %
                       ('root', 'abcd1234', 'localhost', 'ims'),
                       encoding='utf-8', echo=False,
                       pool_size=100, pool_recycle=10)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
