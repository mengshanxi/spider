# coding=gbk
from service.monitor_baike_service import MonitorBaikeService


class TestEs(object):
    if __name__ == "__main__":
        # 百科舆情
        test = '中视好食品科技(北京)有限公司'
        print(test.replace("(", "（").replace(")","）"))
        service = MonitorBaikeService()
        service.monitor_baike('中视好食品科技(北京)有限公司',27)
