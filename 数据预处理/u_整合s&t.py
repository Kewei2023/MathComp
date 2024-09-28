import pandas as pd
from  util import  *


for i in range(len(point)):
    # 读取 a.csv 和 b.csv
    a_df = pd.read_csv(path_lane+point[i]+point[i][:-1]+"_realtime_intersection.csv")
    b_df = pd.read_csv(path + point[i] + point[i][:-1] + "_allrow_realtime_intersection.csv")

    # 选择 a.csv 的第 4，6，7，9 列
    selected_columns = a_df.iloc[:, [3, 5, 6, 8]]

    # 删除 b.csv 中多余的行
    b_df = b_df.iloc[:selected_columns.shape[0]]

    # 创建 b.csv 的新列并赋值
    b_df[['row1_to_row2', 'row2_to_row1', 'row2_to_argent', 'argent_to_row2']] = selected_columns.values


    # 保存为新的 CSV 文件
    b_df.to_csv("integrated_data/"+point[i][:-1]+'.csv', index=False)
