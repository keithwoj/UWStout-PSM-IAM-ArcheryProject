import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys, os
import glob
import seaborn as sns

script_dir = sys.path[0]
data_directory = '_Data_Files'
score_output_path = 'Score_Sorts'
row_output_path = 'Row_Sorts'


# not used at the moment
# def remove_whitespace(x):
#     """
#     Helper function to remove ALL blank space from a string
#     x: a string
#     """
#     try:
#         # Remove spaces inside of the string
#         x = "".join(x.split())
#
#     except:
#         pass
#
#     return x


# list of all archer .dat files in data subdirectory
list_of_files = glob.glob(os.path.join(data_directory, './*.dat'))
full_data_frame = pd.DataFrame()

# initialize dictionaries
archer_list = {}
archer_dat_dict = {}
row_sort_by_date_dict = {}
score_sort_by_date_dict = {}
row_sort_by_score_dict = {}
row_sort_by_grade_dict = {}
score_sort_by_grade_dict = {}
row_sort_by_gender_dict = {}
score_sort_by_gender_dict = {}
row_sort_by_school_dict = {}
score_sort_by_school_dict = {}
row_sort_by_format_dict = {}
score_sort_by_format_dict = {}


# intialize a dictionary of archers to use as key names in dataframe dictionary
for k in range(1, 43):
    archer_list[k] = 'Archer_{:d}'.format(k + 108)
for k in range(108):
    archer_list[k + 43] = 'Archer_{:d}'.format(k + 1)

for index, file_ in enumerate(list_of_files):
    # # uncomment  these lines to check that archer numbers matches intended archer dat file
    # # Archer_1 should be 26589.dat
    # # Archer_2 should be 56257.dat ...
    # # ... Archer_150 should be 101306.dat
    # print(archer_list[index + 1])
    # print(file_)
    archer_dat_dict[archer_list[index + 1]] = pd.read_table(file_, sep = ',', \
                       names = ['Date','Score','Grade','Gender','School','Format'])

# print to 'Data_Overview.txt'
file_out_name = 'Data_Overview.txt'
fd = open(file_out_name, 'w')  # create and/or open file in write mode
old_stdout = sys.stdout  # store the default system handler so you can restore at end
sys.stdout = fd  # Now your file is used by print as destination

# concatenate all data so that it's pooled together
full_df = pd.concat(archer_dat_dict.values(), ignore_index = False)

# strip trailing and leading whitespace and capitalize only first letter of each word
# Also replace / with __ in strings because / can't be used in file names
full_df_strings = full_df.select_dtypes(['object'])
full_df[full_df_strings.columns] = \
    full_df_strings.apply(lambda x: x.str.strip().str.title().str.replace('/', '__'))

list_of_dates = pd.unique(full_df['Date'])
list_of_scores = pd.unique(full_df['Score'])
list_of_grades = pd.unique(full_df['Grade'])
list_of_genders = pd.unique(full_df['Gender'])
list_of_schools = pd.unique(full_df['School'])
list_of_formats = pd.unique(full_df['Format'])


print("\n__________________________________\n")
print("List_of_Dates: \n")
for index, date in enumerate(list_of_dates):
    print(date)
    score_sort_by_date_dict[date] = []
    row_sort_by_date_dict[date] = []

print("\n__________________________________\n")
print("List_of_Scores: \n")
for index, score in enumerate(list_of_scores):
    print(score)
    row_sort_by_score_dict[score] = []

print("\n__________________________________\n")
print("List_of_Grades: \n")
for index, grade in enumerate(list_of_grades):
    print(grade)
    score_sort_by_grade_dict["Grade_{}".format(grade)] = []
    row_sort_by_grade_dict["Grade_{}".format(grade)] = []

print("\n__________________________________\n")
print("List_of_Genders: \n")
for index, gender in enumerate(list_of_genders):
    print(gender)
    score_sort_by_gender_dict[gender] = []
    row_sort_by_gender_dict[gender] = []

print("\n__________________________________\n")
print("List_of_Schools: \n")
for index, school in enumerate(list_of_schools):
    print(school)
    score_sort_by_school_dict[school] = []
    row_sort_by_school_dict[school] = []

print("\n__________________________________\n")
print("List_of_Formats: \n")
for index, format in enumerate(list_of_formats):
    print(format)
    score_sort_by_format_dict[format] = []
    row_sort_by_format_dict[format] = []

print("\n__________________________________\n")
print("Total number of Archery scores (all): ", np.shape(full_df)[0])


# fill grouping dictionaries - each group will have one dictionary which is just the scores
# and the other will be the entire archer dataframe for each archer in that group
for index, date in enumerate(list_of_dates):
    date_scores = full_df.loc[full_df['Date'] == date]
    score_sort_by_date_dict[date].append(date_scores['Score'])
    row_sort_by_date_dict[date].append(date_scores)

for index, score in enumerate(list_of_scores):
    score_rows = full_df.loc[full_df['Score'] == score]
    row_sort_by_score_dict[score].append(score_rows)

for index, grade in enumerate(list_of_grades):
    grade_scores = full_df.loc[full_df['Grade'] == grade]
    score_sort_by_grade_dict["Grade_{}".format(grade)].append(grade_scores['Score'])
    row_sort_by_grade_dict["Grade_{}".format(grade)].append(grade_scores)

for index, gender in enumerate(list_of_genders):
    gender_scores = full_df.loc[full_df['Gender'] == gender]
    score_sort_by_gender_dict[gender].append(gender_scores['Score'])
    row_sort_by_gender_dict[gender].append(gender_scores)

for index, school in enumerate(list_of_schools):
    school_scores = full_df.loc[full_df['School'] == school]
    score_sort_by_school_dict[school].append(school_scores['Score'])
    row_sort_by_school_dict[school].append(school_scores)

for index, format in enumerate(list_of_formats):
    format_scores = full_df.loc[full_df['Format'] == format]
    score_sort_by_format_dict[format].append(format_scores['Score'])
    row_sort_by_format_dict[format].append(format_scores)

date_output_directory = '{}\Sort_By_Date_Scores'.format(score_output_path)
grade_output_directory = '{}\Sort_By_Grade_Scores'.format(score_output_path)
gender_output_directory = os.path.join(score_output_path, 'Sort_By_Gender_Scores')
school_output_directory = os.path.join(score_output_path, 'Sort_By_School_Scores')
format_output_directory = os.path.join(score_output_path, 'Sort_By_Format_Scores')


for key, value in score_sort_by_date_dict.items():
    file_out_name = '{}.txt'.format(key)
    if not os.path.exists(date_output_directory):
        os.makedirs(date_output_directory)
    fd = open(os.path.join(date_output_directory, file_out_name), 'w')
    sys.stdout = fd
    score_sort_by_date_dict[key] = np.concatenate(score_sort_by_date_dict[key])
    for index, entry in enumerate(score_sort_by_date_dict[key]):
        print(entry)

date_output_directory = '{}\Sort_By_Date_Rows'.format(row_output_path)
for key, value in row_sort_by_date_dict.items():
    file_out_name = '{}.txt'.format(key)
    if not os.path.exists(date_output_directory):
        os.makedirs(date_output_directory)
    fd = open(os.path.join(date_output_directory, file_out_name), 'w')
    sys.stdout = fd
    row_sort_by_date_dict[key] = pd.concat(row_sort_by_date_dict[key])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(row_sort_by_date_dict[key])

score_output_directory = '{}\Sort_By_Score_Rows'.format(row_output_path)
for key, value in row_sort_by_score_dict.items():
    file_out_name = '{}.txt'.format(key)
    if not os.path.exists(score_output_directory):
        os.makedirs(score_output_directory)
    fd = open(os.path.join(score_output_directory, file_out_name), 'w')
    sys.stdout = fd
    row_sort_by_score_dict[key] = pd.concat(row_sort_by_score_dict[key])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(row_sort_by_score_dict[key])

for key, value in score_sort_by_grade_dict.items():
    if not os.path.exists(grade_output_directory):
        os.makedirs(grade_output_directory)
    file_out_name = '{}.txt'.format(key)
    fd = open(os.path.join(grade_output_directory, file_out_name), 'w')
    sys.stdout = fd
    score_sort_by_grade_dict[key] = np.concatenate(score_sort_by_grade_dict[key])
    for index, entry in enumerate(score_sort_by_grade_dict[key]):
        print(entry)

grade_output_directory = '{}\Sort_By_Grade_Rows'.format(row_output_path)
for key, value in row_sort_by_grade_dict.items():
    file_out_name = '{}.txt'.format(key)
    if not os.path.exists(grade_output_directory):
        os.makedirs(grade_output_directory)
    fd = open(os.path.join(grade_output_directory, file_out_name), 'w')
    sys.stdout = fd
    row_sort_by_grade_dict[key] = pd.concat(row_sort_by_grade_dict[key])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(row_sort_by_grade_dict[key])

for key, value in score_sort_by_gender_dict.items():
    if not os.path.exists(gender_output_directory):
        os.makedirs(gender_output_directory)
    file_out_name = '{}.txt'.format(key)
    fd = open(os.path.join(gender_output_directory, file_out_name), 'w')
    sys.stdout = fd
    score_sort_by_gender_dict[key] = np.concatenate(score_sort_by_gender_dict[key])
    for index, entry in enumerate(score_sort_by_gender_dict[key]):
        print(entry)

gender_output_directory = '{}\Sort_By_Gender_Rows'.format(row_output_path)
for key, value in row_sort_by_gender_dict.items():
    file_out_name = '{}.txt'.format(key)
    if not os.path.exists(gender_output_directory):
        os.makedirs(gender_output_directory)
    fd = open(os.path.join(gender_output_directory, file_out_name), 'w')
    sys.stdout = fd
    row_sort_by_gender_dict[key] = pd.concat(row_sort_by_gender_dict[key])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(row_sort_by_gender_dict[key])

for key, value in score_sort_by_school_dict.items():
    if not os.path.exists(school_output_directory):
        os.makedirs(school_output_directory)
    file_out_name = '{}.txt'.format(key)
    fd = open(os.path.join(school_output_directory, file_out_name), 'w')
    sys.stdout = fd
    score_sort_by_school_dict[key] = np.concatenate(score_sort_by_school_dict[key])
    for index, entry in enumerate(score_sort_by_school_dict[key]):
        print(entry)

school_output_directory = '{}\Sort_By_School_Rows'.format(row_output_path)
for key, value in row_sort_by_school_dict.items():
    file_out_name = '{}.txt'.format(key)
    if not os.path.exists(school_output_directory):
        os.makedirs(school_output_directory)
    fd = open(os.path.join(school_output_directory, file_out_name), 'w')
    sys.stdout = fd
    row_sort_by_school_dict[key] = pd.concat(row_sort_by_school_dict[key])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(row_sort_by_school_dict[key])

for key, value in score_sort_by_format_dict.items():
    if not os.path.exists(format_output_directory):
        os.makedirs(format_output_directory)
    file_out_name = '{}.txt'.format(key)
    fd = open(os.path.join(format_output_directory, file_out_name), 'w')
    sys.stdout = fd
    score_sort_by_format_dict[key] = np.concatenate(score_sort_by_format_dict[key])
    for index, entry in enumerate(score_sort_by_format_dict[key]):
        print(entry)

format_output_directory = '{}\Sort_By_Format_Rows'.format(row_output_path)
for key, value in row_sort_by_format_dict.items():
    file_out_name = '{}.txt'.format(key)
    if not os.path.exists(format_output_directory):
        os.makedirs(format_output_directory)
    fd = open(os.path.join(format_output_directory, file_out_name), 'w')
    sys.stdout = fd
    row_sort_by_format_dict[key] = pd.concat(row_sort_by_format_dict[key])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(row_sort_by_format_dict[key])

# print to 'Data_Overview.txt'
file_out_name = 'Data_Overview.txt'
fd = open(file_out_name, 'a')  # create and/or open file in write mode
sys.stdout = fd  # Now your file is used by print as destination

print("____________________________________")
print("____________________________________")
print("____________________________________")
print("____________________________________")


print("\n======================================\n")
for key, value in score_sort_by_date_dict.items():
    print("\n------------------------------------\n")
    print("Number of archery scores from {}: ".format(key), len(score_sort_by_date_dict[key]))
    print("------------------------------------\n")
print("\n======================================\n")
for key, value in score_sort_by_grade_dict.items():
    print("\n------------------------------------\n")
    print("Number of archery scores from {}: ".format(key), len(score_sort_by_grade_dict[key]))
    print("{}_mean score: ".format(key), np.mean(score_sort_by_grade_dict[key]))
    print("{}_median score: ".format(key), np.median(score_sort_by_grade_dict[key]))
    print("------------------------------------")
print("\n======================================\n")
for key, value in score_sort_by_gender_dict.items():
    print("\n------------------------------------\n")
    print("Number of archery scores from {}: ".format(key), len(score_sort_by_gender_dict[key]))
    print("{}_mean score: ".format(key), np.mean(score_sort_by_gender_dict[key]))
    print("{}_median score: ".format(key), np.median(score_sort_by_gender_dict[key]))
    print("------------------------------------\n")
print("\n======================================\n")
for key, value in score_sort_by_school_dict.items():
    print("\n------------------------------------\n")
    print("Number of archery scores from {}: ".format(key), len(score_sort_by_school_dict[key]))
    print("{}_mean score: ".format(key), np.mean(score_sort_by_school_dict[key]))
    print("{}_median score: ".format(key), np.median(score_sort_by_school_dict[key]))
    print("\n------------------------------------\n")
print("\n======================================\n")
for key, value in score_sort_by_format_dict.items():
    print("\n------------------------------------\n")
    print("Number of archery scores from {}: ".format(key), len(score_sort_by_format_dict[key]))
    print("{}_mean score: ".format(key), np.mean(score_sort_by_format_dict[key]))
    print("{}_median score: ".format(key), np.median(score_sort_by_format_dict[key]))
    print("\n------------------------------------\n")

# print to 'Dictionary_Keys.txt'
file_out_name = 'Dictionary_Examples.txt'
fd = open(file_out_name, 'w')  # create and/or open file in write mode
sys.stdout = fd  # Now your file is used by print as destination

print("Example of dictionary use:\n")
print("\n\n---------------------------------------------")
print("Example 1 - score_sort_by_date_dict['3__3__2017']:")
print("---------------------------------------------")
print(" \n\n", score_sort_by_date_dict['3__3__2017'])
print("\n\n---------------------------------------------")
print("Example 2 - row_sort_by_date_dict['3__3__2017']:")
print("---------------------------------------------")
print("\n\n", row_sort_by_date_dict['3__3__2017'])
print("\n\n---------------------------------------------")
print("Example 3 - archer_dat_dict['Archer_1']:")
print("---------------------------------------------")
print("\n\n", archer_dat_dict['Archer_1'])
print("\n\n---------------------------------------------")
print("Example 4 - score_sort_by_gender_dict['Girls']:")
print("---------------------------------------------")
print("\n\n", score_sort_by_gender_dict['Girls'])
print("\nNotice the abridged list.  In order to access entire list of scores, load the score file, or enumerate:\n")
print("\nfor index, entry in enumerate(score_sort_by_gender_dict['Girls']):")
print("     (entry)\n")
for index, entry in enumerate(score_sort_by_gender_dict['Girls']):
        print(entry)


# print to 'Dictionary_Keys.txt'
file_out_name = 'Dictionary_Keys.txt'
fd = open(file_out_name, 'w')  # create and/or open file in write mode
sys.stdout = fd  # Now your file is used by print as destination

print("\n============================\n")
print("Dictionary keys:")
print("\n============================\n")

print("\n__________________________________\n")
print("\nSort By Date Dictionary Keys\n")
print("\n__________________________________\n")
print("\n\n---------------------------------------------------------------\n")
print("score_sort_by_date_dict (and row_sort_by_date_dict) Keys: \n")
print("---------------------------------------------------------------\n")
for key, value in score_sort_by_date_dict.items():
    print("KEY: \n", key)

print("\n__________________________________\n")
print("\nSort By Grade Dictionary Keys\n")
print("\n__________________________________\n")
print("\n\n--------------------------------------------------------------\n")
print("score_sort_by_grade_dict (and row_sort_by_grade_dict) Keys: \n")
print("\n--------------------------------------------------------------\n")
for key, value in score_sort_by_grade_dict.items():
    print("KEY: \n", key)

print("\n__________________________________\n")
print("\nSort By Gender Dictionary Keys\n")
print("\n__________________________________\n")
print("\n\n--------------------------------------------------------------\n")
print("score_sort_by_gender_dict (and row_sort_by_gender_dict) Keys: \n")
print("\n--------------------------------------------------------------\n")
for key, value in score_sort_by_gender_dict.items():
    print("KEY: \n", key)

print("\n__________________________________\n")
print("\nSort By School Dictionary Keys\n")
print("\n__________________________________\n")
print("\n--------------------------------------------------------------\n")
print("score_sort_by_school_dict (and row_sort_by_school_dict) Keys: \n")
print("\n\n--------------------------------------------------------------\n")
for key, value in score_sort_by_school_dict.items():
    print("KEY: \n", key)

print("\n__________________________________\n")
print("\nSort By Format Dictionary Keys\n")
print("\n__________________________________\n")
print("\n\n--------------------------------------------\n")
print("score_sort_by_format_dict (and row_sort_by_format_dict) Keys: \n")
print("\n--------------------------------------------\n")
for key, value in score_sort_by_format_dict.items():
    print("KEY: \n", key)


# print to 'Full_Archer_List.txt'
file_out_name = 'Full_Archer_List.txt'
fd = open(file_out_name, 'w')  # create and/or open file in write mode
sys.stdout = fd  # Now your file is used by print as destination

k = 0
for key, archer in archer_dat_dict.items():

    k += 1
    print("\n===========================Archer_{:d}===========================\n".format(k))
    # create index to filter out non-string columns so .str methods work
    archer_df_obj = archer.select_dtypes(['object'])
    #use filter in archer list to select correct string columns, then take out "/" character and proper case
    archer[archer_df_obj.columns] = \
        archer_df_obj.apply(lambda x: x.str.strip().str.title().str.replace('/', '__'))
    print("\n____________________\n")
    print("adjusted dictionary key: ", key)
    print("\n____________________\n")
    print("Archer data: \n", archer)
    print("\n____________________\n")
    print("This archer's mean score is: ", np.mean(archer['Score']))
    print("This archer's median score is: ", np.median(archer['Score']))
    print("\n____________________\n")
    print("\n=================================================================================\n")


# _____________________________________________________________________________________________________________________
# test some stuff here; print it out to see if it's what you want

# print to file 'testing.txt'
file_out_name = 'testing.txt'
fd = open(file_out_name, 'w')  # create and/or open file in write mode
sys.stdout = fd  # Now your file is used by print as destination

# example file:  Let's open file 1__1__2014.txt from Score_Sorts\Sort_By_Date_Scores directory
# it should contain only the scores as a numerical list, no tags or names
file_path = 'Score_Sorts\Sort_By_Date_Scores'
file_name = '1__1__2014.txt'
file_to_read = os.path.join(file_path, file_name)

# # Use this one to read in data from Row_Sorts directory
# df = pd.read_table(file_to_read, names = ['Date','Score','Grade','Gender','School','Format'])
# print(df)
# print("\n=================================================================================\n")
# print(type(df))
# print("\n=================================================================================\n")
# print(len(df))
# print("\n=================================================================================\n")
# print("mean of these scores: ", np.mean(df))
# print("\n=================================================================================\n")

# # OR

# # Use this one to read in data from Score_Sorts directory
score_file = pd.read_table(file_to_read)
print(score_file)
print("\n=================================================================================\n")
print(type(score_file))
print("\n=================================================================================\n")
print("Number of Scores: ", len(score_file))
print("\n=================================================================================\n")
print("Mean of these Scores: ", np.mean(score_file))
print("\n=================================================================================\n")
print("If you prefer to work with numpy arrays, load in a Score_Sorts file using the np.loadtxt() command:\n")
array_data = np.loadtxt(file_to_read)
print("data as numpy array: ", array_data)
print("\n=================================================================================\n")
print("You should also be able to load in the Score_Sorts files with R, if you want to, like we do in STAT 740")
#________________________________________

# # plotting
# sns.set(style = "ticks")
# # sort by date
# full_df['Date'] = pd.to_datetime(full_df.Date)
# full_df_by_date = full_df.sort_values('Date')
# full_df_by_grade = full_df.sort_values('Grade')
#
# full_df_by_date.plot(x = 'Date', y = 'Score', marker = 'o', linewidth = 0, title = "Full data")
# full_df_by_grade.plot(x = 'Grade', y = 'Score', marker = 'o', linewidth = 0, title = "Full data")
#
# fig, ax = plt.subplots()
#
# full_df.boxplot(column = "Score",        # Column to plot
#                  by = "Gender",         # Column to split upon
#                  fontsize = 10,
#                  rot = 0,
#                  figsize = (10,10))
# full_df.boxplot(column = "Score",        # Column to plot
#                  by = "Grade",         # Column to split upon
#                  fontsize = 10,
#                  figsize = (10, 10))
# full_df.boxplot(column = "Score",        # Column to plot
#                  by = "School",         # Column to split upon
#                  fontsize = 6,
#                  rot = 45,
#                  figsize = (10, 10),
#                  ax = ax)
#
# # # Set xticklabels to right alignment
# ax.set_xticklabels(ax.get_xticklabels(), ha = 'right')
#
#
# sns.pairplot(full_df, hue = "Gender")
# sns.factorplot(x = "Grade", y = "Score", hue = "Gender", data = full_df)
# sns.pairplot(full_df, hue = "Format")
# sns.factorplot(x = "Grade", y = "Score", hue = "Format", data = full_df)
# sns.pairplot(full_df, hue = "School")
# school_plot = sns.factorplot(x = "School", y = "Score", hue = "Grade", data = full_df)
# school_plot.set_xticklabels(fontsize = 6, rotation = 45, ha = 'right')
# plt.show()

sys.stdout = old_stdout # this line restores default behavior of printing (i.e: back to console)