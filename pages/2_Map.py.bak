import folium
import streamlit as st
from streamlit_folium import st_folium
import time

st.set_page_config(page_title="Konnekt - Map", page_icon=":car:", layout="wide")

# center on Liberty Bell, add marker
fmap = folium.Map(location=[46.7754325,23.5870139], zoom_start=12)

fg = folium.FeatureGroup(name="Vehicle Locations")
for vehicle in st.session_state.get("vehicles", []):
    fg.add_child(folium.Marker(location=[46.7754325,23.5870139], popup=vehicle["name"]))

# call to render Folium map in Streamlit
st_folium(fmap, feature_group_to_add=fg, width="100%")

for i in range(10):
    # Wait a bit and then update the marker location
    time.sleep(1)
    