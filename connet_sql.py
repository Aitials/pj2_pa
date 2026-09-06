import pymysql
from pachong.pac import Bpachong

connet = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="mysql",
    database="pj2_pachong",
    charset='utf8'
)

url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1&web_location=333.934&w_rid=754f67358c1be868d0ba2b5dbcd7f452&wts=1788680819'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36'
}

cursor = connet.cursor()

insrtsql = '''
insert into videos (aid,tname,title,deses) values(%s,%s,%s,%s)
'''

lit = Bpachong(url=url, headers=headers)
for i in lit:
    data = (i['aid'], i['tname'], i['title'], i['desc'])
    cursor.execute(insrtsql, data)

connet.commit()
cursor.close()
connet.close()
print('插入成功！')