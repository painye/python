import requests
from bs4 import BeautifulSoup


class downLoader(object):

    # 设置需要的各种变量
    def __init__(self):
        self.server = ''
        self.target = 'https://www.23us.so/files/article/html/24/24420/index.html'
        self.name = []     # 存放各章节的名字
        self.urls = []     # 存放各章节的连接
        self.nums = 0      # 章节数
        self.html = ''     # 存放源代码
        self.text = ''

    # 获取到斗破苍穹的目录页
    def get_page(self):
        url = self.target
        response = requests.get(url)
        # 将乱码转换为utf-8格式
        self.html = response.text.encode(response.encoding).decode('utf-8')

    def get_list(self):
        soup = BeautifulSoup(self.html, 'lxml')
        lists = soup.select('#at .L')
        self.nums = len(lists)
        for l in lists:
            self.name.append(l.text)
            self.urls.append(l.a['href'])

    def get_text(self):
        for url, title in zip(self.urls, self.name):
            response = requests.get(url)
            html = response.text.encode(response.encoding).decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            texts = soup.select('.bdsub #contents')
            # select获得的都是列表，这里只能获取到一个text所以我们使用texts[0]
            print(title, '已经加载成功')
            text = texts[0].text
            fileName = 'C:\\Users\\dell\\Desktop\\reptile\\' + '斗破苍穹.text'
            with open(fileName, 'a', encoding='utf-8') as f:
                f.write(title + '\n')
                f.writelines(text + '\n\n')
                f.close()
            # self.text = self.text + title + '\n' + texts[0].text

    def print_text(self):
            print(self.text)


def man():
    d1 = downLoader()
    d1.get_page()
    d1.get_list()
    d1.get_text()
    d1.print_text()


if __name__ == '__main__':
    man()