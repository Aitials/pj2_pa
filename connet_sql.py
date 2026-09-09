import pymysql
from pachong.pac import Bpachong

connet = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="mysql",
    database="pj2_pachong",
    charset='utf8mb4'
)

cursor = connet.cursor()

insrtsql = '''
insert into videos (aid, tname, title, deses, author, view, reply, favorite, share, coin)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    tname = VALUES(tname),
    title = VALUES(title),
    deses = VALUES(deses),
    author = VALUES(author),
    view = VALUES(view),
    reply = VALUES(reply),
    favorite = VALUES(favorite),
    share = VALUES(share),
    coin = VALUES(coin)
'''

lit = Bpachong(page = 25)
for i in lit:
    data = (i['aid'], i['tname'], i['title'], i['desc'],i['owner']['name'],i['stat']['view'],i['stat']['reply'],i['stat']['favorite'],i['stat']['share'],i['stat']['coin'])
    cursor.execute(insrtsql, data)

connet.commit()
cursor.close()
connet.close()
print('数据爬取成功！')