from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from utils import *
import logging
import time
import re

logging.basicConfig(filename='logger.log', level=logging.ERROR, format='%(asctime)s - %(name)s - %(message)s')

def wait_and_click(path):
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, path))).click()
    
def wait_and_sendkeys(path, key):
    if path[0]=='/':
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, path))).send_keys(Keys.CONTROL + "a")
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, path))).send_keys(key)
    else:
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, path))).send_keys(Keys.CONTROL + "a")
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, path))).send_keys(key)

proxies = read_proxies_from_file('ips.txt')

while True:
    mail = generate_random_email()
    mail_url = "https://www.yopmail.com?login=" + mail.split('@')[0]
    print(f"mail is {mail}")
    print(f"mail url is {mail_url}")
    print("starting...")
    chrome_options = webdriver.ChromeOptions()
    proxy = random.choice(proxies)
    chrome_options.add_argument('--proxy-server=%s' % proxy)
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-popup-blocking')
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    driver.get("https://dev.trustyfy.com")
    start_time = time.time()
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="email"]')))
    elapsed_time = time.time() - start_time
    logging.error(f'It took {str(round(elapsed_time, 2))} sec to load the login page.')
    wait_and_sendkeys('//input[@name="email"]', mail)
    wait_and_click('//button[contains(text(), "Submit")]')
    driver.execute_script(f"window.open('{mail_url}');")
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//iframe[@id="ifmail"]')))
    iframe = driver.find_element(By.XPATH, '//iframe[@id="ifmail"]')
    #driver.switch_to.frame(iframe)
    code = ""
    while True:
        try:
            driver.switch_to.frame(iframe)
            code_text = driver.find_element(By.TAG_NAME, 'tbody').text
        except:
            code_text = "Nan"
        code = extract_login_code(code_text)
        if code:
            break
        else:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.XPATH, '//button[@id="refresh"]').click()
            except:
                pass
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    wait_and_sendkeys('//input[@name="otpnumber"]', code)
    try:
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Create a wallet")]'))).click()
        elapsed_time = time.time() - start_time
        logging.error(f'It took {str(round(elapsed_time, 2))} for user {mail} sec to load the create wallet page.')
        wallet = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div/div/div[3]/div[3]'))).text
        with open('addresses.txt', 'a') as file:
            file.write(f'mail:{mail}, address:{wallet}' + '\n')
        wait_and_click('//button[contains(text(), "Start using Trustyfy")]')
        wait_and_click('//button[contains(text(), "No thanks, I will do this later")]')
    except:
        print('user already created wallet')
    driver.close()
    driver.quit()


# WebDriverWait(driver, 120).until(
#     EC.element_to_be_clickable(element1_locator) or
#     EC.element_to_be_clickable(element2_locator)
# )