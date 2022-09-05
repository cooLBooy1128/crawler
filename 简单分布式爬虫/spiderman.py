from htmldownloader import HtmlDownloader
from htmlparser import HtmlParser
from multiprocessing.managers import BaseManager
import time

class SpiderMan():
    def __init__(self):
        BaseManager.register('task_queue')
        BaseManager.register('result_queue')
        self.m=BaseManager(address=('127.0.0.1',8000),authkey='libo'.encode('utf-8'))
        self.m.connect()
        self.task=self.m.task_queue()
        self.result=self.m.result_queue()
        self.downloader=HtmlDownloader()
        self.parser=HtmlParser()

    def crawl(self):
        while True:
            #print('爬虫节点开始工作')
            if not self.task.empty():
                url=self.task.get()
                if url=='end':
                    print('爬虫节点停止工作')
                    self.result.put({'new_urls':'end','data':'end'})
                    return
                print('爬虫节点正在解析：%s'%url)
                html=self.downloader.download(url)
                new_urls,new_data=self.parser.parser(url,html)
                print('new_urls:'+str(len(new_urls)))
                self.result.put({'new_urls':new_urls,'data':new_data})
                #print('爬虫节点传输队列大小：'+str(self.result.qsize()))
            '''else:
                print('无任务')'''
        
spiderman=SpiderMan()
spiderman.crawl()
        
