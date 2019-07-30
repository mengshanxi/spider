import time
from selenium import webdriver

cookie = {
    'domain': '.qichacha.com',  # 注意前面有个点
    'name': 'CNZZDATA1254842228',
    'value': '563173376-1529324664-%7C1529324664',
    'path': '/'
    # 这些都可以在cookie里找到
}
browser = webdriver.PhantomJS(executable_path='D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe',
                              service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
browser.set_window_size(1055, 800)
# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
browser.get("https://www.qichacha.com/")
browser.add_cookie(cookie)

time.sleep(5)

print
browser.page_source

# 获取页面名为 wrapper的id标签的文本内容
data = browser.find_element_by_id("searchkey").text

# 打印数据内容
print
data

# 打印页面标题 "百度一下，你就知道"
print
browser.title

# id="kw"是百度搜索输入框，输入字符串"长城"
browser.find_element_by_id("searchkey").send_keys(u"京东")

# id="su"是百度搜索按钮，click() 是模拟点击
browser.find_element_by_id("V3_Search_bt").click()
time.sleep(2)
# 打印网页渲染后的源代码
print
browser.page_source

# 获取新的页面快照
browser.save_screenshot("jd.png")

# 获取当前页面Cookie
print
browser.get_cookies()
browser.quit()
