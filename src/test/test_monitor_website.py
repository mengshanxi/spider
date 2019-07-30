# coding:utf-8

import util.globalvar as gl
from manager.spider_manager import SpiderManager

gl.set_value(str(23), 11)
SpiderManager.inspect(23,11)
