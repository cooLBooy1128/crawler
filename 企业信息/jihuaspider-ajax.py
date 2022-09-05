import requests
import json
from pyquery import PyQuery as pq
import re
import urllib.parse
import time
import random
import pandas as pd

def read_canmes(filename):
    df=pd.read_excel(filename)
    return df['匹配到的名称']

def search(cname,filename):
    try:
        #print('开始查询')
        headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        base_url='https://xin.baidu.com/s?q={}'.format(urllib.parse.quote(cname))
        r1=requests.get(base_url,headers=headers1)
        p=pq(r1.text)
        #print('查询{}是否存在'.format(cname))
        pid=re.search('pid=(.*)',p('a.zx-list-item-url').attr('href')).group(1)
        url='https://xin.baidu.com/detail/basicAjax?pid={}'.format(pid)
        headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Referer': 'https://xin.baidu.com/detail/compinfo?pid={}'.format(pid),
        'X-Requested-With': 'XMLHttpRequest'
    }
        r2=requests.get(url,headers=headers2)
        address=r2.json()['data']['regAddr']
        industry=r2.json()['data']['industry']
        cname=r2.json()['data']['entName']
        shareholders=r2.json()['data']['shares']
        shareholder=''
        for i in range(len(shareholders)):
            shareholder=shareholder+' '+shareholders[i]['name']
        shareholder=shareholder.strip()
        print(cname+','+industry+','+shareholder+','+address)
        with open(filename,'a',encoding='utf-8') as file:
            file.write(cname+','+industry+','+shareholder+','+address+'\n')
    except Exception as e:
        print(e,cname)
        
if __name__ == '__main__':  

    cnames=read_canmes(r'C:\Users\szu\Desktop\new-09.16\吉华街道存续企业.xlsx')
    filename=r'C:\Users\szu\Desktop\new-09.16\爬虫\企业信息\吉华街道.txt'  
    for cname in cnames[838:999]:
        search(cname,filename)

    