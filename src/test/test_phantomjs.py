# coding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver

# https://www.xicidaili.com/nt/
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


class TestMysql(object):
    if __name__ == "__main__":
        # --load-images=false 图片不加载
        # --disk - cache = true 启用缓存
        # --max-disk-cache-size=1024 设置最大缓存数量
        SERVICE_ARGS = [' --disk-cache=true', '--max-disk-cache-size=1024', '--load-images=false']
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36')
        dcap['phantomjs.page.settings.host'] = (
            'www.qichacha.com')
        headers = {
            'Cookie': '_uab_collina=152905475626038564211156; zg_did=%7B%22did%22%3A%20%2216402c3dd9f1a3-048c8f157b8bef-62101875-15f900-16402c3dda240e%22%7D; _umdata=65F7F3A2F63DF020E71AEDA6F30593EA2A3D12D925F079E1C3AD72E105725A3834473AB8A6F2708CCD43AD3E795C914CDE7897677D443EB4C388E3204FFBF1CF; saveFpTip=true; UM_distinctid=16c2cc5326d31c-0c9a87f30aaef5-3f385c06-15f900-16c2cc5326ee7; QCCSESSID=lajs6k2n011qdt4muhp6pvpvu6; acw_tc=8bd7c0a715688745163558521e01768ca3582d4469d3fedb6973ead086; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568874516,1568958347,1569310892,1569379185; CNZZDATA1254842228=2046742533-1539154952-https%253A%252F%252Fwww.baidu.com%252F%7C1569381685; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201569382004980%2C%22updated%22%3A%201569382005321%2C%22info%22%3A%201568874515460%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22211a877f4df3307566603a3b5918bf6e%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1569382005'}
        for key, value in headers.items():
            dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
        dcap[
            'cookie'] = '_uab_collina=152905475626038564211156; zg_did=%7B%22did%22%3A%20%2216402c3dd9f1a3-048c8f157b8bef-62101875-15f900-16402c3dda240e%22%7D; _umdata=65F7F3A2F63DF020E71AEDA6F30593EA2A3D12D925F079E1C3AD72E105725A3834473AB8A6F2708CCD43AD3E795C914CDE7897677D443EB4C388E3204FFBF1CF; saveFpTip=true; UM_distinctid=16c2cc5326d31c-0c9a87f30aaef5-3f385c06-15f900-16c2cc5326ee7; QCCSESSID=lajs6k2n011qdt4muhp6pvpvu6; acw_tc=8bd7c0a715688745163558521e01768ca3582d4469d3fedb6973ead086; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568874516,1568958347,1569310892,1569379185; CNZZDATA1254842228=2046742533-1539154952-https%253A%252F%252Fwww.baidu.com%252F%7C1569392486; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201569392539325%2C%22updated%22%3A%201569394579962%2C%22info%22%3A%201568874515460%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22211a877f4df3307566603a3b5918bf6e%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1569394580'
        dcap["phantomjs.page.settings.loadImages"] = False
        driver = webdriver.PhantomJS(executable_path="D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                                     desired_capabilities=dcap,
                                     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                                   '--load-images=false'],
                                     service_log_path="D:/a.log")

        driver.set_page_load_timeout(30)
        driver.set_script_timeout(10)
        driver.maximize_window()
        try:
            # url = "https://httpbin.org/get?show_env=1&q=nihao&bbb=c"
            # url="https://www.trackingmore.com/bestex-tracking/cn.html?number=71636028337857"
            url = "https://www.qichacha.com/"
            driver.get(url)
            driver.implicitly_wait(5)
            driver.find_element_by_id('searchkey').send_keys('京东')
            driver.find_element_by_id("V3_Search_bt").click()
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            title = soup.find(name="title").get_text()
            if str(title) == "会员登录 - 企查查":
                print()
            tbodys = soup.find_all(id="search-result")
            trs = tbodys[0].find_all('tr')
            tds = trs[0].find_all('td')
            a = tds[2].find_all('a')
            name = a[0].get_text().strip()
            href = a[0].get('href')
            driver.get("https://www.qichacha.com" + str(href))
            driver.save_screenshot("D:/a.png")
        except Exception as e:
            print(e)
        finally:
            driver.quit()
