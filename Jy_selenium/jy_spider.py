import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://account.geetest.com/login'
# HEADERS = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
# }
browser = webdriver.Chrome()
browser.get(url)
wait = WebDriverWait(browser,10)

uname = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="base"]/div[2]/div/div[2]/div[3]/div/form/div[1]/div/div/input')))
uname.send_keys('11111111')
pword = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="base"]/div[2]/div/div[2]/div[3]/div/form/div[2]/div/div[1]/input')))
pword.send_keys('11111111')
yz_bt = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="captchaIdLogin"]/div/div[2]/div[1]/div[3]')))
yz_bt.click()
