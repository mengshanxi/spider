import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains

url = "https://www.trackingmore.com/login-cn.html"
dcap = dict(DesiredCapabilities.PHANTOMJS.copy())
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
for key, value in headers.items():
    dcap['phantomjs.page.customHeaders.{}'.format(key)] = value

try:
    # driver = webdriver.PhantomJS(executable_path="D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe",
    #                              desired_capabilities=dcap,
    #                              service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
    #                                            '--load-images=false'])
    driver = webdriver.PhantomJS(executable_path="D:/develop/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                                 desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.get(url)
    driver.find_element_by_id("email").send_keys("rujiahua@payeasenet.com")
    driver.find_element_by_id("password").send_keys("0418YXYwlx")
    driver.find_element_by_id("login_test").click()
    list = ['LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038',
            'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038', 'LX43903175',
            'LX44244508',
            'LX44243492', 'LX44234574',
            'LX44231527', 'LX44227495',
            'LX44227359', 'LX44217199',
            'LX44206171', 'LX44201125',
            'LX44199801', 'LX44197201',
            'LX44182984', 'LX44181506',
            'LX44167272', 'LX44148955',
            'LX44148883', 'LX44146639',
            'LX44145642', 'LX44144587',
            'LX44142367', 'LX44142038']

    time.sleep(5)
    # for i in range(len(list)):
    #     number = list[i]
    #     driver.get(
    #         "https://my.trackingmore.com/numbers.php?lang=cn&p=1&keywordType=trackNumber&searchnumber=" + number)
    #     driver.maximize_window()
    #     time.sleep(1)
    #     driver.find_element_by_class_name("show_lastEvent").click()
    #     time.sleep(1)
    #     driver.save_screenshot("D://snapshots/" + str(time.time()) + ".png")
    number = 'LX43903175'
    driver.get(
        "https://my.trackingmore.com/numbers.php?lang=cn&p=1&keywordType=trackNumber&searchnumber=" + number)
    driver.maximize_window()
    time.sleep(1)
    driver.find_element_by_class_name("show_lastEvent").click()
    time.sleep(1)
    driver.save_screenshot("D://snapshots/" + str(time.time()) + ".png")
    driver.get(
        "https://my.trackingmore.com/data/data-numbers.php?lang=cn&action=get_my_number&source=2&where=lang%3Dcn%26p%3D1%26keywordType%3DtrackNumber%26searchnumber%3DLX43903175&page=1")
    source = driver.page_source
    print(source)
except Exception as e:
    print(e)
finally:
    driver.quit()
