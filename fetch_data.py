import requests
import pandas as pd

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.football-data.org/v4/'

def fetch_premier_league_data():
    url = f'{BASE_URL}competitions/PL/matches?dateFrom=2024-08-16&dateTo=2025-01-16'
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(url, headers=headers)
    print(f"Fetching Premier League data: {response.status_code}")
    if response.status_code != 200:
        print(f"Error fetching Premier League data: {response.status_code}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    data = response.json()
    matches = data.get('matches', [])
    print(f"Fetched {len(matches)} matches")

    processed_data = {
        'Date': [],
        'Home Team': [],
        'Away Team': [],
        'Home Score': [],
        'Away Score': []
    }

    teams_data = {
        'Team ID': [],
        'Name': [],
        'Short Name': [],
        'Crest': [],
        'Coach Name': []
    }

    teams_seen = set()

    for match in matches:
        processed_data['Date'].append(match['utcDate'])
        processed_data['Home Team'].append(match['homeTeam']['name'])
        processed_data['Away Team'].append(match['awayTeam']['name'])
        home_score = match['score']['fullTime'].get('home')
        away_score = match['score']['fullTime'].get('away')
        processed_data['Home Score'].append(home_score if home_score is not None else '')
        processed_data['Away Score'].append(away_score if away_score is not None else '')

        for team in [match['homeTeam'], match['awayTeam']]:
            if team['id'] not in teams_seen:
                teams_seen.add(team['id'])
                teams_data['Team ID'].append(team['id'])
                teams_data['Name'].append(team['name'])
                teams_data['Short Name'].append(team['shortName'])
                teams_data['Crest'].append(team['crest'])
                teams_data['Coach Name'].append(team['coach']['name'])

    matches_df = pd.DataFrame(processed_data)
    teams_df = pd.DataFrame(teams_data)
    return matches_df, teams_df

def fetch_standings_data():
    url = f'{BASE_URL}competitions/PL/standings'
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(url, headers=headers)
    print(f"Fetching Premier League standings: {response.status_code}")
    if response.status_code != 200:
        print(f"Error fetching Premier League standings: {response.status_code}")
        return pd.DataFrame()
    data = response.json()
    standings = data.get('standings', [])[0].get('table', [])
    print(f"Fetched {len(standings)} standings")

    standings_data = {
        'Position': [],
        'Team': [],
        'Played Games': [],
        'Won': [],
        'Draw': [],
        'Lost': [],
        'Points': [],
        'Goals For': [],
        'Goals Against': [],
        'Goal Difference': []
    }

    for team in standings:
        standings_data['Position'].append(team['position'])
        standings_data['Team'].append(team['team']['name'])
        standings_data['Played Games'].append(team['playedGames'])
        standings_data['Won'].append(team['won'])
        standings_data['Draw'].append(team['draw'])
        standings_data['Lost'].append(team['lost'])
        standings_data['Points'].append(team['points'])
        standings_data['Goals For'].append(team['goalsFor'])
        standings_data['Goals Against'].append(team['goalsAgainst'])
        standings_data['Goal Difference'].append(team['goalDifference'])

    standings_df = pd.DataFrame(standings_data)
    print(standings_df.head())  # Print the first few rows of the DataFrame for debugging
    return standings_df

def main():
    matches_df, teams_df = fetch_premier_league_data()
    standings_df = fetch_standings_data()
    if not matches_df.empty:
        matches_df.to_csv('premier_league_data.csv', index=False)
        print('Matches data saved to premier_league_data.csv')
    if not teams_df.empty:
        teams_df.to_csv('teams_data.csv', index=False)
        print('Teams data saved to teams_data.csv')
    if not standings_df.empty:
        standings_df.to_csv('standings_data.csv', index=False)
        print('Standings data saved to standings_data.csv')

if __name__ == '__main__':
    main()