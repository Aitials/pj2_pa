import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:mysql@localhost:3306/pj2_pachong?charset=utf8mb4')
data = pd.read_sql('SELECT * FROM pj2_pachong.videos', engine)

data.replace(['','-'],np.nan, inplace=True)
data['deses'] = data['deses'].fillna('该视频的简介为空！')

data.to_sql('videos', con=engine, if_exists='replace', index=False)
print('成功写入！')




