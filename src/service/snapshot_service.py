import time
from urllib import request

from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from config.config_load import base_filepath, ims_rest_base
from config.mylog import logger
from dao.third_config_dao import ThirdConfigDao
from service.webdriver_util import WebDriver


class SnapshotService:

    @staticmethod
    def create_snapshot(driver, batch_num, website, senti_type):
        timestamp = int(time.time())
        snapshot = batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_" + senti_type + "_" + str(
            timestamp) + ".png"
        path = base_filepath + "/" + batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_" + senti_type + "_" + str(
            timestamp)
        try:
            driver.save_screenshot(path + ".png")
            im = Image.open(path + ".png")
            im_resize = im.resize((50, 50), Image.ANTIALIAS)
            im_resize.save(path + "_thumb.bmp")
        except Exception as e:
            logger.info(e)
            return snapshot
        return snapshot

    def snapshot_weburl(driver, batch_num, weburl, senti_type):
        timestamp = int(time.time())
        snapshot = batch_num + "_" + weburl.merchant_name + "_" + weburl.merchant_num + "_" + senti_type + "_" + str(
            timestamp) + ".png"
        path = base_filepath + "/" + batch_num + "_" + weburl.merchant_name + "_" + weburl.merchant_num + "_" + senti_type + "_" + str(
            timestamp)
        try:
            driver.save_screenshot(path + ".png")
            im = Image.open(path + ".png")
            im_resize = im.resize((50, 50), Image.ANTIALIAS)
            im_resize.save(path + "_thumb.bmp")
        except Exception as e:
            logger.info(e)
            return snapshot
        return snapshot

    @staticmethod
    def snapshot_qichacha(batch_num, url, website):
        timestamp = int(time.time())
        snapshot = batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_工商_" + str(
            timestamp) + ".png"
        path = base_filepath + "/" + batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_工商_" + str(
            timestamp)
        try:
            dcap = dict(DesiredCapabilities.PHANTOMJS.copy())
            third_config_dao = ThirdConfigDao()
            cookie = third_config_dao.get_by_name("qichacha")
            headers = {
                'cookie': cookie,
                'Host': 'www.qichacha.com',
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
            for key, value in headers.items():
                dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
            driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs",
                                         desired_capabilities=dcap,
                                         service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'],
                                         service_log_path="/home/seluser/logs/phantomjs.log")

            driver.set_page_load_timeout(10)
            driver.set_script_timeout(10)
            driver.maximize_window()
            driver.get(url)
            driver.save_screenshot(path + ".png")
            img = Image.open(path + ".png")
            jpg = img.crop((265, 158, 420, 258))
            jpg.save(path + "_thumb.bmp")
            return driver, snapshot
        except Exception as e:
            logger.info(e)
            return None, None

    @staticmethod
    def snapshot_tracking(driver, tracking_detail):
        timestamp = int(time.time())
        path = base_filepath + "/" + tracking_detail.tracking_num + "_" + str(
            timestamp)
        snapshot = tracking_detail.tracking_num + "_" + str(timestamp) + ".png"
        try:
            driver.save_screenshot(path + ".png")
            im = Image.open(path + ".png")
            im_resize = im.resize((50, 50), Image.ANTIALIAS)
            im_resize.save(path + "_thumb.bmp")
        except Exception as e:
            logger.info(e)
            return snapshot
        return snapshot

    @staticmethod
    def simulation_404(url):
        timestamp = str(time.time())
        snapshot = timestamp + ".png"
        path = ims_rest_base + "/views/system/404.jsp?url=" + str(url)
        img_404 = base_filepath + "/" + timestamp
        try:
            driver = WebDriver.get_chrome()
            driver.get(path)
            driver.save_screenshot(img_404 + ".png")
            im = Image.open(img_404 + ".png")
            im_resize = im.resize((50, 50), Image.ANTIALIAS)
            im_resize.save(img_404 + "_thumb.bmp")
        except Exception as e:
            logger.info(e)
            return snapshot
        return snapshot

    @staticmethod
    def download(jpg_link):
        timestamp = int(time.time())
        path = base_filepath + "/" + str(timestamp) + ".png"
        try:
            request.urlretrieve(jpg_link, path)
        except Exception as e:
            logger.info(e)
            return None
        return path
