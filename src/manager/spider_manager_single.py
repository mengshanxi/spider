import util.globalvar as gl
from config.mylog import logger
from service.inspect_service import InspectService
from service.monitor_bc_service import MonitorBcService
from service.monitor_senti_service import MonitorSentiService
from service.monitor_website_service import MonitorWebsiteService


class SpiderManager:

    @staticmethod
    def inspect(task_id, batch_num):

        logger.info("service all urls for websites, begin...")
        inspect_service = InspectService()
        websites = inspect_service.get_websites(task_id)
        if websites is None:
            logger.info("get_websites return none! return !")
            return
        count = 0
        for website in websites:
            count = count + 1
            logger.info("inspect count :  %s", count)
            if gl.check_by_task(task_id):
                # 网站监控
                service = MonitorWebsiteService()
                logger.info("website monitor begin,website : %s", website["websiteName"])
                if website["domainName"] is not "":
                    service.monitor_website(website, batch_num)
                    logger.info("website monitor done! website: %s ", website["websiteName"])
                else:
                    logger.info("website domain is empty,continue! ")
                # 舆情监控
                logger.info("sentiment monitor begin,merchantName : %s", website["merchantName"])

                if website["websiteName"] is not "":
                    monitor_senti_service = MonitorSentiService()
                    monitor_senti_service.monitor_senti(website["websiteName"],website["merchantName"], task_id, batch_num)
                    monitor_senti_service.monitor_senti(website["merchantName"], website["merchantName"], task_id,
                                                        batch_num)
                    logger.info("sentiment monitor done!websiteName : %s", website["websiteName"])
                else:
                    logger.info("website name is empty,with merchantName! ")
                    monitor_senti_service = MonitorSentiService()
                    monitor_senti_service.monitor_senti(website["merchantName"],website["merchantName"], task_id, batch_num)
                    logger.info("sentiment monitor done!merchantName : %s", website["merchantName"])

                # 工商监控
                logger.info("qichacha monitor  begin,merchantName : %s", website["merchantName"])
                service = MonitorBcService()
                url = service.get_merchant_url(str(batch_num), merchant_name=website["merchantName"])
                logger.info("get qichacha url  : %s", str(url))
                if url is not None:
                    try:
                        service.inspect(str(batch_num), "https://www.qichacha.com" + url,website["merchantName"], website["legalPerson"])
                        print()
                    except Exception as e:
                        logger.info(e)
                        pass

                logger.info("qichacha monitor  done!merchantName : %s", website["merchantName"])
