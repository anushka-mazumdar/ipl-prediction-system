import pandas as pd
import os

matches = pd.read_csv('data_processing/raw_data/matches.csv')
deliveries = pd.read_csv('data_processing/raw_data/deliveries.csv')


# Convert date to datetime
if 'date' in matches.columns:
    matches['date'] = pd.to_datetime(matches['date'], errors='coerce')

if 'winner' in matches.columns:
    matches = matches.dropna(subset=['winner'])

team_columns = ['team1', 'team2', 'winner', 'toss_winner']
for col in team_columns:
    if col in matches.columns:
        matches[col] = matches[col].astype(str).str.strip().str.upper()

matches.to_csv('data_processing/cleaned_matches.csv', index=False)



print("Deliveries columns:", deliveries.columns.tolist())

player_columns = ['batsman', 'bowler', 'batter']  # depending on dataset
for col in player_columns:
    if col in deliveries.columns:
        deliveries[col] = deliveries[col].astype(str).str.strip().str.upper()

if 'dismissal_kind' in deliveries.columns:
    deliveries['dismissal_kind'] = deliveries['dismissal_kind'].fillna('none')

# Convert key numeric fields to correct type
numeric_columns = ['batsman_runs', 'total_runs']
for col in numeric_columns:
    if col in deliveries.columns:
        deliveries[col] = pd.to_numeric(deliveries[col], errors='coerce').fillna(0).astype(int)

deliveries.to_csv('data_processing/cleaned_deliveries.csv', index=False)

print("✅ Data cleaning complete. Cleaned files saved.")
