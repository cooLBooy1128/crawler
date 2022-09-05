from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class HtmlParser():
    def parser(self,url,html):
        if url is None or html is None:
            return
        soup=BeautifulSoup(html,'lxml')
        #print(soup.prettify()) '''调试此处网页是否存在乱码'''
        new_urls=self.get_new_urls(url,soup)
        new_data=self.get_new_data(url,soup)
        return new_urls,new_data

    def get_new_urls(self,url,soup):
        new_urls=set()
        try:
            soup1=soup.find('div',class_='content-wrapper')
            for a in soup1.find_all('a',href=re.compile(r'/item/.*')):
                new_part_url=a.get('href')
                new_url=urljoin(url,new_part_url)
                new_urls.add(new_url)
        except Exception as e:
            print(e)
        return new_urls

    def get_new_data(self,url,soup):
        data={}
        data['url']=url
        raw_title=soup.head.title.get_text()
        title=re.compile(r'(.*)_百度百科').match(raw_title).group(1)
        data['title']=title
        raw_description=soup.head.find('meta',attrs={'name':'description'}).get('content')
        description=re.compile(r'(.*)...').match(raw_description).group(1)
        data['description']=description
        return data
        

