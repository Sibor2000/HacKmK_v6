import pandas as pd
import json

hoods = json.load(open("lor_ortsteile.geojson"))
crimes = pd.read_csv("Berlin_crimes_GCE.csv")

# # Crimes has a column called Code
# # Hoods has a sch that will be transformed shortly
# features = hoods['features']
# for feature in features:
#     feature['properties']['sch'] = int(feature['properties']['sch'][7:])

# # print schs
# x = []
# for feature in features:
#     x.append(feature['properties']['sch'])
# x.sort()
# print(x)

# # Find the codes in the hoods data that are not in the crimes data
# i = 0
# codes = crimes['Code'].unique()
# for feature in features:
#     if feature['properties']['sch'] not in codes:
#         i += 1
#         # print(f"Code {feature['properties']['sch']} not in crimes data")

# print(f"Total: {i}/{len(features)} codes not in crimes data")

# # Find the codes in the crimes data that are not in the hoods data
# i = 0
# codes = set([feature['properties']['sch'] for feature in features])
# for code in crimes['Code'].unique():
#     if code not in codes:
#         i += 1
#         # print(f"Code {code} not in hoods data")

# print(f"Total: {i}/{len(crimes['Code'].unique())} codes not in hoods data")

names_from_crimes = crimes['Location'].unique()
names_from_hoods = set([feature['properties']['spatial_alias'] for feature in hoods['features']])

# Find the names in the hoods data that are not in the crimes data
i = 0
for name in names_from_hoods:
    if name not in names_from_crimes:
        i += 1
        print(f"Name {name} not in crimes data")

print(f"Total: {i}/{len(names_from_hoods)} names not in crimes data")

# Find the names in the crimes data that are not in the hoods data
i = 0
for name in names_from_crimes:
    if name not in names_from_hoods:
        i += 1
        print(f"Name {name} not in hoods data")

print(f"Total: {i}/{len(names_from_crimes)} names not in hoods data")


