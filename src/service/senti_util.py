from config.mylog import logger
from dao.keyword_dao import KeywordDao
from dao.monitor_third_dao import MonitorThirdDao
from model.monitor_third import MonitorThird
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver

"""
舆情处理工具
"""


class SentiUtil:

    @staticmethod
    def senti_process_text(platform, website_name, text, href, batch_num):

        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=chromedriver_path)
        """""

        driver = WebDriver.get_phantomJS()
        keyword_dao = KeywordDao()
        keywords = keyword_dao.get_keywords()
        monitor_third_dao = MonitorThirdDao()

        #  截图
        try:
            driver.get(href)
            snapshot = SnapshotService.create_snapshot(driver)
            is_normal = "正常"

            for keyword in keywords:
                index = text.find(keyword.name)
                monitor_third = MonitorThird()
                monitor_third.website_name = website_name
                monitor_third.batch_num = batch_num
                monitor_third.url = href
                monitor_third.type = platform
                if index != -1:
                    is_normal = "异常"
                    monitor_third.is_normal = is_normal
                    monitor_third.level = 3
                    monitor_third.outline = '检测到敏感词：' + str(keyword.name)
                    monitor_third.snapshot = snapshot

                    monitor_third_dao.add(monitor_third)
                else:
                    pass
            if is_normal == "正常":
                if platform == "百度百科":
                    monitor_third.level = 0
                    monitor_third.outline = '首页截图'
                    monitor_third.is_normal = is_normal
                    monitor_third.snapshot = snapshot
                    monitor_third_dao.add(monitor_third)
                pass

            # 关闭浏览器
            driver.quit()
        except Exception as e:
            logger.error(e)
            driver.quit()
            return

    @staticmethod
    def snapshot_home(platform, website_name, href, batch_num, driver):
        monitor_third_dao = MonitorThirdDao()

        #  截图
        try:
            snapshot = SnapshotService.create_snapshot(driver)
            is_normal = "正常"
            monitor_third = MonitorThird()
            monitor_third.website_name = website_name
            monitor_third.batch_num = batch_num
            monitor_third.url = href
            monitor_third.type = platform
            monitor_third.level = 0
            monitor_third.outline = '首页截图'
            monitor_third.is_normal = is_normal
            monitor_third.snapshot = snapshot
            monitor_third_dao.add(monitor_third)
            # 关闭浏览器
            driver.quit()
        except Exception as e:
            logger.error(e)
            driver.quit()
            return
