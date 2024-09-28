import pandas as pd
from util import *

for i in range(len(point)):
    df_row1 = pd.read_csv(path+point[i]+point[i][:-1]+"_row1_realtime_intersection.csv")
    df_row2 = pd.read_csv(path + point[i] + point[i][:-1] + "_row2_realtime_intersection.csv")

    # 确保两个 DataFrame 的形状相同
    if df_row1.shape[0] == df_row2.shape[0] and df_row1.shape[1] >= 3:
        # 数据进行相加并除以 2
        all_speed_df = df_row1.iloc[:, 2:6] + df_row2.iloc[:, 2:6]
        all_speed_df /= 2

        new_df1 = df_row1.iloc[:, 6:8] + df_row2.iloc[:, 6:8]
        # 将新的 DataFrame 连接上前两列
        result_df = pd.concat([df_row1.iloc[:, :2], all_speed_df,new_df1], axis=1)
        # 保存到新的 CSV 文件
        result_df.to_csv(path + point[i] + point[i][:-1] + "_allrow_realtime_intersection.csv", index=False)
    else:
        print("两个 DataFrame 的形状不匹配，请检查输入文件。")
