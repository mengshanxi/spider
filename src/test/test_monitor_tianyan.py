import urllib.request

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from src.config.config_load import phantomjs_path


class TestQichachaService(object):
    if __name__ == "__main__":
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        headers = {
            }
        for key, value in headers.items():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(executable_path=phantomjs_path,
                                     desired_capabilities=desired_capabilities,
                                     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        merchant_name = urllib.parse.quote("小金袋")
        driver.get("https://www.baidu.com/s?ie=utf-8&newi=1&mod=1&isbd=1&isid=b1fc888a000073cc&wd=%E4%BA%AC%E4%B8%9C&rsv_spt=1&rsv_iqid=0x9355389400007f54&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&oq=%25E4%25BA%25AC%25E4%25B8%259C&rsv_t=29d2BSIDqkKmg7EfrEsdF%2FTE6eG%2Fy0VCd2y1KOpte3%2BvxltXwQprYLWnaEdv0QWM0ZzE&rsv_pq=b1fc888a000073cc&bs=%E4%BA%AC%E4%B8%9C&rsv_sid=1421_21081_26350_20930&_ss=1&clist=35c0f81e8bc230c4&hsug=&f4s=1&csor=2&_cr1=33111");
        source = driver.page_source
        print(source)
