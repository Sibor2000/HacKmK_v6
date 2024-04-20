import folium
import streamlit as st
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="my_app")

# Get location coordinates for Berlin
location = geolocator.geocode("Berlin")


st.set_page_config(page_title="Konnekt - Berlin's District", page_icon=":car:", layout="wide")

fmap = folium.Map(location=[location.latitude,location.longitude], zoom_start=12)

fg = folium.FeatureGroup(name="Berlin Districts")
berlin_districts_geojson = './data/berlin_districts.geojson'

with open(berlin_districts_geojson, 'r', encoding='utf-8') as f:
    geojson_data = f.read()

folium.GeoJson(geojson_data).add_to(fg)

folium.LayerControl().add_to(fmap)

st_folium(fmap, feature_group_to_add=fg, width="100%")
