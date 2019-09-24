import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    chrome_options = Options()
    url="http://yuhangren.com/"
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Remote(command_executor='http://172.19.27.54:8915/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME,
                              options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(10)
    try:
        if str(url).startswith("http"):
            http_url = str(url)
        else:
            http_url = "http://" + str(url)
        driver.get(http_url)
        title = driver.title
        if title.__contains__('404'):
            #return None, None
            print()
        else:
            print()
    except Exception as e:
        print()
    finally:
        driver.quit()
