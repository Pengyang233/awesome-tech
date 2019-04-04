# -*- coding: UTF-8 -*-
import requests, sys
from bs4 import BeautifulSoup

class downloader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'http://www.biqukan.com/1_1094/'
        self.names = []
        self.urls = []
        self.nums = 0

    def get_download_urls(self):
        response = requests.get(url = self.target)
        html = response.text
        bf = BeautifulSoup(html)
        temp = bf.find_all('div', class_ = 'listmain')
        a_bf = BeautifulSoup(str(temp[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_contents(self, target_url):
        response = requests.get(url = target_url)
        html = response.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', class_ = 'showtxt')
        texts = texts[0].text.replace('\xa0'*8,'\n\n')
        return texts
    
    def writer(self, name, path, text):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n' )
            f.writelines(text)
            f.write('\n\n')



if __name__ == '__main__':
    dl = downloader()
    dl.get_download_urls()
    for i in range(dl.nums):
        text_i = dl.get_contents(dl.urls[i])
        dl.writer(dl.names[i], '一念永恒.txt', text_i)
        sys.stdout.write("  已下载:%.3f%%" %  float(i/dl.nums) + '\r')
        sys.stdout.flush()
    print("下载完成")