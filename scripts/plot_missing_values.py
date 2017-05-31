import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd


cancer = pd.read_csv('data/recepteurs.csv', sep='\t')
features = cancer[['AGE', 'MENOP', 'TNM', 'TAILLE', 'ROQUANT', 'RPQUANT', 'HISTO', 'SBR',
                   'NBGANG', 'CHIR', 'RAD']]


# Missing values matrix
msno.matrix(features, figsize=(14, 10), inline=False)
plt.savefig('figures/missing_matrix.png')
