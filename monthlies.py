import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys, os
import glob

#These lines go into directory _Data_Files to read the .txt files
script_dir = sys.path[0]
data_directory = '_Data_Files'
list_of_files = glob.glob(os.path.join(data_directory, './*.dat'))

# initialize some dictionaries
archer_list = {}
archer_dat_dict = {}

# intialize a dictionary of archers to use as key names in dataframe dictionary
for k in range(1, 43):
    archer_list[k] = 'Archer_{:d}'.format(k + 108)
for k in range(108):
    archer_list[k + 43] = 'Archer_{:d}'.format(k + 1)

#create archer dictionary with keys Archer_1, Archer_2, etc
for index, file_ in enumerate(list_of_files):
    archer_dat_dict[archer_list[index + 1]] = pd.read_table(file_, sep = ',', \
                       names = ['Date','Score','Grade','Gender','School','Format'])

# concatenate all data so that it's pooled together in one data frame called full_df
full_df = pd.concat(archer_dat_dict.values(), ignore_index = False)


# create and/or print to new .txt file
file_out_name = 'Monthly Means and Std. Devs (all scores).txt'
fd = open(file_out_name, 'w')  # create and/or open file in write mode
old_stdout = sys.stdout  # store the default system handler so you can restore at end
sys.stdout = fd  # Now your file is used by print as destination

#convert to datetime format and use some built in pandas date sorters
#this is sorting entire dataframe by month and then taking mean and std dev.
full_df['Date'] = pd.to_datetime(full_df.Date)# convert to datetime format
full_df.index = full_df['Date']# have to make date the index since following functions operate on datetime indices
monthly_full_df_means = full_df.resample('M').mean() # this takes monthly means
monthly_full_df_std_dev = full_df.resample('M').std()# this takes monthly std devs
monthly_full_df_means = monthly_full_df_means.dropna()# drop NaN values
monthly_full_df_std_dev  = monthly_full_df_std_dev.dropna()# drop NaN values
print("\nMonthly means: \n", monthly_full_df_means)
print("____________________________")
print("\nMonthly Std. Devs: \n", monthly_full_df_std_dev)


# create and/or print to new .txt file
file_out_name = 'Monthly Means and Std. Devs (per archer).txt'
fd = open(file_out_name, 'w')  # create and/or open file in write mode
sys.stdout = fd  # Now your file is used by print as destination

#This block is doing the same thing except for each individual archer at a time
k = 0
for key, value in archer_dat_dict.items():
    k += 1
    value['Date'] = pd.to_datetime(value.Date)
    value.index = value['Date']# have to make date the index since following functions operate on datetime indices
    monthly_means = value.resample('M').mean()# this takes monthly means
    monthly_means = monthly_means.dropna()# this drops the NaN values from last step
    monthly_std_devs = value.resample('M').std()# monthly std devs
    monthly_std_devs = monthly_std_devs.dropna()# drop NaN values
    print("\n============================\n\n")
    print("\nThis Archer's Monthly Means: \n", monthly_means)
    print("\n____________________________\n\n")
    print("\nThis Archer's Monthly Std. Devs: \n", monthly_std_devs)
    print("\n============================\n\n")

sys.stdout = old_stdout