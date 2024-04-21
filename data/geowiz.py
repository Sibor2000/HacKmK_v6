import pandas as pd

def main():
    crime = pd.read_csv("Berlin_crimes_geolocated_combined.csv")
    areas = pd.read_csv("Berlin_areas.csv")

    # Preprocess areas: get unique district names
    new_entries = []
    districts = areas['District name'].unique()
    for district in districts:
        # If the districs name is "one-two", split it, try to find the two entries, and create a new entry
        if '-' in district:
            parts = district.split('-')
            entry1 = areas[(areas['District name'] == district) & (areas['Name'] == parts[0])]
            entry2 = areas[(areas['District name'] == district) & (areas['Name'] == parts[1])]
            if len(entry1) == 0 or len(entry2) == 0:
                print(f"Could not find area for {district}")
                continue
            # Create a new entry
            entry = entry1.copy()
            entry['District name'] = district
            entry['Name'] = district
            entry['Area'] = entry1['Area'].values[0] + entry2['Area'].values[0]
            entry['Population'] = entry1['Population'].values[0] + entry2['Population'].values[0]
            entry['Density'] = entry1['Density'].values[0] + entry2['Density'].values[0]
            print(f"Fixing {district}")
            new_entries.append(entry)

    # Add the new entries
    if new_entries:
        areas = pd.concat([areas] + new_entries, ignore_index=True)
    print(new_entries)  

    for i in range(len(crime)):
        district = crime['District'][i]
        neighborhood = crime['Location'][i]

        # Get area entries where the district name and neighborhood match
        areas_entry = areas[(areas['District name'] == district) & (areas['Name'] == neighborhood)]
        if len(areas_entry) == 0:
            # Fall back to only matching the district name twice
            areas_entry = areas[(areas['District name'] == district) & (areas['Name'] == district)]
            if len(areas_entry) == 0:
                print(f"Could not find area for {district}, {neighborhood}")
                continue
        
        # Add the data
        crime.loc[i, 'Area'] = areas_entry['Area'].values[0]
        crime.loc[i, 'Population'] = areas_entry['Population'].values[0]
        crime.loc[i, 'Density'] = areas_entry['Density'].values[0]
    print("Added area data to crime data")

    print("Engineering new features")
    # Total crime: Robbery,Street_robbery,Injury,Agg_assault,Threat,Theft,Car,From_car,Bike,Burglary,Fire,Arson,Damage,Graffiti,Drugs
    crime['Total crimes'] = crime['Robbery'] + crime['Street_robbery'] + crime['Injury'] + crime['Agg_assault'] + crime['Threat'] + crime['Theft'] + crime['Car'] + crime['From_car'] + crime['Bike'] + crime['Burglary'] + crime['Fire'] + crime['Arson'] + crime['Damage'] + crime['Graffiti'] + crime['Drugs']
    crime['Crime geodensity'] = crime['Total crimes'] / crime['Area']
    crime['Crime per capita'] = crime['Total crimes'] / crime['Population']
    # Same metrics but just with theft
    crime['Theft density'] = crime['Theft'] / crime['Area']
    crime['Theft per capita'] = crime['Theft'] / crime['Population']
    # Calculate total crime trend based on Year (derived from differences)
    # For example, if the total crime in 2018 is 100 and in 2019 is 110, the trend is +10%
    # Calculate total crime trend based on Year (derived from differences)
    crime['Total crime trend'] = crime.groupby('District')['Total crimes'].pct_change() * 100

    # Calculate total theft trend based on Year (derived from differences)
    crime['Total theft trend'] = crime.groupby('District')['Theft'].pct_change() * 100

    # Calculate average crime for district, and difference from average
    avg_crime_by_district = crime.groupby('District')['Total crimes'].mean()
    crime['Deviation from district average'] = crime['Total crimes'] - crime['District'].map(avg_crime_by_district)

    # Drop the crime columns except for Theft
    crime = crime.drop(columns=['Robbery', 'Street_robbery', 'Injury', 'Agg_assault', 'Threat', 'Car', 'From_car', 'Bike', 'Burglary', 'Fire', 'Arson', 'Damage', 'Graffiti', 'Drugs'])

    # Save the new data
    crime.to_csv("Berlin_crimes_GCE.csv", index=False)

if __name__ == "__main__":
    main()