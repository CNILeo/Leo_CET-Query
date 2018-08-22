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

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
		password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

sys.setdefaultencoding('utf8')

socket.setdefaulttimeout(1)
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
type = 2 #四级修改为1，六级修改为2
kc = 83 #考场默认从1开始，可以自行修改
zwh = 1 #座位号默认从1开始，可以自行修改
zwh_gd = 0 #确认座位号的请把0修改为1
name = '杨庆新'#修改为自己的名字
zkzh = (((xxdm*1000 + 181)*10+ type)*1000 + kc) * 100 + zwh #切勿修改此处
print name
if type == 1:
    Type = 'CET4_181_DANGCI,'
elif type == 2:
    Type = 'CET6_181_DANGCI,'
values['data']=Type+bytes(zkzh)+','+name
print values['data']
test_url = 'http://cache.neea.edu.cn/Imgs.do?c=CET&ik=' + bytes(zkzh) + '&t=0.2626517146154804'
print u'正在尝试'+bytes(zkzh)
chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰用户名的密码', '96001') #修改为超级鹰的账号密码
while 1:
    # 第一次请求网页得到cookie
    request = urllib2.Request(loginUrl, None, headers=header)
    try:
        response = opener.open(request,timeout=5)
    except:
        print u'访问超时，如多次超时请检查网络'
        continue
    request = urllib2.Request(test_url, None, header)
    try:
        cache = opener.open(request,timeout=60)
    except:
        print u'执行验证码获取脚本，如多次超时请检查网络'
        continue
    try:
        yzm = cache.read().decode('utf-8')
    except socket.timeout:
        continue
    except socket.error:
        continue
    #print yzm
    pattern = re.compile('"(.*?)"', re.S)
    url = re.findall(pattern, yzm)
    try:
        yzm_url = url[0]
    except:
        print u'验证码地址获取超时，如多次超时请检查网络'
        continue
    try:
        urlretrieve(yzm_url, 'yzm.png')
    except urllib.ContentTooShortError:
        print u'下载验证码超时，如多次超时请检查网络'
        continue
    except IOError:
        print u'下载验证码超时，如多次超时请检查网络'
        continue
    f = open('yzm.png', 'rb').read()
    try:
        yzm = chaojiying.PostPic(f, 1902)
    except:
        print u'验证码识别超时，如多次超时请检查网络'
        continue
    values['v'] = yzm
    #带验证码模拟登陆
    postdata = urllib.urlencode(values)
    request = urllib2.Request(queryUrl,postdata,header)
    try:
        response = opener.open(request, timeout = 5)
    except:
        print u'提交准考证超时，如多次超时请检查网络'
        continue
    try:
        result = response.read().decode('utf-8')
    except:
        print u'获取查询结果超时，如多次超时请检查网络'
        continue
    if u'验证码错误' in result:
        continue
    if u'您查询的结果为空' in result:
        if zwh_gd:
            zkzh = zkzh + 100
        else:
            zkzh += 1
            kc += 1
            temp = zkzh - 31
            if temp % 100 == 0:
                zkzh = zkzh + 70
        values['data'] = Type + bytes(zkzh) +','+name
        test_url = 'http://cache.neea.edu.cn/Imgs.do?c=CET&ik=' + bytes(zkzh) + '&t=0.6178564395368832'
        print u'正在尝试'+bytes(zkzh)
    if 'z' in result:
        print u'查找成功，准考证为：'+bytes(zkzh)
        os.system('C:\\Users\\Leo\\Desktop\\find.mp3')
        break