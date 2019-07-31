import re
import time
import urllib.request

from PIL import Image
from bs4 import BeautifulSoup

import util.globalvar as gl
from config.config_load import base_filepath
from config.mylog import logger
from dao.bc_benefit_dao import BcBenifitDao
from dao.bc_person_dao import BcPersonDao
from dao.monitor_bc_dao import MonitorBcDao
from dao.website_dao import WebsiteDao
from model.bc_benefit import BcBenefit
from model.bc_person import BcPerson
from model.monitor_bc import MonitorBc
from service.senti_util import SentiUtil
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver

"""
企查查监控服务
url = "https://www.qichacha.com/company_getinfos?unique="+url[30:62]+"&companyname="+urllib.parse.quote(merchant_name)+"&tab=fengxian"
"""


class MonitorBcService:

    @staticmethod
    def is_merchant_exist(merchant_name, url):

        monitor_bc_dao = MonitorBcDao()

        if url == 'NONE':
            monitor_bc = MonitorBc()
            monitor_bc.merchant_name = merchant_name
            monitor_bc.snapshot = ''
            monitor_bc.outline = '企查查没有查询到商户公司'
            monitor_bc.is_normal = '异常'
            monitor_bc_dao.add(monitor_bc)
            return

        driver = WebDriver.get_phantomJS_withcookie()
        try:
            driver.get("https://www.qichacha.com" + url)
            source = driver.page_source
            senti_util = SentiUtil()
            website_dao = WebsiteDao()
            website = website_dao.getwebsite_by_merchant(merchant_name)
            senti_util.senti_process_text("企查查", website.website_name, source, "https://www.qichacha.com" + url)
        except Exception as e:
            logger.error(e)

        """
        es_util = EsUtil()
        es_util.index_monitor_bc(merchant_name, source)
        keyword_dao = KeywordDao()
        keywords = keyword_dao.get_keyword()
        json_dic = es_util.search('monitor_bc', ' '.join(keywords))
        total = json_dic['hits']['total']
        for i in range(total):
            monitor_bc = MonitorBc()
            merchant_name = json_dic['hits']['hits'][i]['_source']['merchant_name']
            monitor_bc.merchant_name = str(merchant_name)
            monitor_bc.outline = '包含异常信息'
            monitor_bc.is_normal = '异常'
            monitor_bc.snapshot = str(timestamp) + ".png"
            monitor_bc_dao.update(monitor_bc)
        """

    @staticmethod
    def inspect(batch_num, url, merchant_name, legalman):
        if not gl.check_by_batch_num(batch_num):
            return
        monitor_bc_dao = MonitorBcDao()
        driver = WebDriver.get_phantomJS_withcookie()
        # 经营异常
        monitor_bc = MonitorBc()
        monitor_bc.batch_num = batch_num
        monitor_bc.merchant_name = merchant_name
        try:
            rest_url = "https://www.qichacha.com/company_getinfos?unique=" + url[
                                                                             30:62] + "&companyname=" + urllib.parse.quote(
                merchant_name) + "&tab=fengxian"
            driver.get(rest_url)
        except Exception as e:
            logger.info(e)
            return

        snapshot = SnapshotService.create_snapshot(driver)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        infos = soup.find_all(name='section', id='Exceptions')
        if infos.__len__() == 0:
            # 无异常
            monitor_bc.outline = '未检测到经营异常风险'
            monitor_bc.snapshot = str(snapshot)
            monitor_bc.is_normal = '正常'
            monitor_bc.kinds = '经营风险'
            monitor_bc.level = 0
        else:
            clearfix = infos[0].find_all(name='div', class_='clearfix')
            innet_text = clearfix[0].get_text()
            index = str(innet_text).find("移出")
            if index != -1:
                monitor_bc.outline = '未检测到经营异常风险'
                monitor_bc.snapshot = str(snapshot)
                monitor_bc.is_normal = '正常'
                monitor_bc.kinds = '经营风险'
                monitor_bc.level = 0
            else:
                monitor_bc.outline = '检测到经营异常风险'
                monitor_bc.snapshot = str(snapshot)
                monitor_bc.is_normal = '异常'
                monitor_bc.kinds = '经营风险'
                monitor_bc.level = 2
        monitor_bc_dao.add(monitor_bc)

        try:
            driver.get(url)
        except Exception as e:
            logger.info(e)
            driver.quit()
            return
        # 截图
        source = driver.page_source
        # 内容分析
        soup = BeautifulSoup(source, 'html.parser')
        # 受益人
        shouyirens = soup.find_all(name='section', id=re.compile('syrlist'))
        if shouyirens.__len__() > 0:
            shouyiren = shouyirens[0]
            tbodys = shouyiren.find_all('tbody')
            trs = tbodys[0].find_all('tr')
            num = 0

            bc_benefit_dao = BcBenifitDao()

            for tr in trs:
                num += 1
                if (num != 1):
                    tds = tr.find_all('td')
                    fullname = tds[1].find_all(name='a')[0].get_text()
                    proportion = tds[2].get_text()
                    invest_train = tds[3].get_text()

                    bc_benefit = BcBenefit()
                    bc_benefit.batch_num = batch_num
                    bc_benefit.merchant_name = merchant_name.strip()
                    bc_benefit.fullname = fullname.strip()
                    bc_benefit.proportion = proportion.strip()
                    bc_benefit.invest_train = invest_train.strip()

                    bc_benefit_dao.add(bc_benefit)
        # 股东成员
        chengyuans = soup.find_all(name='section', id=re.compile('Mainmember'))
        if chengyuans.__len__() > 0:
            chengyuan = chengyuans[0]
            tbodys = chengyuan.find_all('tbody')
            trs = tbodys[0].find_all('tr')
            line_num = 0
            bc_person_dao = BcPersonDao()
            for tr in trs:
                line_num += 1
                if (line_num != 1):
                    tds = tr.find_all('td')
                    fullname = tds[1].find_all('a')[0].get_text()
                    job = tds[2].get_text()

                    bc_person = BcPerson()
                    bc_person.batch_num = batch_num
                    bc_person.merchant_name = merchant_name.strip()
                    bc_person.fullname = fullname.strip()
                    bc_person.job = job.strip()

                    bc_person_dao.add(bc_person)

        # 法人变更
        timestamp = int(time.time())
        snapshot = str(timestamp) + ".png"
        path = base_filepath + "/imgs/" + str(timestamp)
        try:
            driver.save_screenshot(path + "_temp.png")
            bc_info = driver.find_element_by_xpath('//section[@id="Cominfo"]')
            locations = bc_info.location
            sizes = bc_info.size
            rangle = (int(locations['x']), int(locations['y']), int(locations['x'] + sizes['width']),
                      int(locations['y'] + sizes['height']))
            img = Image.open(path + "_temp.png")
            jpg = img.crop(rangle)
            jpg.save(path + ".png")
            im = Image.open(path + ".png")
            im_resize = im.resize((50, 50))
            im_resize.save(path + "_thumb.bmp")
        except Exception as e:
            pass
            logger.info(e)

        legalmans = soup.find_all(class_='seo font-20')
        if str(legalman).strip() is "":
            monitor_bc.outline = '未检测到法人变更'
            monitor_bc.snapshot = str(snapshot)
            monitor_bc.is_normal = '正常'
            monitor_bc.kinds = '法人变更'
            if legalmans.__len__() > 0:
                monitor_bc.kinds = '法人变更:' + legalmans[0].get_text()
            monitor_bc.level = 0
            monitor_bc_dao.add(monitor_bc)
        else:
            if legalmans.__len__() > 0:
                if str(legalman).strip() == legalmans[0].get_text():
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '正常'
                    monitor_bc.kinds = '法人变更:' + legalmans[0].get_text()
                    monitor_bc.outline = '未检测到法人变更'
                    monitor_bc.level = 0
                else:
                    monitor_bc.outline = '检测到法人信息与系统中维护的法人不一致'
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '异常'
                    monitor_bc.kinds = '法人变更:' + legalmans[0].get_text()
                    monitor_bc.level = 1
                monitor_bc_dao.add(monitor_bc)

        # 经营状态：注销 迁出
        cminfo = soup.find_all(name='section', id=re.compile('Cominfo'))
        tables = cminfo[0].find_all(name='table', class_='ntable')
        tds = tables[1].find_all(name='td')
        manage_state = tds[5].get_text().strip()
        # 经营状态-注销
        if str(manage_state).find("注销") >= 0:
            monitor_bc.outline = '检测到经营状态异常：注销'
            monitor_bc.snapshot = str(snapshot)
            monitor_bc.is_normal = '异常'
            monitor_bc.kinds = '经营状态'
            monitor_bc.level = 3
        else:
            monitor_bc.outline = '经营状态正常，无 注销'
            monitor_bc.snapshot = str(snapshot)
            monitor_bc.is_normal = '正常'
            monitor_bc.kinds = '经营状态'
            monitor_bc.level = 0
        monitor_bc_dao.add(monitor_bc)
        # 经营状态-迁出
        if str(manage_state).find("迁出") >= 0:
            monitor_bc.outline = '检测到经营状态异常：迁出'
            monitor_bc.snapshot = str(snapshot)
            monitor_bc.is_normal = '异常'
            monitor_bc.kinds = '经营状态'
            monitor_bc.level = 0
        else:
            monitor_bc.outline = '经营状态正常，无 迁出'
            monitor_bc.snapshot = str(snapshot)
            monitor_bc.is_normal = '正常'
            monitor_bc.kinds = '经营状态'
            monitor_bc.level = 0
        monitor_bc_dao.add(monitor_bc)

        # 严重违法
        try:
            driver.get(url + "#fengxian")
        except Exception as e:
            logger.info(e)
            return
        snapshot = SnapshotService.create_snapshot(driver)

        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        companys = soup.find_all(name='div', class_='company-nav-tab')
        risks = companys[3].find_all(name='span')
        manage_abn = risks[2].get_text()
        serious_illegal = risks[4].get_text()
        logger.info("manage_abn:%s", str(manage_abn))
        logger.info("serious_illegal:%s", str(serious_illegal))
        # 严重违法
        if int(manage_abn[4:]) > 0:
            monitor_bc.outline = '检测到严重违法风险'
            monitor_bc.snapshot = str(snapshot)
            monitor_bc.is_normal = '异常'
            monitor_bc.kinds = '严重违法'
            monitor_bc.level = 2
        else:
            monitor_bc.outline = '未检测到严重违法风险'
            monitor_bc.snapshot = str(snapshot)
            monitor_bc.is_normal = '正常'
            monitor_bc.kinds = '严重违法'
            monitor_bc.level = 0
        monitor_bc_dao.add(monitor_bc)

    @staticmethod
    def get_merchant_url(batch_num, merchant_name):

        driver = WebDriver.get_phantomJS_withcookie()
        url = "https://www.qichacha.com/search?key=" + urllib.parse.quote(merchant_name)
        try:
            driver.get(url)
        except Exception as e:
            logger.error(e)
            return None
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        title = soup.find(name="title").get_text()
        logger.info("qichacha res title :%s", str(title))
        if (str(title) == "会员登录 - 企查查"):
            return None
        else:
            pass
        try:
            tbodys = soup.find_all('tbody')
            trs = tbodys[0].find_all('tr')
            tds = trs[0].find_all('td')
            a = tds[1].find_all('a')

            name = a[0].get_text().strip()
            if name == merchant_name.strip():
                href = a[0].get('href')
                if str(href) == "None":
                    # 截图
                    driver.get(str(url))
                    snapshot = SnapshotService.create_snapshot(driver)
                    monitor_bc_dao = MonitorBcDao()
                    monitor_bc = MonitorBc()
                    monitor_bc.batch_num = batch_num
                    monitor_bc.merchant_name = merchant_name
                    monitor_bc.snapshot = snapshot
                    monitor_bc.outline = '企查查没有查询到商户公司'
                    monitor_bc.is_normal = '异常'
                    monitor_bc.kinds = '企业是否可查'
                    monitor_bc.level = 0
                    monitor_bc_dao.add(monitor_bc)
                    driver.quit()
                    return None
                else:
                    return href.strip()
            else:
                snapshot = SnapshotService.create_snapshot(driver)
                monitor_bc_dao = MonitorBcDao()
                monitor_bc = MonitorBc()
                monitor_bc.batch_num = batch_num
                monitor_bc.merchant_name = merchant_name
                monitor_bc.snapshot = snapshot
                monitor_bc.outline = '企查查没有查询到商户公司'
                monitor_bc.is_normal = '异常'
                monitor_bc.kinds = '企业是否可查'
                monitor_bc.level = 0
                monitor_bc_dao.add(monitor_bc)
                return None

        except Exception as e:
            logger.error(e)
            return None
