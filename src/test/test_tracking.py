import json
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

# url = "https://www.trackingmore.com/login-cn.html"
# dcap = dict(DesiredCapabilities.PHANTOMJS.copy())
# headers = {
#     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
# for key, value in headers.items():
#     dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
# status_dict = {'0': '查询中', '1': '查询不到', '2': '运输途中', '3': '到达待取', '4': '成功签收', '5': '运输过久',
#                '6': '投递失败', '7': '可能异常'}
# normal_status_dict = {'0': '查询中', '1': '查询不到', '2': '运输途中', '3': '到达待取', '4': '成功签收', '5': '运输过久'}
# try:
#     # driver = webdriver.PhantomJS(executable_path="D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe",
#     #                              desired_capabilities=dcap,
#     #                              service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
#     #                                            '--load-images=false'])
#     driver = webdriver.PhantomJS(executable_path="D:/software/phantomjs-2.1.1-windows/bin/phantomjs.exe",
#                                  desired_capabilities=dcap,
#                                  service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
#     driver.get(url)
#     driver.find_element_by_id("email").send_keys("rujiahua@payeasenet.com")
#     driver.find_element_by_id("password").send_keys("0418YXYwlx")
#     driver.find_element_by_id("login_test").click()
#     list = ['LX43903175',
#             'LX44244508',
#             'LX44142367', 'LX44142038']
#
#     time.sleep(5)
# for i in range(len(list)):
#     number = list[i]
#     driver.get(
#         "https://my.trackingmore.com/numbers.php?lang=cn&p=1&keywordType=trackNumber&searchnumber=" + number)
#     driver.maximize_window()
#     time.sleep(1)
#     driver.find_element_by_class_name("show_lastEvent").click()
#     time.sleep(1)
#     driver.save_screenshot("D://snapshots/" + str(time.time()) + ".png")
#     number = '1Z2051YX0306842250'
#     driver.get(
#         "https://my.trackingmore.com/numbers.php?lang=cn&p=1&keywordType=trackNumber&searchnumber=" + number)
#     driver.maximize_window()
#     time.sleep(2)
#     driver.find_element_by_class_name("show_lastEvent").click()
#     time.sleep(1)
#     driver.save_screenshot("D://snapshots/" + str(time.time()) + ".png")
#     url = "https://my.trackingmore.com/data/data-numbers.php?lang=cn&action=get_my_number" \
#           "&source=2&where=lang%3Dcn%26p%3D1%26keywordType%3DtrackNumber%26searchnumber%3D" + number + "&page=1"
#     driver.get(url)
#     json_data = driver.find_element_by_tag_name("body").text
#     json_obj = json.loads(str(json_data))
#     print(json_obj['data'])
#     print(json_obj['data'][0])
#     status = json_obj['data'][0]['track_status']
#     print(status)
#     if status in normal_status_dict:
#         print("正常")
#     else:
#         print("异常")
# except Exception as e:
#     print(e)
# finally:
#     driver.quit()

aaa = "测试-"
print(aaa.index("-") != -1)
print(aaa[0:aaa.index("-")])