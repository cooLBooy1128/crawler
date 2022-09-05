import json
import requests
from requests.exceptions import RequestException
import re
import time
from bs4 import BeautifulSoup
 
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    soup=BeautifulSoup(html,'lxml')
    soup1=soup.find('dl',class_='board-wrapper')
    for r in range(10):
        yield {
            'index': soup1.find_all('dd')[r].find('i').get_text(),
            'image': soup1.find_all('dd')[r].find('img',class_='board-img').get('data-src'),
            'title': soup1.find_all('dd')[r].find('a').get('title'),
            'actor': soup1.find_all('dd')[r].find('p',class_='star').get_text().strip()[3:],
            'time': soup1.find_all('dd')[r].find('p',class_='releasetime').get_text().strip()[5:],
            'country': soup1.find_all('dd')[r].find('p',class_='releasetime').get_text().strip()[5:],
            'score': soup1.find_all('dd')[r].find('p',class_='score').get_text()
        }

def write_to_file(content):
    with open('猫眼电影排行榜.json', 'a', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False,indent=4)

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
        time.sleep(1)
