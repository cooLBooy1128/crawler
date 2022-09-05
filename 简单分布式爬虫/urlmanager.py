import hashlib
import pickle

class UrlManager():
    def __init__(self):
        self.new_urls=self.load_progress('new_urls.txt')
        self.old_urls=self.load_progress('old_urls.txt')
        
    def has_new_url(self):
        return self.get_new_urls_size()!=0

    def get_new_url(self):
        new_url=self.new_urls.pop()
        m=hashlib.md5()
        m.update(new_url.encode())
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url
   
    def add_new_url(self,url):
        if url is None:
            return
        m=hashlib.md5()
        m.update(url.encode())
        if url not in self.new_urls and m.hexdigest()[8:-8] not in self.old_urls:
            self.new_urls.add(url)
        
    def add_new_urls(self,urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.add_new_url(url)

    def get_new_urls_size(self):
        return len(self.new_urls)

    def get_old_urls_size(self):
        return len(self.old_urls)

    def save_progress(self,path,data):
        with open(path,'wb') as f:
            pickle.dump(data,f)

    def load_progress(self,path):
        print('文件加载中：%s'%path)
        try:
            with open(path,'rb') as f:
                return pickle.load(f)
        except:
            print('无文件，创建：%s'%path)
        return set()
