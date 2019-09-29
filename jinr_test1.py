import requests


'''headers = {
    'cookie':'__utma=24953151.1804983764.1535863290.1535863290.1535863290.1; tt_webid=6718301413208049156; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6718301413208049156; csrftoken=fd6d8d5cd96e91d1424b2eccd0804476; uuid="w:b9ae73b2a2324149ace87238abf7ba76"; __tasessionId=h6e39uygz1564626720887; s_v_web_id=bd9ddf412b02652b6c617d36afd4bbe2',
    'referer':'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D%E5%9B%BE%E9%9B%86',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'x-requested-with':'XMLHttpRequest'
    }
url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D%E5%9B%BE%E9%9B%86&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1564626794092'
response = requests.get(url, headers=headers)
print(response.text)'''

from bs4 import BeautifulSoup

url = 'http://toutiao.com/group/6689978596221518350/'
headers = {
    'cookie': 'tt_webid=6718301413208049156; __utma=24953151.1804983764.1535863290.1535863290.1535863290.1; tt_webid=6718301413208049156; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6718301413208049156; csrftoken=fd6d8d5cd96e91d1424b2eccd0804476; uuid="w:b9ae73b2a2324149ace87238abf7ba76"; __tasessionId=wb5szu3cv1564633040095',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
title = soup.select('title')[0].get_text()
print(title)