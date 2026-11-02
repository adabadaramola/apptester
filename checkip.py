from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
PROXY = "172.31.208.1:40004" # demo proxy
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options,
)
chrome.get("http://checkip.amazonaws.com")
body_text = chrome.find_element(By.TAG_NAME, 'body').text
print(body_text)
sleep(10)
chrome.quit()