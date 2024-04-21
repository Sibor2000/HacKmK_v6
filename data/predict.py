import pandas as pd

# Load the dataset
data = pd.read_csv("Berlin_crimes_GCE.csv")

# Drop rows with missing values
data = data.dropna()

# Define weights for each feature
weights = {
    'Theft': 0.4,
    'Local': 0.2,
    'Area': 0.1,
    'Population': 0.3,
    'Density': 0.2,
    'Total crimes': 0.4,
    'Crime per capita': 0.4,
    'Theft density': 0.4,
    'Theft per capita': 0.4,
    'Total crime trend': 0.2,
    'Total theft trend': 0.3,
    'Deviation from district average': 0.3
}

# Select relevant features
selected_features = list(weights.keys())

# Normalize the selected features
normalized_data = (data[selected_features] - data[selected_features].mean()) / data[selected_features].std()

# Calculate the weighted sum of normalized features
weighted_sum = (normalized_data * pd.Series(weights)).sum(axis=1)

# Rescale the score to a range between 0 and 1
min_score = weighted_sum.min()
max_score = weighted_sum.max()
danger_score = (weighted_sum - min_score) / (max_score - min_score)

# Add the danger score to the dataset
data['Danger Score'] = danger_score

# For each location, calculate the average danger score
location_scores = data.groupby('Location')['Danger Score'].mean()
# Sort the locations by average danger score
location_scores = location_scores.sort_values(ascending=False)

dfx = pd.read_csv("waaa_detailed.csv")
# New empty dataframe
dfy = pd.DataFrame(columns=['sch', 'danger_score'])
for i in range(len(dfx)):
    code = dfx['Location'][i]
    danger_score = location_scores[code]
    # Find sch in the row that has a matching location
    sch = dfx[dfx['Location'] == code]['sch'].values[0]
    dfy = pd.concat([dfy, pd.DataFrame({'sch': [sch], 'danger_score': [danger_score]})], ignore_index=True)
dfy.to_csv("waaa_danger.csv", index=False)

# Plot the average danger scores on the 0-1 scale
import matplotlib.pyplot as plt

# plt.figure(figsize=(10, 6))
# plt.barh(location_scores.index, location_scores.values)
# plt.xlabel('Average Danger Score')
# plt.ylabel('Location')
# plt.title('Average Danger Score by Location in Berlin')

# plt.savefig('danger_score.png')

# Create an array from just the values
scores = location_scores.values

# import numpy as np
# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt

# def find_optimal_num_clusters(data, max_clusters=10):
#     wcss = []
#     for i in range(1, max_clusters + 1):
#         kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
#         kmeans.fit(data)
#         wcss.append(kmeans.inertia_)
        
#     # Plot the elbow
#     plt.plot(range(1, max_clusters + 1), wcss)
#     plt.title('Elbow Method')
#     plt.xlabel('Number of Clusters')
#     plt.ylabel('WCSS')
#     plt.savefig('elbow_method.png')

# # Example usage
# data = np.array(scores).reshape(-1, 1)
# find_optimal_num_clusters(data)

import numpy as np
from sklearn.cluster import KMeans

def find_cluster_boundaries(data, num_clusters):
    # Reshape the data
    data = np.array(data).reshape(-1, 1)
    
    # Fit KMeans clustering model
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(data)
    
    # Get sorted cluster centers
    cluster_centers = np.sort(kmeans.cluster_centers_, axis=0)
    print("Cluster Centers:", cluster_centers)
    
    # Calculate cluster boundaries
    cluster_boundaries = []
    for i in range(1, len(cluster_centers)):
        boundary = (cluster_centers[i-1][0] + cluster_centers[i][0]) / 2
        cluster_boundaries.append(boundary)
    
    return cluster_boundaries

# Example usage
data = scores
num_clusters = 6

boundaries = find_cluster_boundaries(data, num_clusters)
print("Cluster Boundaries:", boundaries)

# Create a bar plot with counts of locations in each cluster
def plot_cluster_counts(data, boundaries):
    # Assign each location to a cluster
    clusters = np.digitize(data, boundaries)
    
    # Count the number of locations in each cluster
    cluster_counts = np.bincount(clusters)
    
    # Plot the cluster counts
    plt.bar(range(1, len(cluster_counts) + 1), cluster_counts)
    plt.xlabel('Cluster')
    plt.ylabel('Number of Locations')
    plt.title('Number of Locations in Each Cluster')
    plt.savefig('cluster_counts.png')

plot_cluster_counts(data, boundaries)