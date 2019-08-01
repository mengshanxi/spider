import datetime
import pymysql

pymysql.install_as_MySQLdb()
from dao.db import session
from model.models import Global


class TestMysql(object):
    if __name__ == "__main__":
        # 创建新User对象:
        new_config = Global(level='Bob', freq='1',create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # 添加到session:
        session.add(new_config)
        # 提交即保存到数据库:

        config1 = session.query(Global).filter(Global.id == 4).one()
        print(config1.level)
        config2 = session.query(Global).filter(Global.level == 'Bob').all()
        for i in config2:
            print(i.id, i.level)
        session.query(Global).filter(Global.id == 4).update({"level": "1099"})
        # 关闭session:
        session.close()
