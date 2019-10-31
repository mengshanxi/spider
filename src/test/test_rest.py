import json
from urllib import request, parse

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

try:
    url = "http://localhost/ims/open/api/v1/agent/monitor_bc"
    merchantNum = "1"
    data_json = {"merchantNum": merchantNum, "merchantName": "2"}
    data = bytes(parse.urlencode(data_json), encoding="utf8")
    new_url = request.Request(url, data)
    res = request.urlopen(new_url).read().decode('utf-8')
    bc_response = json.loads(res)
    if bc_response['status'] is True:
        pass
    else:
        pass
    url = "http://localhost/ims/views/system/qichacha.jsp?merchantNum=" + merchantNum
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    driver = webdriver.PhantomJS(executable_path="D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                                 desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                               '--load-images=false'],
                                 service_log_path="D:/a.log")
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(10)
    driver.maximize_window()
    driver.get(url)
    driver.save_screenshot("D:/hhh.png")
except Exception as e:
    print(e)
finally:
    driver.quit()
