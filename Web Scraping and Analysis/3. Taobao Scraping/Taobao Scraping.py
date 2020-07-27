# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 22:32:32 2020

@author: May Xiao
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote

from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import time
from pyquery import PyQuery as pq
import requests
import csv

START_PAGE = 1
MAX_PAGE = 10

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
KEYWORD = '茶叶'
url = "https://s.taobao.com/search?q=" + quote(KEYWORD)

def login(url):
    try:
        browser.get(url)
        browser.maximize_window()
        button = browser.find_element_by_class_name('login-password')
        button.click()
        user_name = browser.find_element_by_name('fm-login-id')
        user_name.clear()
        user_name.send_keys('***') #输入淘宝名字
        time.sleep(1)
        user_keys = browser.find_element_by_name('fm-login-password')
        user_keys.clear()
        user_keys.send_keys('***') #输入密码
        time.sleep(2)
        
        source=browser.find_element_by_xpath("//*[@id='nc_1_n1z']")
        ActionChains(browser).drag_and_drop_by_offset(source,280,0).perform()
        time.sleep(1)
        browser.find_element_by_xpath(".//*[@type='submit']").click()

        time.sleep(1)
        cookies = browser.get_cookies()
        ses=requests.Session() # 维持登录状态
        c = requests.cookies.RequestsCookieJar()
        for item in cookies:
            c.set(item["name"],item["value"])
            ses.cookies.update(c)
            ses=requests.Session()
            time.sleep(1)
        print('登录成功')    
    except:
        print("登录失败")
        
def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print(' 正在爬取第 ', page, ' 页 ')
    
    try: 
        if page > 1:
            browser.find_element_by_css_selector('li.item.next').click()
    except TimeoutException:
        index_page(page)
        

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    """提取商品数据"""
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {'web': item.find('.row.row-2.title .J_ClickStat').attr('href'),
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.row.row-2.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()}
        print(product)
        write_to_csv(product)
        
def write_to_csvField(fieldname):
    with open("茶叶.csv",'a',encoding = 'utf-8', newline = '') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

def write_to_csv(product):
    with open('茶叶.csv', 'a', encoding = 'utf-8', newline='') as csvfile:    
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
        writer.writerow(product)

def main():
    login(url)
    """遍历每一页"""
    for i in range(START_PAGE, MAX_PAGE+1):
        index_page(i)
        get_products()
        sleep(2)
    
if __name__ == '__main__':
    fieldnames = ['web', 'image', 'price', 'deal', 'title', 'shop', 'location']
    write_to_csvField(fieldnames)
    main()