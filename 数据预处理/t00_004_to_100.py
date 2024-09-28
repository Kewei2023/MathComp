import pandas as pd
import numpy as np
import os
import ipdb

root = './processed-lane'

for ip_dir in os.listdir(root):

    if not os.path.isdir(os.path.join(root, ip_dir)): continue
    print("?")
    for csv_file in os.listdir(os.path.join(root, ip_dir)):
        if 'csv' in csv_file:
            df = pd.read_csv(os.path.join(root, ip_dir, csv_file))
            # ipdb.set_trace()
            df['time_ceil'] = np.ceil(df.iloc[:, 0]/10).astype(int)
            # df['time(s)'] = df['time(s)'].round().astype(int)
            result = df.groupby('time_ceil').sum().reset_index()

            result.to_csv(os.path.join(root, ip_dir, csv_file.replace(".csv", "_flow.csv")))
        # break
    # break
