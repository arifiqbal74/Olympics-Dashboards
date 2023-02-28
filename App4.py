# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 21:58:55 2023

@author: Asif Iqbal
"""

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

#load data sets
athletes = pd.read_csv('https://raw.githubusercontent.com/arifiqbal74/Olympics-Dashboards/main/athlete_events_till_150K.csv') 
athletes2 = pd.read_csv('https://raw.githubusercontent.com/arifiqbal74/Olympics-Dashboards/main/athlete_events_from_150K.csv')
regions = pd.read_csv('https://raw.githubusercontent.com/arifiqbal74/Olympics-Dashboards/main/noc_regions.csv')

print(athletes.head())

print(regions.head())

append = athletes.append(athletes2)

# Join the Dataframes on base of NOC Column
athletes_df = athletes.merge(regions, how='left', on = 'NOC')
print(athletes_df.head())

# how many rows and columns
athletes_df.shape

# rename last two columns with upper case(first letter)
athletes_df.rename(columns={'region':'Region', 'notes':'Notes'},inplace=True)
print(athletes_df.head())

# data type
athletes_df.info()

# numerical values of the dataframes
athletes_df.describe()

# null values count
athletes_df.isna().sum()

#Replace the null values of “Age” column by 0.
athletes_df["Age"].replace(np.nan, 0, inplace=True)
athletes_df['Age'].unique()

#Replace the null value of “Height” column by the last value.
athletes_df['Height'].fillna(method='ffill',inplace=True)
athletes_df['Height'].unique()

## for missing "Weight" value, replace it with rounded mean value.
athletes_df['Weight'].fillna(round(athletes_df.Weight.mean()), inplace=True)

athletes_df.info()

#Replace the null values of Medal column by 0.
athletes_df["Medal"].replace(np.nan, 0, inplace=True)
athletes_df['Medal'].unique()

athletes_df.info()

import streamlit as st

#st.set_page_config(layout="wide")

# Title
st.title('Olympics Dashboard')

# use Country to filter data
countries = athletes_df['Team'].unique()
selection = st.selectbox('Select Country', countries)
subset = athletes_df[athletes_df['Team'] == selection]
st.dataframe(subset)
                        

# the metric component takes the value you want to show and the change from a prev. value (it shows it as up/down arrow based on the change value)
curr_count = 100
inc_count = 10

curr_medals = 50
inc_medals = -4

country_count = 14
inc_count = 5
countries = athletes_df['Region'].nunique()
gold_medals = 13732
Silver_medal = 13116
bronze_medal = 13295 

# combining metrics and columns to create 
#st.header('Olympics - {}'.format(Country))
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Number of Olympians', athletes_df['ID'].nunique())
col2.metric('Participating Countries', countries)
col3.metric('Gold Medals', gold_medals)
col4.metric('Silver Medals', Silver_medal)
col5.metric('Bronze Medals', bronze_medal)

# Creating Visuals
st.header('Number of Medals Over Years')
chart_data = pd.DataFrame(
  np.random.rand(20,3),
  columns=['GOLD', 'SILVER', 'BRONZE'])
st.line_chart(chart_data)

#medal_count = athletes_df['Medal'].value_counts()
#st.header('Numbers of Medals Recieved by Each Athletes')
#plt.rcParams['figure.figsize']=[14,8]
#colors = ['green','yellow','blue']
#fig = plt.bar(x = medal_count.index, height = medal_count.values, color = colors)

#plt.title('medal_count')
#plt.xlabel('Medals')
#plt.ylabel('Athletes')
#st.pyplot()

top_5_sports = athletes_df.groupby('Sport')['Medal'].value_counts().sort_values(ascending=False)
st.header('Top 5 Medals Recieved in Each Sports')
Table = pd.DataFrame(top_5_sports)
Table.head(5)
st.table(Table.head(5))


st.header('Number of Medals Over Age')
top_10_countries = athletes_df.Team.value_counts().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,12))
plt.xlabel('Age')
plt.ylabel('Medals')
plt.hist(athletes_df.Age, bins=10, edgecolor='black', width=10);
st.pyplot()

st.header('Number of Medals Bifurcated by Gender')
plt.figure(figsize=(12,2.5))
athletes_df.groupby('Sex')['Medal'].count().sort_values(ascending=False).plot(kind='pie',autopct='%0.05f%%')
st.pyplot()

medal_count = athletes_df['Medal'].value_counts()
st.header('Numbers of Medals Recieved in Each Season')
plt.rcParams['figure.figsize']=[14,8]
colors = ['green','yellow','blue']
plt.bar(x = medal_count.index, height = medal_count.values, color = colors)

#plt.title('medal_count')
plt.xlabel('Seasons')
plt.ylabel('Medals')
st.pyplot()
