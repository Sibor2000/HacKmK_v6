import pandas as pd
import random

# Load the location data
data = pd.read_csv("Berlin_crimes_GCE.csv")

# Keep the Code column, only, the distinct values
keepColumns = ["Code"]
keepTable = data[keepColumns]

def generate_values_with_frequency(values, frequencies, num_samples):
    # Create a list to store the generated values
    generated_values = []
    
    # Repeat the process for the desired number of samples
    for _ in range(num_samples):
        # Use random.choices() to generate a value based on the specified frequencies
        value = random.choices(values, weights=frequencies)[0]
        generated_values.append(value)
    
    return generated_values

# Example usage
labels = ["Missing Product","Damaged Product","Wrong product","Late","Other"]
frequencies = [0.1, 0.3, 0.1, 0.3, 0.2]
num_samples = 100000

generated_values = generate_values_with_frequency(labels, frequencies, num_samples)

# Create a data frame for the values, also add a random time on the same day
endTable = pd.DataFrame(generated_values, columns=["Complaint"])
endTable["Time"] = [f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}" for _ in range(num_samples)]
endTable["Location"] = keepTable["Code"].sample(n=num_samples, replace=True).tolist()

# Create a spike in the number of some complaints at a specific location in two hours
spike_mod = 0.1
spike_location = 10113 # Alexanderplatz
spike_samples = int(num_samples * spike_mod)
spike_values = generate_values_with_frequency(["Missing Product", "Other"], [0.8, 0.2], spike_samples)
spike_times = [f"{random.randint(10, 11):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}" for _ in range(spike_samples)]
spike_locations = [spike_location] * spike_samples

spike_data = pd.DataFrame(zip(spike_values, spike_times, spike_locations), columns=["Complaint", "Time", "Location"])
endTable = pd.concat([endTable, spike_data])

# Keep only count samples, decimate the rest uniformly
true_num_samples = 500
endTable = endTable.sample(n=true_num_samples, replace=True)

# Save the generated data
endTable.to_csv("waaa.csv", index=False)

# Create a plot of the complaint distribution (type, hour, location)
import matplotlib.pyplot as plt

# Plot the distribution of complaints by type
plt.figure(figsize=(10, 6))
endTable["Complaint"].value_counts().plot(kind="bar")
# Complaint type labels should be horizontal
plt.xticks(rotation=0)
plt.xlabel("Complaint Type")
plt.ylabel("Number of Complaints")
plt.title("Distribution of Complaint Types")
plt.savefig("complaint_types.png")

# Plot the distribution of complaints by hour
# Sort the times by hour
plt.figure(figsize=(10, 6))
endTable["Time"].str[:2].value_counts().sort_index().plot(kind="bar")
plt.xlabel("Hour")
plt.ylabel("Number of Complaints")
plt.title("Distribution of Complaints by Hour")
plt.savefig("complaint_hours.png")

# Plot the distribution of complaints by location
plt.figure(figsize=(10, 6))
endTable["Location"].value_counts().plot(kind="bar")
plt.xlabel("Location")
plt.ylabel("Number of Complaints")
plt.title("Distribution of Complaints by Location")
plt.savefig("complaint_locations.png")