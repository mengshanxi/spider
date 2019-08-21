from PIL import Image
from selenium.webdriver.common.keys import Keys

from model.models import Weburl
from service.accessible_service import AccessibleService
from service.monitor_bc_service import MonitorBcService
from service.monitor_weburl_service import MonitorWeburlService
from service.webdriver_util import WebDriver


class TestEs(object):
    if __name__ == "__main__":
        service = MonitorBcService()
        url = service.get_merchant_url(str(1), merchant_name='河北纷橙电子商务有限公司')
        if url is not None:
            try:
                service.inspect(str(1), "https://www.qichacha.com" + url, '河北纷橙电子商务有限公司',
                                '靳建通')
            except Exception as e:
                pass
