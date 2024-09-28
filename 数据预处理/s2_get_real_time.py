import pandas as pd
from util import *

seconds_list = [time_to_seconds(t) for t in base_time]

for i in range(len(point)):
    # df_row1 = pd.read_csv(path+point[i]+point[i][:-1]+"_row1.csv")
    # n_row1 = len(df_row1)
    # time_list_row1 = [seconds_list[i] + j*10 for j in range(n_row1)]
    # df_row1.iloc[:, 1] = time_list_row1
    # df_row1.to_csv(path+point[i]+point[i][:-1]+"_row1_realtime.csv", index=False)
    for t in ["mean", "sum"]:
        df_row2 = pd.read_csv(path+point[i]+ point[i][:-1] +t+".csv")
        n_row2 = len(df_row2)
        time_list_row2 = [seconds_list[i] + j for j in range(n_row2)]
        df_row2.iloc[:, 1] = time_list_row2
        df_row2.to_csv(path+point[i]+ point[i][:-1] +t+"realtime.csv", index=False)
