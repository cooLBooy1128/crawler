import pymongo
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


def homepage_search():
    print('进入淘宝主页')
    browser.get('https://www.taobao.com/')
    input_ = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#q')))
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-search.tb-bg')))  
    input_.send_keys(KEYWORD)
    time.sleep(random.uniform(1,3))
    button.click()


#滑块验证待调试
'''def login():
    print('进入登陆页面')
    link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.forget-pwd.J_Quick2Static')))
    time.sleep(random.uniform(0,3))
    link.click()
    
    input_user=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#TPL_username_1')))
    input_psw=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#TPL_password_1')))
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#J_SubmitStatic')))
    input_user.send_keys('tb1806987942')
    time.sleep(random.uniform(1,3))
    input_psw.send_keys('1354321688lbw')
    time.sleep(random.uniform(1,3))
    dragger=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span#nc_1_n1z')))
    action=ActionChains(browser)
    action.click_and_hold(dragger).perform()
    for index in range(90):
        action.move_by_offset(5, 0).perform() #平行移动鼠标
        action.reset_actions()
    time.sleep(random.uniform(1,3))
    while browser.find_element_by_css_selector('div.errloading'):        
        browser.refresh()
        dragger=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span#nc_1_n1z')))
        action=ActionChains(browser)
        action.click_and_hold(dragger).perform()
        for index in range(90):
            action.move_by_offset(5, 0).perform() #平行移动鼠标
            action.reset_actions()
        if browser.find_element_by_css_selector('span.nc-lang-cnt').text=='验证通过':
            break
    time.sleep(random.uniform(1,3))
    input_psw=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#TPL_password_1')))
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#J_SubmitStatic')))
    input_psw.send_keys('1354321688lbw')
    time.sleep(random.uniform(1,3))
    button.click()'''
    
    
def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        if page > 1:
            input_ = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input_.clear()
            time.sleep(random.uniform(0,3))
            input_.send_keys(page)
            time.sleep(random.uniform(0,3))
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': 'https:' + item.find('.pic .img').attr('data-src'),
            'price': float(item.find('.price').text().replace('¥','').replace('\n','')),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text().replace('\n',''),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(product):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[KEYWORD].insert_one(product):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def main():
    """
    遍历每一页
    """
    homepage_search()
    for i in range(START_PAGE, END_PAGE + 1):
        index_page(i)
        time.sleep(random.uniform(1,5))
    print('所有数据存储完成')
    browser.close()


if __name__ == '__main__':
    MONGO_URL = 'localhost'
    MONGO_DB = 'taobao'
    KEYWORD = '手机'
    START_PAGE = 96
    END_PAGE = 100
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
    #chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(browser, 10)
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    main()
