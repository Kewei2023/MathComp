import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from util import *



for f in ["all_speed","all_count"]:
    df_j0 = pd.read_csv(path + point[0] + point[0][:-1] + "_row2_realtime_intersection.csv")
    df_j1 = pd.read_csv(path + point[1] + point[1][:-1] + "_row2_realtime_intersection.csv")
    df_j2 = pd.read_csv(path + point[2] + point[2][:-1] + "_row2_realtime_intersection.csv")
    df_j3 = pd.read_csv(path + point[3] + point[3][:-1] + "_row2_realtime_intersection.csv")
    data = pd.concat([
        df_j0[[f]].rename(columns={"32.31.250.103": f + '_from_' + point[0][-1] + "_row2"}),
        df_j1[[f]].rename(columns={"32.31.250.105": f + '_from_' + point[1][-1] + "_row2"}),
        df_j2[[f]].rename(columns={"32.31.250.107": f + '_from_' + point[2][-1] + "_row2"}),
        df_j3[[f]].rename(columns={"32.31.250.108": f + '_from_' + point[3][-1] + "_row2"})
    ], axis=1)
    # print(data.shape)

    correlation = data.corr()

    plt.figure(figsize=(6, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    plt.title(f'Correlation Heatmap: between point about {f} in row1')
    plt.savefig(f'Correlation_Heatmap_about_{f}_in_row1.png')

    plt.close()
