# Import libraries
import pandas as pd
import numpy as np
import os
from os import listdir
import pathlib

## This file processes world bank data from a directory and outputs a .csv file containing
## only data for countries and years of interest. Output is a dataframe where each entry is
## a dictionary with years as keys and economic data as values.

# Create list of years containing the full date range for clinical data (may need to be adjusted)
years_list = ['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']

# Create list of country codes for each nation in the clinical study
data_nations = ['BOL','COL','ECU','GHA','GTM','HND','HTI','KHM','KIR','LBR','MDG','MNG',
                'NGA','NIC','PER','PHL','PRY','SLV','VEN','SLE','ZWE']

# Specify directory
file_path_1 = 'Economic Indicators/All_Indicators'

# Check files in directory
files = [f for f in pathlib.Path(file_path_1).iterdir() if f.is_file()]
print(files)

# Function to process data from dataframe and return dictionary of key:value pairs for each year
def process_edata(input_df):
    input_df = input_df.loc[:, years_list]
    df_dict = pd.Series(input_df.to_dict(orient='records'))
    nations_list = input_df.index.to_list()
    df_series = df_dict.set_axis(nations_list)
    df_series = df_series.loc[data_nations]
    return df_series

# Function to process data from all files in directory and combine in single dataframe
def process_files(file_path):
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

# Process combined dataframe
combined_df = process_files(file_path_1)

# Rename country indices to match clinical data
combined_df.rename(index={'SLE':'WAL','LBR':'LIB'}, inplace=True)

# Write to .csv file
combined_df.to_csv('all_econ_data.csv')
