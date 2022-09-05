from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote
import time
import random
from selenium.webdriver import ActionChains
import pandas as pd

def read_canmes(filename):
    df=pd.read_excel(filename)
    return df['匹配到的名称']

def homepage_search(cname):
    #print('进入企业查询主页')
    browser.get('https://xin.baidu.com')
    input_ = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input.search-text')))
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.search-btn'))) 
    input_.send_keys(cname)
    time.sleep(random.uniform(5,10))
    button.click()
    time.sleep(random.uniform(5,10))

def sub_search(cname):
    #print('进入子页查询')
    input_ = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input.search-text')))
    input_.clear()
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.search-btn'))) 
    input_.send_keys(cname)
    time.sleep(random.uniform(5,10))
    button.click()
    time.sleep(random.uniform(5,10))

def store_info(cname,filename):
    try:
        #print('查询并储存企业信息')
        time.sleep(random.uniform(5,10))
        info1=wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.zx-detail-basic-table')))
        industry=info1.text.split('\n')[2].split()[-1]
        address=info1.text.split('\n')[8].split()[1][:-4]
        info2=wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div#basic-shareholder'))).text
        if info2 != '':
            info2=wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table.zx-detail-table tbody')))
            i=2
            shareholder=''
            while i < len(info2.text.split('\n')):
                shareholder=shareholder+' '+info2.text.split('\n')[i].split()[0]
                i+=3
            shareholder=shareholder.strip()
        else:
            shareholder=''
        print(cname+','+industry+','+shareholder+','+address)
        with open(filename,'a',encoding='utf-8') as file:
            file.write(cname+','+industry+','+shareholder+','+address+'\n')
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(random.uniform(5,10))
    except TimeoutException:
        store_info(cname,filename)
 
                
if __name__ == '__main__':  
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
    #chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(browser, 10)
    
    cnames=read_canmes(r'C:\Users\szu\Desktop\new-09.16\吉华街道存续企业.xlsx')
    filename=r'C:\Users\szu\Desktop\new-09.16\爬虫\企业信息\吉华街道.txt'
    homepage_search(cnames[16])
    count=wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'em.zx-result-counter'))).text
        if count!='0':
            link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.zx-list-item-url'))) 
            link.click()
            time.sleep(random.uniform(5,10))
            browser.switch_to.window(browser.window_handles[1])
            store_info(cnames[16],filename)
        else:
            print('无搜索结果:',cname)
        
    for cname in cnames[17:]:
        sub_search(cname)
        count=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'em.zx-result-counter'))).text
        if count!='0':
            link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.zx-list-item-url'))) 
            link.click()
            time.sleep(random.uniform(5,10))
            browser.switch_to.window(browser.window_handles[1])
            store_info(cname,filename)
        else:
            print('无搜索结果:',cname)
    browser.quit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    