from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver

url = "https://www.trackingmore.com/cn/1ZY8A3910360411591"
dcap = dict(DesiredCapabilities.PHANTOMJS.copy())
headers = {
    'Cookie': '_uab_collina=152905475626038564211156; zg_did=%7B%22did%22%3A%20%2216402c3dd9f1a3-048c8f157b8bef-62101875-15f900-16402c3dda240e%22%7D; _umdata=65F7F3A2F63DF020E71AEDA6F30593EA2A3D12D925F079E1C3AD72E105725A3834473AB8A6F2708CCD43AD3E795C914CDE7897677D443EB4C388E3204FFBF1CF; saveFpTip=true; UM_distinctid=16c2cc5326d31c-0c9a87f30aaef5-3f385c06-15f900-16c2cc5326ee7; QCCSESSID=lajs6k2n011qdt4muhp6pvpvu6; acw_tc=8bd7c0a715688745163558521e01768ca3582d4469d3fedb6973ead086; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568874516,1568958347,1569310892,1569379185; CNZZDATA1254842228=2046742533-1539154952-https%253A%252F%252Fwww.baidu.com%252F%7C1569381685; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201569382004980%2C%22updated%22%3A%201569382005321%2C%22info%22%3A%201568874515460%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22211a877f4df3307566603a3b5918bf6e%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1569382005',
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
for key, value in headers.items():
    dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
driver = webdriver.PhantomJS(executable_path="D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                             desired_capabilities=dcap,
                             service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                           '--load-images=false'])
try:
    driver.get(url)
except Exception as e:
    driver.quit()
try:
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    a_tags = soup.find_all("a", attrs={'class': 'ulliselect'})
    has_tracking = False
    if a_tags.__len__() > 0:
        for a_tag in a_tags:
            if a_tag.get_text().strip() == "UPS":
                has_tracking = True
                url = "http:" + a_tag.get("href")
                driver.get(url)
                try:
                    source = driver.page_source
                    soup = BeautifulSoup(source, 'html.parser')
                    item_length = soup.find_all("li", attrs={'class': 's-packStatst'}).__len__()
                    if item_length > 0:
                        print("正常")
                    else:
                        print("没有查询到物流信息")
                except Exception as e:
                    print(e)
                    # 正常
            else:
                pass
        if not has_tracking:
            print("提供的单号-快递公司关系疑似不匹配")
    else:
        item_length = soup.find_all("dd", attrs={'class': 'post_message'})
        if item_length.__len__() > 0:
            print("正常")
        else:
            print("没有查询物流信息")
except Exception as e:
    print(e)
finally:
    driver.quit()
