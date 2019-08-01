from dao.third_config_dao import ThirdConfigDao


class TestMysql(object):
    if __name__ == "__main__":
        ThirdConfigDao = ThirdConfigDao()
        ThirdConfigDao.get_by_name("qichacha")
