import requests

class HtmlDownloader():
    def download(self,url):
        if url is None:
            return None
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        r=requests.get(url,headers=headers)
        if r.status_code==200:
            r.encoding='utf-8'
            return r.text
        return None
