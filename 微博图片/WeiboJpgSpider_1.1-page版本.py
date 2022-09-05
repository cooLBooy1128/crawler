import requests
import json
from pyquery import PyQuery as pq
import time
import os
import re

def get_page_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Referer': 'https://m.weibo.cn/u/2145291155',
        'X-Requested-With': 'XMLHttpRequest'
    }
    r=requests.get(url,headers=headers)
    if r.status_code==200:
        return r.json()


def get_jpg_url(page_json):
    jpg_url=[]
    if page_json:
        if page_json.get('data').get('cards'):
            for item in page_json.get('data').get('cards'):
                if item.get('card_type')==9:
                    pics=item.get('mblog').get('pics')
                    if pics:
                        for pic in pics:
                            jpg_url.append('https://wx4.sinaimg.cn/large/'+pic.get('pid')+'.jpg')
            return jpg_url
        else:
            return []

def format_file(filename):
    with open(filename,'r',encoding='utf-8') as f:
            l=f.read()
    with open(filename,'w',encoding='utf-8') as f:
            f.write(l.replace('\n][',','))
            
def store_jpg_urls(jpg_urls,name):
    if not os.path.exists(name):
        os.mkdir(name)
    if not os.path.exists('{}/{}_jpg_urls.json'.format(name,name)):
        with open('{}/{}_jpg_urls.json'.format(name,name), 'w', encoding='utf-8') as f:
            json.dump(jpg_urls,f,indent=4,ensure_ascii=False)
            print('首次存储图片链接完成')
        with open('{}/{}_jpg_urls_add_{}.json'.format(name, name, time.strftime('%Y%m%d%H%M%S')), 'w', encoding='utf-8') as f:
            json.dump(jpg_urls,f,indent=4,ensure_ascii=False)
            print('存储新的图片链接完成')
    else:
        with open('{}/{}_jpg_urls.json'.format(name, name), 'r', encoding='utf-8') as f:
            l1=json.load(f)
        add_urls=list(set(jpg_urls)-set(l1))
        if add_urls:
            with open('{}/{}_jpg_urls.json'.format(name, name), 'a', encoding='utf-8') as f:
                json.dump(add_urls,f,indent=4,ensure_ascii=False)
                print('存储总的图片链接完成')
            format_file('{}/{}_jpg_urls.json'.format(name, name))
            print('已格式化图片总链接文件')
            with open('{}/{}_jpg_urls_add_{}.json'.format(name, name, time.strftime('%Y%m%d%H%M%S')), 'w', encoding='utf-8') as f:
                json.dump(add_urls,f,indent=4,ensure_ascii=False)
                print('存储新的图片链接完成')
        else:
            print('没有新的图片链接')

def store_page_api_urls(page_api_urls,name):
    with open('{}/{}_page_api_urls.json'.format(name,name), 'a', encoding='utf-8') as f:
            json.dump(page_api_urls,f,indent=4,ensure_ascii=False)
            print('存储页面api链接完成')
                
def store_jpg(jpg_urls,name,jpg_count):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    count = 1
    if not os.path.exists(name):
        os.mkdir(name)
    for jpg in jpg_urls[:min(jpg_count,len(jpg_urls))]:
        r = requests.get(jpg,headers=headers)
        with open('{}/{}_{}.jpg'.format(name,name,count), 'wb') as f:
            f.write(r.content)
            print('存储图片中...{}/{}'.format(count,min(jpg_count,len(jpg_urls))))
        count+=1

def store_all_jpg(jpg_urls,name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    count = 1
    if not os.path.exists(name):
        os.mkdir(name)
    for jpg in jpg_urls:
        try:
            r = requests.get(jpg,headers=headers)
        except Exception as e:
            print(e)
        with open('{}/{}_{}.jpg'.format(name,name,count), 'wb') as f:
            f.write(r.content)
            print('存储图片中...{}/{}'.format(count, len(jpg_urls)))
        count+=1

def get_page_count(page_json):
    if page_json:
        total=page_json.get('data').get('cardlistInfo').get('total')
        return int((total+9)/10)

def get_url(base_url,page_json,url,page_api_urls,p_count):
    if page_json:
        if page_json.get('data').get('cards'):
            page = page_json.get('data').get('cardlistInfo').get('page')
            if page:
                page=str(page)
                print(re.match('(.*?&page=).*',base_url).group(1) + page)
                p_count+=1
                page_api_urls.append(re.match('(.*?&page=).*',base_url).group(1) + page)
                return re.match('(.*?&page=).*',base_url).group(1) + page,p_count
            else:
                return None,p_count
        else:
            page=str(int(re.search('page=(.*)',url).group(1))+1)
            print(re.match('(.*?&page=).*',base_url).group(1) + page)
            return re.match('(.*?&page=).*',base_url).group(1) + page,p_count
    else:
        return None,p_count
        
def set_base_url(uid,page):
    return 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid=107603{}&page={}'.format(uid,uid,page)

def get_user_name(page_json):
    if page_json:
        return page_json.get('data').get('cards')[0].get('mblog').get('user').get('screen_name')

def main(uid,page,page_count_max=700,jpg_count=None):
    '''
    用户id；
    url中的since_id参数，表示查询的起始页码，默认从头开始；
    查询的微博页数，默认最多为700页；
    要存储的图片数量，默认存储所有图片。
    '''
    base_url=set_base_url(uid,page)
    page_json=get_page_json(base_url)
    name=get_user_name(page_json)
    page_count=get_page_count(page_json)
    if page_json and name and page_count:
        print('页面总数为：'+str(page_count))
        print(base_url)
        jpg_urls=[]
        page_api_urls=[base_url]  
        url=base_url
        count= min(page_count,page_count_max)
        p_count=1
        while p_count<=count:
            if url is None:
                print('已到达最后一页')
                break
            else:
                print('获取图片链接中...页数：{}/{}'.format(p_count,count))
                page_json = get_page_json(url)
                if get_jpg_url(page_json):
                    jpg_urls+=get_jpg_url(page_json)
                url,p_count=get_url(base_url,page_json,url,page_api_urls,p_count)
                time.sleep(0.1)          
        jpg_urls_f=list(set(jpg_urls))
        jpg_urls_f.sort(key=jpg_urls.index)
        print('图片总数为：'+str(len(jpg_urls_f)))
        store_jpg_urls(jpg_urls_f,name)
        store_page_api_urls(page_api_urls,name)    
        if jpg_count<=0:
            print('图片不需要存储')
        elif jpg_count is None:
            store_all_jpg(jpg_urls_f, name)
            print('所有图片存储完成')
        else:
            store_jpg(jpg_urls_f,name,jpg_count)
            print('{}张图片存储完成'.format(jpg_count))
    else:
        print('base_url得到的json内容为空')
    
if __name__ == '__main__':
    '''
    用户id；
    url中的since_id参数，表示查询的起始页码，默认从头开始；
    查询的微博页数，默认最多为700页；
    要存储的图片数量，默认存储所有图片。
    '''
    main(5649085126,page=1,page_count_max=700,jpg_count=0)

