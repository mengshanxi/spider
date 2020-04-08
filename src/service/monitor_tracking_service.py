import datetime
import json
import time

import config.global_val as gl
from config.mylog import logger
from dao.tracking_detail_dao import TrackingDetailDao
from manager.ims_api import ImsApi
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver

"""
快递单号巡检
"""


class MonitorTrackingService:

    @staticmethod
    def monitor(task_id, status):
        ims_api = ImsApi()
        tracking_dao = TrackingDetailDao()
        status_dict = {'0': '查询中', '1': '查询不到', '2': '运输途中', '3': '到达待取', '4': '成功签收', '5': '运输过久',
                       '6': '投递失败', '7': '可能异常'}
        normal_status_dict = {'0': '查询中', '1': '查询不到', '2': '运输途中', '3': '到达待取', '4': '成功签收', '5': '运输过久'}
        tracking_details = tracking_dao.get_by_task(task_id, status)
        if tracking_details.__len__() > 0:
            try:
                driver = WebDriver.get_chrome()
                driver.get("https://www.trackingmore.com/login-cn.html")
                driver.find_element_by_id("email").send_keys("rujiahua@payeasenet.com")
                driver.find_element_by_id("password").send_keys("0418YXYwlx")
                driver.find_element_by_id("login_test").click()
                time.sleep(5)
                for tracking_detail in tracking_details:
                    if gl.get_value('TRACKING_STATUS'):
                        pass
                    else:
                        logger.info("快递单任务已停止，任务id：%s", task_id)
                        gl.set_value('STATUS', False)
                        gl.set_value('TRACKING_STATUS', False)
                        ims_api.done_tracking(task_id)
                        return
                    tracking_detail.start_time = datetime.datetime.now()
                    tracking_detail.status = "done"
                    logger.info("准备检查单号:%s ", tracking_detail.tracking_num)
                    try:
                        driver.get(
                            "https://my.trackingmore.com/numbers.php?lang=cn&p=1&keywordType=trackNumber&searchnumber="
                            + tracking_detail.tracking_num)
                        driver.maximize_window()
                        time.sleep(3)
                        # driver.find_element_by_class_name("show_lastEvent").click()
                        driver.find_element_by_id('trackItem_0').click()
                        time.sleep(1)
                        snapshot = SnapshotService.snapshot_tracking(driver, tracking_detail)
                        url = "https://my.trackingmore.com/data/data-numbers.php?lang=cn&action=get_my_number" \
                              "&source=2&where=lang%3Dcn%26p%3D1%26keywordType%3DtrackNumber%26searchnumber%3D" \
                              + tracking_detail.tracking_num + "&page=1"
                        driver.get(url)
                        json_data = driver.find_element_by_tag_name("body").text
                        json_obj = json.loads(str(json_data))
                        status = json_obj['data'][0]['track_status']
                        tracking_detail.des = status_dict[status]
                        tracking_detail.end_time = datetime.datetime.now()
                        tracking_detail.url = ""
                        tracking_detail.snapshot = snapshot
                        if status in normal_status_dict:
                            logger.info("单号巡检状态:%s", status)
                            tracking_detail.result = "true"
                        else:
                            tracking_detail.result = "false"
                        tracking_dao.update(tracking_detail)
                    except Exception as e:
                        logger.error(e)
                        tracking_detail.result = "false"
                        tracking_detail.des = "检测疑似异常，建议手动验证！"
                        tracking_detail.end_time = datetime.datetime.now()
                        tracking_detail.url = ""
                        tracking_detail.snapshot = ""
                        tracking_dao.update(tracking_detail)
                        time.sleep(600)
            except Exception as e:
                logger.error(e)
                tracking_detail.result = "false"
                tracking_detail.des = "检测疑似异常，建议手动验证！"
                tracking_detail.end_time = datetime.datetime.now()
                tracking_detail.url = ""
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
