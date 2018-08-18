# -*- coding: utf-8 -*-

import re
import urllib
from urllib import urlretrieve
import urllib2
import cookielib

cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

login_url = "http://cet.neea.edu.cn/cet/"
code_url = "http://cache.neea.edu.cn/Imgs.do"
query_url="http://cache.neea.edu.cn/cet/query"

request = urllib2.Request(login_url, None)
response = opener.open(request)


header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'http://cet.neea.edu.cn/cet/'
}
values={
    'data':'',
    'v':''
}
Get_Data={
    'c':'CET',
    'ik':'12004017220101',
    't':'0.07860860804733794'
}
kc = 27
zwh = 9
zkzh = 120040172102709
while 1:
    print zkzh
    values['data']="CET4_172_DANGCI,"+bytes(zkzh)+",林婉滢"
    Get_Data['ik']=zkzh
    code = code_url + "?" + urllib.urlencode(Get_Data)
    request = urllib2.Request(code, None,header)
    response = opener.open(request)
    content=response.read().decode("utf-8")
    pattern=re.compile('"(.*?)"',re.S)
    text = re.findall (pattern, content)
    print text[0]
    yzm_url = text[0]
    urlretrieve(yzm_url, 'yzm.png')
    print u'请输入验证码'
    values['v']=raw_input()
    request = urllib2.Request(query_url, urllib.urlencode(values), header)
    response = opener.open(request)
    result = response.read().decode("utf-8")
    print result
    if 'z' in result:
        print "查找成功！"+bytes(zkzh)
        break
    elif u'您查询的结果为空' in result:
        zwh += 1
        if zwh==31:
            zwh = 1
            kc += 1
        zkzh = (1200401721 * 1000 + kc) * 100 + zwh