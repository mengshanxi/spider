# coding:utf-8
import threading

from flask import Flask
from flask import request

from config.mylog import logger
from manager.gather_center import GatherCenter
from service.monitor_bc_service import MonitorBcService
from service.webdriver_util import WebDriver
from service.weburl_service import WeburlService

app = Flask(__name__)
global status
status = True


@app.route('/api/v1/test/chrome', methods=['GET'])
def test():
    driver = WebDriver.get_phantomJS()
    driver.get("http://baidu.com")
    title = driver.title
    return str(title)


@app.route('/api/v1/verify_cookie', methods=['POST'])
def verify_cookie():
    monitor_bc_service = MonitorBcService()
    return monitor_bc_service.check_cookie()


'''
爬取数据
'''


@app.route('/api/v1/spider/execute', methods=['POST'])
def execute():
    global status
    status = True
    try:
        task_id = request.form['taskId']
        batch_num = request.form['batchNum']
        logger.info("inspect, taskId: %s" % str(task_id))
        t = threading.Thread(target=inspect, args=(task_id, batch_num,))
        t.setDaemon(True)
        t.start()
        return 'OK'
    except Exception as e:
        logger.error(e)


def inspect(task_id, batch_num):
    spider_manager = GatherCenter()
    while status:
        logger.info("gather start!  taskId:%s" % str(task_id))
        spider_manager.gather(task_id, batch_num)
        logger.info("gather end!  taskId:%s" % str(task_id))


@app.route('/api/v1/spider/gather_urls', methods=['POST'])
def gather_urls():
    try:
        task_id = request.form['taskId']
        weburl_service = WeburlService()
        weburl_service.gather_urls_by_task(task_id)
        return 'KeyError'
    except KeyError as e:
        print(e)
        return 'KeyError'


@app.route('/api/v1/spider/stop', methods=['POST'])
def stop():
    global status
    status = False
    return 'SUCCESS'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
