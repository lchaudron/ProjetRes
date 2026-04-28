import pandas as pd
import numpy as np

# 1. Chargement
file = 'Data/cleaned_data.csv'
df = pd.read_csv(file)

# 2. Listes de colonnes
critical_cols = ['age', 'diploma', 'gender', 'living_place', 'csp', 'find_job', 'weight']
# On récupère toutes les colonnes qui ne sont pas dans les exceptions (donc les réseaux + professions)
cols_to_fix = [c for c in df.columns if c not in critical_cols]

# 3. Traitement des colonnes "Exceptions" (CSP et Find_Job)
# On prend le premier chiffre et on gère les codes d'erreur
df['csp'] = pd.to_numeric(df['csp'].astype(str).str[0], errors='coerce')
df['find_job'] = pd.to_numeric(df['find_job'].astype(str).str[0], errors='coerce')

df.loc[df['csp'] > 7, 'csp'] = np.nan
df.loc[df['find_job'] > 8, 'find_job'] = np.nan

# 4. Traitement des colonnes "Fix" (Réseaux et Professions)
for col in cols_to_fix:
    # On remplace les codes d'erreur par NaN
    df.loc[df[col] > 7, col] = np.nan
    # On extrait le premier chiffre de manière sécurisée
    # (Le .str[0] ne créera pas de 'n' car on ne convertit pas les NaN en string ici)
    df[col] = pd.to_numeric(df[col].astype(str).str[0], errors='coerce')

# 5. Suppression des lignes vides UNIQUEMENT sur les colonnes critiques
# Comme tu l'as demandé, on ne drop pas si c'est une colonne de profession qui est vide
df = df.dropna(subset=critical_cols)

# 6. Conversion finale en Int64 pour tout le monde (sauf le poids qui est un float)
all_int_cols = [c for c in df.columns if c != 'weight']
for col in all_int_cols:
    # pd.to_numeric nettoie les derniers caractères bizarres ('n', '.', etc.) avant la conversion
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

# 7. Sauvegarde
df.to_csv('Data/cleaned_data_no_na.csv', index=False)

print(f"Nettoyage terminé.")
print(f"Nombre de lignes finales : {len(df)}")
print(f"Colonnes conservées : {df.columns.tolist()}")