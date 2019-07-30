# -*- coding: utf-8 -*-
import logging
import logging.config
from os import path

# logging初始化工作

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'server.log')
logging.basicConfig(level=logging.INFO,
                    filemode='a',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='server.log')


def get_logger():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logger = logging.getLogger('')
    logger.addHandler(console)

    return logger


logger = get_logger()
