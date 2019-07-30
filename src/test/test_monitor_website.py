# coding:utf-8

from src.service.monitor_website_service import MonitorWebsiteService
from src.dao.monitor_website_dao import MonitorWebsiteDao
from src.manager.spider_manager import SpiderManager
import src.util.globalvar as gl

gl.set_value(str(23), 11)
SpiderManager.inspect(23,11)
