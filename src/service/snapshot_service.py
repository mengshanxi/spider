import time

from PIL import Image

from config.config_load import base_filepath, ims_rest_base
from config.mylog import logger
from urllib import request

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
