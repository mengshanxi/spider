import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from src.config.config_load import phantomjs_path


class TestWangdaitianyan(object):
    if __name__ == "__main__":
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:/chromedriver_2.38/chromedriver.exe")
        """
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
        driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap,
                                     service_args=['--ignore-ssl-errors=true'])
        driver.get("https://www.p2peye.com/search.php?mod=zonghe&srchtxt=" + urllib.parse.quote("京东"))
        source = driver.page_source
        print(source)
        soup = BeautifulSoup(source, 'html.parser')
        news = soup.find_all(attrs={'class': 'result-t'})
        if news.__len__() > 0:
            for new in news:
                href = new.find_all('a')[0].get("href")
                print(href[2:])
                print(new.get_text())
        # 关闭浏览器
        driver.quit()
        '''
        www.p2peye.com/thread-2099641-1-1.html

京东白条可临时提额啦 白条临时额度你要吗？

www.p2peye.com/thread-2097341-1-1.html

京东白条暂停部分信用卡支付功能

www.p2peye.com/thread-2097455-1-1.html

京东、清华大学、沃尔玛和IBM联合成立“区块链食品安全联盟（BFSA）”，开发食品安全和可溯源区块链项目

www.p2peye.com/thread-2101886-1-1.html

【普汇云通】全民返利强势走起，邀您畅享红包、iPhoneX、4000元京东卡

www.p2peye.com/thread-2100662-1-1.html

【普汇云通】邀您畅享红包、iPhoneX、最高4000元京东卡

www.p2peye.com/thread-2102110-1-1.html

京东4.83亿参股安联财险，将区块链等技术综合运用在运营和保险业务中

news.p2peye.com/article-513689-1.html

厦门公布不予备案P2P，京东金融子公司前途未卜

www.p2peye.com/thread-2097355-1-1.html

京东白条暂停部分信用卡支付服务


        '''
