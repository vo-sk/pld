import requests  # Imports the requests library to make HTTP requests
import pandas as pd  # Imports the pandas library for data manipulation

API_KEY = '2b09ddc1a88d428d8b9c7d2fa34754cb'  # Replace with your actual API key
BASE_URL = 'https://api.football-data.org/v4/'  # Base URL for the football data API

def fetch_premier_league_data():
    url = f'{BASE_URL}competitions/PL/matches?dateFrom=2024-08-16&dateTo=2025-01-16'  # URL to fetch match data
    headers = {'X-Auth-Token': API_KEY}  # Headers including the API key for authentication
    response = requests.get(url, headers=headers)  # Makes the HTTP GET request to fetch data
    print(f"Fetching Premier League data: {response.status_code}")  # Prints the status of the request
    if response.status_code != 200:
        print(f"Error fetching Premier League data: {response.status_code}")  # Error message if request fails
        return pd.DataFrame(), pd.DataFrame()  # Returns empty dataframes in case of error
    data = response.json()  # Converts the response to JSON format
    matches = data.get('matches', [])  # Extracts the 'matches' field from the JSON data
    print(f"Fetched {len(matches)} matches")  # Prints the number of matches fetched

    # Initializes dictionaries to store processed match and team data
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

    teams_seen = set()  # A set to keep track of seen teams

    for match in matches:
        processed_data['Date'].append(match['utcDate'])  # Adds the match date
        processed_data['Home Team'].append(match['homeTeam']['name'])  # Adds the home team name
        processed_data['Away Team'].append(match['awayTeam']['name'])  # Adds the away team name
        home_score = match['score']['fullTime'].get('home')  # Gets the home team score
        away_score = match['score']['fullTime'].get('away')  # Gets the away team score
        processed_data['Home Score'].append(home_score if home_score is not None else '')  # Adds home score
        processed_data['Away Score'].append(away_score if away_score is not None else '')  # Adds away score

        for team in [match['homeTeam'], match['awayTeam']]:
            if team['id'] not in teams_seen:
                teams_seen.add(team['id'])  # Adds team ID to the set of seen teams
                teams_data['Team ID'].append(team['id'])  # Adds team ID
                teams_data['Name'].append(team['name'])  # Adds team name
                teams_data['Short Name'].append(team['shortName'])  # Adds team short name
                teams_data['Crest'].append(team['crest'])  # Adds team crest URL
                teams_data['Coach Name'].append(team['coach']['name'])  # Adds team coach name

    # Converts the dictionaries to dataframes
    matches_df = pd.DataFrame(processed_data)
    teams_df = pd.DataFrame(teams_data)
    return matches_df, teams_df  # Returns the dataframes

def fetch_standings_data():
    url = f'{BASE_URL}competitions/PL/standings'  # URL to fetch standings data
    headers = {'X-Auth-Token': API_KEY}  # Headers including the API key for authentication
    response = requests.get(url, headers=headers)  # Makes the HTTP GET request to fetch data
    print(f"Fetching Premier League standings: {response.status_code}")  # Prints the status of the request
    if response.status_code != 200:
        print(f"Error fetching Premier League standings: {response.status_code}")  # Error message if request fails
        return pd.DataFrame()  # Returns an empty dataframe in case of error
    data = response.json()  # Converts the response to JSON format
    standings = data.get('standings', [])[0].get('table', [])  # Extracts the 'standings' table from the JSON data
    print(f"Fetched {len(standings)} standings")  # Prints the number of standings fetched

    # Initializes a dictionary to store processed standings data
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
        standings_data['Position'].append(team['position'])  # Adds team position
        standings_data['Team'].append(team['team']['name'])  # Adds team name
        standings_data['Played Games'].append(team['playedGames'])  # Adds number of games played
        standings_data['Won'].append(team['won'])  # Adds number of games won
        standings_data['Draw'].append(team['draw'])  # Adds number of games drawn
        standings_data['Lost'].append(team['lost'])  # Adds number of games lost
        standings_data['Points'].append(team['points'])  # Adds number of points
        standings_data['Goals For'].append(team['goalsFor'])  # Adds number of goals scored
        standings_data['Goals Against'].append(team['goalsAgainst'])  # Adds number of goals conceded
        standings_data['Goal Difference'].append(team['goalDifference'])  # Adds goal difference

    standings_df = pd.DataFrame(standings_data)  # Converts the dictionary to a dataframe
    print(standings_df.head())  # Prints the first few rows of the dataframe for debugging
    return standings_df  # Returns the dataframe

def main():
    matches_df, teams_df = fetch_premier_league_data()  # Calls the function to fetch match data
    standings_df = fetch_standings_data()  # Calls the function to fetch standings data
    if not matches_df.empty:
        matches_df.to_csv('premier_league_data.csv', index=False)  # Saves match data to CSV
        print('Matches data saved to premier_league_data.csv')  # Confirmation message
    if not teams_df.empty:
        teams_df.to_csv('teams_data.csv', index=False)  # Saves team data to CSV
        print('Teams data saved to teams_data.csv')  # Confirmation message
    if not standings_df.empty:
        standings_df.to_csv('standings_data.csv', index=False)  # Saves standings data to CSV
        print('Standings data saved to standings_data.csv')  # Confirmation message

if __name__ == '__main__':
    main()  # Runs the main function if the script is executed
