import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load pickup points data
pickup_points_df = pd.read_csv('pickup_points.csv')
pickup_points_df['id'] = pickup_points_df['id'].astype(str)
# print(pickup_points_df.head())

# Load truck routes data
truck_routes_df = pd.read_csv('truck_routes.csv')

# Create map centered at average coordinates of pickup points
map_center = [pickup_points_df['latitude'].mean(), pickup_points_df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Interactive component to select pickup point
selected_pickup_point = st.selectbox('Select Pickup Point:', pickup_points_df['id'])
# print(selected_pickup_point)

selected_point_row = pickup_points_df[pickup_points_df['id'] == selected_pickup_point]

folium.Marker([selected_point_row['latitude'].values[0], selected_point_row['longitude'].values[0]],
              popup=selected_pickup_point,
              icon=folium.Icon(color='blue')).add_to(m)

# print(truck_routes_df['from_id'])
selected_pickup_point = int(selected_pickup_point)
# Filter truck routes data for the selected pickup point as 'from_id'
# print(truck_routes_df['from_id'])
selected_routes = truck_routes_df[truck_routes_df['from_id'] == selected_pickup_point]
# print(selected_routes.head())

# Add markers for other pickup points
for index, row in selected_routes.iterrows():
        # Check if there's a route from selected point to the current point
        to_point = pickup_points_df[pickup_points_df['id'].astype(int) == row['to_id']]

        if not to_point.empty:
            delay = row['delay']
            cause_of_delay = row['cause_of_delay']
            popup_content = f'<b>{to_point["name"]}</b><br>Delay: {delay} minutes<br>Cause of Delay: {cause_of_delay}'
            folium.Marker([to_point.iloc[0]['latitude'], to_point.iloc[0]['longitude']],
                popup=popup_content,
                icon=folium.Icon(color='red' if delay > 5 else 'green')).add_to(m)

# Display map
st.markdown(f'## Pickup Points Map for {selected_pickup_point}')
st.markdown('Click on a marker to see the delay and cause of delay.')
folium_static(m)
