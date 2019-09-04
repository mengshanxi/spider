# coding:utf-8
import os
import threading

from flask import Flask
from flask import request

import config.global_val as gl
from config.mylog import logger
from manager.gather_center import GatherCenter
from manager.ims_api import ImsApi
from service.monitor_bc_service import MonitorBcService
from service.weburl_service import WeburlService

app = Flask(__name__)
gl._init()

# 定义跨模块全局变量
gl.set_value('STATUS', False)
ims_api = ImsApi()


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
    os.environ['browser'] = '172.17.161.230'
    os.environ['port'] = '8911'
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
        # task_id = request.form['taskId']
        gl.set_value('STATUS', True)
        weburl_service = WeburlService()
        weburl_service.gather_urls_by_task(None)
        gl.set_value('STATUS', False)
        return 'SUCCESS'
    except KeyError as e:
        print(e)
        return 'ERROR'


@app.route('/spider/stop', methods=['POST'])
def stop():
    gl.set_value('STATUS', False)
    return 'SUCCESS'


def heartbeat():
    ims_api.heartbeat()
    timer = threading.Timer(30, heartbeat)
    timer.start()


if __name__ == '__main__':
    ims_api.register()
    timer = threading.Timer(60, heartbeat)
    timer.start()
    app.run(debug=True, host='0.0.0.0')
