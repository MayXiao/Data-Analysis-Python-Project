# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 18:47:07 2020

@author: May Xiao
"""

import json  
import requests  
from requests.exceptions import RequestException  
from lxml import etree
import time  

def get_one_page(url):  
    try:  
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like \
                Gecko) Chrome/65.0.3325.162 Safari/537.36'  
        }

        response = requests.get(url, headers=headers)  
        if response.status_code == 200:  
            return response.text  
        return None  
    except RequestException:  
        return None  

def parse_one_page(html): 
    html_1 = etree.HTML(html)
    index = html_1.xpath('//dd/i[contains(@class,"board-index")]/text()')
    result_star = html_1.xpath('//p[@class="star"]/text()')
    star = [i.strip() for i in result_star]
    img = html_1.xpath('//dd//img/@data-src')
    title = html_1.xpath('//p[@class="name"]//text()')
    actor = html_1.xpath('//p[@class="star"]//text()')
    time = html_1.xpath('//p[@class="releasetime"]/text()')
    result_score = html_1.xpath('//p[@class="score"]//text()')
    f = [int(i)/10 for i in result_score[1::2]] 
    i = [int(i.replace('.', '')) for i in result_score[0::2]]
    score = [x + y for x, y in zip(i, f)]
    for i in range(10):
        yield {'index': index[i], 'image': img[i], 'title': title[i], 'actor': star[i], 'time': time[i], 'score':  score[i]}

def write_to_file(content):  
    with open('result.txt', 'a', encoding='utf-8') as f:  
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  

def main(offset):  
    url = 'http://maoyan.com/board/4?offset=' + str(offset)  
    html = get_one_page(url)  
    for item in parse_one_page(html):  
        print(item)  
        write_to_file(item)  

if __name__ == '__main__':  
    for i in range(10):  
        main(offset=i * 10)  
        time.sleep(1)