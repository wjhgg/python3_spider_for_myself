#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/22 18:49
# @Author  : wjh
# @Site    :
# @Software: PyCharm

'''豆瓣好于100%-90%的科幻片'''
import sqlite3

from bs4 import BeautifulSoup  # 网页解析 获取数据
import re  # 正则表达式
import urllib.request  # 指定url获取页面数据
import urllib.error
import xlwt  # 进行excel操作
from selenium import webdriver


def main():
    url = "https://www.bilibili.com/ranking?spm_id_from=333.851.b_7072696d61727950616765546162.3"

    savepath = ".\\B站全站排行Top100.xls"
    dbpath = 'bilibiliTop100.db'
    datelist = getInfo(url)
    # 保存数据
    # saveInfo(savepath, datelist)
    bili_db(dbpath,datelist)
    # chrome(url)

# 模拟浏览器
def chrome(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
    except Exception as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

    return html

####################
####### 正则 ########
####################
pm = re.compile(r'<div class="num">(.*?)</div>')  # 排行榜
bt = re.compile(r'<a .* target="_blank" class="title">(.*?)</a>')  # 标题名称
lj = re.compile(r'<a href="(.*?)">')  # 视频链接
bf = re.compile(r'<span class="data-box"><i class="b-icon play"></i>(.*?)</span>')  # 播放量
dm = re.compile(r'<span class="data-box"><i class="b-icon view"></i>(.*?)</span>')  # 弹幕
upid = re.compile(r'<span class="data-box"><i class="b-icon author"></i>(.*?)</span>')  # up主id
upzy = re.compile(r'<a.*href="(.*?)">')  # UP主页链接
zhdf = re.compile(r'<div class="pts"><div>(.*?)</div>(.*?)</div>',re.S)  # 综合得分

# 爬取想要的内容
def getInfo(url):
    datalist = []

    html = chrome(url)   # 保存获取的网页源码
    # print(html)
    # 解析网页
    soup = BeautifulSoup(html, 'html.parser')  # html.parser；lxml；xml；html5lib。
    # 查找获取想要的info
    for item in soup.find_all('div', class_="content"):

        # print(item)

        data = []  # 保存我们想要的信息
        item = str(item)

        # 通过正则获取信息
        # 排名
        p = re.findall(pm, item)
        data.append(p)
        # 标题名称
        b = re.findall(bt, item)
        data.append(b)
        # 视频链接
        l = re.findall(lj, item)
        data.append(l)
        # 播放量
        f = re.findall(bf, item)
        data.append(f)
        # 弹幕
        d = re.findall(dm, item)
        data.append(d)
        # up主id
        i = re.findall(upid, item)
        data.append(i)
        # UP主页链接
        z = re.findall(upzy, item)
        data.append(z)
        # 综合得分
        h = re.findall(zhdf, item)
        data.append(h)

        datalist.append(data)
    return datalist

# 保存数据:EXCEL
def saveInfo(savepath, datalist):
    print("begin save......")
    workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)  # 创建workbook对象
    worksheet = workbook.add_sheet("B站全站排行Top100", cell_overwrite_ok=True)  # 创建工作表
    col = ("排名","标题名称","视频链接","播放量","弹幕","up主id","UP主页链接",'综合得分')
    for i in range(0,8):
        worksheet.write(0,i,col[i])
    for i in range(0,100):
        print("第%d条"%(i+1))
        data=datalist[i]
        for s in range(0,8):
            worksheet.write(i+1,s,data[s])  #数据

    workbook.save(savepath) #保存

# 保存数据:SQL
def bili_db(dbpath):
    sql = '''
     create table bilibiliTop100
     (
     id integer primary key autoincrement,
     pm int,
     bname varchar,
     ca_link text,
     bf int,
     dm int,
     upid int,
     upmain text,
     fs int
     )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # main()
    bili_db('test.db')
    print('Finnish！')
