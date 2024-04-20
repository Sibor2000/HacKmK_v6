import json
import copy
import folium
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="my_app")

# Get location coordinates for Berlin
location = geolocator.geocode("Berlin")


st.set_page_config(page_title="Konnekt - Berlin's District", page_icon=":car:", layout="wide")

fmap = folium.Map(location=[location.latitude,location.longitude], zoom_start=12)

fg = folium.FeatureGroup(name="Berlin Districts")
berlin_districts_geojson = './data/bezirksgrenzen.geojson'
berlin_hoods_geojson = './data/berlin_hoods.geojson'

with open(berlin_districts_geojson, 'r', encoding='utf-8') as f:
    larger_districts = json.load(f)
with open(berlin_hoods_geojson, 'r', encoding='utf-8') as f:
    smaller_districts = json.load(f)

smaller_districts_copy = copy.deepcopy(smaller_districts)

# complaints_df = pd.read_csv("./data/waaa.csv")

# for feature in smaller_districts_copy['features']:
#     feature['properties']['sch'] = int(feature['properties']['sch'][6:])
#     # print(feature['properties']['sch'])

# district_counts = complaints_df.groupby('Location').size().reset_index(name='count')

# for code in district_counts['Location']:
#     # Find the corresponding feature in the GeoJSON
#     for feature in smaller_districts_copy['features']:
#         if feature['properties']['sch'] == code:
#             # Add the count to the feature properties
#             feature['properties']['count'] = int(district_counts[district_counts['Location'] == code]['count'])
#             break
    
#     print(f"Could not find district with code {code}")

waaa = pd.read_csv("./data/waaa_count.csv")

folium.Choropleth(
    geo_data=smaller_districts_copy,
    data=waaa,  # DataFrame containing metric values for each district
    columns=['sch', 'count'],  # Specify the column names
    key_on='properties.sch',  # Path to the feature property containing the district code
    fill_color='OrRd',  # Color scale (e.g., 'YlGn', 'YlGnBu', 'PuBu', 'RdPu', etc.)
    fill_opacity=0.7,  # Opacity of the fill color
    line_opacity=0.2,  # Opacity of the boundary lines
    line_color="black",
    nan_fill_color="gray",
    nan_fill_opacity=0.4,
    legend_name='Number of Complaints'  # Name of the legend
).add_to(fmap)

tooltips = folium.FeatureGroup("Tooltips")
for feature in smaller_districts_copy['features']:
    # Find the count for the district code in the DataFrame
    count_series = waaa[waaa['sch'] == int(feature['properties']['sch'])]['count']
    # Check if the count series is not empty
    if not count_series.empty:
        count = count_series.values[0]
    else:
        # If the district code is not found in the DataFrame, set count to 0
        count = 0
    folium.GeoJson(
        feature,
        tooltip=f"<b>District Code:</b> {feature['properties']['sch']} <br><b>Complaint Count:</b> {count}",
        style_function=lambda x: {
            'color': 'gray',  # Change the border color to gray
            'fillOpacity': 0,  # Make the fill transparent
        }

        ).add_to(tooltips)
    
    tooltips.add_to(fmap)

# folium.GeoJson(smaller_districts).add_to(fmap)


larger_districts_fg = folium.FeatureGroup(name="Larger Districts")
for feature in larger_districts['features']:
    folium.GeoJson(feature).add_to(larger_districts_fg)


# Create checkboxes for selecting larger districts
selected_district_names = st.multiselect('Select Larger Districts', [feature['properties']['Gemeinde_name'] for feature in larger_districts['features'] if 'Gemeinde_name' in feature['properties']])
selected_districts = {}
for feature in larger_districts['features']:
    if feature['properties']['Gemeinde_name'] in selected_district_names:
            selected_districts[feature['properties']['Schluessel_gesamt']] = feature

selected_districts_fg = folium.FeatureGroup(name = "Selected Districts")
# Add the selected larger districts to the map
for feature in larger_districts['features']:
    if 'Gemeinde_name' in feature['properties']:
        district_name = feature['properties']['Gemeinde_name']
        if district_name in selected_district_names:
            folium.GeoJson(feature).add_to(selected_districts_fg)

smaller_districts_by_code = {}
for feature in smaller_districts['features']:
    # Extract the larger district code from the feature properties
    larger_district_code = feature['properties']['sch'][:-4]
    # Create a new FeatureGroup for the smaller districts if not already present
    # print(larger_district_code)
    if larger_district_code in selected_districts:
         # Create a new FeatureGroup for the smaller districts if not already present
        if larger_district_code not in smaller_districts_by_code:
            smaller_districts_by_code[larger_district_code] = folium.FeatureGroup(name=f"{feature['properties']['name']}")
        # Add the smaller district feature to the corresponding feature group
        folium.GeoJson(feature).add_to(smaller_districts_by_code[larger_district_code])

for fg in smaller_districts_by_code.values():
    # fg.add_to(fmap)
    pass

# Add feature groups to the map
# fg.add_to(fmap)
# larger_districts_fg.add_to(fmap)

# selected_districts_fg.add_to(fmap)

folium.LayerControl().add_to(fmap)

st_folium(fmap, width="100%")
