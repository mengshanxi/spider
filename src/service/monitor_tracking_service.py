import datetime
import random
import time

from bs4 import BeautifulSoup

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
                    time.sleep(strategy.frequency)
                random_seconds = random.randint(10, 15)
                logger.info("快递单检测随机等待 %s 秒...", str(random_seconds))
                time.sleep(random_seconds)
                tracking_detail.start_time = datetime.datetime.now()
                tracking_detail.status = "done"
                logger.info("准备检查单号:%s ", tracking_detail.tracking_num)
                url = "https://www.trackingmore.com/cn/" + tracking_detail.tracking_num
                logger.info("url:%s ", url)
                driver = WebDriver.get_phantomjs()
                try:
                    driver.get(url)
                except Exception as e:
                    logger.error(e)
                    tracking_detail.result = "true"
                    tracking_detail.des = "检测超时,建议手动验证:" + url
                    tracking_detail.end_time = datetime.datetime.now()
                    tracking_detail.url = url
                    tracking_detail.snapshot = ""
                    tracking_dao.update(tracking_detail)
                    logger.info("单号巡检发生异常，跳过")
                    driver.quit()
                    continue

                try:
                    source = driver.page_source
                    soup = BeautifulSoup(source, 'html.parser')
                    snapshot = SnapshotService.snapshot_tracking(driver, tracking_detail)
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
                                    items = soup.find_all(attrs={'class': 'line-gutter-backdrop'})
                                    # 异常为0
                                    if items.__len__() != 0:
                                        tracking_detail.result = "false"
                                        tracking_detail.des = "爬虫请求疑似被拦截，建议手动验证!"
                                        tracking_detail.end_time = datetime.datetime.now()
                                        tracking_detail.url = url
                                        tracking_detail.snapshot = snapshot
                                    else:
                                        soup = BeautifulSoup(source, 'html.parser')
                                        item_length = soup.find_all("li", attrs={'class': 's-packStatst'}).__len__()
                                        if item_length > 0:
                                            tracking_detail.result = "true"
                                            tracking_detail.des = "物流正常"
                                            tracking_detail.end_time = datetime.datetime.now()
                                            tracking_detail.url = url
                                            tracking_detail.snapshot = snapshot
                                        else:
                                            tracking_detail.result = "false"
                                            tracking_detail.des = "没有查询到物流信息"
                                            tracking_detail.end_time = datetime.datetime.now()
                                            tracking_detail.url = url
                                            tracking_detail.snapshot = snapshot
                                except Exception as e:
                                    print(e)
                                    # 正常
                                    tracking_detail.result = "false"
                                    tracking_detail.des = "检测疑似异常，建议手动验证！"
                                    tracking_detail.end_time = datetime.datetime.now()
                                    tracking_detail.url = url
                                    tracking_detail.snapshot = snapshot
                                break
                            else:
                                continue
                        if not has_tracking:
                            tracking_detail.result = "false"
                            tracking_detail.des = "提供的单号-快递公司关系疑似不匹配"
                            tracking_detail.end_time = datetime.datetime.now()
                            tracking_detail.url = url
                            tracking_detail.snapshot = snapshot

                    else:
                        item_length = soup.find_all("dd", attrs={'class': 'post_message'})
                        if item_length.__len__() > 0:
                            tracking_detail.result = "true"
                            tracking_detail.des = "巡检正常"
                            tracking_detail.end_time = datetime.datetime.now()
                            tracking_detail.url = url
                            tracking_detail.snapshot = snapshot
                        else:
                            tracking_detail.result = "false"
                            tracking_detail.des = "没有查询物流信息"
                            tracking_detail.end_time = datetime.datetime.now()
                            tracking_detail.url = url
                            tracking_detail.snapshot = snapshot
                    tracking_dao.update(tracking_detail)
                except Exception as e:
                    logger.error(e)
                    tracking_detail.result = "false"
                    tracking_detail.des = "检测疑似异常，建议手动验证！"
                    tracking_detail.end_time = datetime.datetime.now()
                    tracking_detail.url = url
                    tracking_detail.snapshot = ""
                    tracking_dao.update(tracking_detail)
                finally:
                    driver.quit()
            else:
                logger.info("单号任务没有需要检索的单号，任务id：%s，单号状态: %s", task_id, status)
                gl.set_value('STATUS', False)
                gl.set_value('TRACKING_STATUS', False)
            ims_api.done_tracking(task_id)
            gl.set_value('STATUS', False)
            gl.set_value('TRACKING_STATUS', False)
