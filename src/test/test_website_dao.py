from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


# https://www.xicidaili.com/nt/
class TestMysql(object):
    if __name__ == "__main__":
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
        headers = {
            'cookie': "_uab_collina=152905475626038564211156; zg_did=%7B%22did%22%3A%20%2216402c3dd9f1a3-048c8f157b8bef-62101875-15f900-16402c3dda240e%22%7D; _umdata=65F7F3A2F63DF020E71AEDA6F30593EA2A3D12D925F079E1C3AD72E105725A3834473AB8A6F2708CCD43AD3E795C914CDE7897677D443EB4C388E3204FFBF1CF; saveFpTip=true; UM_distinctid=16c2cc5326d31c-0c9a87f30aaef5-3f385c06-15f900-16c2cc5326ee7; QCCSESSID=lajs6k2n011qdt4muhp6pvpvu6; acw_tc=8bd7c0a715688745163558521e01768ca3582d4469d3fedb6973ead086; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568874516,1568958347,1569310892; hasShow=1; CNZZDATA1254842228=2046742533-1539154952-https%253A%252F%252Fwww.baidu.com%252F%7C1569311470; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201569316566287%2C%22updated%22%3A%201569316567763%2C%22info%22%3A%201568874515460%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22211a877f4df3307566603a3b5918bf6e%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1569316569"}
        for key, value in headers.items():
            dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs",
                                  desired_capabilities=dcap,service_log_path="/home/seluser/logs/a.log")
        # driver = webdriver.PhantomJS(executable_path="D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe", desired_capabilities=dcap,
        #                              service_args=['--ignore-ssl-errors=true'])
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(10)
        driver.maximize_window()
        url = "https://www.baidu.com/"
        driver.get(url)
        driver.implicitly_wait(5)
        driver.save_screenshot("/home/seluser/spider/b.png")
        try:
            driver.get(url)
            driver.implicitly_wait(5)
            driver.find_element_by_id("searchkey").send_keys("京东")
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
            driver.get("https://www.qichacha.com" + str(href) + "#base")
            driver.save_screenshot("/home/seluser/spider/a.png")
        except Exception as e:
            print()
        finally:
            driver.quit()
        # if check_item["bcIsAbn"] is 1 or check_item["bcIsMoveout"] is 1 or check_item["bcIsLogout"] is 1 or  check_item["bcLegalpersonChg"] is 1:

        # task_dao = TrackingTaskDao()
        # task_dao.close_task(65)
        # chrome_options = Options()
        # strategy_service = StrategyService()
        # strategy = strategy_service.get_strategy()
        # if strategy.proxy_server is None or strategy.proxy_server == '':
        #     print()
        # else:
        #     proxy_servers = strategy.proxy_server.split(",")
        #     print(str(choice(proxy_servers)))
        # chrome_options = Options()
        # chrome_options.add_argument("--proxy-server=https://115.200.251.158:8118")
        # # 禁止图片和css加载
        # prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Remote(command_executor='http://172.17.161.230:8911/wd/hub',
        #                           desired_capabilities=DesiredCapabilities.CHROME,
        #                           options=chrome_options)
        #
        # driver.set_page_load_timeout(30)
        # driver.set_script_timeout(10)
        # driver.maximize_window()
        # driver.get("https://www.qichacha.com/firm_b40ecf6c3e7e4e0414c501f6ce53dd37.html#fengxian")
        # driver.save_screenshot("D:/cc.jpg")
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        # req = urllib.request.Request("http://www.melaleuca.com.cn", headers=headers )
        # web_page = urllib.request.urlopen(req, timeout=10)
        # html = web_page.read()
        # soup = BeautifulSoup(html, 'html.parser', from_encoding="gb18030")
        # for k in soup.find_all('a'):
        #     href = str(k.get('href'))
        #     print(href)
        # task_pools = session.query(TaskItem).filter(TaskItem.batch_num == '11').filter(
        #     TaskItem.status == 'pending')
        # if task_pools is None:
        #     print()
        # task_pool_service = TaskPoolService()
        # entity, task_pool = task_pool_service.get_pending_task("11111")
        # if entity is None:
        #     print()
        # check_item = json.loads(task_pool.check_item)
        # if task_pool.type == "weburl" and check_item["websiteIsBadwords"] is 1:
        #     print()
        # elif task_pool.type == "website":
        #     if check_item["websiteIsForward"] is 1 or check_item["websiteIsOpen"] is 1:
        #         # 网站监控
        #         print()
        #     else:
        #         print()

    # driver.find_element_by_id("searchkey").send_keys("京东")
    # driver.find_element_by_id("V3_Search_bt").click()
    # source = driver.page_source
    # soup = BeautifulSoup(source, 'html.parser')

    # title = soup.find(name="title").get_text()
    # logger.info("qichacha res title :%s", str(title))
    # tbodys = soup.find_all(id="search-result")
    # trs = tbodys[0].find_all('tr')
    # tds = trs[0].find_all('td')
    # a = tds[2].find_all('a')
    # name = a[0].get_text().strip()
    # print(name)
    # driver.set_page_load_timeout(10)
    # driver.set_script_timeout(10)
    # driver.maximize_window()
    # weburl_service = WeburlService()
    # weburl_service.gather_urls(1, "http://rczhiyun.com", "财新联合汽车租赁（北京）有限公司","rczhiyun.com", 0)
    # insepect_task_service =  InspectTaskService()
    # insepect_task_service.get_websites(34)
    # test='/usr/local/snapshots'
    # print(test[:10])
    # website_dao = WebsiteDao()
    # website = website_dao.get_by_name("威海紫光科技园有限公司")
    #  print(website.merchant_name)
    # spider_manager = GatherCenter()
    # spider_manager.gather('', '')
    # weburl = WeburlService()
    # weburl.gather_urls(website)
    # service = MonitorBcService()
    # batch_num = '1'
    # # url = service.get_merchant_url('1', merchant_name='威海紫光科技园有限公司')
    # url = '/firm_6d1f03aac2ffea7e98592821fe618a62.html'
    # if url is not None:
    #     try:
    #         service.inspect(str(batch_num), "https://www.qichacha.com" + url, '威海紫光科技园有限公司','')
    #         print()
    #     except Exception as e:
    #         pass
