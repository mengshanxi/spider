from config.mylog import logger
from service.monitor_bc_service import MonitorBcService
from service.monitor_senti_service import MonitorSentiService
from service.monitor_website_service import MonitorWebsiteService
from service.monitor_weburl_service import MonitorWeburlService
from service.task_pool_service import TaskPoolService
import config.global_val as gl


class GatherCenter:

    @staticmethod
    def gather(batch_num):

        task_pool_service = TaskPoolService()
        entity, task_id, type, task_pool_id = task_pool_service.get_pending_task(batch_num)
        if entity is None:
            gl.set_value('STATUS', False)
            return
        if type == "weburl":
            monitor_weburl_service = MonitorWeburlService()
            monitor_weburl_service.monitor_website(entity, batch_num)
            task_pool_service.close_task(task_pool_id)
            return
        elif type == "website":
            # 网站监控
            logger.info("gather data for website_name:%s", entity.website_name)
            service = MonitorWebsiteService()
            logger.info("website monitor begin,domain_name : %s", entity.domain_name)
            if entity.domain_name is not None:
                service.monitor_website(entity, batch_num)
                logger.info("website monitor done! domain_name: %s ", entity.domain_name)
            else:
                logger.info("website domain is empty,continue! ")
            # 舆情监控
            logger.info("sentiment monitor begin,merchant_name : %s", entity.merchant_name)
            if entity.website_name is not None:
                monitor_senti_service = MonitorSentiService()
                monitor_senti_service.monitor_senti(entity.website_name, entity.website_name, task_id,
                                                    batch_num, entity.merchant_name, entity.merchant_num)
                monitor_senti_service.monitor_senti(entity.merchant_name, entity.website_name, task_id,
                                                    batch_num, entity.merchant_name, entity.merchant_num)
                logger.info("sentiment monitor done!merchant_name : %s", entity.merchant_name)
            else:
                logger.info("website name is empty,with merchantName! ")
                monitor_senti_service = MonitorSentiService()
                monitor_senti_service.monitor_senti(entity.merchant_name, entity.website_name, task_id,
                                                    batch_num, entity.merchant_name, entity.merchant_num)
                logger.info("sentiment monitor done!merchantName : %s", entity.merchant_name)

            # 工商监控
            logger.info("qichacha monitor  begin,merchantName : %s", entity.merchant_name)
            service = MonitorBcService()
            url = service.get_merchant_url(str(batch_num), merchant_name=entity.merchant_name)
            logger.info("get qichacha url  : %s", str(url))
            if url is not None:
                try:
                    service.inspect(str(batch_num), "https://www.qichacha.com" + url, entity)
                except Exception as e:
                    logger.info(e)
                    pass
            logger.info("qichacha monitor  done!merchantName : %s", entity.merchant_name)
            task_pool_service.close_task(task_pool_id)
