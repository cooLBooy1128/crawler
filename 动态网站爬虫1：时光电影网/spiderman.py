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

    def crawl(self,root_url):
        self.manager.add_new_url(root_url)
        while self.manager.has_new_url() and self.manager.get_old_urls_size()<20:
            print('new_urls_size:'+str(self.manager.get_new_urls_size()))
            url=self.manager.get_new_url()
            rate_dict_url,newurl_dict_url=self.parser.parser(url)
            html1=self.downloader.download(rate_dict_url)
            new_data=self.parser.parser_rate_dict(rate_dict_url,html1)
            html2=self.downloader.download(newurl_dict_url)
            new_urls=self.parser.parser_newurl(newurl_dict_url,html2)
            self.manager.add_new_urls(new_urls)
            self.output.store_data(new_data) 
            print('old_urls_size:'+str(self.manager.get_old_urls_size()))
            #检验存储的数据是否有乱码
            print(new_data)
            
        self.output.output_json()
        self.output.output_csv()
        self.output.output_mysql()

url='http://movie.mtime.com/236310/'
spiderman=SpiderMan()
spiderman.crawl(url)
        
