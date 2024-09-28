import pandas as pd
import numpy as np
import os
import ipdb

root = './004to100（第一版数据，原版）'
save_dir = './004to100'

os.makedirs(save_dir, exist_ok=True)
for ip_dir in os.listdir(root):

    if not os.path.isdir(os.path.join(root, ip_dir)): continue

    os.makedirs(os.path.join(save_dir, ip_dir), exist_ok=True)
    for csv_file in os.listdir(os.path.join(root, ip_dir)):
        if 'csv' in csv_file:
            df = pd.read_csv(os.path.join(root, ip_dir, csv_file))
            # ipdb.set_trace()
            df['time_ceil'] = np.ceil(df['time(s)']).astype(int)
            # df['time(s)'] = df['time(s)'].round().astype(int)
            result_1 = df.groupby('time_ceil')[
                ['all_speed', 'all_box_width', 'big_car_speed', 'big_car_box_width']].mean().reset_index()
            result_2 = df.groupby('time_ceil')[['all_count', 'big_car_count']].sum().reset_index()

            result = pd.merge(result_1, result_2, on='time_ceil')
            result.to_csv(os.path.join(save_dir, ip_dir, csv_file.replace(".csv", "traffic_flow.csv")))