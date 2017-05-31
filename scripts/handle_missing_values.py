import pandas as pd


cancer = pd.read_csv('data/recepteurs.csv', sep='\t')
features = cancer[['AGE', 'MENOP', 'TNM', 'TAILLE', 'ROQUANT', 'RPQUANT', 'HISTO', 'SBR',
                   'NBGANG', 'CHIR', 'RAD']]

# Discard rows that have more that one missing values
cancer_2 = cancer[features.isnull().sum(axis='columns') < 2].copy()

# Discard rows with ages less than 18
cancer_3 = cancer_2[cancer_2['AGE'] > 18].copy()

# Discard rows with no last event date
cancer_4 = cancer_3[cancer_3['D_DN'].notnull()].copy()

# Categorical variables
for col in ('TNM', 'HISTO', 'SBR', 'RAD'):
    cancer_4[col].fillna(cancer_3[col].value_counts().idxmax(), inplace=True)

# Continuous variables
for col in ('TAILLE', 'ROQUANT', 'RPQUANT', 'NBGANG'):
    cancer_4[col].fillna(cancer_4[col].median(), inplace=True)

cancer_4.to_csv('data/recepteurs_v2.csv', index=False)
