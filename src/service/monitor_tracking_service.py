import datetime

from bs4 import BeautifulSoup

import config.global_val as gl
from config.mylog import logger
from dao.tracking_detail_dao import TrackingDetailDao
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver

"""
快递单号巡检
"""


class MonitorTrackingService:

    @staticmethod
    def monitor(task_id, status):
        driver = WebDriver.get_chrome()
        try:
            tracking_dao = TrackingDetailDao()
            tracking_details = tracking_dao.get_by_task(task_id, status)
            if tracking_details.__len__() > 0:
                for tracking_detail in tracking_details:
                    # logger.info("检索单号:%s", tracking_detail.tracking_num)
                    tracking_detail.start_time = datetime.datetime.now()
                    tracking_detail.status = "done"
                    url = "https://www.trackingmore.com/cn/" + tracking_detail.tracking_num
                    driver.get(url)
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
                        tracking_detail.des = "没有查询到快递公司"
                        tracking_detail.end_time = datetime.datetime.now()
                        tracking_detail.url = url
                        tracking_detail.snapshot = snapshot
                    tracking_dao.update(tracking_detail)
            else:
                pass
                # gl.set_value('STATUS', False)
                # logger.info("单号任务没有需要检索的单号，任务id：%s，单号状态: %s", task_id, status)
        except Exception as e:
            logger.error(e)
            return
        finally:
            # gl.set_value('STATUS', False)
            driver.quit()
