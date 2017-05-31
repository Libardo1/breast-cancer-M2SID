import datetime as dt

import numpy as np
import pandas as pd


cancer = pd.read_csv('data/recepteurs_v2.csv')

# Extract disease-free event

cancer['E_DF'] = (cancer[['E_DECES', 'E_META', 'E_RECI', 'E_CONT']].sum(axis='columns') == 0)
cancer['E_DF'] = cancer['E_DF'].astype(int)

# Melt dataframe to get events

event_cols = ['E_DECES', 'E_META', 'E_RECI', 'E_CONT', 'E_DF']

cancer_2 = pd.melt(
    cancer,
    id_vars=[col for col in cancer.columns if col not in event_cols],
    value_vars=event_cols,
    var_name='EVENEMENT',
    value_name='OCCURRENCE'
)

# Extract the date of each event so as to get a single column

def get_date_of_event(row):
    """For each type of event get the corresponding event date"""
    if row['EVENEMENT'] == 'E_DECES':
        return row['D_DECES']
    elif row['EVENEMENT'] == 'E_META':
        return row['D_META']
    elif row['EVENEMENT'] == 'E_RECI':
        return row['D_RECI']
    elif row['EVENEMENT'] == 'E_CONT':
        return row['D_CONT']
    return row['D_DN']

cancer_2['DATE'] = cancer_2.apply(get_date_of_event, axis='columns')
cancer_2['DATE'].fillna(cancer_2['D_DN'], inplace=True)

# Drop the rows with no dates

cancer_3 = cancer_2[(cancer_2['DATE'].notnull())].copy()

# Get features for indicating co-occurrent events

cancer_3['E_META'] = ((cancer_3['D_META'].notnull()) & (cancer_3['D_META'] <= cancer_3['D_FIRST'])).astype(int)
cancer_3['E_RECI'] = ((cancer_3['D_RECI'].notnull()) & (cancer_3['D_RECI'] <= cancer_3['D_FIRST'])).astype(int)
cancer_3['E_CONT'] = ((cancer_3['D_CONT'].notnull()) & (cancer_3['D_META'] <= cancer_3['D_FIRST'])).astype(int)

# Convert dates to datetimes

def parse_date(date):
    """Transform the year of each from xx to 19xx and convert to Python datetime"""
    date_parts = date.split('/')
    year = '19' + date_parts[-1]
    return dt.datetime.strptime('/'.join(date_parts[:-1] + [year]), '%d/%m/%Y')

cancer_3['DATE'] = cancer_3['DATE'].apply(parse_date)
cancer_3['D_FIRST'] = cancer_3['D_FIRST'].apply(parse_date)

# Extract year from initial date and event dates

cancer_3['DATE_YEAR'] = cancer_3['DATE'].dt.year
cancer_3['D_FIRST_YEAR'] = cancer_3['D_FIRST'].dt.year

# Calculate the difference between the first date and the event date

def get_days_diff(row):
    """Get the difference in days between the initial date and the event date"""
    initial_date = row['D_FIRST']
    event_date = row['DATE']
    return (event_date - initial_date).days

cancer_3['DIFF_JOURS'] = cancer_3.apply(get_days_diff, axis='columns')

# Fill null death causes

most_occurring_death_event = cancer_3['CAUSEDC'].value_counts().idxmax()

def fill_death_cause(row):
    if not np.isnan(row['CAUSEDC']):
        return row['CAUSEDC']
    elif row['EVENEMENT'] == 'E_DECES':
        return most_occurring_death_event
    return 0

cancer_3['CAUSEDC'] = cancer_3.apply(fill_death_cause, axis='columns')

# Remove the unnecessary columns

cols_to_drop = ['D_DECES', 'D_META', 'D_RECI', 'D_CONT', 'D_DN', 'D_FIRST']
cancer_3.drop(cols_to_drop, axis='columns', inplace=True)

# Save the final dataframe

cancer_3.sort_values(['IDENT', 'DATE']).to_csv('data/recepteurs_v3.csv', index=False)
