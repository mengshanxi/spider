# import pytesseract
from PIL import Image

from config.mylog import logger


class PicRecgService:

    @staticmethod
    def tran2text(url):
        # TODO
        logger.error("TODO %s" % url)
        return None
        try:
            if str(url).endswith(".jpg") or str(url).endswith(".png") or str(url).endswith(".bmp") or str(url).endswith(
                    ".jpeg"):
                logger.info("src path: %s" % url)
                text = pytesseract.image_to_string(Image.open(url), lang='chi_sim')
                logger.info("text: %s", str(text))
                if text == "":
                    return None
                return text
            else:
                logger.error("url is not pic! url:%s" % url)
                return None
        except Exception as e:
            logger.error(e)
            return None
