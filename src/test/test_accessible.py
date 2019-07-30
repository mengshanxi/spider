from src.service.accessible_service import AccessibleService


class TestEs(object):
    if __name__ == "__main__":
        access = AccessibleService()
        rtn = access.get_access_res("www.zhongguohsp.com")
        if rtn:
            print("可以访问")
        else:
            print("不可以访问")
