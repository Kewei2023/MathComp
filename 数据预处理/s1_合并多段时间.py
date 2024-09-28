import pandas as pd
from util import *

for i in range(len(point)):
    # df_row1 = []
    # for r in row1[i]:
    #     filepath = path+point[i] + r + ".csv"
    #     df = pd.read_csv(filepath)
    #     df_row1.append(df[1:])
    # combined_df = pd.concat(df_row1, ignore_index=True)
    # combined_df.to_csv(path+point[i]+ point[i][:-1] +"_row1.csv", index=False)
    for t in ["mean", "sum"]:
        df_row2 = []
        for r in row2_special[i]:
            filepath = path + point[i] + r +t+ ".csv"
            df = pd.read_csv(filepath)
            df_row2.append(df[1:])
        combined_df = pd.concat(df_row2, ignore_index=True)
        combined_df.to_csv(path+point[i]+ point[i][:-1] +t+".csv", index=False)
