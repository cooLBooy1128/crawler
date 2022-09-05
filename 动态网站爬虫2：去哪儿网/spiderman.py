from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import datetime
import csv
import random

def output_csv_header():
    header=['h_number','h_name','h_score','h_price','h_address','h_link']
    with open('%s_%s_%s_去哪儿网酒店预订.csv'%(city,from_date,to_date),'w',newline='',encoding='utf-8') as f:
        f_csv=csv.DictWriter(f,header)
        f_csv.writeheader()
        
def output_csv(data):
    header=['h_number','h_name','h_score','h_price','h_address','h_link']
    with open('%s_%s_%s_去哪儿网酒店预订.csv'%(city,from_date,to_date),'a',newline='',encoding='utf-8') as f:
        f_csv=csv.DictWriter(f,header)
        f_csv.writerow(data)

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver.set_window_size(1000,600)
page_number=0

driver.get('https://www.qunar.com')
time.sleep(random.uniform(5,10))
driver.find_element_by_class_name('qhf_hotel').click()
time.sleep(random.uniform(5,10))
#mainland=driver.find_element_by_id('js_searchtype_mainland')
#inter=driver.find_element_by_id('js_searchtype_inter')
mainlandform=driver.find_element_by_id('mainlandForm')
tocity=mainlandform.find_element_by_name('toCity')
#q=mainlandform.find_element_by_name('q')
fromdate=mainlandform.find_element_by_id('fromDate')
todate=mainlandform.find_element_by_id('toDate')
search=mainlandform.find_element_by_link_text('搜  索')

city='深圳'
#入住
from_date='2019-04-13'
#离店
to_date='2019-04-14'
tocity.click()
time.sleep(random.uniform(5,10))
tocity.send_keys(city)
time.sleep(random.uniform(5,10))
tocity.send_keys(Keys.ENTER)
time.sleep(random.uniform(5,10))
fromdate.click()
time.sleep(random.uniform(5,10))
driver.find_element_by_css_selector('.dpart.dbg'+from_date[6]).find_elements_by_tag_name('td')[int(from_date[-2:])-1].click()
time.sleep(random.uniform(5,10))
todate.click()
time.sleep(random.uniform(5,10))
driver.find_elements_by_css_selector('.dpart.dbg'+to_date[6])[1].find_elements_by_tag_name('td')[int(to_date[-2:])-1].click()
time.sleep(random.uniform(5,10))
output_csv_header()
search.click()
time.sleep(random.uniform(5,10))

while page_number<5:
    try:
        WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.b_result_box.js_list_block.b_result_commentbox')))
    except Exception as e:
        print(e)
        print('加载超时,酒店信息未加载出来')
        break
    time.sleep(random.uniform(5,10))
    
    js='window.scrollTo(0,document.body.scrollHeight);'
    driver.execute_script(js)
    time.sleep(random.uniform(25,30))
    html=driver.page_source

    soup=BeautifulSoup(html,'lxml')
    page_number=int(soup.find(class_='item active').get_text())
    hotels=soup.find_all(class_='b_result_box js_list_block b_result_commentbox')
    hotel_data={}
    for h in hotels:
        hotel_data['h_number']=str(page_number)+'-'+h.find(class_='hotel_num js_hotel_num').get_text()
        hotel_data['h_name']=h.find(class_='e_title js_list_name').get_text()
        hotel_data['h_link']='http://hotel.qunar.com'+h.find(class_='e_title js_list_name').get('href')
        hotel_data['h_address']=h.find(class_='area_contair').get_text().strip()
        hotel_data['h_score']=float(h.find(class_='level_score js_list_score').find('strong').get_text())
        hotel_data['h_price']=int(h.find(class_='item_price js_hasprice').find('b').get_text())
        output_csv(hotel_data) 

    print(soup.find(class_='pager_count').get_text())
    time.sleep(random.uniform(10,20))
    try:
        next_page=WebDriverWait(driver,60).until(EC.visibility_of(driver.find_element_by_css_selector('.item.next')))
        next_page.click()
        time.sleep(random.uniform(10,20))
    except Exception as e:
        print(e)
        print('加载超时,没有下一页')
        break

driver.close()
driver.quit()
    

        
