from util import *
import pandas as pd


def detect_changes(lst):
    changes = {
        'row1_to_row2': [],
        'row1_to_argent': [],
        'row2_to_row1': [],
        'row2_to_argent': [],
        'argent_to_row1': [],
        'argent_to_row2': [],
    }

    for i in range(len(lst) - 1):
        if lst[i] == 'row1' and lst[i + 1] == 'row2':
            changes['row1_to_row2'].append(i+1)
        elif lst[i] == 'row1' and lst[i + 1] == 'argent':
            changes['row1_to_argent'].append(i+1)
        elif lst[i] == 'row2' and lst[i + 1] == 'row1':
            changes['row2_to_row1'].append(i+1)
        elif lst[i] == 'row2' and lst[i + 1] == 'argent':
            changes['row2_to_argent'].append(i+1)
        elif lst[i] == 'argent' and lst[i + 1] == 'row1':
            changes['argent_to_row1'].append(i+1)
        elif lst[i] == 'argent' and lst[i + 1] == 'row2':
            changes['argent_to_row2'].append(i+1)

    return changes


for i in range(len(point)):
    for f in files_lane_change[i]:
        print(i)
        print(f)
        df = pd.read_csv(path_lane+point[i]+f+".csv", header=None)
        # 删除所有数据为“lose track”的
        df.replace('lose track', '', inplace=True)

        # 创建一个新的 DataFrame，用于存储结果
        result = pd.DataFrame()
        result[0] = df[0].iloc[1:]
        for col in ['row1_to_row2', 'row1_to_argent', 'row2_to_row1', 'row2_to_argent', 'argent_to_row1', 'argent_to_row2']:
            result[col] = 0  # 或者使用 None


        for column in df.columns[1:]:
            # 获取当前列的数据
            data_list = df[column].dropna().tolist()
            data_list = [item for item in data_list if item != ""]
            # print(data_list)
            changes=detect_changes(data_list)
            # print(changes)

            # 创建一个字典来存储映射
            index_mapping_dict = {}
            # 生成下标映射
            for idx, item in enumerate(data_list):
                original_index = df[column].dropna().index[idx]
                index_mapping_dict[idx] = original_index
            # print(index_mapping_dict)

            for key, value in changes.items():
                if len(value)==0:continue
                for v in value:
                    result.at[index_mapping_dict[v]-1, key] += 1
            # break

        result.to_csv(path_lane + point[i] + f + "_deal.csv", index=False)
        # break
    # break

