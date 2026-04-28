import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


file = 'Data/cleaned_data_no_na.csv'
capsoc = pd.read_csv(file)

masks = {
    "Rural": capsoc['living_place'] == 0,
    "Small Town": (capsoc['living_place'] >= 1) & (capsoc['living_place'] <= 3),
    "Mid Town": (capsoc['living_place'] >= 4) & (capsoc['living_place'] <= 6),
    "Metropolis": capsoc['living_place'] >= 7
}


# 1. Définition des scores de prestige
statut_scores = {
    "csoc_Q01_01": 34.75, "csoc_Q01_02": 67.59, "csoc_Q01_03": 28.70,
    "csoc_Q01_04": 43.44, "csoc_Q01_05": 67.59, "csoc_Q01_06": 74.02,
    "csoc_Q01_07": 37.97, "csoc_Q01_08": 59.23, "csoc_Q01_09": 60.89,
    "csoc_Q01_10": 69.75
}

professions = list(statut_scores.keys())
scores_values = np.array(list(statut_scores.values()))

# 2. Création du masque (True si réponse 1, 2 ou 3)
# On vérifie pour chaque colonne de profession si la valeur est entre 1 et 3
has_link = capsoc[professions].isin([1, 2, 3])

# --- CALCULS ---

# A. Diversity : Somme des True par ligne
capsoc['pg_diversity'] = has_link.sum(axis=1)

# B. Upper Reachability : Somme pour les colonnes spécifiques (02, 05, 06)
prestige_scores = {
    "csoc_Q01_02": 10, # Cadre
    "csoc_Q01_06": 10, # Avocat
    "csoc_Q01_05": 8,  # RH
    "csoc_Q01_10": 7,  # Enseignant
    "csoc_Q01_08": 6,  # Infirmier
    "csoc_Q01_09": 5,  # Policier
    "csoc_Q01_07": 4,  # Mécanicien
    "csoc_Q01_04": 4,  # Coiffeur
    "csoc_Q01_01": 3,  # Chauffeur
    "csoc_Q01_03": 2,  # Agent d'entretien
    "csoc_Q01_10": 5   # Assistant social (estimation)
}

# On crée des colonnes temporaires pour chaque score
temp_cols = []
for col, score in prestige_scores.items():
    temp_col_name = f"val_{col}"
    # Si le répondant connaît (1), il reçoit le score, sinon 0
    capsoc[temp_col_name] = np.where(capsoc[col] == 1, score, 0)
    temp_cols.append(temp_col_name)

# LA VARIABLE FINALE : Le maximum atteint parmi toutes les connaissances
capsoc['pg_upper'] = capsoc[temp_cols].max(axis=1)

# C. Range (Max - Min)
# On remplace les False par NaN pour que min/max ne prennent en compte que les liens réels
prestige_accessible = has_link.multiply(scores_values, axis=1).replace(0, np.nan)

pg_max = prestige_accessible.max(axis=1)
pg_min = prestige_accessible.min(axis=1)

# Si pg_diversity > 1, on fait Max - Min, sinon 0
capsoc['pg_range'] = (pg_max - pg_min).fillna(0)

# 3. Réorganisation des colonnes (équivalent du select everything)
cols_to_front = ['pg_diversity', 'pg_upper', 'pg_range']
other_cols = [c for c in capsoc.columns if c not in cols_to_front]
capsoc = capsoc[cols_to_front + other_cols]


## Résultats 
# On crée une colonne vide
capsoc['habitat_cat'] = np.nan

# On remplit selon tes masques existants
for name, mask in masks.items():
    capsoc.loc[mask, 'habitat_cat'] = name


### Diversity of social capital 
print(capsoc.groupby('habitat_cat')['pg_diversity'].mean())
df_means = capsoc.groupby('habitat_cat')['pg_diversity'].mean().reset_index()
habitat_order = ["Metropolis", "Mid Town", "Small Town", "Rural"]
df_means['habitat_cat'] = pd.Categorical(df_means['habitat_cat'], categories=habitat_order, ordered=True)
df_means = df_means.sort_values('habitat_cat')

plt.figure(figsize=(8, 6))
sns.scatterplot(x='habitat_cat', y='pg_diversity', data=df_means, s=200, color='darkblue')

plt.ylim(4.5, 7)

plt.title('Number of different types of professionals in social network')
plt.ylabel('Mean (Diversity)')
plt.xlabel('')
plt.grid(axis='y', linestyle=':', alpha=0.5)


plt.savefig('outputs/social_position_diversity.png', dpi=300)

### Graphique upper reachability 
# --- UPPER REACHABILITY ---
df_means_upper = capsoc.groupby('habitat_cat')['pg_upper'].mean().reset_index()
df_means_upper['habitat_cat'] = pd.Categorical(df_means_upper['habitat_cat'], categories=habitat_order, ordered=True)
df_means_upper = df_means_upper.sort_values('habitat_cat')

plt.figure(figsize=(8, 6))
sns.scatterplot(x='habitat_cat', y='pg_upper', data=df_means_upper, s=200, color='darkred') # Rouge pour le prestige


plt.title('Upper Reachability by location type (mean)')
plt.ylabel('Mean (Upper Reach)')
plt.xlabel('')
plt.grid(axis='y', linestyle=':', alpha=0.5)

plt.savefig('outputs/social_position_upper.png', dpi=300)
plt.close() # Important pour ne pas superposer les graphes


### Graphique range 
df_means_range = capsoc.groupby('habitat_cat')['pg_range'].mean().reset_index()
df_means_range['habitat_cat'] = pd.Categorical(df_means_range['habitat_cat'], categories=habitat_order, ordered=True)
df_means_range = df_means_range.sort_values('habitat_cat')

plt.figure(figsize=(8, 6))
sns.scatterplot(x='habitat_cat', y='pg_range', data=df_means_range, s=200, color='darkgreen') # Vert pour l'étendue

plt.ylim(25, 45) # Échelle adaptée aux scores de prestige de Donald Treiman

plt.title('Range of social capital by location type')
plt.ylabel('Mean (Range)')
plt.xlabel('')
plt.grid(axis='y', linestyle=':', alpha=0.5)

plt.savefig('outputs/social_position_range.png', dpi=300)
plt.close()