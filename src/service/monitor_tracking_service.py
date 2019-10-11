import datetime

import time
from bs4 import BeautifulSoup
from selenium.webdriver.remote.command import Command

import config.global_val as gl
from config.mylog import logger
from dao.tracking_detail_dao import TrackingDetailDao
from manager.ims_api import ImsApi
from service.snapshot_service import SnapshotService
from service.strategy_service import StrategyService
from service.webdriver_util import WebDriver

"""
快递单号巡检
"""


class MonitorTrackingService:

    @staticmethod
    def monitor(task_id, status):
        driver = WebDriver.get_chrome()
        ims_api = ImsApi()
        tracking_dao = TrackingDetailDao()
        strategy_service = StrategyService()
        strategy = strategy_service.get_strategy()
        tracking_details = tracking_dao.get_by_task(task_id, status)
        if tracking_details.__len__() > 0:
            for tracking_detail in tracking_details:
                if gl.get_value('TRACKING_STATUS'):
                    pass
                else:
                    logger.info("快递单任务已停止，任务id：%s", task_id)
                    gl.set_value('STATUS', False)
                    gl.set_value('TRACKING_STATUS', False)
                    ims_api.done_tracking(task_id)
                    return
                if strategy.frequency == 0 or strategy.frequency is None:
                    logger.info("未设置爬取频率限制,继续执行任务..")
                else:
                    logger.info("爬取频率限制为:%s 秒", strategy.frequency)
                    # time.sleep(strategy.frequency)
                tracking_detail.start_time = datetime.datetime.now()
                tracking_detail.status = "done"
                url = "https://www.trackingmore.com/cn/" + tracking_detail.tracking_num
                try:
                    driver.get(url)
                except Exception as e:
                    logger.error(e)
                    tracking_detail.result = "true"
                    tracking_detail.des = "检测超时"
                    tracking_detail.end_time = datetime.datetime.now()
                    tracking_detail.url = url
                    tracking_detail.snapshot = ""
                    tracking_dao.update(tracking_detail)
                    logger.info("单号巡检发生异常，跳过:%s 秒", )
                    continue
                try:
                    source = driver.page_source
                    soup = BeautifulSoup(source, 'html.parser')
                    a_tags = soup.find_all("a", attrs={'class': 'ulliselect'})
                    has_tracking = False
                    if a_tags.__len__() > 0:
                        for a_tag in a_tags:
                            if a_tag.get_text().strip() == tracking_detail.tracking_name:
                                has_tracking = True
                                url = "http:" + a_tag.get("href")
                                driver.get(url)
                                snapshot = SnapshotService.snapshot_tracking(driver, tracking_detail)
                                try:
                                    source = driver.page_source
                                    soup = BeautifulSoup(source, 'html.parser')
                                    soup.find_all("li", attrs={'class': 's-packStatst'})
                                    tracking_detail.result = "false"
                                    tracking_detail.des = "没有查询到物流信息"
                                    tracking_detail.end_time = datetime.datetime.now()
                                    tracking_detail.url = url
                                    tracking_detail.snapshot = snapshot
                                except Exception as e:
                                    print(e)
                                    # 正常
                                    tracking_detail.result = "true"
                                    tracking_detail.des = "物流正常"
                                    tracking_detail.end_time = datetime.datetime.now()
                                    tracking_detail.url = url
                                    tracking_detail.snapshot = snapshot
                                break
                            else:
                                continue
                        if not has_tracking:
                            snapshot = SnapshotService.snapshot_tracking(driver, tracking_detail)
                            tracking_detail.result = "false"
                            tracking_detail.des = "提供的单号-快递公司关系疑似不匹配"
                            tracking_detail.end_time = datetime.datetime.now()
                            tracking_detail.url = url
                            tracking_detail.snapshot = snapshot

                    else:
                        snapshot = SnapshotService.snapshot_tracking(driver, tracking_detail)
                        tracking_detail.result = "false"
                        tracking_detail.des = "没有查询物流信息"
                        tracking_detail.end_time = datetime.datetime.now()
                        tracking_detail.url = url
                        tracking_detail.snapshot = snapshot
                    tracking_dao.update(tracking_detail)
                except Exception as e:
                    logger.error(e)
                    snapshot = SnapshotService.snapshot_tracking(driver, tracking_detail)
                    tracking_detail.result = "true"
                    tracking_detail.des = "巡检正常"
                    tracking_detail.end_time = datetime.datetime.now()
                    tracking_detail.url = url
                    tracking_detail.snapshot = snapshot
                    tracking_dao.update(tracking_detail)
            else:
                logger.info("单号任务没有需要检索的单号，任务id：%s，单号状态: %s", task_id, status)
                gl.set_value('STATUS', False)
                gl.set_value('TRACKING_STATUS', False)
            driver.quit()
            ims_api.done_tracking(task_id)
            gl.set_value('STATUS', False)
            gl.set_value('TRACKING_STATUS', False)
