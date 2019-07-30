import time

from PIL import Image

from config.config_load import base_filepath
from config.mylog import logger
from urllib import request


class SnapshotService:

    @staticmethod
    def create_snapshot(driver):
        timestamp = int(time.time())
        snapshot = str(timestamp) + ".png"
        path = base_filepath + "/imgs/" + str(timestamp)
        try:
            driver.save_screenshot(path + ".png")
            im = Image.open(path + ".png")
            im_resize = im.resize((50, 50), Image.ANTIALIAS)
            im_resize.save(path + "_thumb.bmp")
        except Exception as e:
            logger.info(e)
            driver.quit()
            return snapshot
        return snapshot

    @staticmethod
    def simulation_404():
        timestamp = int(time.time())
        snapshot = str(timestamp) + ".png"
        path = base_filepath + "/imgs/" + str(timestamp)
        img_404 = base_filepath + "/template/404.png"
        try:
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
        path = base_filepath + "/imgs/" + str(timestamp) + ".png"
        try:
            request.urlretrieve(jpg_link, path)
        except Exception as e:
            logger.info(e)
            return None
        return path
