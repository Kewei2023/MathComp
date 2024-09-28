# import math
#
# def calculate_distance(begin, end):
#     x1, y1 = begin
#     x2, y2 = end
#     distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#     return math.floor(distance)
#
# begin = [1026,512]
# end = [1203,566]
# frame=4
# result = calculate_distance(begin, end)
# mps=4.5/result/(0.04*frame)
# kmph=4.5/result/(0.04*frame)/3.6
# #1 m/s = 3.6 km/h
# print(kmph)
# print(kmph*600)

'''
3
begin = [429,618]
end = [505,475]
frame=2
0.09704968944099379

5:
begin = [198, 364]
end = [133, 406]
frame=4
0.10146103896103895

7
begin = [3,542]
end = [305,420]
frame=4
0.024038461538461536

8
begin = [1026,512]
end = [1203,566]
frame=4
0.04222972972972973
'''
coefficient=[0.09704968944099379,0.10146103896103895,0.024038461538461536,0.04222972972972973]


import pandas as pd
from util import *


for i in range(len(point)):
    for t in ["mean", "sum"]:
        df_row2 = pd.read_csv(path+point[i]+ point[i][:-1] +t+"realtime.csv")
        df_row2["all_speed"]*=coefficient[i]
        df_row2["big_car_speed"] *= coefficient[i]
        df_row2.to_csv(path+point[i]+ point[i][:-1] +t+"realtime_realspeed.csv", index=False)

