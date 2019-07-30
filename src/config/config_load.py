# encoding:utf-8
import os
import configparser

# 获取文件的当前路径（绝对路径）
cur_path = os.path.dirname(os.path.realpath(__file__))

# 获取config.ini的路径
config_path = os.path.join(cur_path, 'config.ini')

conf = configparser.ConfigParser()
conf.read(config_path, encoding="utf-8")

phantomjs_path = conf.get('dev', 'phantomjs_path')
host = conf.get('dev', 'host')
username = conf.get('dev', 'username')
password = conf.get('dev', 'password')
port = conf.get('dev', 'port')
database = conf.get('dev', 'database')
base_filepath = conf.get('dev', 'base_filepath')
chromedriver_path = conf.get('dev', 'chromedriver_path')
ims_rest_base = conf.get('dev', 'ims_rest_base')
