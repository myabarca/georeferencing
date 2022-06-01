# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:58:40 2022

@author: abarc
"""

import folium
import pandas as pd
# import requests
  
    

# MAPPING FROM GEOJSON FILE #

# 1. Create basemap

m = folium.Map(location=[40.43148077979194, -121.6627849541342],
           zoom_start=6,
           tiles='https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
           attr = 'Esri, HERE, Garmin, © OpenStreetMap contributors, and the GIS User Community')

# JSON file downloaded from Native Land Digital (https://native-land.ca/resources/api-docs/#Files)
geojson = r"indigenousTerritories.json"

g = folium.GeoJson(
    geojson,
    name='geojson'
).add_to(m)

folium.GeoJsonTooltip(fields=["Name"]).add_to(g)    # Name here refers to indigenous territory name provided in geoJSON


# 2. Plot points on basemap

# Read csv with our coordinates
df = pd.read_csv(r"localityDataWithGeorefData-samplePublic.csv")

# Make locationIDs strings so they can be used for popup and tooltip (those only take str and not int)
df['locationID'] = df['locationID'].apply(str)
df['county'] = df['county'].apply(str)      

for i, point in df.iterrows():
    #iterrows will store the row index in i, and store the row in point
    folium.Marker(
    location=[point['decimalLatitude_x'], point['decimalLongitude_x']], 
    tooltip= '<strong>Database County: </strong><br>' + point['county'] + ', ' + point['stateProvince'], #<strong> tag adds some styling to popup & tooltip.
    popup='<strong>locationID: </strong><br>'+ point['locationID']
        # Note that you have to click on the marker for the popup to show (not just hover over the marker like with the tooltip option)
    ).add_to(m)

filepath = r"CASG-nativeLandsLocs.html"
m.save(filepath)


# MAPPING FROM A REQUEST #
    # Didn't purse this method after all. Went with code above.

# Use requests.get(url) to get the url
# Since data is in JSON, can use .json() to format the response object as a json/dictionary
#response = requests.get('https://native-land.ca/wp-json/nativeland/v1/api/index.php?maps=territories').json()

# Usually would print response.content, but since we added .json(), we can just print response without content method
# print(response)
    
# The result is a list of objects
# Loop through list to isolate the data you're interested in
    
#for data in response:
     #print(data)       # response data is now not in a list of objects, but printed as each item (and each item is a dictionary). Useful for seeing what keys we need to pull from.
#    if data['properties']['Name']:
#        print(data['properties']['Name'])
#    else:
#        continue

