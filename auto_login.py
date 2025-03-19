# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00260B05ED1DF0CACF5CB105173D76F4B374023363BCBC9E7D40C30384392E2728E05318090A717790621366BBAC72E5822A1947CF22AC1A7B0B558C28FB596F19AE7C0D60C23C965F7368093B851DF5EA81E5122850514B0E6FD24423F8F46A33B87E9886406A24ED57019973A7C79D65F12294581099C065BEABD94635CBD824699B253D6DDDA406EFBB4EA4C791B9B027615C9C262CE94826AAB0091BE306BC45D0D6B51F530012B55B918286F9F1575BB2BC72FABCECA15C3D78A53D12002F6CA18FA090EAA540BBE626C1CCA11243678EC72BB1E4CF2C481880BA716059BC3A93AF148EB69615ECA642E02725F8A306B61FD699C99486471101B57FAF1F92AD39F3A69BCAC384F83EB03BED05EF5104F0DB86543D54ACA4F58FECFB1ACCB78835B932515E272A7DD37A8801F0367D18800CC7BE2CE33A61D6B079DBBCE046BDD8D383B9BED1E39B52D6A171F83C5C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
