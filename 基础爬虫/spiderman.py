from urlmanager import UrlManager
from htmldownloader import HtmlDownloader
from htmlparser import HtmlParser
from dataoutput import DataOutput

class SpiderMan():
    def __init__(self):
        self.manager=UrlManager()
        self.downloader=HtmlDownloader()
        self.parser=HtmlParser()
        self.output=DataOutput()

    def crawl(self,raw_url):
        self.manager.add_new_url(raw_url)
        while self.manager.has_new_url() and self.manager.get_old_urls_size()<50:
            print('new_urls_size:'+str(self.manager.get_new_urls_size()))
            url=self.manager.get_new_url()
            html=self.downloader.download(url)
            new_urls,new_data=self.parser.parser(url,html)
            self.manager.add_new_urls(new_urls)
            self.output.store_data(new_data) 
            print('old_urls_size:'+str(self.manager.get_old_urls_size()))
            #检验存储的数据是否有乱码
            print(new_data)
            
        self.output.output_csv()

url='https://baike.baidu.com/item/Fate%2FGrand%20Order/15091274'
spiderman=SpiderMan()
spiderman.crawl(url)
        
