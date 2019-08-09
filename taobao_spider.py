from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import  requests
import time
import re

# 定义一个浏览器对象
browser = webdriver.Edge()
wait = WebDriverWait(browser, 5)


# 搜索美食首页
def search():
    try:
        # 请求淘宝首页
        browser.get('https://www.jd.com')
        # 获得搜索框对象
        inputs = wait.until(
            # 这里出现了参数个数不匹配的错误，本来只有两个参数，需要传的参数和self，所以应该用两个括号，将选择器括起来
            EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
        )
        # 获得搜索按钮
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button > i")))
        # 向搜索框发送需要搜索的内容
        inputs.send_keys('美食')

        # 点击按钮
        submit.click()
        # 获取搜索到的美食一共有多少页
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        return total.text
    except TimeoutException:
        # 如果出现超时现象，重新运行
        return search()


# 调用搜索到的下一页,翻页
def next_page(page_number):
    try:
        # 获取需要传递的页数的文本框对象
        inputs = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input'))
        )
        # 获取确定按钮
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a'))
        )
        # 清空文本框
        inputs.clear()
        # 传递页数到文本框
        inputs.send_keys(page_number)
        # 点击按钮，执行翻页操作
        submit.click()
        # 等待当前页为下一页
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page_number)))
        get_product()
    except TimeoutException:
        next_page(page_number)


def get_product():
    # 判定iterm是否加载成功
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList .gl-warp .gl-item')))
    html = browser.page_source
    # pyquery解析网页源代码
    doc = pq(html)
    items = doc('#J_goodsList .gl-warp .gl-item').items()
    pattern = re.compile('<img width="220".*?src="(.*?)"', re.S)
    for item in items:
        product = {
            'image': item.find('.gl-i-wrap .p-img .err-product').attr('data-lazy-img'),
            # 'price': item.find('.gl-i-wrap .p-price').text()[1:],
            # 'judge': item.find('.gl-i-wrap .p-commit').text()[:-3],
            'title': item.find('.gl-i-wrap .p-name').text()[4:]
        }
        title = re.sub('\s|/|<|>|\*|:|\|', '', product['title'])
        if product['image']:
            image = "https:" + str(product['image'])
            print(image)
            fileName = "C:\\Users\\dell\\Desktop\\reptile\\jindong\\" + title + '.jpg'
            url = requests.get(image)
            with open(fileName, 'wb') as f:
                f.write(url.content)
                f.close()


def main():
    # 返回的文本是，共80页，第页，需要正则匹配
    total = int(search())
    '''# 创建模式对象
    pattern = re.compile('(\d+)')
    # 匹配数字
    total = pattern.search(total).group(1)'''
    get_product()
    for i in range(2, total+1):
        next_page(i)


if __name__ == '__main__':
    main()
