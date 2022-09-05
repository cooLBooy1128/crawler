import csv
import time
import re

class DataOutput():
    def __init__(self):
        self.datas=[]

    def store_data(self,data):
        if data is None:
            return
        self.datas.append(data)

    def output_csv(self):
        raw_title=self.datas[0]['title']
        if re.compile(r'(.*)（.*）').match(raw_title):
            title=re.compile(r'(.*)（.*）').match(raw_title).group(1).replace('/',' ').replace(':',' ')
        else:
            title=raw_title.replace('/',' ').replace(':',' ')
            
        header=['url','title','description']
        with open('%s_%s_基础爬虫.csv'%(title,time.strftime('%Y_%m_%d_%H_%M_%S')),'w',newline='',encoding='utf-8') as f:
            f_csv=csv.DictWriter(f,header)
            f_csv.writeheader()
            f_csv.writerows(self.datas)
                
        
