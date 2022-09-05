import time
import urllib.parse
import requests
from pyquery import PyQuery as pq
import re
import os
import json

def get_page_json(keyword,offset):
    cookie='csrftoken=fae31018ae51e77acf19dd9cc25fc764; tt_webid=6684875962541458956; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6684875962541458956; UM_distinctid=16a634a93551b1-0ce62eb02c62e-7b5c650f-100200-16a634a9356166; s_v_web_id=7abb312ee3d0e25ed0909dcb2ef7bf3c; __tasessionId=98762cx7g1556524313083; CNZZDATA1259612802=267433023-1556441929-%7C1556524468'
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.toutiao.com/search/?keyword={}'.format(urllib.parse.quote(keyword)),
        'content-type': 'application/x-www-form-urlencoded',
        'cookie':cookie
    }
    query={
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    try:
        r=requests.get('https://www.toutiao.com/api/search/content/?'+urllib.parse.urlencode(query)+'&timestamp={}'.format(round(time.time()*1000)),headers=headers)
        if r.status_code==200:
            return r.json()
    except Exception as e:
        print('get_page_json获取链接出错：',e)

def get_items(page_json):
    if page_json.get('data'):
        for item in page_json.get('data'):
            if item.get('image_list') and item.get('image_count') and item.get('image_count') > 0:
                yield{
                    'media_name':item.get('media_name'),
                    'datetime':item.get('datetime'),
                    'title':item.get('title'),
                    'item_id':item.get('item_id'),
                    'keyword':item.get('keyword')
                }
    else:
        print('此页的json文本无data，或已到达最后一页')
    
def get_image_urls(item_id):
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    url='https://www.toutiao.com/a{}/'.format(item_id)
    try:
        r=requests.get(url,headers=headers)
        if r.status_code==200:
            doc=pq(r.text)
            if re.search("content: '(.*?)'", doc('body').text(),re.S):
                content=re.search("content: '(.*?)'", doc('body').text(),re.S).group(1)
                image_urls=re.findall('(http:.*?)&quot', content)
                return image_urls
            elif re.search('JSON.parse.?"(.*?)".?', doc('body').text(),re.S):
                content=re.search('JSON.parse.?"(.*?)"\),', doc('body').text(),re.S).group(1)
                url_json=json.loads(content.replace('\\', ''))
                image_urls=[i.get('url') for i in url_json.get('sub_images')]
                return image_urls
    except Exception as e:
        print('get_image_urls获取链接出错：',e)

def store_images(image_urls,title,datetime,media_name,keyword,pid):
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    global count
    try:
        for url in image_urls:
            r=requests.get(url,headers=headers)
            if r.status_code==200:
                fdatetime = re.sub('[/:*?"<>|.]', '', datetime).replace('\\', '')
                ftitle = re.sub('[/:*?"<>|.]', '', title).replace('\\', '')
                fmedia_name=','.join(media_name)
                if not os.path.exists(keyword):
                    os.mkdir(keyword)
                if not os.path.exists(keyword+'/'+fdatetime+'_'+fmedia_name+'_'+ftitle):
                    os.mkdir(keyword+'/'+fdatetime+'_'+fmedia_name+'_'+ftitle)
                if not os.path.exists('{}/{}/{}.jpeg'.format(keyword,fdatetime+'_'+fmedia_name+'_'+ftitle,re.search('.*/(.*)',url).group(1))):
                    with open('{}/{}/{}.jpeg'.format(keyword,fdatetime+'_'+fmedia_name+'_'+ftitle,re.search('.*/(.*)',url).group(1)),'wb') as f:
                        f.write(r.content)
                        print('{}：第{}张图片存储完毕'.format(pid,count))
                        count+=1
                else:
                    print('{}：图片已存在'.format(pid))
    except Exception as e:
        print('store_images获取链接出错：',e)

def main(keyword,offset):
    pid=os.getpid()
    page_json=get_page_json(keyword,offset)
    for item in get_items(page_json):
        title=item.get('title')
        in_keyword=item.get('keyword')
        datetime=item.get('datetime')
        media_name=item.get('media_name'),
        item_id=item.get('item_id')
        image_urls=get_image_urls(item_id)
        store_images(image_urls,title,datetime,media_name,in_keyword,pid)

if __name__ == '__main__':
    '''搜索关键字，起始页码，终止页码'''
    KEYWORD='泰山' 
    START_PAGE=1
    END_PAGE=9
    offsets=[i*20 for i in range(START_PAGE-1,END_PAGE)]
    for offset in offsets:
        count=1
        main(KEYWORD,offset)
        time.sleep(1)
    print('所有图片存储完毕')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

