#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/22 17:31
# @Author  : wjh
# @Site    :
# @Software: PyCharm

'''获取一个 get 请求'''
import urllib.request

reponse = urllib.request.urlopen('http://www.bing.com')
print(reponse.read().decode('utf-8'))

'''获取一个 post 请求'''
import urllib.parse,urllib.request # 数据解析

data = bytes(urllib.parse.urlencode({'hello': 'world'}), encoding='utf-8')
reponse = urllib.request.urlopen('http://httpbin.org/post', data= data)
print(reponse.read().decode('utf-8'))

'''请求”超时“处理'''
import urllib.request

try:
    reponse = urllib.request.urlopen('http://www.bing.com',timeout=0.01) # 0.01
    print(reponse.read().decode('utf-8'))
except Exception as f:
    print(f)

