import os
import pandas as pd

frame = pd.read_excel("大数据(Big Data)的统计学基础 15课.xlsx")

for Link in frame.loc[9,"Link"]:
    command = Link # 'youtube-dl -f 22 https://www.youtube.com/watch?v=6usedS9OT-I&index=7&list=PLGperkq3MzWI4fBIf0tAxTcX2__ogShXI'
    os.system(command)

os.system(command)

