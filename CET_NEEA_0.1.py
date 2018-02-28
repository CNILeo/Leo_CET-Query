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
import socket

print '本程序来自https://github.com/CNILeo/Leo_CET-Query'
print '     版权归TJPU-Leo所有，严禁用于商业用途！      '
print '        如在使用本软件的过程中出现报错           '
print '            可加入QQ群362699550反馈              '

socket.setdefaulttimeout(5)

loginUrl = 'http://cet.neea.edu.cn/cet/'
queryUrl= 'http://cache.neea.edu.cn/cet/query'

#cookie
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

#postdata
values = {
    'data':'',
    'v': ''
}
postdata = urllib.urlencode(values)
#headers
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer':'http://cet.neea.edu.cn/cet/'
}

xxdm = 120040 #请自行修改学校代码
type = 1 #四级修改为1，六级修改为2
kc = 83 #考场默认从1开始，可以自行修改
zwh = 1 #座位号默认从1开始，可以自行修改
zwh_gd = 0 #确认座位号的请把0修改为1
name = '郑海生'#修改为自己的名字
print '请输入学校6位代码，请自行在百度查询'
xxdm = input()
print '四级请输入1，六级请输入2'
type = input()
print '请输入开始搜索的考场号，不输入则从1号考场开始搜索'
kc = input()
zkzh = (((xxdm*1000 + 172)*10+ type)*1000 + kc) * 100 + zwh #切勿修改此处
print '请输入姓名'
name = raw_input()
values['data']='CET6_172_DANGCI,'+bytes(zkzh)+','+name
test_url = 'http://cache.neea.edu.cn/Imgs.do?c=CET&ik=' + bytes(zkzh) + '&t=0.6178564395368832'
print '正在尝试'+bytes(zkzh)
while 1:
    # 第一次请求网页得到cookie
    request = urllib2.Request(loginUrl, None, headers=header)
    try:
        response = opener.open(request,timeout=5)
    except:
        print '访问超时，如多次超时请检查网络'
        continue
    request = urllib2.Request(test_url, None, header)
    try:
        cache = opener.open(request,timeout=5)
    except:
        print '执行验证码获取脚本，如多次超时请检查网络'
        continue
    yzm = cache.read().decode('utf-8')
    #print yzm
    pattern = re.compile('"(.*?)"', re.S)
    url = re.findall(pattern, yzm)
    try:
        yzm_url = url[0]
    except:
        print '验证码地址获取超时，如多次超时请检查网络'
        continue
    try:
        urlretrieve(yzm_url, 'yzm.png')
    except urllib.ContentTooShortError:
        print '下载验证码超时，如多次超时请检查网络'
        continue
    except IOError:
        print '下载验证码超时，如多次超时请检查网络'
        continue
    f = open('yzm.png', 'rb').read()
    url = 'http://120.79.199.172:7775/api'
    try:
        yzm = requests.post(url,data = f,timeout=5).text.lower()
    except:
        print '验证码识别超时，如多次超时请检查网络'
        continue
    values['v'] = yzm
    #带验证码模拟登陆
    postdata = urllib.urlencode(values)
    request = urllib2.Request(queryUrl,postdata,header)
    try:
        response = opener.open(request, timeout = 5)
    except:
        print '提交准考证超时，如多次超时请检查网络'
        continue
    try:
        result = response.read().decode('utf-8')
    except:
        print '获取查询结果超时，如多次超时请检查网络'
        continue
    if u'验证码错误' in result:
        continue
    if u'您查询的结果为空' in result:
        if zwh_gd:
            zkzh = zkzh + 100
        else:
            zkzh += 1
            temp = zkzh - 31
            if temp % 100 == 0:
                zkzh = zkzh + 70
        values['data'] = 'CET6_172_DANGCI,' + bytes(zkzh) +','+name
        test_url = 'http://cache.neea.edu.cn/Imgs.do?c=CET&ik=' + bytes(zkzh) + '&t=0.6178564395368832'
        print '正在尝试'+bytes(zkzh)
    if 'z' in result:
        print '查找成功，准考证为：'+bytes(zkzh)
        break