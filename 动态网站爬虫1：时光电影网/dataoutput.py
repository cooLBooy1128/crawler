import csv
import time
import re
import json
import pymysql

class DataOutput():
    def __init__(self):
        self.datas={}
        self.datas['上映后已下架']=[]
        self.datas['正在上映']=[]
        self.datas['即将上映']=[]
        self.datas['上映未收录']=[]
        self.datas['暂未上映']=[]
        self.datas['未知']=[]
        
    def store_data(self,data):
        if data is None:
            return
        if data.get('上映后已下架'):
            self.datas['上映后已下架'].append(data.get('上映后已下架'))
        elif data.get('正在上映'):
            self.datas['正在上映'].append(data.get('正在上映'))
        elif data.get('即将上映'):
            self.datas['即将上映'].append(data.get('即将上映'))
        elif data.get('上映未收录'):
            self.datas['上映未收录'].append(data.get('上映未收录'))     
        elif data.get('暂未上映'):
            self.datas['暂未上映'].append(data.get('暂未上映'))
        elif data.get('未知'):
            self.datas['未知'].append(data.get('未知'))
        

    def output_csv(self):
        if self.datas.get('上映后已下架'):
            header1=['movieId','movieTitle','RatingFinal','Usercount','AttitudeCount','TotalBoxOffice(Unit:万)','EndDate']
            with open('上映后已下架_%s_动态爬虫.csv'%(time.strftime('%Y_%m_%d_%H_%M_%S')),'w',newline='',encoding='utf-8') as f:
                f_csv=csv.DictWriter(f,header1)
                f_csv.writeheader()
                f_csv.writerows(self.datas['上映后已下架'])
                
        if self.datas.get('正在上映'):
            header2=['movieId','movieTitle','RatingFinal','Usercount','AttitudeCount','TotalBoxOffice(Unit:万)','EndDate','ShowDays']
            with open('正在上映_%s_动态爬虫.csv'%(time.strftime('%Y_%m_%d_%H_%M_%S')),'w',newline='',encoding='utf-8') as f:
                f_csv=csv.DictWriter(f,header2)
                f_csv.writeheader()
                f_csv.writerows(self.datas['正在上映'])
                
        if self.datas.get('即将上映'):
            header3=['movieId','movieTitle','RatingFinal','Usercount','AttitudeCount','Ranking','RankChanging']
            with open('即将上映_%s_动态爬虫.csv'%(time.strftime('%Y_%m_%d_%H_%M_%S')),'w',newline='',encoding='utf-8') as f:
                f_csv=csv.DictWriter(f,header3)
                f_csv.writeheader()
                f_csv.writerows(self.datas['即将上映'])

        if self.datas.get('上映未收录'):
            header5=['movieId','movieTitle','RatingFinal','Usercount','AttitudeCount']
            with open('上映未收录_%s_动态爬虫.csv'%(time.strftime('%Y_%m_%d_%H_%M_%S')),'w',newline='',encoding='utf-8') as f:
                f_csv=csv.DictWriter(f,header5)
                f_csv.writeheader()
                f_csv.writerows(self.datas['上映未收录'])

        if self.datas.get('暂未上映'):
            header4=['movieId','movieTitle','RatingFinal','Usercount','AttitudeCount','Ranking','RankChanging']
            with open('暂未上映_%s_动态爬虫.csv'%(time.strftime('%Y_%m_%d_%H_%M_%S')),'w',newline='',encoding='utf-8') as f:
                f_csv=csv.DictWriter(f,header4)
                f_csv.writeheader()
                f_csv.writerows(self.datas['暂未上映'])

        if self.datas.get('未知'):
            with open('未知_%s_动态爬虫.csv'%(time.strftime('%Y_%m_%d_%H_%M_%S')),'w',encoding='utf-8') as f:
                f_csv=csv.writer(f)
                for u in self.datas['未知']:
                    f_csv.writerow(u)

    def output_json(self):
        with open('%s_动态爬虫.json'%(time.strftime('%Y_%m_%d_%H_%M_%S')),'w',encoding='utf-8') as f:
            json.dump(self.datas,f,indent=4,ensure_ascii=False)
        
    def output_mysql(self):
        con=pymysql.connect('localhost','root','135432','spiderone',3306)
        cur=con.cursor()
        '''cur.execute('create table 上映后已下架(id int unsigned auto_increment primary key,movieId int not null,movieTitle varchar(20),RatingFinal decimal(2,1),Usercount int,AttitudeCount int,TotalBoxOffice万 decimal(10,1),EndDate datetime)')
        cur.execute('create table 正在上映(id int unsigned auto_increment primary key,movieId int not null,movieTitle varchar(20),RatingFinal decimal(2,1),Usercount int,AttitudeCount int,TotalBoxOffice万 decimal(10,1),EndDate datetime,ShowDays int)')
        cur.execute('create table 即将上映(id int unsigned auto_increment primary key,movieId int not null,movieTitle varchar(20),RatingFinal decimal(2,1),Usercount int,AttitudeCount int,Ranking int,RankChanging int)')
        cur.execute('create table 上映未收录(id int unsigned auto_increment primary key,movieId int not null,movieTitle varchar(20),RatingFinal decimal(2,1),Usercount int,AttitudeCount int)')
        cur.execute('create table 暂未上映(id int unsigned auto_increment primary key,movieId int not null,movieTitle varchar(20),RatingFinal decimal(2,1),Usercount int,AttitudeCount int,Ranking int,RankChanging int)')
        cur.execute('create table 未知(id int unsigned auto_increment primary key,url varchar(200) not null)')'''

        for data in self.datas["上映后已下架"]:
            cur.execute("insert ignore into 上映后已下架 values(null,%s,%s,%s,%s,%s,%s,%s)",(data['movieId'],data['movieTitle'],data['RatingFinal'],data['Usercount'],data['AttitudeCount'],data['TotalBoxOffice(Unit:万)'],data['EndDate']))
            con.commit()
        for data in self.datas["正在上映"]:            
            cur.execute("insert ignore into 正在上映 values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(None,data['movieId'],data['movieTitle'],data['RatingFinal'],data['Usercount'],data['AttitudeCount'],data['TotalBoxOffice(Unit:万)'],data['EndDate'],data['ShowDays']))
            con.commit()
        for data in self.datas["即将上映"]:            
            cur.execute("insert ignore into 即将上映 values(%s,%s,%s,%s,%s,%s,%s,%s)",(None,data['movieId'],data['movieTitle'],data['RatingFinal'],data['Usercount'],data['AttitudeCount'],data['Ranking'],data['RankChanging']))
            con.commit()
        for data in self.datas["上映未收录"]:           
            cur.execute("insert ignore into 上映未收录 values(%s,%s,%s,%s,%s,%s)",(None,data['movieId'],data['movieTitle'],data['RatingFinal'],data['Usercount'],data['AttitudeCount']))
            con.commit()
        for data in self.datas["暂未上映"]:           
            cur.execute("insert ignore into 暂未上映 values(%s,%s,%s,%s,%s,%s,%s,%s)",(None,data['movieId'],data['movieTitle'],data['RatingFinal'],data['Usercount'],data['AttitudeCount'],data['Ranking'],data['RankChanging']))
            con.commit()
        for data in self.datas["未知"]:           
            cur.execute("insert ignore into 未知 values (%s,%s)",(None,data[0]))
            con.commit()

        con.close()


        
        
