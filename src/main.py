# coding:utf-8
import urllib.request

from bs4 import BeautifulSoup
from flask import Flask
from flask import request

from src.config.mylog import logger
from src.manager.ims_api import ImsApi
from src.manager.spider_manager import SpiderManager
from src.service.webdriver_util import WebDriver
import threading
import src.util.globalvar as gl

app = Flask(__name__)


@app.route('/api/v1/test/chrome', methods=['GET'])
def test():
    driver = WebDriver.get_phantomJS()
    driver.get("http://baidu.com")
    source = driver.page_source
    driver.quit()
    print(source)
    return str(driver.title)


@app.route('/api/v1/verify_cookie', methods=['POST'])
def verify_cookie():
    if request.method == 'POST':
        driver = WebDriver.get_phantomJS_withcookie()
        url = "https://www.qichacha.com/search?key=" + urllib.parse.quote("天津融宝支付网络有限公司")
        driver.get(url)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        tbodys = soup.find_all('tbody')
        trs = tbodys[0].find_all('tr')
        tds = trs[0].find_all('td')
        a = tds[1].find_all('a')
        name = a[0].get_text().strip()
        if name == "天津融宝支付网络有限公司".strip():
            href = a[0].get('href')
            if href != 'NONE':
                driver.get("https://www.qichacha.com" + href)
                source = driver.page_source

                soup = BeautifulSoup(source, 'html.parser')
                title = soup.find(name="title").get_text()
                driver.quit()
                if (str(title) == "会员登录 - 企查查"):
                    return "false"
                else:
                    return "true"
            driver.quit()

        else:
            driver.quit()
            return "false"


'''
爬取数据
'''


@app.route('/api/v1/spider/execute', methods=['POST'])
def execute():
    try:
        task_id = request.form['taskId']
        batch_num = request.form['batchNum']
        logger.info("inspect, taskId: %s" % str(task_id))

        gl.set_value(str(task_id), batch_num)

        t = threading.Thread(target=inspect, args=(task_id, batch_num,))
        t.setDaemon(True)
        t.start()

        return 'OK'
    except Exception as e:
        logger.error(e)


def inspect(task_id, batch_num):
    spider_manager = SpiderManager()
    if gl.check_by_task(task_id):
        spider_manager.inspect(task_id, batch_num)
        logger.info("inspect done!  taskId:%s" % str(task_id))

    if gl.check_by_task(task_id):
        ims_interface = ImsApi()
        ims_interface.create_report(task_id, batch_num)
        logger.info("trigger ims to create port!  taskId: %s,batch_num: %s" % (str(task_id), str(batch_num)))


@app.route('/api/v1/spider/stop', methods=['POST'])
def stop():
    try:
        task_id = request.form['taskId']
        if gl.get_value(task_id) is not None:
            batch_num = gl.get_value(task_id)
            gl.remove(task_id)
            return batch_num
        return 'KeyError'
    except KeyError as e:
        print(e)
        return 'KeyError'


"""
def execute_task():
    logger.info("inspect auto...")
    spider_manager = SpiderManager()
    spider_manager.inspect_all_auto()
    logger.info("inspect auto done!")


@app.route('/api/v1/spider/start_task', methods=['GET'])
def start_task():
    logger.info("schedule task start")
    schedule.every().day.at("01:00").do(execute_task)
    while True:
        logger.info("wait to execute...")
        time.sleep(30)
        schedule.run_pending()
        time.sleep(1)
"""

if __name__ == '__main__':
    gl.init()
    app.run(debug=True)
