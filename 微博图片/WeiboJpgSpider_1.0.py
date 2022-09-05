import requests
import json
from pyquery import PyQuery as pq
import time
import os

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
        data=page_json.get('data')
        for item in data.get('cards'):
            if item.get('card_type')==9:
                pics=item.get('mblog').get('pics')
                if pics:
                    for pic in pics:
                        jpg_url.append('https://wx4.sinaimg.cn/large/'+pic.get('pid')+'.jpg')
        return jpg_url

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
                print('存储图片链接完成')
            with open('{}/{}_jpg_urls_add_{}.json'.format(name, name, time.strftime('%Y%m%d%H%M%S')), 'w', encoding='utf-8') as f:
                json.dump(add_urls,f,indent=4,ensure_ascii=False)
                print('存储新的图片链接完成')
        else:
            print('没有新的图片链接')
                
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

def get_url(base_url,page_json):
    if page_json:
        since_id = str(page_json.get('data').get('cardlistInfo').get('since_id'))
        print(base_url + '&since_id=' + since_id)
        return base_url + '&since_id=' + since_id

def set_base_url(uid):
    return 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid=107603{}'.format(uid,uid)

def get_user_name(page_json):
    if page_json:
        return page_json.get('data').get('cards')[0].get('mblog').get('user').get('screen_name')

def main(uid,page_count_max=700,jpg_count=None):
    '''
    用户id；查询的微博页数，默认最多为700页；要存储的图片数量，默认存储所有图片。
    '''
    jpg_urls=[]
    base_url=set_base_url(uid)
    page_json=get_page_json(base_url)
    name=get_user_name(page_json)
    jpg_urls=get_jpg_url(page_json)
    page_count=get_page_count(page_json)
    print('页面总数为：'+str(page_count))
    count= min(page_count,page_count_max)
    print('获取图片链接中...1/{}'.format(count))
    time.sleep(0.2)
    for i in range(count-1):
        url=get_url(base_url,page_json)
        page_json = get_page_json(url)
        print('获取图片链接中...{}/{}'.format(i+2,count))
        jpg_urls+=get_jpg_url(page_json)
        time.sleep(0.5)
    jpg_urls_f=list(set(jpg_urls))
    jpg_urls_f.sort(key=jpg_urls.index)
    print('图片总数为：'+str(len(jpg_urls_f)))
    store_jpg_urls(jpg_urls_f,name)
    if jpg_count is None:
        store_all_jpg(jpg_urls_f, name)
    else:
        store_jpg(jpg_urls_f,name,jpg_count)
    print('存储完成')
    
if __name__ == '__main__':
    main(1083922002,page_count_max=700,jpg_count=0)

