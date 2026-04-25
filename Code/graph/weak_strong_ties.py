import pandas as pd
import matplotlib.pyplot as plt

file = 'Data/cleaned_data_no_na.csv'
capsoc = pd.read_csv(file)

masks = {
    "Rural": capsoc['living_place'] == 1,
    "Small Town": (capsoc['living_place'] >= 2) & (capsoc['living_place'] <= 3),
    "Mid Town": capsoc['living_place'] == 4,
    "Large City": (capsoc['living_place'] >= 5) & (capsoc['living_place'] <= 6),
    "Metropolis": capsoc['living_place'] >= 7
}

mapping_fin_job = {1:'Close family',
                   2: 'Distant family',
                   3: 'Close friends',
                   4: 'Neighbors',
                   5: 'Colleagues',
                   6: 'Someone else',
                   7: 'No one',
                   8: "Can't choose"}


capsoc['find_job_cat'] = capsoc['find_job'].map(mapping_fin_job)
capsoc['find_job_cat'] = pd.Categorical(
    capsoc['find_job_cat'],
    categories=list(mapping_fin_job.values()),
    ordered=True
)

interest_var = 'find_job_cat'

# Create a location column for grouping
location_labels = pd.Series(index=capsoc.index, dtype='object')
for location, mask in masks.items():
    location_labels[mask] = location

capsoc['location'] = location_labels

# Calculate weighted counts for all combinations
weighted_counts = capsoc.groupby([interest_var, 'location'])['weight'].sum().unstack(fill_value=0)

# Plot grouped bar chart
fig, ax = plt.subplots(figsize=(14, 6))
weighted_counts.plot(kind='bar', ax=ax, edgecolor='black')

# Mise en forme
plt.title(f'Weighted Distribution of {interest_var} by Location Type', fontsize=14)
plt.xlabel(interest_var, fontsize=12)
plt.ylabel('Total Weight (Population Estimate)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Location Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()