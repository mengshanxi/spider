# -*- coding: utf-8 -*-
import socket
import time

# logging初始化工作
#rootPath = '/home/seluser/logs/'

rootPath = 'D:/logs/'

import logging.handlers

logger = logging.getLogger()
logger.setLevel(logging.INFO)
hostname = socket.gethostname()
data_format = time.strftime('%Y-%m-%d', time.localtime(time.time()))
log_file_path = rootPath + str(hostname) + "_spider_" + data_format + '.log'
rht = logging.handlers.TimedRotatingFileHandler(log_file_path, 'D')
fmt = logging.Formatter("%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s  %(levelname)s - %(message)s",
                        "%Y-%m-%d %H:%M:%S")
rht.setFormatter(fmt)
console_log = logging.StreamHandler()
console_log.setLevel(logging.INFO)
console_fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console_log.setFormatter(console_fmt)
logger.addHandler(console_log)
logger.addHandler(rht)
