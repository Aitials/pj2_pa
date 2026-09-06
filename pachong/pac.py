from tokenize import cookie_re

import requests

url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1&web_location=333.934&w_rid=754f67358c1be868d0ba2b5dbcd7f452&wts=1788680819'

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers)
doc = response.json()
list1 = doc['data']['list']
for i in list1:
    print(i)
print(type(list1))

