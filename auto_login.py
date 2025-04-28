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
    browser.add_cookie({"name": "MUSIC_U", "value": "000C59BBDE3D58B9CA6DB78E5CF86696E6A204E29DC1079A27549A33B6D720FD83BF32071804F70E9540FF714FACBDDB0E5FA358B2AF9FBCB86F19D5BB522C3D595B98A021CBB0524B8C14E97E1A03166C8FE240099484FDCEBA5EB7A34F2DF695135C54C7F0876CC6EB191BF4D2D5B46FB060A20813014C8357C660A928937ED43453DC11D86777DF2962A3A9AF8D9649346AB268CF7086793257E9E4DF6C3B244EB215261A4F0F6419556122560E3EA4474C05A89DA71C3A2825E69757B4B51B18826C3422180887A280A07B4B4E3111179E5AFBF16E9E5DB7A8FE5E609278A1A58C08A976140B6578800EDBBBDDB3C9F47D72FF1C36B7B28A94F5D9A3F5344D7B3BEF75E9F9FFDDA1F880B9A2C6D7B1DAE737698A96BE878B59BDA7B544873D70F15D1E147830E5CC4E06DCC1EA2C338880C71CB030C6B476C8319E7FB5BE5ABE05D1E91FA81D0C36C042320FD848E1"})
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
