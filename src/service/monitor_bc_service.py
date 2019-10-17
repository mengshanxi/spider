import datetime
import random
import re
import time

from PIL import Image
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

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
        monitor_bc.domain_name = website.domain_name
        monitor_bc.merchant_num = website.merchant_num
        monitor_bc.website_name = website.website_name
        monitor_bc.merchant_name = website.merchant_name
        monitor_bc.saler = website.saler
        random_seconds = random.randint(20, 30)
        logger.info("企查查随机等待 %s 秒...", str(random_seconds))
        time.sleep(random_seconds)
        driver, snapshot = SnapshotService.snapshot_qichacha(batch_num, url, website)
        logger.info("driver: %s ,snapshot:%s", driver, snapshot)
        try:
            if driver is None:
                logger.info("由于企查查反扒策略无法继续！")
                monitor_bc.snapshot = '中'
                monitor_bc.is_normal = '异常'
                monitor_bc.kinds = '检测失败'
                monitor_bc.outline = '由于企查查反扒策略无法访问企业详情页。请尝试手动访问：' + url,
                monitor_bc.level = '高'
                monitor_bc_dao.add(monitor_bc)
                return
            else:
                logger.info("企查查完成截图 : %s", website.merchant_name)
            logger.info("企查查检测股东成员 : %s", website.merchant_name)
            # 2.股东成员
            random_seconds = random.randint(10, 20)
            logger.info("企查查随机等待 %s 秒...", str(random_seconds))
            time.sleep(random_seconds)
            driver.get(url)
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
            try:
                # 3.法人变更
                driver.find_element_by_link_text("工商信息").send_keys(Keys.RETURN)
                logger.info("企查查检测法人变更 : %s", website.merchant_name)
                legalmans = soup.find_all(class_='seo font-20')
                if str(website.legal_person).strip() is "":
                    monitor_bc.outline = '商户未维护法人信息，不作对比'
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '正常'
                    monitor_bc.kinds = '法人变更'
                    if legalmans.__len__() > 0:
                        monitor_bc.kinds = '法人变更:' + legalmans[0].get_text()
                    monitor_bc.level = '-'
                    monitor_bc_dao.add(monitor_bc)
                else:
                    if legalmans.__len__() > 0:
                        if str(website.legal_person).strip() == legalmans[0].get_text():
                            monitor_bc.snapshot = str(snapshot)
                            monitor_bc.is_normal = '正常'
                            monitor_bc.kinds = '法人变更:' + legalmans[0].get_text()
                            monitor_bc.outline = '未检测到法人变更'
                            monitor_bc.level = '-'
                        else:
                            monitor_bc.snapshot = str(snapshot)
                            monitor_bc.is_normal = '异常'
                            monitor_bc.kinds = '法人变更:' + legalmans[0].get_text()
                            monitor_bc.outline = '检测到法人变更，变更为:' + legalmans[0].get_text()
                            monitor_bc.level = '低'
                        monitor_bc_dao.add(monitor_bc)
            except Exception as e:
                logger.info(e)
                logger.info("html没有解析到[工商信息]..")
                monitor_bc.snapshot = str(snapshot)
                monitor_bc.is_normal = '正常'
                monitor_bc.kinds = '法人变更'
                monitor_bc.outline = '页面没有解析到工商信息。'
                monitor_bc.level = '-'
                monitor_bc_dao.add(monitor_bc)
            try:
                #  4.经营状态：注销 迁出
                logger.info("准备检测经营状态：注销 迁出 : %s ...", website.merchant_name)
                cminfo = soup.find_all(name='section', id=re.compile('Cominfo'))
                tables = cminfo[0].find_all(name='table', class_='ntable')
                trs = tables[0].find_all(name='tr')
                tds = trs[2].find_all(name='td')
                manage_state = tds[1].get_text().strip()
                # 5.经营状态-注销
                logger.info("企查查检测经营状态-注销 : %s", website.merchant_name)
                if str(manage_state).find("注销") >= 0:
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '异常'
                    monitor_bc.kinds = '经营状态'
                    monitor_bc.outline = '检测到经营状态异常：注销',
                    monitor_bc.level = '高'
                else:
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '正常'
                    monitor_bc.kinds = '经营状态'
                    monitor_bc.outline = '经营状态正常，无注销',
                    monitor_bc.level = '-'
                monitor_bc_dao.add(monitor_bc)
                # 6.经营状态-迁出
                logger.info("企查查检测经营状态-迁出 : %s", website.merchant_name)
                if str(manage_state).find("迁出") >= 0:
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '异常'
                    monitor_bc.kinds = '经营状态'
                    monitor_bc.outline = '检测到经营状态异常：迁出',
                    monitor_bc.level = '高'
                else:
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '正常'
                    monitor_bc.kinds = '经营状态'
                    monitor_bc.outline = '经营状态正常，无 迁出',
                    monitor_bc.level = '-'
                monitor_bc_dao.add(monitor_bc)
            except Exception as e:
                logger.info(e)
                logger.info("html没有解析到[经营状态]..")
                monitor_bc.snapshot = str(snapshot)
                monitor_bc.is_normal = '正常'
                monitor_bc.kinds = '经营状态'
                monitor_bc.outline = '页面没有解析到经营状态信息。'
                monitor_bc.level = '-'
                monitor_bc_dao.add(monitor_bc)
            try:
                # 7.严重违法
                logger.info("企查查检测严重违法 : %s", website.merchant_name)
                driver.find_element_by_partial_link_text("经营风险").send_keys(Keys.RETURN)
                source = driver.page_source
                soup = BeautifulSoup(source, 'html.parser')
                companys = soup.find_all(name='div', class_='company-nav-tab')
                risks = companys[3].find_all(name='span')
                manage_abn = risks[2].get_text()
                serious_illegal = risks[4].get_text()
                # 经营状态异常数: 严重违法 0
                # 严重风险数: 股权出质 0
                logger.info("经营状态异常数: %s", str(manage_abn))
                logger.info("严重风险数: %s", str(serious_illegal))
                if (len(str(manage_abn).split()) == 1 and int(manage_abn) > 0) or (
                        len(str(manage_abn).split()) == 2 and int(str(manage_abn).split()[1]) > 0):
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '异常'
                    monitor_bc.kinds = '经营状态'
                    monitor_bc.outline = '检测到经营异常风险',
                    monitor_bc.level = '高'
                else:
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '正常'
                    monitor_bc.kinds = '经营状态'
                    monitor_bc.outline = '未检测到经营异常风险',
                    monitor_bc.level = '-'
                monitor_bc_dao.add(monitor_bc)
                # 8.严重违法
                if (len(str(serious_illegal).split()) == 1 and int(serious_illegal) > 0) or (
                        len(str(serious_illegal).split()) == 2 and int(str(serious_illegal).split()[1]) > 0):
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '异常'
                    monitor_bc.kinds = '严重违法'
                    monitor_bc.outline = '检测到严重违法风险',
                    monitor_bc.level = '高'
                else:
                    monitor_bc.snapshot = str(snapshot)
                    monitor_bc.is_normal = '正常'
                    monitor_bc.kinds = '严重违法'
                    monitor_bc.outline = '未检测到严重违法风险',
                    monitor_bc.level = '-'
                monitor_bc_dao.add(monitor_bc)
            except Exception as e:
                logger.info(e)
                logger.info("html没有解析到[经营风险]..")
                monitor_bc.snapshot = str(snapshot)
                monitor_bc.is_normal = '正常'
                monitor_bc.kinds = '严重违法'
                monitor_bc.outline = '页面没有解析到经营风险信息。'
                monitor_bc.level = '-'
                monitor_bc_dao.add(monitor_bc)

                # 1.受益人
                logger.info("企查查检测受益人 : %s", website.merchant_name)
                rest_url = url + "#base"
                driver.get(rest_url)
                random_seconds = random.randint(20, 30)
                logger.info("企查查随机等待 %s 秒...", str(random_seconds))
                time.sleep(random_seconds)
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
                                shouyirens = tds[1].find_all(name='span',
                                                             class_=re.compile('ntag sm text-primary click'))
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

        except Exception as e:
            logger.info(e)
        finally:
            if driver is not None:
                driver.quit()
            else:
                pass

    @staticmethod
    def get_merchant_url(batch_num, website):
        monitor_bc_dao = MonitorBcDao()
        url = "https://www.qichacha.com"
        driver = WebDriver.get_chrome_by_local()
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.maximize_window()
        timestamp = int(time.time())
        snapshot = batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_工商_" + str(
            timestamp) + ".png"
        path = base_filepath + "/" + batch_num + "_" + website.merchant_name + "_" + website.merchant_num + "_工商_" + str(
            timestamp)
        try:
            random_seconds = random.randint(20, 30)
            logger.info("企查查随机等待 %s 秒...", str(random_seconds))
            time.sleep(random_seconds)
            driver.get(url)
            driver.find_element_by_id("searchkey").send_keys(website.merchant_name)
            driver.find_element_by_id("V3_Search_bt").click()
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            title = soup.find(name="title")
            if title is None or str(title.get_text()) == "会员登录 - 企查查" or str(title.get_text()) == "405":
                logger.info("qichacha res title :%s", str(title))
                driver.save_screenshot(path + ".png")
                img = Image.open(path + ".png")
                jpg = img.crop((265, 158, 420, 258))
                jpg.save(path + "_thumb.bmp")
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       merchant_num=website.merchant_num,
                                       website_name=website.website_name,
                                       domain_name=website.domain_name,
                                       saler=website.saler,
                                       snapshot=snapshot,
                                       is_normal='异常',
                                       kinds='企业是否可查',
                                       level='-',
                                       outline='由于企查查反扒策略无法获取企业详情链接地址。',
                                       create_time=datetime.datetime.now())
                monitor_bc_dao.add(monitor_bc)
                return None
            tbodys = soup.find_all(id="search-result")
            trs = tbodys[0].find_all('tr')
            tds = trs[0].find_all('td')
            a = tds[2].find_all('a')
            name = a[0].get_text().strip()
            href = a[0].get('href')
            if name == website.merchant_name.strip() and str(href) is not None:
                return href.strip()
            else:
                driver.save_screenshot(path + ".png")
                img = Image.open(path + ".png")
                jpg = img.crop((265, 158, 420, 258))
                jpg.save(path + "_thumb.bmp")
                monitor_bc_dao = MonitorBcDao()
                monitor_bc = MonitorBc(batch_num=batch_num,
                                       merchant_name=website.merchant_name,
                                       merchant_num=website.merchant_num,
                                       website_name=website.website_name,
                                       domain_name=website.domain_name,
                                       saler=website.saler,
                                       snapshot=snapshot,
                                       is_normal='正常',
                                       kinds='企业是否可查',
                                       level='-',
                                       outline='企查查没有查询到商户公司',
                                       create_time=datetime.datetime.now())
                monitor_bc_dao.add(monitor_bc)
            return None
        except Exception as e:
            logger.error(e)
            driver.save_screenshot(path + ".png")
            img = Image.open(path + ".png")
            jpg = img.crop((265, 158, 420, 258))
            jpg.save(path + "_thumb.bmp")
            monitor_bc = MonitorBc(batch_num=batch_num,
                                   merchant_name=website.merchant_name,
                                   merchant_num=website.merchant_num,
                                   website_name=website.website_name,
                                   domain_name=website.domain_name,
                                   saler=website.saler,
                                   snapshot=snapshot,
                                   is_normal='异常',
                                   kinds='企业是否可查',
                                   level='-',
                                   outline='由于企查查反扒策略无法获取企业详情链接地址。建议手动进行验证。',
                                   create_time=datetime.datetime.now())
            monitor_bc_dao.add(monitor_bc)
            return None
        finally:
            if driver is not None:
                driver.quit()
            else:
                pass
