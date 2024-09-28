import pandas as pd
from util import *

for i in range(len(point)):
    df_row1 = []
    for r in files_lane_change[i]:
        filepath = path_lane+point[i] + r + "_deal_flow.csv"
        df = pd.read_csv(filepath)
        df_row1.append(df[1:])
    combined_df = pd.concat(df_row1, ignore_index=True)
    combined_df.to_csv(path_lane+point[i]+ point[i][:-1] +".csv", index=False)

