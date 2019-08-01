from dao.keyword_dao import KeywordDao


class TestMysql(object):
    if __name__ == "__main__":
        keyword_dao = KeywordDao()
        keywords = keyword_dao.get_all()
        for i in keywords:
            print(i.name, i.level)
