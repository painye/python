import time
from selenium import webdriver

browser = webdriver.Edge()
browser.get('https://www.taobao.com')
browser.execute_script('window.open()')   # 新建一个选项卡
print(browser.window_handles)
browser.switch_to.window(browser.window_handles[1])  # 切换到第二个选项卡
browser.get('https://www.taobao.com')
time.sleep(1)
browser.switch_to.window(browser.window_handles[0]) # 切换到第二个选项卡
browser.get('https://www.baidu.com')# dsffsdfsdfsdfdwf
