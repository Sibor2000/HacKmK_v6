from shapely.geometry import Point, shape
import json
import pandas as pd

def point_in_polygon(lat, lon, polygons):
    # Create a Point object from the lat, lon pair
    point = Point(lon, lat)
    
    # Iterate over the polygons and check if the point is within any of them
    for polygon in polygons:
        if polygon['geometry'].contains(point):
            return polygon['properties']['name']  # Assuming the polygon has a 'name' property
    return None  # Return None if the point is not within any polygon

def point_in_polygon_sch(lat, lon, polygons):
    # Create a Point object from the lat, lon pair
    point = Point(lon, lat)
    
    # Iterate over the polygons and check if the point is within any of them
    for polygon in polygons:
        if polygon['geometry'].contains(point):
            return polygon['properties']['sch']  # Assuming the polygon has a 'name' property
    return None  # Return None if the point is not within any polygon

def main():
    # Load the GeoJSON file containing the polygonal features
    with open('berlin_hoods.geojson') as f:
        data = json.load(f)
    
    # Extract the polygons from the GeoJSON file
    polygons = []
    for feature in data['features']:
        polygons.append({
            'geometry': shape(feature['geometry']),
            'properties': feature['properties']
        })
    
    # Coordinates
    crimes = pd.read_csv("Berlin_crimes_GCE.csv")
    crimes = crimes.dropna()
    # crimes = crimes[['Latitude', 'Longitude']]
    lat_lon_pairs = [
        (lat, lon) for lat, lon in zip(crimes['Latitude'], crimes['Longitude'])
    ]
    
    # Determine which polygon each lat, lon pair belongs to
    for lat, lon in lat_lon_pairs:
        polygon_name = point_in_polygon(lat, lon, polygons)
        if polygon_name:
            # print(f"The point ({lat}, {lon}) belongs to {polygon_name}.")
            pass
        else:
            print(f"No polygon found for the point ({lat}, {lon}).")
    

    # Load waaa
    waaa = pd.read_csv("waaa.csv")
    waaa = waaa.dropna()
    print(crimes.head())
    for entry in range(len(waaa)):
        code = waaa['Location'][entry]
        lat, lon = crimes[crimes['Code'] == code][['Latitude', 'Longitude']].values[0]
        polygon_sch = point_in_polygon_sch(lat, lon, polygons)
        if not polygon_sch:
            print(f"No polygon found for the point ({lat}, {lon}).")
            break
        waaa.loc[entry, 'sch'] = polygon_sch
        # Find the location name in data
        for polygon in data['features']:
            if polygon['properties']['sch'] == polygon_sch:
                waaa.loc[entry, 'Location'] = polygon['properties']['name']
                break

    # Count by sch and export (sch, count)
    waaa = waaa.groupby(['sch', 'Location']).size().reset_index(name='count')
    waaa.to_csv("waaa_count.csv", index=False)

if __name__ == "__main__":
    main()
