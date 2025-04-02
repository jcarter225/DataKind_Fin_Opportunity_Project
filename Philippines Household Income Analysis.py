
"""
Analysis by Justin Carter
3/18/2025
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib import patches as mpatches

survey = pd.read_csv('FIES PUF 2023 Volume2 Household Summary.CSV')
meta = pd.read_excel('fies_2023_vol2_metadata(dictionary).xlsx')
province_names = pd.read_excel('Province Names.xlsx')

#replace ambiguated column names with proper names from metadata

replacement_dict = dict(zip(meta['Unnamed: 4'], meta['Unnamed: 5']))
province_dict = dict(zip(province_names['Province Code'], province_names['Province Name']))

survey.rename(columns=replacement_dict, inplace=True) #change names to recognizable descriptions
survey['Province'] = survey['Province'].replace(province_dict) #add province names

#check for missing values
print(survey.isna().sum().sum()) #zero missing values across the dataset

#get monthly incomes by province, including average across all provinces
country_avg_monthly_income = survey['Total Income'].mean()/12 #country
income_by_province =survey.groupby('Province')['Total Income'].mean()/12 #provinces
income_by_province_df = income_by_province.reset_index() #convert to df
income_by_province_df.loc[len(income_by_province_df)] = ['Entire Country Average', 
                                                     country_avg_monthly_income]


# ======================Create a horizontal bar plot===========================
#create heatmap for bar chart for easier viewing

#normalize data range for heatmap
normalize = plt.Normalize(income_by_province_df['Total Income'].min(),
                       income_by_province_df['Total Income'].max())

#create colormap to apply to bar charts
cmap = plt.cm.get_cmap('coolwarm')


#map income values to colors
income_by_province_df['Color'] = income_by_province_df['Total Income'].apply(lambda x: cmap(normalize(x)))


fig, ax = plt.subplots(figsize=(8.5,11), dpi = 300)
sns.barplot(x="Total Income", y="Province", data=income_by_province_df.iloc[:30],
            palette=income_by_province_df['Color'][:30].to_list())


#Add a vertical line for the "Entire Country Average"
plt.axvline(x=income_by_province_df[income_by_province_df["Province"] == "Entire Country Average"]["Total Income"].values[0], 
            color='red', linestyle='--', label="Country Average")

#create color legend
high_patch = mpatches.Patch(color=[0.705673158, 0.01555616, 0.150232812, 1.0], label='High Income')
low_patch = mpatches.Patch(color=[0.2298057, 0.298717966, 0.753683153, 1.0], label='Low Income')
legend_handles = [high_patch, low_patch, mpatches.Patch(color='red', label='Country Average')]
ax.legend(handles=legend_handles, loc='upper right', title='Legend')

#Titles and labels
ax.set_title('Monthly Income by Province (1/3)', fontsize=14)
ax.set_xlabel('Monthly Income', fontsize=12)
ax.set_ylabel('Province', fontsize=12)

#Show the plot
plt.xlim(right=50000) #keep x axis the same between charts
sns.despine(top=True)
plt.show()


# ======================Create a horizontal bar plot===========================
#create heatmap for bar chart for easier viewing

#normalize data range for heatmap
normalize = plt.Normalize(income_by_province_df['Total Income'].min(),
                       income_by_province_df['Total Income'].max())

#create colormap to apply to bar charts
cmap = plt.cm.get_cmap('coolwarm')


#map income values to colors
income_by_province_df['Color'] = income_by_province_df['Total Income'].apply(lambda x: cmap(normalize(x)))


fig, ax = plt.subplots(figsize=(8.5,11), dpi=300) #set plot dimensions and resolution
sns.barplot(x="Total Income", y="Province", data=income_by_province_df.iloc[30:61],
            palette=income_by_province_df['Color'][30:61].to_list())


# Add a vertical line for the "Entire Country Average"
plt.axvline(x=income_by_province_df[income_by_province_df["Province"] == "Entire Country Average"]["Total Income"].values[0], 
            color='red', linestyle='--', label="Country Average")

#create color gradient legend
high_patch = mpatches.Patch(color=[0.705673158, 0.01555616, 0.150232812, 1.0], label='High Income')
low_patch = mpatches.Patch(color=[0.2298057, 0.298717966, 0.753683153, 1.0], label='Low Income')
legend_handles = [high_patch, low_patch, mpatches.Patch(color='red', label='Country Average')]
ax.legend(handles=legend_handles, loc='upper right', title='Legend')

# Titles and labels
ax.set_title('Monthly Income by Province (2/3)', fontsize=14)
ax.set_xlabel('Monthly Income', fontsize=12)
ax.set_ylabel('Province', fontsize=12)

# Show the plot
plt.xlim(right=50000) #keep x axis the same between charts
sns.despine(top=True)
plt.show()

# ======================Create a horizontal bar plot===========================
#create heatmap for bar chart for easier viewing

#normalize data range for heatmap
normalize = plt.Normalize(income_by_province_df['Total Income'].min(),
                       income_by_province_df['Total Income'].max())

#create colormap to apply to bar charts
cmap = plt.cm.get_cmap('coolwarm')


#map income values to colors
income_by_province_df['Color'] = income_by_province_df['Total Income'].apply(lambda x: cmap(normalize(x)))


fig, ax = plt.subplots(figsize=(8.5,11), dpi = 300)
sns.barplot(x="Total Income", y="Province", data=income_by_province_df.iloc[61:-1],
            palette=income_by_province_df['Color'][61:-1].to_list())


#Add a vertical line for the "Entire Country Average"
plt.axvline(x=income_by_province_df[income_by_province_df["Province"] == "Entire Country Average"]["Total Income"].values[0], 
            color='red', linestyle='--', label="Country Average")

#create color gradient legend
high_patch = mpatches.Patch(color=[0.705673158, 0.01555616, 0.150232812, 1.0], label='High Income')
low_patch = mpatches.Patch(color=[0.2298057, 0.298717966, 0.753683153, 1.0], label='Low Income')
legend_handles = [high_patch, low_patch, mpatches.Patch(color='red', label='Country Average')]
ax.legend(handles=legend_handles, loc='upper right', title='Legend')

#Titles and labels
ax.set_title('Monthly Income by Province (3/3)', fontsize=14)
ax.set_xlabel('Monthly Income', fontsize=12)
ax.set_ylabel('Province', fontsize=12)

#Show the plot
plt.xlim(right=50000) #keep x axis the same between charts
sns.despine(top=True)
plt.show()



















































































