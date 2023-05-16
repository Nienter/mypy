import json
import os
import pathlib
import time

from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
targetUrl = 'https://www.douban.com/'
username = ""
psw = ""


def login_zhi_hu():
    loginurl = targetUrl  # 登录页面
    # 加载webdriver驱动，用于获取登录页面标签属性
    # driver = webdriver.Chrome()
    driver.get(loginurl)  # 请求登录页面
    # time.sleep(50)
    # driver.implicitly_wait(10)
    driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])
    bottom = driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')  # 获取用户名输入框，并先清空
    # bottom = driver.find_element_by_class_name('account-tab-account on')
    bottom.click()
    driver.find_element_by_name('username').send_keys(username)  # 输入用户名
    driver.find_element_by_name('password').clear()  # 获取密码框，并清空
    driver.find_element_by_name('password').send_keys(psw)  # 输入密码
    # #
    time.sleep(5)
    bottom = driver.find_element_by_class_name('account-form-field-submit ')
    bottom.click()
    time.sleep(4)
    auth_frame = driver.find_element_by_id('tcaptcha_iframe')
    driver.switch_to.frame(auth_frame)
    element = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_thumb"]')
    ActionChains(driver).click_and_hold(on_element=element).perform()
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=180, yoffset=0).perform()
    tracks = get_tracks(25)  # 识别滑动验证码设置了个随意值，失败概率很大，网上方案抓取缺口图片分析坐标，成功率提高，考虑智能识别为最佳方案
    for track in tracks:
        # 开始移动move_by_offset()
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
        # 7.延迟释放鼠标：release()
    time.sleep(0.5)
    ActionChains(driver).release().perform()


def get_tracks(distance):
    """
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ①v = v0+at
    ②s = v0t+1/2at^2
    """
    # 初速度
    v = 0
    # 单位时间为0.3s来统计轨迹，轨迹即0.3内的位移
    t = 0.31
    # 位置/轨迹列表，列表内的一个元素代表0.3s的位移
    tracks = []
    # 当前位移
    current = 0
    # 到达mid值开始减速
    mid = distance * 4 / 5
    while current < distance:
        if current < mid:
            # 加速度越小，单位时间内的位移越小，模拟的轨迹就越多越详细
            a = 2.3
        else:
            a = -3

        # 初速度
        v0 = v
        # 0.3秒内的位移
        s = v0 * t + 0.5 * a * (t ** 2)
        # 当前的位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))
        # 速度已经到达v,该速度作为下次的初速度
        v = v0 + a * t
    return tracks


def login_with_cookies():
    driver.get(targetUrl)
    with open("cookies.txt", "r") as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.get(targetUrl)
    update_cookies()


def update_cookies():
    f = open("cookies.txt", 'w')
    f.truncate()
    cookies = driver.get_cookies()
    with open("cookies.txt", "w") as fp:
        json.dump(cookies, fp)


def is_file_exit():
    path = pathlib.Path('cookies.txt')
    if not os.path.getsize(path):
        return False
    return path.is_file()


if __name__ == '__main__':
    if is_file_exit():
        login_with_cookies()
    else:
        login_zhi_hu()
        time.sleep(4)
        cookies = driver.get_cookies()
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
