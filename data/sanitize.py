import pandas as pd
from geopy.geocoders import Nominatim

def geolocate_smooth(fn):
    data = pd.read_csv(fn)

    # Obtain latitude and longitude for each address
    geolocator = Nominatim(user_agent="geo_converter")

    # Add columns for latitude and longitude
    data['Latitude'] = None
    data['Longitude'] = None

    for i in range(len(data)):
        print(f"Processing row {i} of {len(data)} ({(i+1)/len(data)*100:.2f})")
        locationStr = data['Location'][i].replace(', nicht zuzuordnen', '')
        query = "Berlin, " + data['District'][i] + ", " + locationStr
        location = geolocator.geocode(query)
        if location is None:
            print(f"Could not find location for {query}")
            data.loc[i, 'Latitude'] = None
            data.loc[i, 'Longitude'] = None
            continue
        data.loc[i, 'Latitude'] = location.latitude
        data.loc[i, 'Longitude'] = location.longitude
        print(f"Found location for {query}")

    data.to_csv(f"{fn[:-4]}_geolocated.csv", index=False)

    # Print location found rate
    print(f"Location found rate: {data['Latitude'].count() / len(data) * 100:.2f}%")

    # Save the entries with missing location data separately
    missing_data = data[data['Latitude'].isnull()]
    missing_data.to_csv(f"{fn[:-4]}_missing.csv", index=False)

def geolocate_zip(fn):
    df = pd.read_csv(fn)
    geolocator = Nominatim(user_agent="geo_converter")
    df['Latitude'] = None
    df['Longitude'] = None
    for i in range(len(df)):
        print(f"Processing row {i} of {len(df)} ({(i+1)/len(df)*100:.2f})")
        query = "Berlin, " + df['District'][i] + ", " + str(df['Code'][i])
        location = geolocator.geocode(query)
        if location is None:
            print(f"Could not find location for {query}")
            df.loc[i, 'Latitude'] = None
            df.loc[i, 'Longitude'] = None
            continue
        df.loc[i, 'Latitude'] = location.latitude
        df.loc[i, 'Longitude'] = location.longitude
        print(f"Found location for {query}")

    df.to_csv(f"{fn[:-4]}_geolocated.csv", index=False)

    # Print location found rate
    print(f"Location found rate: {df['Latitude'].count() / len(df) * 100:.2f}%")

    # Save the entries with missing location data separately
    missing_data = df[df['Latitude'].isnull()]
    missing_data.to_csv(f"{fn[:-4]}_missing.csv", index=False)

def main():
    print("Geolocating Berlin crimes data")
    # geolocate_smooth("Berlin_crimes.csv")
    print("Geolocating Berlin crimes missing data")
    # geolocate_zip("Berlin_crimes_missing.csv")
    print("Done!")

    # Combine the two files
    # data1 = pd.read_csv("Berlin_crimes_geolocated.csv")
    # data2 = pd.read_csv("Berlin_crimes_missing_geolocated.csv")
    # data = pd.concat([data1, data2])

    # Only keep the entries with valid location data
    # data = data.dropna(subset=['Latitude', 'Longitude'])
    # data.to_csv("Berlin_crimes_geolocated_combined.csv", index=False)

    df = pd.read_csv("Berlin_crimes_geolocated_combined.csv")
    # Print columns
    print(df.columns)

if __name__ == "__main__":
    main()