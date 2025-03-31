import pandas as pd
import numpy as np
import openpyxl
import matplotlib
import matplotlib.pyplot as plt

import os
from os import listdir
import pathlib


GDP_df = pd.read_csv('Economic Indicators/GDP Per Capita/GDP_PC.csv', index_col=1, skiprows=4)
print(GDP_df.shape)
print(GDP_df.iloc[:,0:3])

years_list = ['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
GDP_df = GDP_df.loc[:, years_list]
nations_list = GDP_df.index.to_list()
print(GDP_df.iloc[:,0:3])

GDP_dict = pd.Series(GDP_df.to_dict(orient='records'))
GDP_dict = GDP_dict.set_axis(nations_list)
print(GDP_dict)

data_nations = ['BOL','COL','ECU','GHA','GTM','HND','HTI','KHM','KIR','LBR','MDG','MNG',
                'NGA','NIC','PER','PHL','PRY','SLV','VEN','SLE','ZWE']

GDP_subset = GDP_dict.loc[data_nations]
print(GDP_subset)
GDP_subset_2 = GDP_subset.copy()
print(GDP_subset_2)

test_df1 = pd.DataFrame(index=data_nations)
print(test_df1)
test_df1['A'] = GDP_subset
test_df1['B'] = GDP_subset_2
print(test_df1)

file_path_1 = 'Economic Indicators/All_Indicators'

files = [f for f in pathlib.Path(file_path_1).iterdir() if f.is_file()]
print(files)



def process_edata(input_df):
    input_df = input_df.loc[:, years_list]
    df_dict = pd.Series(input_df.to_dict(orient='records'))
    df_series = df_dict.set_axis(nations_list)
    df_series = df_series.loc[data_nations]
    return df_series

def process_files(file_path):
    all_data = []
    add_df = pd.DataFrame(index=data_nations)
    files_lst = [f for f in pathlib.Path(file_path).iterdir() if f.is_file()]
    for f in files_lst:
        file_data = pd.read_csv(f, index_col=1, skiprows=4)
        file_name = os.path.basename(f)
        file_name = file_name[:-4]
        print(file_name)
        indicator_col = process_edata(file_data)
        add_df[file_name] = indicator_col
    return add_df


combined_df = process_files(file_path_1)
combined_df.rename(index={'SLE':'WAL','LBR':'LIB'}, inplace=True)

print(combined_df)

combined_df.to_csv('all_econ_data.csv')
