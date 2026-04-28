import pandas as pd

file = 'Data/fr_cdsp_ddi_elipss_201904csoc.csv'

df = pd.read_csv(file, sep=';', encoding='latin-1')

columns_to_keep = ['cal_AGE2', 'cal_DIPL', 'cal_SEXE', 'insee_TUU2014', 'B_ea19_PCS31', 'csoc_Q77_1', 'csoc_Q77_2', 'csoc_Q77_3', 'csoc_Q77_4', 'csoc_Q78_1', 'csoc_Q78_2', 'csoc_Q78_3', 'csoc_Q78_4', 'csoc_Q07_02', 'POIDS_csoc', 'csoc_Q01_01', 'csoc_Q01_02', 'csoc_Q01_03', 'csoc_Q01_04', 'csoc_Q01_05', 'csoc_Q01_06', 'csoc_Q01_07', 'csoc_Q01_08', 'csoc_Q01_09', 'csoc_Q01_10']
new_names = ['age', 'diploma', 'gender', 'living_place', 'csp', 'close_fam', 'close_friends', 'close_neighbors', 'close_colleagues', 'knows_fam', 'knows_friends', 'knows_neighbors', 'knows_colleagues', 'find_job','weight', 'csoc_Q01_01', 'csoc_Q01_02', 'csoc_Q01_03', 'csoc_Q01_04', 'csoc_Q01_05', 
    'csoc_Q01_06', 'csoc_Q01_07', 'csoc_Q01_08', 'csoc_Q01_09', 'csoc_Q01_10']

df = df[columns_to_keep]
df = df.rename(columns=dict(zip(columns_to_keep, new_names)))

df['weight'] = df['weight'].str.replace(',', '.').astype(float)

df.to_csv('Data/cleaned_data.csv', index=False)
