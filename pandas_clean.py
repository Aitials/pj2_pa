import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine

connet = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="mysql",
    database="pj2_pachong",
    charset='utf8mb4'
)

engine = create_engine('mysql+pymysql://root:mysql@localhost:3306/pj2_pachong?charset=utf8mb4')
data = pd.read_sql('SELECT * FROM pj2_pachong.videos', engine)

data.replace(['','-'],np.nan, inplace=True)
data['deses'] = data['deses'].fillna('该视频的简介为空！')

data.to_sql('videos_temp', con=engine, if_exists='replace', index=False)

cursor = connet.cursor()

update_sql = '''
    UPDATE videos v
    JOIN videos_temp t ON v.aid = t.aid
    SET v.deses = t.deses
    '''

cursor.execute(update_sql)
cursor.execute("DROP TABLE videos_temp;")
connet.commit()
print('原始表成功写入！')
cursor.close()
connet.close()
#缺失值处理然后写回源数据表


data2 = data[['aid']]
data2['观看量（万）'] = (data['view']/10000).round(2)
data2['分享'] = data['share']
data2['评论'] = data['reply']
data2['点赞（万）'] = (data['ulike']/10000).round(2)
data2['收藏'] = data['favorite']
data2['类别'] = data['tname']
data2['标题'] = data['title']
data2['投币'] = data['coin']
data2['视频简介'] = data['deses']


data2.to_sql('videos_data', con=engine, if_exists='replace', index=False)
print('汇报表成功写入！')
#数据计算然后写进汇报表 ，由 pandas 自动建表补全