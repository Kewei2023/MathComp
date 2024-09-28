import pandas as pd
from util import *

for i in range(len(point)):
    df_row1 = pd.read_csv(path_lane+point[i]+point[i][:-1]+"_realtime.csv")
    filtered_df_row1 = df_row1[(df_row1['time_ceil'] >= time_range_lane[0]) & (df_row1['time_ceil'] <= time_range_lane[1])]
    filtered_df_row1.to_csv(path_lane+point[i]+point[i][:-1]+"_realtime_intersection.csv", index=False)