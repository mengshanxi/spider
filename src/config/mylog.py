# -*- coding: utf-8 -*-
import logging
import logging.config
import socket
from logging.handlers import TimedRotatingFileHandler
import os
import time

# logging初始化工作
logging.basicConfig(level=logging.INFO)
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = '/home/seluser/logs/'


def get_logger():
    hostname = socket.gethostname()
    loggers = logging.getLogger("Log")
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)
    data_format = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    log_file_path = rootPath + str(hostname) + "_spider_" + data_format + '.log'
    file_log = TimedRotatingFileHandler(log_file_path,
                                        when="S",
                                        interval=10,
                                        backupCount=4)
    file_log.setLevel(logging.INFO)
    console_fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    file_fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console_log.setFormatter(console_fmt)
    file_log.setFormatter(file_fmt)

    loggers.addHandler(console_log)
    # loggers.addHandler(file_log)
    return loggers


logger = get_logger()
