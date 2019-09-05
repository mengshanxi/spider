import datetime
import re
import time

from PIL import Image
from bs4 import BeautifulSoup

from config.config_load import base_filepath
from config.mylog import logger
from dao.bc_benefit_dao import BcBenefitDao
from dao.bc_person_dao import BcPersonDao
from dao.monitor_bc_dao import MonitorBcDao
from model.models import BcPerson, BcBenefit
from model.models import MonitorBc
from service.snapshot_service import SnapshotService
from service.webdriver_util import WebDriver

"""
企查查监控服务
url = "https://www.qichacha.com/company_getinfos?unique="+url[30:62]+"&companyname="+urllib.parse.quote(merchant_name)+"&tab=fengxian"
"""


class MonitorBcService:

    @staticmethod
    def inspect(batch_num, url, website):
        monitor_bc_dao = MonitorBcDao()
        monitor_bc = MonitorBc()
        monitor_bc.batch_num = batch_num
        monitor_bc.merchant_name = website.merchant_name
        try:
            driver = WebDriver.get_chrome()
            # 1.受益人
            logger.info("企查查检测受益人 : %s", website.merchant_name)
            rest_url = url + "#base"
            driver.get(rest_url)
            driver.implicitly_wait(5)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            shou_yi_rens = soup.find_all(name='section', id=re.compile('partnerslist'))
            if shou_yi_rens.__len__() > 0:
                shouyiren = shou_yi_rens[0]
                tables = shouyiren.find_all('table')
                trs = tables[0].find_all('tr')
                num = 0

                bc_benefit_dao = BcBenefitDao()

                for tr in trs:
                    num += 1
                    if num != 1:
                        tds = tr.find_all('td')
                        if tds.__len__() >= 3:
                            fullname = tds[1].find_all(name='a')[0].get_text()
                            shouyirens = tds[1].find_all(name='span', class_=re.compile('ntag sm text-primary click'))
                            if shouyirens.__len__() >= 1:
                                is_shouyiren = shouyirens[
                                                   0].get_text().find('受益人') > 0
                                if is_shouyiren:
                                    proportion = tds[2].get_text().strip()
                                    invest_train = '-'

                                    bc_benefit = BcBenefit()
                                    bc_benefit.batch_num = batch_num
                                    bc_benefit.merchant_name = website.merchant_name.strip()
                                    bc_benefit.fullname = fullname.strip()
                                    bc_benefit.proportion = proportion.strip()
                                    bc_benefit.invest_train = invest_train.strip()
                                    bc_benefit_dao.add(bc_benefit)

            logger.info("企查查检测股东成员 : %s", website.merchant_name)
            # 2.股东成员
            driver.get(url)
            driver.implicitly_wait(5)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            chengyuans = soup.find_all(name='section', id=re.compile('Mainmember'))
            if chengyuans.__len__() > 0:
                chengyuan = chengyuans[0]
                tbodys = chengyuan.find_all('tbody')
                trs = tbodys[0].find_all('tr')
                line_num = 0
                bc_person_dao = BcPersonDao()
                for tr in trs:
                    line_num += 1
                    if line_num != 1:
                        tds = tr.find_all('td')
                        fullname = tds[1].find_all('a')[0].get_text()
                        job = tds[2].get_text()

                        bc_person = BcPerson()
                        bc_person.batch_num = batch_num
                        bc_person.merchant_name = website.merchant_name.strip()
                        bc_person.fullname = fullname.strip()
                        bc_person.job = job.strip()

                        bc_person_dao.add(bc_person)

                # 3.法人变更
            timestamp = int(time.time())
            snapshot = batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_工商_" + str(
                timestamp) + ".png"
            path = base_filepath + "/" + batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_工商_" + str(
                timestamp)
            from selenium.webdriver.common.keys import Keys
            driver.find_element_by_link_text("工商信息").send_keys(Keys.RETURN)
            logger.info("企查查检测法人变更 : %s", website.merchant_name)
            driver.save_screenshot(path + ".png")
            img = Image.open(path + ".png")
            jpg = img.crop((265, 158, 420, 258))
            jpg.save(path + "_thumb.bmp")

            legalmans = soup.find_all(class_='seo font-20')
            if str(website.legal_person).strip() is "":
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
                    if str(website.legal_person).strip() == legalmans[0].get_text():
                        monitor_bc.snapshot = str(snapshot)
                        monitor_bc.is_normal = '正常'
                        monitor_bc.kinds = '法人变更:' + legalmans[0].get_text()
                        monitor_bc.outline = '未检测到法人变更'
                        monitor_bc.level = 0
                        monitor_bc = MonitorBc(batch_num=batch_num,
                                               merchant_name=website.merchant_name,
                                               outline='未检测到法人变更',
                                               snapshot=str(snapshot),
                                               is_normal='正常',
                                               kinds='法人变更:' + legalmans[0].get_text(),
                                               level=0)
                    else:
                        monitor_bc = MonitorBc(batch_num=batch_num,
                                               merchant_name=website.merchant_name,
                                               outline='检测到法人变更，变更为:' + legalmans[0].get_text(),
                                               snapshot=str(snapshot),
                                               is_normal='异常',
                                               kinds='法人变更:' + legalmans[0].get_text(),
                                               level=1)
                    monitor_bc_dao.add(monitor_bc)

            #  4.经营状态：注销 迁出
            logger.info("企查查检测经营状态：注销 迁出 : %s", website.merchant_name)
            cminfo = soup.find_all(name='section', id=re.compile('Cominfo'))
            tables = cminfo[0].find_all(name='table', class_='ntable')
            trs = tables[0].find_all(name='tr')
            tds = trs[2].find_all(name='td')
            manage_state = tds[1].get_text().strip()
            # 5.经营状态-注销
            logger.info("企查查检测经营状态-注销 : %s", website.merchant_name)
            if str(manage_state).find("注销") >= 0:
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       outline='检测到经营状态异常：注销',
                                       snapshot=str(snapshot),
                                       is_normal='异常',
                                       kinds='经营状态',
                                       level=3)
            else:
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       outline='经营状态正常，无注销',
                                       snapshot=str(snapshot),
                                       is_normal='正常',
                                       kinds='经营状态',
                                       level=0)
            monitor_bc_dao.add(monitor_bc)
            # 6.经营状态-迁出
            logger.info("企查查检测经营状态-迁出 : %s", website.merchant_name)
            if str(manage_state).find("迁出") >= 0:
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       outline='检测到经营状态异常：迁出',
                                       snapshot=str(snapshot),
                                       is_normal='异常',
                                       kinds='经营状态',
                                       level=1)
            else:
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       outline='经营状态正常，无 迁出',
                                       snapshot=str(snapshot),
                                       is_normal='正常',
                                       kinds='经营状态',
                                       level=0)
            monitor_bc_dao.add(monitor_bc)

            # 7.严重违法
            logger.info("企查查检测严重违法 : %s", website.merchant_name)
            timestamp = int(time.time())
            snapshot = batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_工商_" + str(
                timestamp) + ".png"
            path = base_filepath + "/" + batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_工商_" + str(
                timestamp)
            driver.find_element_by_partial_link_text("经营风险").send_keys(Keys.RETURN)
            driver.save_screenshot(path + ".png")
            img = Image.open(path + ".png")
            jpg = img.crop((91, 572, 191, 672))
            jpg.save(path + "_thumb.bmp")
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            companys = soup.find_all(name='div', class_='company-nav-tab')
            risks = companys[3].find_all(name='span')
            manage_abn = risks[2].get_text()
            serious_illegal = risks[4].get_text()
            logger.info("manage_abn:%s", str(manage_abn))
            logger.info("serious_illegal:%s", str(serious_illegal))
            if int(manage_abn) > 0:
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       outline='检测到经营异常风险',
                                       snapshot=str(snapshot),
                                       is_normal='异常',
                                       kinds='经营异常',
                                       level=2)
            else:
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       outline='未检测到经营异常风险',
                                       snapshot=str(snapshot),
                                       is_normal='正常',
                                       kinds='经营异常',
                                       level=0)
            monitor_bc_dao.add(monitor_bc)
            # 8.严重违法
            if int(serious_illegal) > 0:
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       outline='检测到严重违法风险',
                                       snapshot=str(snapshot),
                                       is_normal='异常',
                                       kinds='严重违法',
                                       level=2)
            else:
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       outline='未检测到严重违法风险',
                                       snapshot=str(snapshot),
                                       is_normal='正常',
                                       kinds='严重违法',
                                       level=0)
            monitor_bc_dao.add(monitor_bc)
        except Exception as e:
            logger.info(e)
        finally:
            driver.quit()

    @staticmethod
    def get_merchant_url(batch_num, merchant_name):
        webdriver = WebDriver()
        url = "https://www.qichacha.com"
        driver = webdriver.get_chrome()
        driver.set_window_size(1920, 1080)
        try:
            driver.get(url)
            driver.implicitly_wait(5)
            driver.find_element_by_id("searchkey").send_keys(merchant_name)
            driver.find_element_by_id("V3_Search_bt").click()
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            title = soup.find(name="title").get_text()
            logger.info("qichacha res title :%s", str(title))
            if str(title) == "会员登录 - 企查查":
                return None
            tbodys = soup.find_all(id="search-result")
            trs = tbodys[0].find_all('tr')
            tds = trs[0].find_all('td')
            a = tds[2].find_all('a')
            name = a[0].get_text().strip()
            href = a[0].get('href')
            if name == merchant_name.strip() and str(href) is not None:
                return href.strip()
            else:
                timestamp = int(time.time())
                path = base_filepath + "/" + batch_num + "_" + "_工商_" + str(
                    timestamp)
                snapshot = path + ".png"
                driver.save_screenshot(snapshot)
                img = Image.open(path + ".png")
                jpg = img.crop((265, 158, 420, 258))
                jpg.save(path + "_thumb.bmp")
                monitor_bc_dao = MonitorBcDao()
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=merchant_name,
                                       snapshot=snapshot,
                                       is_normal='正常',
                                       kinds='企业是否可查',
                                       level=0,
                                       outline='企查查没有查询到商户公司',
                                       create_time=datetime.datetime.now())
                monitor_bc_dao.add(monitor_bc)
            return None
        except Exception as e:
            logger.error(e)
            return None
        finally:
            driver.quit()
