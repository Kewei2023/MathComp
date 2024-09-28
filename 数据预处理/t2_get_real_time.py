import pandas as pd
from util import *

seconds_list = [time_to_seconds(t) for t in base_time]

for i in range(len(point)):
    df_row1 = pd.read_csv(path_lane+point[i]+point[i][:-1]+".csv")
    n_row1 = len(df_row1)
    time_list_row1 = [seconds_list[i] + j for j in range(n_row1)]
    df_row1.iloc[:, 1] = time_list_row1
    df_row1.to_csv(path_lane+point[i]+point[i][:-1]+"_realtime.csv", index=False)