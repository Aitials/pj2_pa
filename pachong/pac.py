def Bpachong(url,headers):
    import requests
    response = requests.request("GET", url, headers=headers)
    doc = response.json()
    list = doc['data']['list']
    return list
