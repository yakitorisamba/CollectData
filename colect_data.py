#%%
import os
import re
import pandas as pd

def extract_data_from_param_dut(folder_path, target_strings):
    data = {}
    param_dut_path = os.path.join(folder_path, 'param_dut.scl')
    with open(param_dut_path, 'r') as file:
        for line in file:
            for target_string in target_strings:
                if target_string in line:
                    match = re.search(r'=(\d+)', line)
                    if match:
                        data[f'{target_string}'] = match.group(1)
    return data

def extract_data_from_user_extracted(folder_path):
    data = {}
    user_extracted_path = os.path.join(folder_path, 'user_extracted.txt')
    with open(user_extracted_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            data[key.strip()] = value.strip()
    return data

def aggregate_data(folder_path, specified_strings):
    result = {}
    for folder in os.listdir(folder_path):
        folder_full_path = os.path.join(folder_path, folder)
        if os.path.isdir(folder_full_path):
            condition_number, task_number = folder.split('_')[1:]
            if condition_number not in result:
                result[condition_number] = {'condition_number': condition_number}
            if task_number.endswith('1'):
                param_data = extract_data_from_param_dut(folder_full_path, specified_strings)
                result[condition_number].update(param_data)
            if task_number.endswith('3'):
                user_extracted_data = extract_data_from_user_extracted(folder_full_path)
                result[condition_number].update(user_extracted_data)
    return list(result.values())

# フォルダのパスと指定された文字列リストを指定してデータを集計
folder_path = './'
specified_strings = ["hoge","huga"]  # 指定された文字列リスト
aggregated_data = aggregate_data(folder_path, specified_strings)

# DataFrame に変換
df = pd.DataFrame(aggregated_data)
df.to_csv('./result.csv',index=False)
