import os

import datetime

from bs4 import BeautifulSoup

from config.mylog import logger
from dao.tracking_detail_dao import TrackingDetailDao
from service.snapshot_service import SnapshotService
from service.strategy_service import StrategyService
from service.webdriver_util import WebDriver

if __name__ == "__main__":
    a=["1","2","3"]
    b=a[0:1]
    print(b.__len__())