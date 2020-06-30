# coding:utf-8
import http
from time import sleep

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from model.models import Website
from service.snapshot_service import SnapshotService


def editUserAgent():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
    driver = webdriver.PhantomJS(executable_path="D:/software/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                                 desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                               '--load-images=false'])
    try:
        url = "www.gragreati.com"
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        website = Website()
        website.domain_name=url
        if website.domain_name is None or len(website.domain_name) == 0:
            return
        else:
            pass
        # 首页监控
        domain_names = str(website.domain_name)
        domain_name_list = domain_names.split(",")
        for domain_name in domain_name_list:
            domain_name_rich = domain_name
            dns = domain_name
            if str(domain_name).startswith("http"):
                temp = domain_name[domain_name.find("/") + 2:]
                if str(temp).find("/") == -1:
                    dns = temp
                else:
                    start = temp.find("/")
                    dns = temp[0:start]
            else:
                if str(domain_name).find("/") == -1:
                    pass
                else:
                    start = domain_name.find("/")
                    dns = domain_name[0:start]
                pass
                domain_name_rich = "http://" + domain_name
            try:
                conn = http.client.HTTPSConnection(dns, timeout=10)
                conn.request('GET', domain_name_rich)
                resp = conn.getresponse()
                code = resp.code
            except Exception as e:
                if str(e).find("timed out") == -1:
                    pass
                else:
                    continue
            try:
                driver.get(domain_name_rich)
                current_url = driver.current_url
                title = driver.title
                source = driver.page_source
                snapshot = SnapshotService.create_snapshot(driver, "", website, '网站')
                if str(current_url) == "about:blank" and str(
                        source) == "<html><head></head><body></body></html>" and str(title) == "":
                    driver.quit()
                    continue
                else:
                    pass
                if str(current_url).find(dns) == -1:
                    driver.quit()
                    continue
                else:
                    pass
            except Exception as e:
                print(e)
            finally:
                driver.quit()

        driver.save_screenshot("D:/333.png")
        print()
    except Exception as e:
        print(e)
        driver.quit()


if __name__ == '__main__':
    editUserAgent()
