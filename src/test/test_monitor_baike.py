# coding=gbk
from service.monitor_baike_service import MonitorBaikeService


class TestEs(object):
    if __name__ == "__main__":
        # �ٿ�����
        test = '���Ӻ�ʳƷ�Ƽ�(����)���޹�˾'
        print(test.replace("(", "��").replace(")","��"))
        service = MonitorBaikeService()
        service.monitor_baike('���Ӻ�ʳƷ�Ƽ�(����)���޹�˾',27)
