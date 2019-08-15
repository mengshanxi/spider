from model.models import Weburl
from service.accessible_service import AccessibleService
from service.monitor_weburl_service import MonitorWeburlService


class TestEs(object):
    if __name__ == "__main__":
        monitor_url_service = MonitorWeburlService()
        weburl= Weburl(website_name='深圳市荣格科技有限公司',url='http:/szrgsh.com/index.html')
        monitor_url_service.monitor_website(weburl,'1')
