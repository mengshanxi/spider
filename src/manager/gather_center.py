import json
import random

import time

from config.mylog import logger
from service.monitor_bc_service import MonitorBcService
from service.monitor_senti_service import MonitorSentiService
from service.monitor_website_service import MonitorWebsiteService
from service.monitor_weburl_service import MonitorWeburlService
from service.strategy_service import StrategyService
from service.task_pool_service import TaskPoolService


class GatherCenter:

    @staticmethod
    def gather(batch_num):

        task_pool_service = TaskPoolService()
        entity, task_pool = task_pool_service.get_pending_task(batch_num)
        if entity is None:
            return
        check_item = json.loads(task_pool.check_item)
        strategy_service = StrategyService()
        strategy = strategy_service.get_strategy()
        if strategy.frequency == 0 or strategy.frequency is None:
            logger.info("未设置爬取频率限制,继续执行任务..")
        else:
            logger.info("爬取频率限制为:%s 秒", strategy.frequency)
            time.sleep(strategy.frequency)
        if task_pool.type == "weburl" and check_item["websiteIsBadwords"] is 1:
            logger.info("weburl monitor begin,url: %s", entity.url)
            random_seconds = random.randint(5, 10)
            logger.info("随机等待 %s 秒...", str(random_seconds))
            time.sleep(random_seconds)
            monitor_weburl_service = MonitorWeburlService()
            monitor_weburl_service.monitor_website(entity, batch_num)
            task_pool_service.close_task(task_pool.id)
            logger.info("weburl domain is done,continue! ")
            return
        elif task_pool.type == "website":
            if check_item["websiteIsForward"] is 1 or check_item["websiteIsOpen"] is 1:
                # 网站监控
                logger.info("website monitor begin,domain_name: %s", entity.domain_name)
                service = MonitorWebsiteService()
                service.monitor_website(entity, batch_num)
            else:
                logger.info("%s 跳过网站监控", entity.merchant_name)
        elif task_pool.type == "senti":
            # 舆情监控
            logger.info("sentiment monitor begin,merchant_name : %s", entity.merchant_name)
            random_seconds = random.randint(5, 10)
            logger.info("随机等待 %s 秒...", str(random_seconds))
            time.sleep(random_seconds)
            monitor_senti_service = MonitorSentiService()
            monitor_senti_service.monitor_senti(entity.merchant_name, task_pool, batch_num, entity)
            logger.info("sentiment monitor done!merchantName : %s", entity.merchant_name)
        elif task_pool.type == "bc":
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
            else:
                logger.info("没有获取到商户企查查信息!merchantName : %s", entity.merchant_name)
            logger.info("qichacha monitor  done!merchantName : %s", entity.merchant_name)

        task_pool_service.close_task(task_pool.id)
