#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 09:50:22 2025

@author: justincarter
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib import patches as mpatches
import os
from rapidfuzz import process

# Set your desired path here
path = '/Users/justincarter/Documents/Post Graduation Materials/DataKind Projects/MarApr2025Financial/Finalized Datasets and Tableau Workbook'


# Change the working directory
os.chdir(path)

banks_pop = pd.read_csv('Banks Population Tableau.csv')
income_expenditure = pd.read_csv('income_and_expenditure_by_region.csv')
employment = pd.read_csv('Philippines Employment Status.csv')

#match region names:
    
employment_regions = employment['Region'].unique()


# Function to match regions
def match_region(value, choices):
    match, score, _ = process.extractOne(value, choices)  # Finds closest match
    return match if score > 80 else None  # Adjust similarity threshold if needed

# Apply matching
income_expenditure['matched_region'] = income_expenditure['Region'].apply(lambda x: match_region(x, employment_regions.tolist()))

#clean up unamatched names and drop country average
income_expenditure['matched_region'][9] = employment_regions[4]
income_expenditure['matched_region'][14] = employment_regions[8]
income_expenditure = income_expenditure.drop(17).reset_index(drop=True)

#make matched_region column the official region column
income_expenditure = income_expenditure.drop(columns=['Region'])
income_expenditure = income_expenditure.rename(columns={'matched_region':'Region'})

print(employment_regions)


#do the same for banks_pop dataframe
banks_pop['matched_region'] = banks_pop['Region'].apply(lambda x: match_region(x, employment_regions.tolist()))

#clean up mismatched names
banks_pop['matched_region'][2] = employment_regions[12]


#make matched_region column the official region column
banks_pop = banks_pop.drop(columns=['Region'])
banks_pop = banks_pop.rename(columns={'matched_region':'Region'})


banks_pop.to_csv('Banks and Population Final.csv', header=True, index=False)
income_expenditure.to_csv('Income and Expenditure Final.csv', header=True, index=False)






"""
make employment dataset structured like so: Region, Employment Category, Count
"""

# Group by Region and Employment Status, then count occurrences
employment = employment.groupby(['Region', 'Employment Status']).size().reset_index(name='Count')
employment['Total Count'] = employment.groupby('Region')['Count'].transform('sum')
employment['Percentage'] = (employment['Count']/employment['Total Count']*100)

employment.to_csv('Employment Final.csv', header=True, index=False)