# -*- coding: utf-8 -*-
"""实测：非法手机号提交后后端是否返回红字提示"""
import re
import urllib.parse
import urllib.request
import http.cookiejar

base = 'http://127.0.0.1:8000'
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
out = []


def log(*a):
    out.append(' '.join(str(x) for x in a))


def get(path):
    return opener.open(base + path).read().decode('utf-8')


def post(path, data):
    m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', get(path))
    data['csrfmiddlewaretoken'] = m.group(1)
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(base + path, data=body,
                                 headers={'Referer': base + path, 'Content-Type': 'application/x-www-form-urlencoded'})
    return opener.open(req).read().decode('utf-8')


# 情况 1：合法手机号（1 开头，第二位 8，11 位数字）
html = post('/pretty/add/', {'mobile': '18812345678', 'price': '10', 'level': '1', 'status': '2'})
log('[合法号 18812345678] 提交后含红字错误吗:', '手机号格式不正确' in html or '手机号已存在' in html)

# 情况 2：非法号——11 位但以 2 开头
html = post('/pretty/add/', {'mobile': '22222222222', 'price': '10', 'level': '1', 'status': '2'})
log('[非法号 22222222222（2开头）] 含红字"手机号格式不正确":', '手机号格式不正确' in html)

# 情况 3：非法号——11 位但含字母
html = post('/pretty/add/', {'mobile': 'abcdefghijk', 'price': '10', 'level': '1', 'status': '2'})
log('[非法号 abcdefghijk（字母）] 含红字"手机号格式不正确":', '手机号格式不正确' in html)

# 情况 4：查看输入框实际生成的 HTML 属性
html = get('/pretty/add/')
m = re.search(r'<input[^>]*name="mobile"[^>]*>', html)
log('[输入框实际 HTML]:', m.group(0) if m else 'NOT FOUND')

with open('verify_mobile.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('written', len(out))
