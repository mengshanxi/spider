import time
from selenium import webdriver

browser = webdriver.PhantomJS(executable_path='D:/software/phantomjs-2.1.1-windows/bin/phantomjs.exe')
# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
browser.get("http://www.dianping.com/mylist/ajax/shoprank?rankId=6c3cdc438f5979451b09ed2ea433313f")
time.sleep(5)

# 打印网页渲染后的源代码
print(browser.page_source)

browser.quit()
