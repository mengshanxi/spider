import time
from selenium import webdriver

browser = webdriver.PhantomJS(executable_path='D:/software/phantomjs-2.1.1-windows/bin/phantomjs.exe')
# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
browser.get("http://www.dianping.com/mylist/ajax/shoprank?rankId=6c3cdc438f5979451b09ed2ea433313f")
time.sleep(5)

# 获取新的页面快照
browser.save_screenshot("jd1.png")

# 获取页面名为 wrapper的id标签的文本内容
data = browser.find_element_by_id("keyword").text

# 打印数据内容
print
data

# 打印页面标题 "百度一下，你就知道"
print
browser.title

# id="kw"是百度搜索输入框，输入字符串"长城"
browser.find_element_by_id("keyword").send_keys(u"京东")

# id="su"是百度搜索按钮，click() 是模拟点击
browser.find_element_by_id("btn_query").click()

# 获取新的页面快照
browser.save_screenshot("jd.png")

# 打印网页渲染后的源代码
print
browser.page_source

# 获取当前页面Cookie
print
browser.get_cookies()
browser.quit()
