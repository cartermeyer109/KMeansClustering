#Uses the same features used to determine HDI to cluster into 7 clusters ->
# the same number of tiers in the map displayed at https://ourworldindata.org/grapher/human-development-index?time=2017

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import geopandas as gpd #Requires pip install geopandas matplotlib
import os
import plotly.express as px #Requires pip install plotly
import json

#States HDI Tiers
#https://hdr.undp.org/data-center/human-development-index#/indicies/HDI

#Actual Map of HDI in 2017
#https://ourworldindata.org/grapher/human-development-index?time=2017

#Metric Descriptions of HDI
#https://www.investopedia.com/terms/h/human-development-index-hdi.asp#:~:text=It%20is%20composed%20of%20four,income%20(GNI)%20per%20capita.

#Takes in a string with a slash and adds together the floats on both sides before casting it back to a string
def parse_and_sum_slash(x):
    parts = x.split("/")
    try:
        return str(float(parts[0]) + float(parts[1]))
    except ValueError:
        return None

#Dataset of economic, social, environmental, and infrastructural indicators of many countries from 2017
#https://www.kaggle.com/datasets/sudalairajkumar/undata-country-profiles
df = pd.read_csv("country_profile_variables.csv")

#CLEANUP****************************************************************************************************
#Turns elements with these values to null
df = df[df[:] != "-99"]
df = df[df[:] != "~0.0"]
df = df[df[:] != "-~0.0"]
df = df[df[:] != "~0"]
df = df[df[:] != "..."]
df = df[df[:] != ".../..."]
df = df[df[:] != -99]

#Converts all leftover strings containing "/" into a string containing a single float
df = df.map(lambda x: parse_and_sum_slash(x) if isinstance(x, str) and "/" in x else x)

#Takes labels used to determine HDI as stated here:
#https://www.investopedia.com/terms/h/human-development-index-hdi.asp#:~:text=It%20is%20composed%20of%20four,income%20(GNI)%20per%20capita.

#Enrollment at different education levels are used in absense of data for "mean years of schooling" and
# "expected years of schooling"

#Unemployment % is used in absense of data for GNI per capita
df = df[["country",
         "Life expectancy at birth (females/males, years)", #Health aspect of HDI
         "Education: Tertiary gross enrol. ratio (f/m per 100 pop.)", #Education aspect of HDI
         "Education: Secondary gross enrol. ratio (f/m per 100 pop.)",
         "Education: Primary gross enrol. ratio (f/m per 100 pop.)",
         "Unemployment (% of labour force)"]] #Economic metric of HDI

print("_______________Non-null values for each feature_______________")
df.info()
print()

#Removes all entries/indices with a null
df.dropna(inplace=True)

#Seperates region/country columns
countries = df["country"]
X = df.iloc[:, 1:]

#Converting object features to floats
X = X[:].astype(float)

print("_______________Final Dataframe Used_______________")
X.info()
print()

#MODEL*****************************************************************************************************************

#Normalizing X
X = X.copy().to_numpy() * 1.0
std = np.std(X, axis=0)
X /= std

cluster_count = 7

kmeans = KMeans(n_clusters=cluster_count, n_init=500)
kmeans.fit(X)

#TEXT DISPLAY**********************************************************************************************************
print()
print("______________________Average Stats and Countries in Each Cluster______________________")
for i in range(cluster_count):
    print(f"Average Stats for cluster {i}: {kmeans.cluster_centers_[i] * std}---------------")
    print("***Countries***")
    for country in countries[kmeans.labels_ == i]:
        print(country)
    print()

#MAP DISPLAY**********************************************************************************************************
# Load world map from file: Large scale data, 1:10m
# https://www.naturalearthdata.com/downloads/
world = gpd.read_file("ne_110m_admin_0_countries.shp")

#Combines country names and cluster labels into 1 dataframe
countriesdf = df.loc[:, ['country']].copy()
countriesdf['cluster'] = kmeans.labels_

#Set options to display all rows, columns, and full column width
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
print()
print("______________________List of All Countries and their Cluster Assignment______________________")
print(countriesdf)

# Merge by name (make sure names match those in the GeoDataFrame)
world_clustered = world.merge(countriesdf, how='left', left_on='ADMIN', right_on='country')

#Displays an interactive map in browser
#Clusters are kept as a gradient instead of categories to be more pleasing to the eye
fig = px.choropleth(
    world_clustered,
    geojson=world_clustered.geometry,
    locations=world_clustered.index,
    color='cluster',
    hover_name='ADMIN',
    title="Countries Clustered by HDI Indicators",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()

#Compare this map with the only map from https://ourworldindata.org/grapher/human-development-index?time=2017


