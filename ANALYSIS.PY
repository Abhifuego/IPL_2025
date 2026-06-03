import pandas as pd
import numpy as np
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')
orange_cap = pd.read_csv('orange_cap.csv')
purple_cap = pd.read_csv('purple_cap.csv')
print(matches.head())
print(deliveries.head())
print(orange_cap.head())
print(purple_cap.head())
# check duplicate rows
print("Matches Duplicates:", matches.duplicated().sum())
print("Deliveries Duplicates:", deliveries.duplicated().sum())
print("Orange Cap Duplicates:", orange_cap.duplicated().sum())
print("Purple Cap Duplicates:", purple_cap.duplicated().sum())
# check null values
print(matches.isnull().sum())
print(deliveries.isnull().sum())
print(orange_cap.isnull().sum())
print(purple_cap.isnull().sum())
# check column names
print(matches.columns)
print(deliveries.columns)
print(orange_cap.columns)
print(purple_cap.columns)
print(matches['match_id'].head())
print(deliveries['match_no'].head())
#Data Quality 
print("Matches Shape:", matches.shape)
print("Deliveries Shape:", deliveries.shape)
print("Orange Cap Shape:", orange_cap.shape)
print("Purple Cap Shape:", purple_cap.shape)
#Task 1: Create Total Runs Per Ball
deliveries['total_runs'] = deliveries['runs_of_bat'] + deliveries['extras']
print(deliveries[['runs_of_bat','extras','total_runs']].head())
#1. Total Matches
print("Total Matches:", matches['match_id'].nunique())
#total runs
print("Total Runs:", deliveries['total_runs'].sum())
deliveries['is_wicket'] = np.where(
    deliveries['wicket_type'].notna(),
    1,
    0
)
print(deliveries[['wicket_type','is_wicket']].head(10))
# total wickets
print("Total Wickets:", deliveries['is_wicket'].sum())
#Does winning toss help win matches?
toss_match_win = matches[
    matches['toss_winner']
    ==
    matches['match_winner']
]

percentage = (
    len(toss_match_win)
    /
    len(matches)
) * 100

print(percentage)
#EDA STEP 4: Venue Analysis
venue_matches = matches['venue'].value_counts()

print(venue_matches)
#EDA STEP 5: Batting Analysis
#Top Run Scorers
top_batsmen = deliveries.groupby(
    'striker'
)['runs_of_bat'].sum()

top_batsmen = top_batsmen.sort_values(
    ascending=False
)

print(top_batsmen.head(10))
#Most Fours
deliveries['is_four'] = np.where(
    deliveries['runs_of_bat'] == 4,
    1,
    0
)
most_fours = deliveries.groupby(
    'striker'
)['is_four'].sum()

print(
    most_fours.sort_values(
        ascending=False
    ).head(10)
)
deliveries['is_six'] = np.where(
    deliveries['runs_of_bat'] == 6,
    1,
    0
)

most_sixes = deliveries.groupby(
    'striker'
)['is_six'].sum()

print(
    most_sixes.sort_values(
        ascending=False
    ).head(10)
)
#EDA STEP 6: Bowling Analysis
top_bowlers = deliveries.groupby(
    'bowler'
)['is_wicket'].sum()

print(
    top_bowlers.sort_values(
        ascending=False
    ).head(10) )

#1. Highest Scoring Batsmen by Phase

# Question:

#Who dominates Powerplay, Middle Overs, and Death Overs?
def over_phase(over):
    
    if over <= 6:
        return 'Powerplay'
    
    elif over <= 15:
        return 'Middle Overs'
    
    else:
        return 'Death Overs'

deliveries['phase'] = deliveries['over'].apply(over_phase)

phase_batsman = deliveries.groupby(
    ['phase','striker']
)['total_runs'].sum().reset_index()

print(
    phase_batsman.sort_values(
        'total_runs',
        ascending=False
    ).head(20)
)
#5. Player of the Match Analysis
pom = matches['player_of_the_match'].value_counts()

from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "root"
password = quote_plus("Abhi@54321")   # encodes @ as %40

host = "localhost"
port = "3306"
database = "ipl_2025"
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# Force actual connection
matches.to_sql(
    'matches',
    con=engine,
    if_exists='replace',
    index=False
)

deliveries.to_sql(
    'deliveries',
    con=engine,
    if_exists='replace',
    index=False
)

orange_cap.to_sql(
    'orange_cap',
    con=engine,
    if_exists='replace',
    index=False
)

purple_cap.to_sql(
    'purple_cap',
    con=engine,
    if_exists='replace',
    index=False
)

print("All tables uploaded successfully")