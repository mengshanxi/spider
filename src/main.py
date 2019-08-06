# coding:utf-8
import threading

import time
from flask import Flask
from flask import request
from config.mylog import logger
from manager.gather_center import GatherCenter
from manager.ims_api import ImsApi
from service.monitor_bc_service import MonitorBcService
from service.webdriver_util import WebDriver
from service.weburl_service import WeburlService
import config.global_val as gl

app = Flask(__name__)
gl._init()

# 定义跨模块全局变量
gl.set_value('STATUS', True)
ims_api = ImsApi()


@app.route('/test/chrome', methods=['GET'])
def test():
    driver = WebDriver.get_phantomjs()
    driver.get("http://baidu.com")
    title = driver.title
    return str(title)


@app.route('/verify_cookie', methods=['POST'])
def verify_cookie():
    monitor_bc_service = MonitorBcService()
    # return monitor_bc_service.check_cookie()
    return "SUCCESS"


'''
爬取数据
'''


@app.route('/spider/execute', methods=['POST'])
def execute():
    gl.set_value('STATUS', True)
    try:
        batch_num = request.form['batchNum']
        logger.info("spider begin batchNum: %s" % str(batch_num))
        t = threading.Thread(target=inspect, args=(batch_num,))
        t.setDaemon(True)
        t.start()
        return 'OK'
    except Exception as e:
        logger.error(e)


def inspect(batch_num):
    spider_manager = GatherCenter()
    while gl.get_value('STATUS'):
        logger.info("gather task start!  batch_num:%s" % str(batch_num))
        spider_manager.gather(batch_num)
        logger.info("gather task end!  batch_num:%s" % str(batch_num))
    logger.info("batchNum gather task end!  batch_num:%s" % str(batch_num))


@app.route('/spider/gather_urls', methods=['POST'])
def gather_urls():
    try:
        task_id = request.form['taskId']
        weburl_service = WeburlService()
        weburl_service.gather_urls_by_task(task_id)
        return 'SUCCESS'
    except KeyError as e:
        print(e)
        return 'ERROR'


@app.route('/spider/stop', methods=['POST'])
def stop():
    gl.set_value('STATUS', False)
    return 'SUCCESS'


def run(interval):
    while True:
        try:
            # sleep for the remaining seconds of interval
            time_remaining = interval - time.time() % interval
            time.sleep(time_remaining)
            # execute the command
            ims_api.heartbeat()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ims_api.register()
    run(60)
    app.run(debug=True, host='0.0.0.0')
