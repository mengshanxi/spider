from config.mylog import logger
from service.inspect_service import InspectService
from service.monitor_bc_service import MonitorBcService
from service.monitor_senti_service import MonitorSentiService
from service.monitor_website_service import MonitorWebsiteService


class GatherCenter:

    @staticmethod
    def gather(task_id, batch_num):

        inspect_service = InspectService()
        # 网站监控
        website = inspect_service.get_website(task_id)
        logger.info("gather data for website_name:%s", website.website_name)
        service = MonitorWebsiteService()
        logger.info("website monitor begin,website_name : %s", website.website_name)
        if website.domain_name is not "":
            service.monitor_website(website, batch_num)
            logger.info("website monitor done! website_name: %s ", website.website_name)
        else:
            logger.info("website domain is empty,continue! ")
        # 舆情监控
        logger.info("sentiment monitor begin,merchant_name : %s", website.merchant_name)
        if website.website_name is not "":
            monitor_senti_service = MonitorSentiService()
            monitor_senti_service.monitor_senti(website.website_name, website.merchant_name, task_id,
                                                batch_num)
            monitor_senti_service.monitor_senti(website.merchant_name, website.merchant_name, task_id,
                                                batch_num)
            logger.info("sentiment monitor done!websiteName : %s", website.website_name)
        else:
            logger.info("website name is empty,with merchantName! ")
            monitor_senti_service = MonitorSentiService()
            monitor_senti_service.monitor_senti(website.merchant_name, website.merchant_name, task_id,
                                                batch_num)
            logger.info("sentiment monitor done!merchantName : %s", website.merchant_name)

        # 工商监控
        logger.info("qichacha monitor  begin,merchantName : %s", website.merchant_name)
        service = MonitorBcService()
        url = service.get_merchant_url(str(batch_num), merchant_name=website.merchant_name)
        logger.info("get qichacha url  : %s", str(url))
        if url is not None:
            try:
                service.inspect(str(batch_num), "https://www.qichacha.com" + url, website.merchant_name,
                                website.legal_person)
                print()
            except Exception as e:
                logger.info(e)
                pass
        logger.info("qichacha monitor  done!merchantName : %s", website.merchant_name)
