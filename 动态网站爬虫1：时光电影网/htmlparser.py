from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
import time

class HtmlParser():
    def parser(self,rooturl):
        t=time.strftime('%Y%m%d%H%M%S93418')
        titleid=re.compile('/(\d+)/').search(rooturl).group(1)
        rate_dict_url='http://service.library.mtime.com/Movie.api?Ajax_CallBack=true'\
            '&Ajax_CallBackType=Mtime.Library.Services'\
            '&Ajax_CallBackMethod=GetMovieOverviewRating'\
            '&Ajax_CrossDomain=1'\
            '&Ajax_RequestUrl=%s'\
            '&t=%s'\
            '&Ajax_CallBackArgument0=%s'%(rooturl,t,titleid)
        newurl_dict_url='http://service.library.mtime.com/Movie.api?Ajax_CallBack=true'\
            '&Ajax_CallBackType=Mtime.Library.Services'\
            '&Ajax_CallBackMethod=GetSimilarRecommenMovieInfoByMovieId'\
            '&Ajax_CrossDomain=1'\
            '&Ajax_RequestUrl=%s'\
            '&t=%s'\
            '&Ajax_CallBackArgument0=%s'%(rooturl,t,titleid)
        return rate_dict_url,newurl_dict_url

    
    def parser_rate_dict(self,url,html):
        if url is None or html is None:
            return
        soup=BeautifulSoup(html,'lxml')
        #print(soup.prettify()) '''调试此处网页是否存在乱码'''
        pattern=re.compile(r'=(.*?);')
        rate=pattern.search(soup.getText()).group(1)
        rate_json=json.loads(rate)
        dic={}
        if rate_json.get('value').get('isRelease')==True and rate_json.get('value').get('releaseType')==3:
            dic['上映后已下架']=self.is_release_3(rate_json)
        elif rate_json.get('value').get('isRelease')==True and rate_json.get('value').get('releaseType')==1:
            dic['正在上映']=self.is_release_1(rate_json)
        elif rate_json.get('value').get('isRelease')==True and rate_json.get('value').get('releaseType')==2:
            dic['即将上映']=self.is_release_2(rate_json)
        elif rate_json.get('value').get('isRelease')==True and rate_json.get('value').get('releaseType')==0:
            dic['上映未收录']=self.is_release_0(rate_json)
        elif rate_json.get('value').get('isRelease')==False:
            dic['暂未上映']=self.not_release(rate_json)
        else:
            dic['未知']=[url]
        return dic

    def is_release_3(self,rate_json):
        data={}
        data['movieId']=rate_json.get('value').get('movieRating').get('MovieId')
        data['movieTitle']=rate_json.get('value').get('movieTitle')
        data['RatingFinal']=rate_json.get('value').get('movieRating').get('RatingFinal')
        data['Usercount']=rate_json.get('value').get('movieRating').get('Usercount')
        data['AttitudeCount']=rate_json.get('value').get('movieRating').get('AttitudeCount')
        if rate_json.get('value').get('boxOffice'):
            if rate_json.get('value').get('boxOffice').get('TotalBoxOfficeUnit')=='亿':
                data['TotalBoxOffice(Unit:万)']=float(rate_json.get('value').get('boxOffice').get('TotalBoxOffice'))*10000
            elif rate_json.get('value').get('boxOffice').get('TotalBoxOfficeUnit')=='万':
                data['TotalBoxOffice(Unit:万)']=float(rate_json.get('value').get('boxOffice').get('TotalBoxOffice'))
            else:
                data['TotalBoxOffice(Unit:万)']=None
            data['EndDate']=rate_json.get('value').get('boxOffice').get('EndDate')
        else:
            data['TotalBoxOffice(Unit:万)']=None
            data['EndDate']=None
        return data      

    def is_release_1(self,rate_json):
        data={}
        data['movieId']=rate_json.get('value').get('movieRating').get('MovieId')
        data['movieTitle']=rate_json.get('value').get('movieTitle')
        data['RatingFinal']=rate_json.get('value').get('movieRating').get('RatingFinal')
        data['Usercount']=rate_json.get('value').get('movieRating').get('Usercount')
        data['AttitudeCount']=rate_json.get('value').get('movieRating').get('AttitudeCount')
        if rate_json.get('value').get('boxOffice'):
            if rate_json.get('value').get('boxOffice').get('TotalBoxOfficeUnit')=='亿':
                data['TotalBoxOffice(Unit:万)']=float(rate_json.get('value').get('boxOffice').get('TotalBoxOffice'))*10000
            elif rate_json.get('value').get('boxOffice').get('TotalBoxOfficeUnit')=='万':
                data['TotalBoxOffice(Unit:万)']=float(rate_json.get('value').get('boxOffice').get('TotalBoxOffice'))
            else:
                data['TotalBoxOffice(Unit:万)']=None
            data['EndDate']=rate_json.get('value').get('boxOffice').get('EndDate')
            data['ShowDays']=rate_json.get('value').get('boxOffice').get('ShowDays')
        else:
            data['TotalBoxOffice(Unit:万)']=None
            data['EndDate']=None
            data['ShowDays']=None
        return data

    def is_release_2(self,rate_json):
        data={}
        data['movieId']=rate_json.get('value').get('movieRating').get('MovieId')
        data['movieTitle']=rate_json.get('value').get('movieTitle')
        data['RatingFinal']=rate_json.get('value').get('movieRating').get('RatingFinal')
        data['Usercount']=rate_json.get('value').get('movieRating').get('Usercount')
        data['AttitudeCount']=rate_json.get('value').get('movieRating').get('AttitudeCount')
        if rate_json.get('value').get('hotValue'):
            data['Ranking']=rate_json.get('value').get('hotValue').get('Ranking')
            data['RankChanging']=rate_json.get('value').get('hotValue').get('YesterdayRanking')-rate_json.get('value').get('hotValue').get('Ranking')
        else:
            data['Ranking']=None
            data['RankChanging']=None
        return data

    def is_release_0(self,rate_json):
        data={}
        data['movieId']=rate_json.get('value').get('movieRating').get('MovieId')
        data['movieTitle']=rate_json.get('value').get('movieTitle')
        data['RatingFinal']=rate_json.get('value').get('movieRating').get('RatingFinal')
        data['Usercount']=rate_json.get('value').get('movieRating').get('Usercount')
        data['AttitudeCount']=rate_json.get('value').get('movieRating').get('AttitudeCount')
        return data  

    def not_release(self,rate_json):
        data={}
        data['movieId']=rate_json.get('value').get('movieRating').get('MovieId')
        data['movieTitle']=rate_json.get('value').get('movieTitle')
        data['RatingFinal']=rate_json.get('value').get('movieRating').get('RatingFinal')
        data['Usercount']=rate_json.get('value').get('movieRating').get('Usercount')
        data['AttitudeCount']=rate_json.get('value').get('movieRating').get('AttitudeCount')
        if rate_json.get('value').get('hotValue'):
            data['Ranking']=rate_json.get('value').get('hotValue').get('Ranking')
            data['RankChanging']=rate_json.get('value').get('hotValue').get('YesterdayRanking')-rate_json.get('value').get('hotValue').get('Ranking')
        else:
            data['Ranking']=None
            data['RankChanging']=None
        return data

    def parser_newurl(self,url,html):
        if url is None or html is None:
            return
        soup=BeautifulSoup(html,'lxml')
        #print(soup.prettify()) '''调试此处网页是否存在乱码'''
        pattern=re.compile(r'=(.*?);')
        rate=pattern.search(soup.getText()).group(1)
        rate_json=json.loads(rate)
        newurl=set()
        if rate_json.get('value').get('movieList'):
            for url in rate_json.get('value').get('movieList'):
                newurl.add(url.get('url'))    
        return newurl
    


        

