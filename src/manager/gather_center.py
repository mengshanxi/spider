import json

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
        entity, task_pool = task_pool_service.get_pending_task(batch_num)
        if entity is None:
            return
        check_item = json.loads(task_pool.check_item)
        if task_pool.type == "weburl" and check_item["websiteIsBadwords"] is 1:
            monitor_weburl_service = MonitorWeburlService()
            monitor_weburl_service.monitor_website(entity, batch_num)
            task_pool_service.close_task(task_pool.task_pool_id)
            return
        elif task_pool.type == "website":
            if check_item["websiteIsForward"] is 1 or check_item["websiteIsOpen"] is 1:
                # 网站监控
                logger.info("gather data for website_name:%s", entity.website_name)
                service = MonitorWebsiteService()
                logger.info("website monitor begin,domain_name : %s", entity.domain_name)
                service.monitor_website(entity, batch_num)
                logger.info("website domain is empty,continue! ")
            else:
                pass
            if check_item["zfzj"] is 1 \
                    or check_item["baidu"] is 1 \
                    or check_item["baike"] is 1 \
                    or check_item["tousu"] is 1 \
                    or check_item["paynews"] is 1 \
                    or check_item["zhifujie"] is 1 \
                    or check_item["paycircle"] is 1:
                # 舆情监控
                logger.info("sentiment monitor begin,merchant_name : %s", entity.merchant_name)
                if not entity.website_name:
                    logger.info("website name is empty,with merchantName! ")
                    monitor_senti_service = MonitorSentiService()
                    monitor_senti_service.monitor_senti(entity.merchant_name, task_pool.task_id, batch_num, entity)
                    logger.info("sentiment monitor done!merchantName : %s", entity.merchant_name)
                else:
                    monitor_senti_service = MonitorSentiService()
                    monitor_senti_service.monitor_senti(entity.website_name, task_pool.task_id, batch_num, entity)
                    monitor_senti_service.monitor_senti(entity.merchant_name, task_pool.task_id, batch_num, entity)
                    logger.info("sentiment monitor done!merchant_name : %s", entity.merchant_name)
            else:
                pass
            if check_item["bcIsMoveout"] is 1 or check_item["bcIsLogout"] is 1 or check_item["bcLegalpersonChg"] is 1:
                # 工商监控
                logger.info("qichacha monitor  begin,merchantName : %s", entity.merchant_name)
                service = MonitorBcService()
                url = service.get_merchant_url(str(batch_num), entity)
                logger.info("get qichacha url  : %s", str(url))
                if url is not None:
                    try:
                        service.inspect(str(batch_num), "https://www.qichacha.com" + url, entity)
                    except Exception as e:
                        logger.info(e)
                        pass
                logger.info("qichacha monitor  done!merchantName : %s", entity.merchant_name)
            else:
                pass
            task_pool_service.close_task(task_pool.task_pool_id)
