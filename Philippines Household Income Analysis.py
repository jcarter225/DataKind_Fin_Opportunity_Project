
"""
Analysis by Justin Carter
3/18/2025
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib import patches as mpatches
import os

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



#=============================================================================
#======Percentage of households receiving financial support from abroad=======
#=============================================================================
abroad_df = survey.copy()

abroad_df = abroad_df[['Household ID', 'Province', 'Cash Receipts, Support, etc. from Abroad',
                       ]]

#create binary variable to represent presence or lack of financial support from abroad
binary_lambda = lambda x: 1 if x > 0 else 0 

abroad_df['Abroad Support?'] = abroad_df['Cash Receipts, Support, etc. from Abroad']\
    .apply(binary_lambda)

#get counts of each province in dataset
province_counts = abroad_df['Province'].value_counts()
province_counts = province_counts.sort_index()

#group data by province and turn back into dataframe
abroad_province_df =abroad_df.groupby('Province')['Abroad Support?'].sum().reset_index()

#add province counts to abroad_province_df
abroad_province_df['Prov Count'] = abroad_province_df['Province'].map(province_counts)

abroad_province_df['Abroad Support %'] = round(abroad_province_df['Abroad Support?'] / abroad_province_df['Prov Count'] * 100, 2)

#get country average abroad support percentage
country_abroad_support = round(sum(abroad_province_df['Abroad Support?'] / abroad_province_df['Prov Count']), 2)

print(country_abroad_support) #average is 22.65%



def bp(df, r1, r2):
# ======================Create a horizontal bar plot===========================
    #df is data being used
    #r1 is the start of the range that I want to make the barplot for
    #r2 is the end value that I want to make the barplot for

    #create heatmap for bar chart for easier viewing
    
    #normalize data range for heatmap
    normalize = plt.Normalize(df['Abroad Support %'].min(),
                           df['Abroad Support %'].max())
    
    #create colormap to apply to bar charts
    cmap = plt.cm.get_cmap('coolwarm')
    
    
    #map income values to colors
    df['Color'] = df['Abroad Support %'].apply(lambda x: cmap(normalize(x)))
    
    
    fig, ax = plt.subplots(figsize=(8.5,11), dpi = 300)
    sns.barplot(x="Abroad Support %", y="Province", data=df.iloc[r1:r2],
                palette=df['Color'][r1:r2].to_list())
    
    
    #Add a vertical line for the "Entire Country Average"
    plt.axvline(x=country_abroad_support, 
                color='red', linestyle='--', label="Percentage of Country Obtaining Support")
    
    #create color gradient legend
    high_patch = mpatches.Patch(color=[0.705673158, 0.01555616, 0.150232812, 1.0], label='High Support %')
    low_patch = mpatches.Patch(color=[0.2298057, 0.298717966, 0.753683153, 1.0], label='Low Support %')
    legend_handles = [high_patch, low_patch, mpatches.Patch(color='red', label='Country Average')]
    ax.legend(handles=legend_handles, loc='upper right', title='Legend')
    
    #Titles and labels
    ax.set_title('Percentage of Filipino Households Receiving Remittances from Abroad By Province', fontsize=14)
    ax.set_xlabel('Percentage Receiving Remittances', fontsize=12)
    ax.set_ylabel('Province', fontsize=12)
    
    #Show the plot
    plt.xlim(right=100) #keep x axis the same between charts
    sns.despine(top=True)
    plt.show()



bp(abroad_province_df, 0, 30)

bp(abroad_province_df, 31, 61)

bp(abroad_province_df, 61, -1)


ordered_abroad_province_df = abroad_province_df.sort_values('Abroad Support %')

print('The provinces with the lowest percentage of households receiving remittances from abroad are:')
print(f'{ordered_abroad_province_df["Province"].values [0]} at {ordered_abroad_province_df["Abroad Support %"].values [0]}%')
print(f'{ordered_abroad_province_df["Province"].values [1]} at {ordered_abroad_province_df["Abroad Support %"].values [1]}%')
print(f'{ordered_abroad_province_df["Province"].values [2]} at {ordered_abroad_province_df["Abroad Support %"].values [2]}%')

print()
print('The provinces with the highest percentage of households receiving remittances from abroad are:')
print(f'{ordered_abroad_province_df["Province"].values [-1]} at {ordered_abroad_province_df["Abroad Support %"].values [-1]}%')
print(f'{ordered_abroad_province_df["Province"].values [-2]} at {ordered_abroad_province_df["Abroad Support %"].values [-2]}%')
print(f'{ordered_abroad_province_df["Province"].values [-3]} at {ordered_abroad_province_df["Abroad Support %"].values [-3]}%')



























