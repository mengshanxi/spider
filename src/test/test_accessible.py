import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

if __name__ == "__main__":
    driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(10)
    url = "http://xueshu.baidu.com/"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for k in soup.find_all('a'):
        href = str(k.get('href'))
        #print("origin href: %s", href)
        if href.endswith(".jpg") or href.endswith(".jpeg") or href.endswith(".bmp") or href.endswith(
                ".png") or href.endswith(
            ".swf") or href == '/' or href == 'http://' or href == '#' or href.startswith(
            'javascript') or href == 'None' or href.startswith('tencent://'):
            continue
        elif href.startswith('http://') or href.startswith('https://'):
            href = href
        elif href.startswith('/'):
            href = "http://" + "www.baidu.com" + href
        elif href.startswith('./'):
            href = url + href[1:]
        else:
            href = url + "/" + href
        print(href.replace("//", "/").replace("/../", "/"))
