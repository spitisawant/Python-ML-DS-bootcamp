# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:45:11 2020

@author: spiti
"""
import numpy as np
import pandas as pd

df = pd.read_csv("C:/Users/spiti/Documents/IM/Udemy/911.csv")

df.info()
# RangeIndex: 99492 entries, 0 to 99491
# =============================================================================
# Data columns (total 9 columns):
# lat          99492 non-null float64
# lng          99492 non-null float64
# desc         99492 non-null object
# zip          86637 non-null float64
# title        99492 non-null object
# timeStamp    99492 non-null object
# twp          99449 non-null object
# addr         98973 non-null object
# e            99492 non-null int64
# dtypes: float64(3), int64(1), object(5)
# =============================================================================
df['title'].head(5)

############################### BASIC QUESTIONS ###############################
# ** What are the top 5 zipcodes for 911 calls? **
df['zip'].nunique() #104 unique zip codes
df['zip'].value_counts().head(5)
# =============================================================================
# 19401.0    6979
# 19464.0    6643
# 19403.0    4854
# 19446.0    4748
# 19406.0    3174
# =============================================================================

# How many unique titles are there?
df['title'].nunique() #110

# What are the top 5 reasons of calling 911?
df['title'].value_counts().head(5)
# =============================================================================
# Traffic: VEHICLE ACCIDENT -    23066
# Traffic: DISABLED VEHICLE -     7702
# Fire: FIRE ALARM                5496
# EMS: RESPIRATORY EMERGENCY      5112
# EMS: CARDIAC EMERGENCY          5012
# =============================================================================

# What are the top 5 townships for 911 calls?
df['twp'].value_counts().head(5)
# =============================================================================
# LOWER MERION    8443
# ABINGTON        5977
# NORRISTOWN      5890
# UPPER MERION    5227
# CHELTENHAM      4575
# =============================================================================

###########################NEW FEATURES########################################
# Split the title column into a new column: "Reason"
df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
df['Reason'].head(5)
# =============================================================================
# 0     EMS
# 1     EMS
# 2    Fire
# 3     EMS
# 4     EMS
# =============================================================================

#** What is the most common Reason for a 911 call based off of this new column? **
df['Reason'].value_counts().head()
# =============================================================================
# EMS        48877
# Traffic    35695
# Fire       14920
# =============================================================================

import matplotlib.pyplot as plt
import seaborn as sns

#** Now use seaborn to create a countplot of 911 calls by Reason. **
sns.countplot(x='Reason',data = df)

# Converting datatype of time from object to datetime.
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
type(df['timeStamp'].iloc[0])
# pandas._libs.tslibs.timestamps.Timestamp
df['Date'].head()

#Splitting date and time into new columns
df['Date'], df['Time'] = df['timeStamp'].dt.normalize(), df['timeStamp'].dt.time

# Creating Day of the week column
df['Day of Week'] = df['timeStamp'].apply(lambda time : time.dayofweek)
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)

df['Month'] = df['timeStamp'].apply(lambda time : time.month)

df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
#** Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column. **
sns.countplot(x='Day of Week', data=df, hue='Reason')
# =============================================================================
# Conclusion:
# 1. Traffic is the least on Sundays. So no traffic problem.
# 2.Fire calls on any day of the week has same frquency.
# =============================================================================
# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# Doing the same based off of Month 
sns.countplot(x='Month',data=df, hue = 'Reason')
# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

#** Did you notice something strange about the Plot? **
# It is missing some months! 9,10, and 11 are not there.

# Creating a groupby object called byMonth, where you group the DataFrame by the month column and use the count() method for aggregation.
byMonth = df.groupby('Month').count()
byMonth.head()

# Creating a simple plot off of the dataframe indicating the count of calls per month. 
byMonth['twp'].plot()

# use reset index to set a list of integers from 0 to length of it  as index.
sns.lmplot(x='Month', y='twp', data = byMonth.reset_index())

df['Date'] = df['timeStamp'].apply(lambda t:t.date())

# ** Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.**
df.groupby('Date').count()['twp'].plot()
plt.tight_layout()

# Reason : EMS
df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()

# Reason : Traffic
df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()

# Reason : Fire
df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()

# CREATING HEATMAPS WITH SEABORN 

dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
dayHour.head()

# creating heatmap using new dataframe
plt.figure(figsize=(12,6))
sns.heatmap(dayHour, cmap = 'coolwarm')

#** Now create a clustermap using this DataFrame. *
sns.clustermap(dayHour, cmap = 'coolwarm')

# Now repeat these same plots and operations, for a DataFrame that shows the Month as the column.
dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
dayMonth.head()

plt.figure(figsize=(12,6))
sns.heatmap(dayMonth, cmap = 'coolwarm')

sns.clustermap(dayMonth, cmap = 'coolwarm')
#comments
