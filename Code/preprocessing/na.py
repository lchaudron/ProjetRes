import pandas as pd
import numpy as np

file = 'Data/cleaned_data.csv'
df = pd.read_csv(file)

df['csp'] = np.where(df['csp'] > 70, np.nan, df['csp'].astype(str).str[0].astype('Int64'))
df['find_job'] = np.where(df['find_job'] > 8, np.nan, df['find_job'].astype(str).str[0].astype('Int64'))

# 2. Liste des variables à exclure du traitement générique
exceptions = ['csp', 'age', 'diploma', 'gender', 'living_place', 'weight', 'find_job']

# 3. Application du filtre (> 7) sur toutes les autres colonnes
cols_to_fix = [c for c in df.columns if c not in exceptions]

for col in cols_to_fix:
    df.loc[df[col] > 7, col] = np.nan

df = df.dropna()


for col in cols_to_fix:
    df[col] = df[col].astype(str).str[0].astype('Int64')

df['csp'] = df['csp'].astype(str).str[0].astype('Int64')
df['find_job'] = df['find_job'].astype(str).str[0].astype('Int64')

df.to_csv('Data/cleaned_data_no_na.csv', index=False)
