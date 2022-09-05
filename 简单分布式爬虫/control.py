from multiprocessing.managers import BaseManager
from urlmanager import UrlManager
from dataoutput import DataOutput
from multiprocessing import Queue
from multiprocessing import Process
from multiprocessing import freeze_support
import time

class Controler():
    def __init__(self):
        self.url_q=Queue()
        self.result_q=Queue()
        self.store_q=Queue()
        self.conn_q=Queue()
        
    def start_manager(self):
        def task():
            return self.url_q
        def result():
            return self.result_q
        BaseManager.register('task_queue',callable=task)
        BaseManager.register('result_queue',callable=result)
        manager=BaseManager(address=('127.0.0.1',8000),authkey='libo'.encode('utf-8'))
        return manager

    def url_manager_proc(self,root_url):
        url_manager=UrlManager()
        url_manager.add_new_url(root_url)

        while True:
            while url_manager.has_new_url():
                print('new_url='+str(url_manager.get_new_urls_size()))
                url=url_manager.get_new_url()
                self.url_q.put(url)
                print('old_url='+str(url_manager.get_old_urls_size()))
                if(url_manager.get_old_urls_size()>=500):
                    self.url_q.put('end')
                    url_manager.save_progress('new_urls.txt',url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt',url_manager.old_urls)
                    print('Url管理进程结束')
                    return

            if not self.conn_q.empty():
                print('新Url传输队列大小:'+str(self.conn_q.qsize()))
                urls=self.conn_q.get()
                url_manager.add_new_urls(urls)

    def result_solve_proc(self):
        while True:
            #print('数据提取进程开始')
            print('返回数据队列大小:'+str(self.result_q.qsize()))
            if not self.result_q.empty():
                content=self.result_q.get()
                if content['new_urls']=='end':
                    self.store_q.put('end')
                    print('数据提取进程结束')
                    return
                #print('数据提取进程进行')
                self.conn_q.put(content['new_urls'])
                self.store_q.put(content['data'])
            '''else:
                print('返回数据队列为空')'''
                
    def store_proc(self):
        while True:
            #print('写文件名')
            if not self.store_q.empty():
                data1=self.store_q.get()
                title=data1['title']
                output=DataOutput(title)
                break
        while True:
            #print('数据存储进程开始')
            print('存储数据队列大小:'+str(self.store_q.qsize()))
            if data1:
                output.store_data(data1)
                data1=None  
            if not self.store_q.empty():
                data=self.store_q.get()
                if data=='end':
                    print('数据存储进程结束')
                    return
                output.store_data(data)
            '''else:
                print('存储数据队列为空')'''
                
                
if __name__=='__main__':
    freeze_support() 
    control=Controler()
    manager=control.start_manager()
    url_manager_proc=Process(target=control.url_manager_proc,args=(
    'https://baike.baidu.com/item/Fate%2FGrand%20Order/15091274',))
    result_solve_proc=Process(target=control.result_solve_proc)
    store_proc=Process(target=control.store_proc)
    url_manager_proc.start()    
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()
