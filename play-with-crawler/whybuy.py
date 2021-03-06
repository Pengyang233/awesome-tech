#待解决问题:写入csv并定期删除和覆盖，删除过期的数据，能否直接提取出价格，关键字索引查询和提醒，能否邮件提醒？更加鲁棒，异常处理等。
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

class WhyBuy():
    def __init__(self):
        self.homepage = 'https://www.smzdm.com/jingxuan/'
        self.current_url = self.homepage
        self.page_num = 1
        self.goods_url = []
        self.goods_name = []

    #返回参数是request.response.
    def get_html(self):
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
        html = requests.get(self.current_url, headers=header)
        if html.status_code != 200:
            print('The statue code is ',html.status_code)
            print('Something goes wrong.')
            exit()
        return html
        
    #解析当前url中的相关信息，这里必须是相关的网页，不是很鲁棒
    def get_goods_info(self, html):
        bf = BeautifulSoup(html.content)
        goods = bf.find_all('h5', class_='feed-block-title')
        for i in goods:
            not_url = i.find('a').get('href')
            self.goods_url.append(not_url)
            self.goods_name.append(i.find('a').text)

    #翻页，暂定只翻页十页
    def turn_page(self):
        self.page_num = 1 + self.page_num
        self.currenu_url = 'https://www.smzdm.com/jingxuan/p'+str(self.page_num)+'/'
        
        
    def writeCsv(self, prices=0):
        with open('goods_info.csv', 'r+') as f:
            f.truncate()
        dataframe = pd.DataFrame({'Names':self.goods_name, 'urls':self.goods_url})
        dataframe.to_csv('goods_info.csv', encoding='utf_8_sig', mode='a')
    
    def searchItem(self):
        pass
    



if __name__ == '__main__':
    wanted_page = 11

    money = WhyBuy()
    html = money.get_html()
    while(money.page_num < wanted_page):
        money.get_goods_info(html)
        # print(temp_goods_name)
        money.turn_page()
        html = money.get_html()

    money.writeCsv()