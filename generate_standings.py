import pandas as pd
from datetime import datetime, timedelta

# Read the match data
matches_df = pd.read_csv('premier_league_data.csv')
print(f"Loaded {len(matches_df)} matches")

# Generate date range
date_from = datetime.strptime('2024-08-16', '%Y-%m-%d')
date_to = datetime.strptime('2025-01-16', '%Y-%m-%d')
date_range = pd.date_range(start=date_from, end=date_to)
print(f"Generated date range from {date_from} to {date_to}")

# Initialize standings
teams = set(matches_df['Home Team']).union(set(matches_df['Away Team']))
standings = {team: {'Points': 0, 'Played Games': 0, 'Won': 0, 'Draw': 0, 'Lost': 0, 'Goals For': 0, 'Goals Against': 0, 'Goal Difference': 0} for team in teams}
print(f"Initialized standings for {len(teams)} teams")

# Function to update standings
def update_standings(match):
    home_team = match['Home Team']
    away_team = match['Away Team']
    home_score = match['Home Score']
    away_score = match['Away Score']

    standings[home_team]['Played Games'] += 1
    standings[away_team]['Played Games'] += 1
    standings[home_team]['Goals For'] += home_score
    standings[away_team]['Goals For'] += away_score
    standings[home_team]['Goals Against'] += away_score
    standings[away_team]['Goals Against'] += home_score
    standings[home_team]['Goal Difference'] = standings[home_team]['Goals For'] - standings[home_team]['Goals Against']
    standings[away_team]['Goal Difference'] = standings[away_team]['Goals For'] - standings[away_team]['Goals Against']

    if home_score > away_score:
        standings[home_team]['Points'] += 3
        standings[home_team]['Won'] += 1
        standings[away_team]['Lost'] += 1
    elif home_score < away_score:
        standings[away_team]['Points'] += 3
        standings[away_team]['Won'] += 1
        standings[home_team]['Lost'] += 1
    else:
        standings[home_team]['Points'] += 1
        standings[away_team]['Points'] += 1
        standings[home_team]['Draw'] += 1
        standings[away_team]['Draw'] += 1

# Create a DataFrame to store the standings for each date
standings_list = []

for date in date_range:
    date_str = date.strftime('%Y-%m-%d')
    matches_on_date = matches_df[matches_df['Date'].str.startswith(date_str)]
    print(f"Processing {len(matches_on_date)} matches on {date_str}")

    for _, match in matches_on_date.iterrows():
        update_standings(match)

    # Sort standings
    sorted_standings = sorted(standings.items(), key=lambda x: (x[1]['Points'], x[1]['Goal Difference'], x[1]['Goals For']), reverse=True)

    # Add standings to the list
    for position, (team, stats) in enumerate(sorted_standings, start=1):
        standings_list.append({
            'Date': date_str,
            'Position': position,
            'Team': team,
            'Points': stats['Points'],
            'Played Games': stats['Played Games'],
            'Won': stats['Won'],
            'Draw': stats['Draw'],
            'Lost': stats['Lost'],
            'Goals For': stats['Goals For'],
            'Goals Against': stats['Goals Against'],
            'Goal Difference': stats['Goal Difference']
        })

# Create a DataFrame from the standings list
standings_df = pd.DataFrame(standings_list)
print(f"Generated standings for {len(standings_df)} rows")

# Save to CSV
standings_df.to_csv('daily_standings.csv', index=False)
print('Standings data saved to daily_standings.csv')