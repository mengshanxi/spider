# coding:utf-8
import signal
import threading

import os
from flask import Flask
from flask import request

import config.global_val as gl
from config.mylog import logger
from dao.tracking_task_dao import TrackingTaskDao
from manager.gather_center import GatherCenter
from manager.ims_api import ImsApi
from service.monitor_bc_service import MonitorBcService
from service.monitor_tracking_service import MonitorTrackingService
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
    job = os.environ['job']
    logger.info(job)
    if job == "bc" or job == "other":
        gl.set_value('STATUS', True)
        ims_api.heartbeat()
        try:
            batch_num = request.form['batchNum']
            logger.info("spider begin batchNum: %s" % str(batch_num))
            t = threading.Thread(target=inspect, args=(batch_num,))
            t.setDaemon(True)
            t.start()
            return 'OK'
        except Exception as e:
            logger.error(e)
    else:
        logger.info("spider is not my job!")
        return 'OK'


def restart_selenium():
    logger.info("restart_selenium...")
    out = os.popen("ps aux | grep selenium").read()
    logger.info(out.splitlines())
    for line in out.splitlines():
        logger.info(line)
        if 'selenium' in line:
            pid = int(line.split()[1])
            try:
                logger.info(pid)
                result = os.kill(pid, signal.SIGKILL)
                logger.info('已杀死pid为%s的进程,　返回值是:%s' % (pid, result))
            except OSError:
                logger.info('没有如此进程!!!')
    os.popen("nohup /opt/bin/start-selenium-standalone.sh &").read()


@app.route('/tracking/execute', methods=['POST'])
def tracking_execute():
    job = os.environ['job']
    if job == "tracking":
        # 重启selenium
        restart_selenium()
        gl.set_value('STATUS', True)
        ims_api.heartbeat()
        try:
            task_id = request.form['taskId']
            status = request.form['status']
            logger.info("tracking begin task_id: %s,status: %s" % (str(task_id), str(status)))
            t = threading.Thread(target=inspect_tracking, args=(task_id, status))
            t.setDaemon(True)
            t.start()
            return 'OK'
        except Exception as e:
            logger.error(e)
    else:
        logger.info("Tracking is not my job!")
        return 'OK'


def inspect_tracking(task_id, status):
    tracking_service = MonitorTrackingService()
    while gl.get_value('STATUS'):
        logger.info("tracking task start!  task_id:%s" % str(task_id))
        tracking_service.monitor(task_id, status)
        logger.info("tracking task end!  task_id:%s" % str(task_id))
    task_dao = TrackingTaskDao()
    task_dao.close_task(task_id)
    logger.info("tracking task end!  task_id:%s" % str(task_id))


def inspect(batch_num):
    spider_manager = GatherCenter()
    while gl.get_value('STATUS'):
        logger.info("gather task start!  batch_num:%s" % str(batch_num))
        spider_manager.gather(batch_num)
        logger.info("gather task end!  batch_num:%s" % str(batch_num))
    logger.info("batchNum gather task end!  batch_num:%s" % str(batch_num))


@app.route('/spider/gather_urls', methods=['POST'])
def gather_urls():
    job = os.environ['job']
    if job == "gather":
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
    else:
        logger.info("Gather is not my job!")
        return 'SUCCESS'


@app.route('/spider/stop', methods=['POST'])
def stop():
    job = os.environ['job']
    if job == "gather":
        logger.info("My Job is gather,ignore the order!")
    else:
        gl.set_value('STATUS', False)
        ims_api.heartbeat()
        return 'SUCCESS'


def heartbeat():
    ims_api.heartbeat()
    timer = threading.Timer(10, heartbeat)
    timer.start()


if __name__ == '__main__':
    ims_api.register()
    timer = threading.Timer(60, heartbeat)
    timer.start()
    app.run(debug=True, host='0.0.0.0')
