import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys, os
import glob
import seaborn as sns
import random
from statsmodels.nonparametric.smoothers_lowess import lowess

script_dir = sys.path[0]
data_directory = '_Data_Files'

# read and create a list of all .dat files in data_directory
list_of_files = glob.glob(os.path.join(data_directory, './*.dat'))

# initialize dictionaries
archer_list = {}# This is just to help in creating the next dictionary and its keys
archer_dat_dict = {}# This dictionary will store each archer's full dataframe

archer_means_full_dict = {}# This dictionary will store each archer's total mean score
archer_stds_dict = {}# This dictionary will store each archer's score's std.deviation
archer_exp_full_dict = {}# This dictionary will store each archer's total number of scores recorded
archer_exp_pre_dict = {}# This one will store each archer's total number of scores recorded prior to last grade participated
monthly_means_full_dict = {}# This dictionary will store each archer's monthly mean scores
monthly_means_pre_dict = {}# This dictionary will store each archer's monthly mean scores prior to last grade participated
archer_means_post_dict = {}# This dictionary will store each archer's mean score for only the last grade they participated

# set up print to .txt file for easier reading
file_out_name = 'output_file.txt' # choose a name
fd = open(file_out_name, 'w')  # create and/or open your new file in write mode
old_stdout = sys.stdout  # store the default system handler so you can restore it at end of code
sys.stdout = fd  # Now your new file is used by print as destination

# intialize a dictionary of archer names to use as key names in main archer dataframe dictionary
for k in range(1, 43):
    archer_list[k] = 'Archer_{:d}'.format(k + 108)
for k in range(108):
    archer_list[k + 43] = 'Archer_{:d}'.format(k + 1)

for index, file_ in enumerate(list_of_files):
    # # uncomment  these lines to check that archer numbers matches intended archer dat file
    # # Archer_1 should be 26589.dat
    # # Archer_2 should be 56257.dat ...
    # # ... Archer_150 should be 101306.dat
    # print("________________________________________")
    # print(archer_list[index + 1], " coresponds to ", file_)
    # print("________________________________________")
    #Here we read in each .dat file and store contents as dataframe, one dataframe per key
    archer_dat_dict[archer_list[index + 1]] = pd.read_table(file_, sep = ',', \
                       names = ['Date','Score','Grade','Gender','School','Format'])
    # Also intitalize all dictionaries which will use Archer_1, Archer_2, etc, for keys, with those keys
    archer_means_full_dict[archer_list[index + 1]] = [] # value for corresponding keys are empty lists for now
    archer_stds_dict[archer_list[index + 1]] = []
    archer_exp_full_dict[archer_list[index + 1]] = []
    monthly_means_full_dict[archer_list[index + 1]] = []
    archer_exp_pre_dict[archer_list[index + 1]] = []
    monthly_means_pre_dict[archer_list[index + 1]] = []
    archer_means_post_dict[archer_list[index + 1]] = []

#iterate through each value (each separate archer's dataframe) in archer_dat_dictionary
for key, archer in archer_dat_dict.items():
    archer['Date'] = pd.to_datetime(archer.Date)# convert date columns to datetime format
    archer.index = archer['Date']# make date the 'index' of each dataframe since next methods need "datetime indices"
    monthly_means_full = archer.resample('M').mean()# this takes monthly means using datetime indices
    monthly_std_devs = archer.resample('M').std()# monthly std devs using datetime indices
    monthly_means_full = monthly_means_full.dropna()# this drops the NaN values from last step
    monthly_std_devs = monthly_std_devs.dropna()# drop NaN values

    # here we select only rows which do not correspond to the archer's final grade, and repeat above
    monthly_means_pre = (archer.loc[archer['Grade'] != np.max(archer['Grade'])]).resample('M').mean()
    monthly_means_pre = monthly_means_pre.dropna()  # this drops the NaN values from last step

    #convert datetimes to "days passed since first day of participation" for easier plotting (and such)
    monthly_means_full = pd.DataFrame(monthly_means_full)
    monthly_means_full.index = (monthly_means_full.index - monthly_means_full.index[0]).days
    monthly_means_pre = pd.DataFrame(monthly_means_pre)
    monthly_means_pre.index = (monthly_means_pre.index - monthly_means_pre.index[0]).days
    monthly_std_devs = pd.DataFrame(monthly_std_devs)
    monthly_std_devs.index = (monthly_std_devs.index - monthly_std_devs.index[0]).days

    # create index to filter out non-string (object) columns so .str methods work
    archer_df_obj = archer.select_dtypes(['object'])
    #next is a .str method:  use above filter to select only string columns, then take out "/" character and proper
    # uppercase;  without the filter it encounters datetime and int columns and you get error
    archer[archer_df_obj.columns] = \
        archer_df_obj.apply(lambda x: x.str.strip().str.title().str.replace('/', '__'))

    archer_exp_full_dict[key] = len(archer['Score'])# store total number of ALL scores for that archer in proper dict
    # store only number of scores from before the last grade of participation in proper dict
    archer_exp_pre_dict[key] = len(archer.loc[archer['Grade'] != np.max(archer['Grade'])])

    # store this archer's mean of ALL scores in proper dict
    archer_means_full_dict[key] = np.mean(archer['Score'])
    # store this archer's mean of only those scores from final grade of participation in proper dict
    archer_means_post_dict[key] = np.mean(archer.loc[archer['Grade'] == np.max(archer['Grade'])]['Score'])
    #store this archer's means for each month, ALL months, in proper dict
    monthly_means_full_dict[key] = monthly_means_full
    #store this archer's means for each month, excluding final grade of particpation, in proper dict
    monthly_means_pre_dict[key] = monthly_means_pre
    # store this archer's std. deviations for each month, ALL months (with more thanone score)
    archer_stds_dict[key] = np.std(archer['Score'])

# it's easiesst to use dictionaries to create new dataframes
# Note that these next two things are... wait for it... dictionaries.... OF DICTIONARIES!  < mind assplode >
# first dictionary setup to create dataframe with columns "Nmbr_Scores" and "Means" and "Stds" (deviations)
new_dict = {'Nmbr_Scores':archer_exp_full_dict, 'Means':archer_means_full_dict, 'Stds':archer_stds_dict}
# second dictionary for same thing except to compare only scores prior to last grade with means from last grade
# also ignoring std. deviations on this one since I didn't make the dictionary and seems unimportant
new_dict_pre = {'Nmbr_Scores_pre':archer_exp_pre_dict, 'Means_post':archer_means_post_dict}

#use the dictionaries to create quick new custom dataframes
new_df = pd.DataFrame(new_dict)
new_df_pre = pd.DataFrame(new_dict_pre)

#copies are always good for safety so as not to change original
X = new_df.copy()
X_pre = new_df_pre.copy()

print("X :\n", X)
print("X_Pre :\n", X_pre)

# pop out columns into separate numerical lists (still have archer indices)
y_means = X.pop('Means')
y_stds = X.pop('Stds')
y_means_post = X_pre.pop('Means_post')

#These are similar to monthly means but grouping by number of scores now instead of months/days passed
means_predict = y_means.groupby(X.Nmbr_Scores).mean()
stds_predict = y_stds.groupby(X.Nmbr_Scores).mean()
means_post_predict = y_means_post.groupby(X_pre.Nmbr_Scores_pre).mean()

print("================================")
print("MEANS PREDICT: ", means_predict)
print("STDS PREDICT: ", stds_predict)
print("means_post PREDICT: ", means_post_predict)
print("================================")

new_df_pre.boxplot(column = "Means_post",        # Column to plot
                 by = "Nmbr_Scores_pre",         # Column to split upon
                  fontsize = 10,
                 rot = 0,
                 figsize = (10,10))

new_df.boxplot(column = "Means",        # Column to plot
                 by = "Nmbr_Scores",         # Column to split upon
                  fontsize = 10,
                 rot = 0,
                 figsize = (10,10))

new_df.boxplot(column = "Stds",        # Column to plot
                 by = "Nmbr_Scores",         # Column to split upon
                 fontsize = 10,
                 rot = 0,
                 figsize = (10,10))

#concatenate each archer's data into one big dataframe called full_df
full_df = pd.concat(archer_dat_dict.values(), ignore_index = False)
full_df.hist()# check hists/normality
plt.suptitle("Full Data")

means_post_predict = pd.DataFrame(means_post_predict).reset_index()

# plot "last grade means" vs "number of recorded scores prior to last grade"
fig, ax = plt.subplots()
means_post_predict.plot(x = 'Nmbr_Scores_pre', y = 'Means_post', ax = ax, marker = 'o', linewidth = 0, \
            title = "Archer Means_post vs Number of Scores_pre")
ys = lowess(means_post_predict['Means_post'], means_post_predict['Nmbr_Scores_pre'])[:, 1]
plt.plot(means_post_predict['Nmbr_Scores_pre'], ys, 'green', linewidth = 1)
plt.show()

#not sure why this one isn't working, it says Nmbr_Scores_pre isn't there, but it is there
# print("means_post_predict", means_post_predict.reset_index())
# sns.regplot(means_post_predict['Nmbr_Scores_pre'], means_post_predict['Means_post'], lowess = True)
# plt.show()


#Let's random sample 10 random archers
#look at some plots, for instance their number of scores prior to their last grade compared to their means in last grade
ten_rand_archers = list(random.sample(archer_dat_dict.keys(), 10))#put 'Archer_x' keys in list to iterate through

for index, entry in enumerate(ten_rand_archers):
    #Print out this archer's monthly means, and pre-last-grade monthly means
    print("Monthly Means for {}: \n".format(entry), monthly_means_full_dict[entry])
    print("Pre-Max_Grade Monthly Means for {} :\n".format(entry), monthly_means_pre_dict[entry])

    #the .reset_index() method explicitly makes the "index" of frame a normal column so you can access it more easily
    df = monthly_means_full_dict[entry].reset_index()

    #setup the proper plots and axes for overlaying trendlines and such
    fig, ax2 = plt.subplots()

    # regression line with polyfit, these are just with Dates
    poly_2 = np.poly1d(np.polyfit(df['Date'], df['Score'], 2))
    m_1, m_2, b = np.polyfit(df['Date'], df['Score'], 2)
    trendline = m_1*(df['Date']**2) + m_2*df['Date'] + b
    plt.plot(df['Date'], df['Score'], '.')
    plt.title("{}".format(entry))
    plt.plot(df['Date'], trendline, '-')
    plt.title("{}".format(entry))
    plt.show()

    # or with "lowess" (?)
    plt.plot(df['Date'], df['Score'], '.')
    plt.title("{}".format(entry))
    ys = lowess(df['Score'], df['Date'])[:, 1]
    plt.plot(df['Date'], ys, 'red', linewidth = 1)
    plt.show()

    # or with seaborn
    reg_plot = sns.regplot(df['Date'], df['Score'], lowess = True)
    reg_plot.axes.set_title("{}".format(entry))
    plt.show()

    #check histograms
    df.hist()
    plt.suptitle("{}".format(entry))
    plt.show()

# #Here is where I tried some PCA/MCA Stuff but I don't think it's appropriate here
# XX = full_df.copy()
#
# # make categorical variables into dummy numerical variables
# XX["School"] = XX["School"].astype('category')
# # XX["School"] = XX["School"].cat.codes
# XX["Gender"] = XX["Gender"].astype('category')
# # XX["Gender"] = XX["Gender"].cat.codes
# XX["Format"] = XX["Format"].astype('category')
# # XX["Format"] = XX["Format"].cat.codes
# XX["Date"] = XX["Date"].astype('category')
# # XX["Date"] = XX["Date"].cat.codes
# # print(XX.head())
#
# df = XX.copy()
# df = XX.drop('Score', 1)
# # df = XX.drop('Date', 1)
#
# print("df.dtypes: \n", df.dtypes)
# print("_________________")
# print(df)
#
# # mca_df = prince.MCA(df, n_components = -1)
# # fig1, ax1 = mca_df.plot_cumulative_inertia()
# # fig2, ax2 = mca.plot_rows(show_points = True, show_labels = False, color_by = 'School', ellipse_fill = True)
#
# mca_df = prince.MCA(df, n_components = 5)
# fig1, ax1 = mca_df.plot_cumulative_inertia()
# fig2, ax2 = mca_df.plot_rows(show_points = True, show_labels = False, color_by = 'School', ellipse_fill = True)
# fig3, ax3 = mca_df.plot_rows_columns()
# fig4, ax4 = mca_df.plot_relationship_square()
# print("_________________")
# print("_________________")
# print(mca_df)
# # print(mca_df.inertia, mca_df.L.sum())
# # mca_df.plot_rows(show_points = True, show_labels = False, color_by = 'School', ellipse_fill = True)
# plt.show()

 # this line restores default behavior of printing (i.e: back to console)
sys.stdout = old_stdout
