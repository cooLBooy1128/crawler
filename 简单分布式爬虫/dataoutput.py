import csv
import time
import re

class DataOutput():
    def __init__(self,raw_title):
        self.datas=[]
        if re.compile(r'(.*)（.*）').match(raw_title):
            title=re.compile(r'(.*)（.*）').match(raw_title).group(1).replace('/',' ').replace(':',' ')
        else:
            title=raw_title.replace('/',' ').replace(':',' ')
        self.filepath='%s_%s_基础爬虫.csv'%(title,time.strftime('%Y_%m_%d_%H_%M_%S'))
        self.output_csvhead(self.filepath)

    def store_data(self,data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas)>9:
            self.output_csv(self.filepath)

    def output_csvhead(self,path):
        header=['url','title','description']
        with open(path,'w',newline='',encoding='utf-8') as f:
            f_csv=csv.writer(f)
            f_csv.writerow(header)

    def output_csv(self,path):
        with open(path,'a',newline='',encoding='utf-8') as f:
            header=['url','title','description']
            f_csv=csv.DictWriter(f,header)
            f_csv.writerows(self.datas)
            self.datas.clear()
                
        
