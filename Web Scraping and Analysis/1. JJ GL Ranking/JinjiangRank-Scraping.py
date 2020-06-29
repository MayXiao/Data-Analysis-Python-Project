# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 10:35:51 2020

@author: May Xiao
"""

import requests
import csv
from lxml import etree

proxies_ip = '118.69.50.154'
proxies_port = '80'
ip_url = proxies_ip + ':' + proxies_port
proxies = {'http': 'http://' + ip_url, 'https': 'https://' + ip_url}
 
# 加上headers用来告诉网站这是通过一个浏览器进行的访问
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/81.0.4044.122 Safari/537.36'}
# 初始化csv文件
with open('JJbooks.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['序号', '作者', '作品', '类型', '风格', '进度', '字数', '作品积分', '发表时间'])
    count = 1
    # page起始值为1，爬取10页
 
    for page in range(1,10):
        url = 'http://www.jjwxc.net/bookbase.php?fw=1&ycx=1&xx=3&mainview=0&sd=0&lx=0&'\
        'fg=0&bq=-1&sortType=0&isfinish=0&collectiontypes=&searchkeywords=&page=' + str(page)
        # python获得网页源代码编码方式
        code = requests.get(url, proxies=proxies).encoding
        # print(code)
        # 获取网页源码
        res = requests.get(url, headers=headers).text
        # F12获得网页实际编码：charset = gb18030
        res = res.encode('ISO-8859-1').decode('gb18030')
        data_all = etree.HTML(res)
        # XPath 是一门在 XML 文档中查找信息的语言，XPath 可用来在 XML 文档中对元素和属性进行遍历
        author = data_all.xpath('//td[position()=1]/a/text()')
        bookname = data_all.xpath('//td[2]/a/text()')
        p_booktype = data_all.xpath('//td[position()=3]/text()[not (contains(., "类型"))]')
        # 去除列表空格和换行
        booktype = [x.strip() for x in p_booktype if x.strip() != '']
        p_style = data_all.xpath('//td[@align and position()=4]/text()')
        style = [x.strip() for x in p_style if x.strip() != '']
        wordnum = data_all.xpath('//td[@align and position()=6]/text()')
        points = data_all.xpath('//td[@align and position()=7]/text()')
        publishTime = data_all.xpath('//td[@align="center" and position()=8]/text()')
        # 筛选进度并去除列表空格和换行
        p_over = data_all.xpath('//td[@align and position()=5]/text()[contains(., "连载中")] | //font[@color="red"]/text()[contains(., "已完成")]')
        over = [x.strip() for x in p_over]

        for i in range(len(bookname)):
            writer.writerow([count, author[i], bookname[i], booktype[i], style[i], over[i], wordnum[i], points[i], publishTime[i]])
            count += 1
 
    # 注意csvfile.close()缩进问题，这应该是与for同级别，否则可能造成：ValueError: I/O operation on closed file.
    csvfile.close()