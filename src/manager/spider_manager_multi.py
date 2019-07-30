# -*-coding:utf-8-*-
import queue
import threading

import util.globalvar as gl
from config.mylog import logger
from service.inspect_service import InspectService
from service.monitor_senti_service import MonitorSentiService
from service.monitor_website_service import MonitorWebsiteService

exit_flag = 0
count = 0

thread_list = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5"]
queue_lock = threading.Lock()
work_queue = queue.Queue(200)


class SpiderThread(threading.Thread):
    def __init__(self, thread_id, name, task_id, batch_num, q):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.task_id = task_id
        self.batch_num = batch_num
        self.q = q

    def run(self):
        logger.info("开启线程：" + self.name)
        process_data(self.name, self.task_id, self.batch_num, self.q)
        logger.info("退出线程：" + self.name)


def process_data(thread_name, task_id, batch_num, q):
    global exit_flag
    global count
    while not exit_flag:
        queue_lock.acquire()
        if not work_queue.empty():
            website = q.get()
            queue_lock.release()

            count = count + 1
            logger.info("--------execute num:  %s --------" % count)

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
                    monitor_senti_service.monitor_senti(website["websiteName"], website["merchantName"], task_id,
                                                        batch_num)
                    monitor_senti_service.monitor_senti(website["merchantName"], website["merchantName"], task_id,
                                                        batch_num)
                    logger.info("sentiment monitor done!websiteName : %s", website["websiteName"])
                else:
                    logger.info("website name is empty,with merchantName! ")
                    monitor_senti_service = MonitorSentiService()
                    monitor_senti_service.monitor_senti(website["merchantName"], website["merchantName"], task_id,
                                                        batch_num)
                    logger.info("sentiment monitor done!merchantName : %s", website["merchantName"])

                # 工商监控
                '''
                logger.info("qichacha monitor  begin,merchantName : %s", website["merchantName"])
                service = MonitorBcService()
                url = service.get_merchant_url(str(batch_num), merchant_name=website["merchantName"])
                logger.info("get qichacha url  : %s", str(url))
                if url is not None:
                    try:
                        service.inspect(str(batch_num), "https://www.qichacha.com" + url, website["merchantName"],
                                        website["legalPerson"])
                        print()
                    except Exception as e:
                        logger.info(e)
                        pass

                logger.info("qichacha monitor  done!merchantName : %s", website["merchantName"])
                '''

            logger.info("%s processing %s" % (thread_name, website))

        else:
            queue_lock.release()
        logger.info("%s thread exit" % (thread_name))


class SpiderManager:

    def inspect(self, task_id, batch_num):

        thread_id = 1
        threads = []

        logger.info("service all urls for websites, begin...")
        inspect_service = InspectService()
        websites = inspect_service.get_websites(task_id)
        if websites is None:
            logger.info("get_websites return none! return !")
            return
        # 填充队列
        queue_lock.acquire()
        for website in websites:
            work_queue.put(website)
        queue_lock.release()

        # 创建新线程
        for tName in thread_list:
            thread = SpiderThread(thread_id, tName, task_id, batch_num, work_queue)
            thread.start()
            threads.append(thread)
            thread_id += 1

        # 等待队列清空
        while not work_queue.empty():
            pass

        # 通知线程是时候退出
        global exit_flag
        exit_flag = 1

        # 等待所有线程完成
        for t in threads:
            t.join()
        logger.info("退出主线程")
        exit_flag = 0
