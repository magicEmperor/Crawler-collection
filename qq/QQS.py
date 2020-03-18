from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get('https://aq.qq.com/cn2/index')
#switcher_plogin
time.sleep(2)
login = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#banner > div.banner-bg > div.banner-header > div > div.header-right > div.header-login > a')))
login.click()
browser.switch_to.frame('embed_login_frame')
username = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#u')))
password = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#p')))
username.clear()
username.send_keys('940040346')
password.send_keys('k1996021')
submit = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#login_button')))
submit.click()