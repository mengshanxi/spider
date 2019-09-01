import time

from PIL import Image

from config.config_load import base_filepath, ims_rest_base
from config.mylog import logger
from urllib import request

from service.webdriver_util import WebDriver


class SnapshotService:

    @staticmethod
    def create_snapshot(driver, batch_num, merchant_name, merchant_num, senti_type):
        timestamp = int(time.time())
        snapshot = batch_num + "_" + merchant_name + "_" + merchant_num + "_" + senti_type + "_" + str(
            timestamp) + ".png"
        path = base_filepath + "/" + batch_num + "_" + merchant_name + "_" + merchant_num + "_" + senti_type + "_" + str(
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
    def simulation_404(url):
        timestamp = int(time.time())
        snapshot = str(timestamp) + ".png"
        path = ims_rest_base + "system/404.jsp?url=" + str(url)
        img_404 = base_filepath + "/snapshots/" + timestamp + ".png"
        try:
            driver = WebDriver.get_chrome()
            driver.get(path)
            driver.save_screenshot(img_404)
            im = Image.open(img_404)
            im_resize = im.resize((641, 458))
            im_resize.save(path + ".png")
            im_resize = im.resize((50, 50), Image.ANTIALIAS)
            im_resize.save(path + "_thumb.bmp")
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
