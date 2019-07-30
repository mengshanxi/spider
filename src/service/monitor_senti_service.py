import src.util.globalvar as gl
from src.service.inspect_task_service import InspectTaskService
from src.service.monitor_baidu_service import MonitorBaiduService
from src.service.monitor_baike_service import MonitorBaikeService
from src.service.monitor_bus_service import MonitorBusService
from src.service.monitor_chinaft_service import MonitorChinaftService
from src.service.monitor_p2peye_service import MonitorP2peyeService
from src.service.monitor_tieba_service import MonitorTiebaService
from src.service.monitor_wdzj_service import MonitorWdzjService
from src.config.mylog import logger

"""
三方监控服务
"""


class MonitorSentiService:

    @staticmethod
    def monitor_senti(website_name,merchant_name, task_id, batch_num):

        inspect_task_service = InspectTaskService()
        platforms = inspect_task_service.get_inspect_paltforms(task_id)
        for platform in platforms:
            if not gl.check_by_task(task_id):
                logger.info("taskId has removed : %s", task_id)
                break

            if platform == "网贷天眼":
                logger.info("sentiment monitor with  : %s", platform)
                p2peye_service = MonitorP2peyeService()
                p2peye_service.monitor_p2peye(website_name,merchant_name, batch_num)
                continue
            if platform == "网贷巴士":
                logger.info("sentiment monitor with  : %s", platform)
                bus_service = MonitorBusService()
                bus_service.monitor_bus(website_name,merchant_name, batch_num)
                continue
            if platform == "交易中国":
                logger.info("sentiment monitor with  : %s", platform)
                chinaft_service = MonitorChinaftService()
                chinaft_service.monitor_chinaft(website_name,merchant_name, batch_num)
                continue
            if platform == "百度贴吧":
                logger.info("sentiment monitor with  : %s", platform)
                tieba_service = MonitorTiebaService()
                tieba_service.monitor_tieba(website_name,merchant_name, batch_num)
                continue
            if platform == "网贷之家":
                logger.info("sentiment monitor with  : %s", platform)
                wdzj_service = MonitorWdzjService()
                wdzj_service.monitor_wdzj(website_name,merchant_name, batch_num)
                continue
            if platform == "百度搜索":
                logger.info("sentiment monitor with  : %s", platform)
                baidu_service = MonitorBaiduService()
                baidu_service.monitor_baidu(website_name,merchant_name, batch_num)
                continue
            if platform == "百度百科":
                logger.info("sentiment monitor with  : %s", platform)
                baike_service = MonitorBaikeService()
                baike_service.monitor_baike(website_name,merchant_name, batch_num)
                continue
