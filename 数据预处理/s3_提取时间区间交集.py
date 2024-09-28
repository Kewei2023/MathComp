import pandas as pd
from util import *

for i in range(len(point)):
    df_row1 = pd.read_csv(path+point[i]+point[i][:-1]+"_row1_realtime.csv")
    filtered_df_row1 = df_row1[(df_row1['time_ceil'] >= time_range[0]) & (df_row1['time_ceil'] <= time_range[1])]
    filtered_df_row1.to_csv(path+point[i]+point[i][:-1]+"_row1_realtime_intersection.csv", index=False)

    df_row2 = pd.read_csv(path + point[i] + point[i][:-1] + "_row2_realtime.csv")
    filtered_df_row2 = df_row2[(df_row2['time_ceil'] >= time_range[0]) & (df_row2['time_ceil'] <= time_range[1])]
    filtered_df_row2.to_csv(path + point[i] + point[i][:-1] + "_row2_realtime_intersection.csv", index=False)