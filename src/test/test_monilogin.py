from selenium import webdriver
import time

# 伪装成浏览器，防止被识破
from selenium.webdriver import DesiredCapabilities, ActionChains

driver = webdriver.Remote(command_executor='http://172.17.161.230:8916/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME)

# 打开登录页面
driver.get('https://www.qichacha.com/user_login')
time.sleep(1)
# 单击用户名密码登录的标签
tag = driver.find_element_by_xpath('//*[@id="normalLogin"]')
tag.click()
time.sleep(1)
# 将用户名、密码注入
driver.find_element_by_id('nameNormal').send_keys('13811668973')
driver.find_element_by_id('pwdNormal').send_keys('Abcd1234')
huakuai=driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
time.sleep(10)  # 休眠，人工完成验证步骤，等待程序单击“登录”
inc_list = ['阿里巴巴', '腾讯', '今日头条', '滴滴', '美团']
inc_len = len(inc_list)


def get_track(distance):      # distance为传入的总距离
    # 移动轨迹
    track=[]
    # 当前位移
    current=0
    # 减速阈值
    mid=distance*4/5
    # 计算间隔
    t=0.2
    # 初速度
    v=0

    while current<distance:
        if current<mid:
            # 加速度为2
            a=2
        else:
            # 加速度为-2
            a=-3
        v0=v
        # 当前速度
        v=v0+a*t
        # 移动距离
        move=v0*t+1/2*a*t*t
        # 当前位移
        current+=move
        # 加入轨迹
        track.append(round(move))
    return track
def move_to_gap(slider,tracks):     # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()
    # 单击登录按钮
    btn = driver.find_element_by_xpath('//*[@id="user_login_normal"]/button')
    btn.click()
    driver.implicitly_wait(5)
    for i in range(inc_len):
        txt = inc_list[i]
        time.sleep(1)
        driver.implicitly_wait(5)
        if (i == 0):
            # 向搜索框注入文字
            driver.find_element_by_id('searchkey').send_keys(txt)
            # 单击搜索按钮
            srh_btn = driver.find_element_by_xpath('//*[@id="V3_Search_bt"]')
            srh_btn.click()
        else:
            # 向搜索框注入下一个公司地址
            driver.find_element_by_id('headerKey').send_keys(txt)
            # 搜索按钮
            srh_btn = driver.find_element_by_xpath('/html/body/header/div/form/div/div/span/button')
            srh_btn.click()

        # 获取首个企业文本
        print(i + 1)
        inc_full = driver.find_element_by_xpath('//*[@id="search-result"]/tr[1]/td[3]/a').text
        print(inc_full)
        money = driver.find_element_by_xpath('//*[@id="search-result"]/tr[1]/td[3]/p[1]/span[1]').text
        print(money)
        date = driver.find_element_by_xpath('//*[@id="search-result"]/tr[1]/td[3]/p[1]/span[2]').text
        print(date)
        mail_phone = driver.find_element_by_xpath('//*[@id="search-result"]/tr[1]/td[3]/p[2]').text
        print(mail_phone)
        addr = driver.find_element_by_xpath('//*[@id="search-result"]/tr[1]/td[3]/p[3]').text
        print(addr)
        try:
            stock_or_others = driver.find_element_by_xpath('//*[@id="search-result"]/tr[1]/td[3]/p[4]').text
            print(stock_or_others)
        except:
            pass

        # 获取网页地址，进入
        inner = driver.find_element_by_xpath('//*[@id="search-result"]/tr[1]/td[3]/a').get_attribute("href")
        driver.get(inner)

        # 单击进入后 官网 通过href属性获得：
        inc_web = driver.find_element_by_xpath(
            '//*[@id="company-top"]/div[2]/div[2]/div[3]/div[1]/span[3]/a').get_attribute("href")
        print("官网：" + inc_web)
        print(' ')
        driver.close()


if __name__ == '__main__':
    move_to_gap(huakuai,get_track(340))