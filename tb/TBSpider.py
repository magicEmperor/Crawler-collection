"""
    实现淘宝网页的数据抓取
"""
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
# 创建浏览器对象,并实现GET访问
browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://www.taobao.com/",)
wait = WebDriverWait(browser, 10)

# 模拟登陆
def Login():
    # 设置显示等待，判断控件是否加载成功
    login_url1 = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-sign > a.h"))
    )
    login_url1.click()
    # login_url2 = wait.until(
    #     EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, "#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static"))
    # )
    # # try:
    #     login_url2.click()
    # except FileNotFoundError:
    #     pass
    input_user = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#TPL_username_1"))
    )
    input_pwd = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#TPL_password_1"))
    )
    submit_login = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#J_SubmitStatic"))
    )
    input_user.clear()
    input_user.send_keys("zl战斗中")
    input_pwd.clear()
    input_pwd.send_keys("zyk19960213")
    time.sleep(2)
    ball = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#nc_1_n1z')))
    ActionChains(browser).click_and_hold(ball).perform()
    ActionChains(browser).move_by_offset(252, 0).perform()
    # submit_login.click()
    S_info()
# 创建方法模拟搜索美食
def S_info():
    try:
        # 设置显示等待，判断控件是否加载成功
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        input.send_keys("美食")
        submit.click()
    except TimeoutException:
        return S_info()


def run():
    Login()


if __name__ == '__main__':
    run()
