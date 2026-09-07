import requests
def Bpachong(page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36'
    }
    alllist = []

    if page > 25:
        page = 25
        print('最多只能爬500条热门视频！')
    for i in range(1,page+1):
        url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn=' + str(i) + '&web_location=333.934&w_rid=754f67358c1be868d0ba2b5dbcd7f452&wts=1788680819'
        response = requests.request("GET", url, headers=headers)
        doc = response.json()
        list = doc['data']['list']
        alllist.extend(list)
    return alllist
