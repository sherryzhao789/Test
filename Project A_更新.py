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

#抽取完整的车辆信息框
temp = soup.find('div',class_="search-result-list")
print(temp)
df = pd.DataFrame(columns = ['car_name', 'car_price', 'imgsource'])
a_list = temp.find_all('a')
print(a_list)

for a in a_list:
    temp = {}
    p_list = a.find_all('p')
    imgsource = a.find_all('img')
    print(imgsource)
    if len(p_list) > 0:
        car_name, car_price, imgsource = p_list[0].text, p_list[1].text, imgsource
        temp['car_name'], temp['car_price'], temp['imgsource'] = car_name, car_price, imgsource
        df = df.append(temp, ignore_index=True)
print(df)

#数据清理
df['car_price'] = df['car_price'].str.replace('万','')
df['car_price'] = df['car_price'].str.replace('暂无','')
print(df['car_price'])
df[['min_price','max_price']] = df['car_price'].str.split('-',expand=True)
df.drop('car_price', axis=1, inplace=True)


#将数据保存到csv文件中
data = pd.DataFrame(columns = ['car_name', 'min_price', 'max_price', 'imgsource'])
data['car_name'], data['min_price'], data['max_price'], data['imgsource'] = df['car_name'], df['min_price'], df['max_price'], df['imgsource']
data.to_csv('易车网.csv', encoding='gbk', index=False)

