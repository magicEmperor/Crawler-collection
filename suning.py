import selenium
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = selenium.webdriver.Chrome()
browser.get('https://passport.suning.com/ids/login')
login = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.main > div > div > div.login-tab > a:nth-child(2)')))
login.click()
username = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#userName')))
password = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#password')))
username.send_keys('123456789')
password.send_keys('123456789')
submit = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#submit')))
submit.click()
vsubmit = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#iar1_sncaptcha_button')))
vsubmit.click()
ball = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.tobe-obfuscate-slide-main > div.tobe-obfuscate-slide-box.sncaptcha-jigsaw > div.tobe-obfuscate-slide-wrap > div.tobe-obfuscate-slider-wrap > div > div.tobe-obfuscate-slider.transparent-icon')))
ActionChains(browser).click_and_hold(ball).perform()