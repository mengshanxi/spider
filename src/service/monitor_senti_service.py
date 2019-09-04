from config.mylog import logger
from service.inspect_task_service import InspectTaskService
from service.monitor_baidu_service import MonitorBaiduService
from service.monitor_baike_service import MonitorBaikeService
from service.monitor_bus_service import MonitorBusService
from service.monitor_chinaft_service import MonitorChinaftService
from service.monitor_p2peye_service import MonitorP2peyeService
from service.monitor_paycircle_service import MonitorPaycircleService
from service.monitor_paynews_service import MonitorPaynewsService
from service.monitor_tieba_service import MonitorTiebaService
from service.monitor_tousu_service import MonitorTousuService
from service.monitor_ts_service import MonitorTsService
from service.monitor_wdzj_service import MonitorWdzjService
from service.monitor_zfzj_service import MonitorZfzjService
from service.monitor_zhifujie_service import MonitorZhifujieService

"""
三方监控服务
"""


class MonitorSentiService:

    @staticmethod
    def monitor_senti(keyword, website_name, task_id, batch_num, merchant_name, merchant_num):

        inspect_task_service = InspectTaskService()
        platforms = inspect_task_service.get_inspect_platforms(task_id)
        for platform in platforms:
            if platform == "网贷天眼":
                logger.info("sentiment monitor with  : %s", platform)
                p2peye_service = MonitorP2peyeService()
                p2peye_service.monitor(website_name, merchant_name, batch_num)
                continue
            if platform == "网贷巴士":
                logger.info("sentiment monitor with  : %s", platform)
                bus_service = MonitorBusService()
                bus_service.monitor(website_name, merchant_name, batch_num)
                continue
            if platform == "交易中国":
                logger.info("sentiment monitor with  : %s", platform)
                chinaft_service = MonitorChinaftService()
                chinaft_service.monitor(website_name, merchant_name, batch_num)
                continue
            if platform == "百度贴吧":
                logger.info("sentiment monitor with  : %s", platform)
                tieba_service = MonitorTiebaService()
                tieba_service.monitor(keyword, website_name, batch_num, merchant_name,
                                      merchant_num)
                continue
            if platform == "网贷之家":
                logger.info("sentiment monitor with  : %s", platform)
                wdzj_service = MonitorWdzjService()
                wdzj_service.monitor(website_name, merchant_name, batch_num)
                continue
            if platform == "百度搜索":
                logger.info("sentiment monitor with  : %s", platform)
                baidu_service = MonitorBaiduService()
                baidu_service.monitor(keyword, website_name, batch_num, merchant_name,
                                      merchant_num)
                continue
            if platform == "百度百科":
                logger.info(platform + " sentiment monitor with  : %s", platform)
                baike_service = MonitorBaikeService()
                baike_service.monitor(keyword, website_name, batch_num, merchant_name,
                                      merchant_num)
                continue
            if platform == "支付圈":
                logger.info(platform + " sentiment monitor with  : %s", platform)
                paycircle_service = MonitorPaycircleService()
                paycircle_service.monitor(keyword, website_name, batch_num, merchant_name,
                                          merchant_num)
                continue
            if platform == "聚投诉":
                logger.info(platform + " sentiment monitor with  : %s", platform)
                ts_service = MonitorTsService()
                ts_service.monitor(keyword, website_name, batch_num, merchant_name,
                                   merchant_num)
                continue
            if platform == "黑猫投诉":
                logger.info(platform + " sentiment monitor with  : %s", platform)
                tousu_service = MonitorTousuService()
                tousu_service.monitor(keyword, website_name, batch_num, merchant_name,
                                      merchant_num)
                continue
            if platform == "支付产业网":
                logger.info(platform + " sentiment monitor with  : %s", platform)
                paynews_service = MonitorPaynewsService()
                paynews_service.monitor(keyword, website_name, batch_num, merchant_name,
                                        merchant_num)
                continue
            if platform == "支付界":
                logger.info(platform + " sentiment monitor with  : %s", platform)
                zhifujie_service = MonitorZhifujieService()
                zhifujie_service.monitor(keyword, website_name, batch_num, merchant_name,
                                         merchant_num)
                continue
            if platform == "支付快讯":
                logger.info(platform + " sentiment monitor with  : %s", platform)
                zfzj_service = MonitorZfzjService()
                zfzj_service.monitor(keyword, website_name, batch_num, merchant_name,
                                     merchant_num)
                continue
