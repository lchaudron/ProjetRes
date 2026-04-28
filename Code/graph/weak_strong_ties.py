import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Chargement des données
file = 'Data/cleaned_data_no_na.csv'
capsoc = pd.read_csv(file)

# 2. Définition des masques et de l'ordre souhaité
masks = {
    "Rural": capsoc['living_place'] == 1,
    "Small Town": (capsoc['living_place'] >= 2) & (capsoc['living_place'] <= 3),
    "Mid Town": capsoc['living_place'] == 4,
    "Large City": (capsoc['living_place'] >= 5) & (capsoc['living_place'] <= 6),
    "Metropolis": capsoc['living_place'] >= 7
}

# Ordre spécifique demandé
location_order = ["Large City", "Metropolis", "Mid Town", "Small Town", "Rural"]

mapping_fin_job = {1:'Close family', 2: 'Distant family', 3: 'Close friends',
                   4: 'Neighbors', 5: 'Colleagues', 6: 'Someone else',
                   7: 'No one', 8: "Can't choose"}

# 3. Préparation des variables catégorielles
capsoc['find_job_cat'] = pd.Categorical(
    capsoc['find_job'].map(mapping_fin_job),
    categories=list(mapping_fin_job.values()),
    ordered=True
)

# Attribution des labels de localisation
location_labels = pd.Series(index=capsoc.index, dtype='object')
for location, mask in masks.items():
    location_labels[mask] = location

# Application de l'ordre spécifique sur la colonne location
capsoc['location'] = pd.Categorical(location_labels, categories=location_order, ordered=True)

interest_var = 'find_job_cat'

# 4. Calculs pondérés et normalisation (Proportions)
weighted_counts = capsoc.groupby([interest_var, 'location'], observed=False)['weight'].sum().unstack(fill_value=0)
weighted_proportions = weighted_counts.div(weighted_counts.sum(axis=0), axis=1) * 100

# 5. Plot
fig, ax = plt.subplots(figsize=(14, 6))
weighted_proportions.plot(kind='bar', ax=ax, edgecolor='black')

# Mise en forme
plt.title('Proportion of Job Search Methods by Location Type', fontsize=14)
plt.xlabel(interest_var, fontsize=12)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Location Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()


plt.savefig('outputs/histograms_ties/distribution_job_location.png', dpi=300)
plt.show()