import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
# import seaborn as sns
import os
import fnmatch


df = pd.DataFrame()
columns = ['Date', 'Score', 'Grade', 'Gender', 'School', 'Type']
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.dat'):
        file_new = pd.read_csv(file, header = 0, names = columns, parse_dates=['Date'], usecols=['Date', 'Score'], dayfirst='') #Also had this index_col='Date'
        df = df.append(file_new)

#Would like to sort data by month instead

#Sort data by year
df_bydate = df.sort_values(by = 'Date')
x = pd.Series(df_bydate['Date'])
y = pd.Series(df_bydate['Score'])


#Initial Full Time Series by year
plt.plot_date(x=x, y=y)
plt.title("Full Date-Score")
plt.ylabel("Score")
plt.grid(True)
plt.show()




