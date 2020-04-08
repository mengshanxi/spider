from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")
try:
    driver.get("https://www.trackingmore.com/login-cn.html")
    driver.find_element_by_id("email").send_keys("rujiahua@payeasenet.com")
    driver.find_element_by_id("password").send_keys("0418YXYwlx")
    driver.find_element_by_id("login_test").click()
    driver.get(
        "https://my.trackingmore.com/numbers.php?lang=cn&p=1&keywordType=trackNumber&searchnumber=1Z885V7Y0383199599")
    sleep(5)
    # captcha_frame_abs_xy = driver.find_element_by_id('tbResult').location
    # ActionChains(driver).move_by_offset(427, 240).click().perform()
    driver.find_element_by_id('trackItem_0').click()
    sleep(5)
    driver.save_screenshot("D:/333.png")
except Exception as e:
    print(e)
finally:
    driver.quit()
