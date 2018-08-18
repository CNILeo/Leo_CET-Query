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
reload(sys)

sys.setdefaultencoding('utf8')

socket.setdefaulttimeout(1)
loginUrl = 'http://cjcx.neea.edu.cn/ncre/query.html'
queryUrl= 'http://cache.neea.edu.cn/report/query'

#cookie
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

#postdata
values = {
    'data':'NCRE,NCRE_1803,0,14,440402199801129080,卢晓婷',
    'iscerti':'',
    'v': ''
}
postdata = urllib.urlencode(values)
#headers
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer':'http://cjcx.neea.edu.cn/ncre/query.html'
}

test_url = 'http://cache.neea.edu.cn/Imgs.do?c=NCRE&ik=440402199801129080&t=0.09857573181718626'

name = 'yzm2.png'

while 1:
    try:
        # 第一次请求网页得到cookie
        request = urllib2.Request(loginUrl, None, headers=header)
        response = opener.open(request,timeout=5)
        request = urllib2.Request(test_url, None, header)
        cache = opener.open(request,timeout=1)
        yzm = cache.read().decode('utf-8')
        pattern = re.compile('"(.*?)"', re.S)
        url = re.findall(pattern, yzm)
        yzm_url = url[0]
        request = urllib2.Request(yzm_url, None, header)
        yzm_cache = opener.open(request, timeout=1)
        with open(name, 'wb') as f:
            f.write(yzm_cache.read())
            f.close()
        f = open(name, 'rb').read()
        url = 'http://127.0.0.1:7775/api'
        yzm = requests.post(url,data = f,timeout=5).text.lower()
        values['v'] = yzm
        postdata = urllib.urlencode(values)
        request = urllib2.Request(queryUrl,postdata,header)
        response = opener.open(request, timeout = 5)
        result = response.read().decode('utf-8')
        if u'验证码错误' in result:
            continue
        elif u'您查询的结果为空' in result:
            print yzm
            os.rename(name, './DATA2/' + yzm.upper() + '.png')
    except Exception,e:
        print e.message
        continue