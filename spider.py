import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import json
import re


def get_page_index(offset, keyword):   # 索引页的请求,返回源代码
    data = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from':'search_tab',
        'pd': 'synthesis',
        'timestamp': '1564585298865'
    }
    headers = {
        # 加入headers确保抓取到正确的源代码
        'content - type': 'application / x - www - form - urlencoded',
        'cookie': '__utma=24953151.1804983764.1535863290.1535863290.1535863290.1; tt_webid=6718301413208049156; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6718301413208049156; csrftoken=fd6d8d5cd96e91d1424b2eccd0804476; uuid="w:b9ae73b2a2324149ace87238abf7ba76"; __tasessionId=h6e39uygz1564626720887; s_v_web_id=bd9ddf412b02652b6c617d36afd4bbe2',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D%E5%9B%BE%E9%9B%86',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)
    try:
        response = requests.get(url, headers=headers)
        # 判断请求是否成功
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:  # 请求出错
        print("请求索引页出错")
        return None


# 获得详情页的地址url
def parse_page_index(html):
    data = json.loads(html)   # 将json字符串转换为json变量，对象
    if data and 'data' in data.keys():   # data.keys()返回data中所有的键名
        # 遍历data
        for item in data.get('data'):
            # 提取目标，生成生成器
            yield item.get('article_url')


# 请求详情页
def get_page_detail(url):
    headers = {
        # 加入headers获取正确的response源代码
        'cookie': 'tt_webid=6718301413208049156; __utma=24953151.1804983764.1535863290.1535863290.1535863290.1; tt_webid=6718301413208049156; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6718301413208049156; csrftoken=fd6d8d5cd96e91d1424b2eccd0804476; uuid="w:b9ae73b2a2324149ace87238abf7ba76"; __tasessionId=wb5szu3cv1564633040095',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        # 判断请求是否成功
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:  # 请求出错
        print("请求索引页出错")
        return None


def pares_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    images_pattern = re.compile('gallery: JSON\.parse\((.*?)\),', re.S)
    # 注意正则表达式匹配的时候不要加“”，将其提取为一个含有引号的字符串
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1))
        # 第一次是将引号里的\"转换为"
        data = json.loads(data)
        # 第二次是将其转换为字典
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            return {
                'title': title,
                'url': url,
                'images': images
            }


def save_image(result):
    title = result['title']
    re.sub('\s', "", title)
    urls = result['images']
    i=0
    for url in urls:
        i = i+1
        images = requests.get(url)
        filename = 'C:\\Users\\dell\\Desktop\\reptile\\jiepai\\' + title + '.' + str(i) + '.jpg'
        with open(filename, 'wb') as fb:
            fb.write(images.content)
            fb.close()


def main():
    for i in range(0, 5):
        html = get_page_index(i*20, '街拍图集')
        for url in parse_page_index(html):
            if url:
                html = get_page_detail(url)
                if html:
                    result = pares_page_detail(html, url)
                    if result:
                        save_image(result)


if __name__ == '__main__':
    main()

