#!/usr/bin/env python
# coding: utf-8

# In[1]:



import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # conversion an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 


from IPython.display import display_html
import pandas as pd
import numpy as np


import requests # library to handle requests
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans


get_ipython().system("conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab")
import folium # map rendering library

print('Libraries imported.')


# In[2]:


get_ipython().system('pip install lxml')
import lxml
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
df = pd.read_html(url, header=0)
df = df[0]
df.head()


# Check the number of 'Not assigned' in Borough 

# In[3]:


df.Borough.value_counts()


# 
# Check the number of 'Not assigned' in Neighborhood
# 

# In[4]:


df.Neighbourhood.value_counts()


#  nan is used to replace "Not assigned" in Borough.

# In[5]:


df.Borough.replace("Not assigned", np.nan, inplace = True)
df.head()


# In[6]:


# Dropping the rows where Borough is 'Not assigned'
df = df[df.Borough != 'Not assigned']

# Combining the neighbourhoods with same Postalcode
df = df.groupby(['Postal Code','Borough'], sort=False).agg(', '.join)
df.reset_index(inplace=True)

# Replacing the name of the neighbourhoods which are 'Not assigned' with names of Borough
df['Neighbourhood'] = np.where(df['Neighbourhood'] == 'Not assigned',df['Borough'], df['Neighbourhood'])

df


# In[7]:


#Importing the csv file conatining the latitudes and longitudes for various neighbourhoods in Canada
latitude_longitude = pd.read_csv('https://cocl.us/Geospatial_data')
latitude_longitude.head()


# In[8]:


#Merging the two tables for getting the Latitudes and Longitudes for various neighbourhoods in Canada

latitude_longitude.rename(columns={'Postal Code':'Postal Code'},inplace=True)
df = pd.merge(df,latitude_longitude,on='Postal Code')
df.head()


# Clustering and the plotting of the neighbourhoods of Canada which contain Toronto in their Borough

# In[9]:


df = df[df['Borough'].str.contains('Toronto',regex=False)]
df


# In[10]:


#Visualizing all the Neighbourhoods of the above data frame using Folium

map_toronto = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

for lat,lng,borough,neighbourhood in zip(df['Latitude'],df['Longitude'],df['Borough'],df['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
    [lat,lng],
    radius=5,
    popup=label,
    color='blue',
    fill=True,
    fill_color='#3186cc',
    fill_opacity=0.7,
    parse_html=False).add_to(map_toronto)
map_toronto


# Using KMeans for the clustering of the neighbourhoods
# 

# In[11]:


k=10
toronto_clustering = df.drop(['Postal Code','Borough','Neighbourhood'],1)
kmeans = KMeans(n_clusters = k,random_state=0).fit(toronto_clustering)
kmeans.labels_
df.insert(0, 'Cluster Labels', kmeans.labels_)
df


# In[12]:


# create map
map_clusters = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

# set color scheme for the clusters
x = np.arange(k)
ys = [i + x + (i*x)**2 for i in range(k)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, neighbourhood, cluster in zip(df['Latitude'], df['Longitude'], df['Neighbourhood'], df['Cluster Labels']):
    label = folium.Popup(' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters


# In[ ]:




