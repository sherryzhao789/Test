# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:32:44 2020

@author: zhaoxinrui
"""


import requests

from bs4 import BeautifulSoup

import pandas as pd

 

# 得到页面的内容

request_url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

html=requests.get(request_url,headers=headers,timeout=10)

content = html.text

# 通过content创建BeautifulSoup对象

soup = BeautifulSoup(content, 'html.parser', from_encoding='gbk')

 

table_head = ['车型', '最低价/万', '最高价/万', '产品图片链接']

df = pd.DataFrame(columns = table_head)

#抽取完整的车辆信息框

table_body = soup.find('div',class_="search-result-list")

 

div_list = table_body.find_all('div',class_='search-result-list-item')
print(div_list)

for div in div_list:

    content = {} 

    url = 'http:' + (div.find('img', class_="img"))['src']
    print(url)

    model = div.find('p', class_="cx-name text-hover").text

    price = div.find('p', class_="cx-price").text
    print(price)

    content[table_head[0]] = model

    content[table_head[1]] = price[0:5]

    content[table_head[2]] = price[6:11]

    content[table_head[3]] = url
    print(content)

    df = df.append(content, ignore_index=True)
print(df)
 

df.to_csv('VW_SUV.csv', index=False, encoding='utf-8')




















