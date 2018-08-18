# -*- coding: utf-8 -*-

'''
NEEA Beta 1.0版本使用说明：
本脚本能且仅能在Python 2环境下运行
如果提示No modolued named 'requests'在CMD输入pip install requests即可解决
本代码版权归TJPU-Leo所有
禁止用于商业用途
'''

import re
import urllib
from urllib import urlretrieve
import urllib2
import cookielib
import requests
import struct
import socket
import sys
import os
import random
import base64

# url = 'http://58.218.207.205:7775/api'
# f = open('yzm.jpg', 'rb').read()
# yzm = requests.post(url, data=f)
# print yzm.text

loginUrl = 'http://cjcx.neea.edu.cn/html1/folder/1508/206-1.htm?sid=300'
queryUrl= 'http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryResults'

#cookie
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

#headers
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer':'http://cjcx.neea.edu.cn'
}

test_url = 'http://search.neea.edu.cn/Imgs.do?act=verify&t=0.7275069643506216'

values = {
    'bkjb':'24',
	'ksnf':'23kozRaPlayV4oxufU78cP',
	'ksxm':'300',
	'name':'440402199801129080',
    'nexturl':'/QueryMarkUpAction.do?act=doQueryCond&sid=300&pram=results&ksnf=23kozRaPlayV4oxufU78cP&sf=&bkjb=24&sfzh=卢晓婷&name=440402199801129080',
	'pram':'results',
    'sf':'',
    'sfzh':'卢晓婷',
    'verify':'',
    'zkzh':''
}

tmp_name = 'v23334.png'

def main():
    while 1:
        try:
            # 第一次请求网页得到cookie
            request = urllib2.Request(loginUrl, None, headers=header)
            response = opener.open(request)
            request = urllib2.Request(test_url, None, header)
            cache = opener.open(request)
            with open(tmp_name, 'wb') as f:
                f.write(cache.read())
                f.close()
            url = 'http://127.0.0.1:7775/api'
            f = open(tmp_name, 'rb').read()
            yzm = requests.post(url, data=f, timeout=5).text
            values['verify'] = yzm
            # 带验证码模拟登陆
            postdata = urllib.urlencode(values)
            request = urllib2.Request(queryUrl, postdata, header)
            response = opener.open(request, timeout=5)
            result = response.read().decode('utf-8')
            if u'结果为空' in result:
                print yzm
                os.rename(tmp_name, './Samples/'+yzm+'.png')
            else:
                print result
                print 'Error'
        except Exception,e:
            main()
            continue

if __name__=='__main__':
    main()