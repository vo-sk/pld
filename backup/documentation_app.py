import dash  # Imports Dash for creating web applications
from dash import dcc, html  # Imports components from Dash
from dash.dependencies import Input, Output  # Imports dependencies for callbacks
import plotly.express as px  # Imports Plotly Express for data visualization
import pandas as pd  # Imports pandas for data manipulation

# Fetch data
matches_df = pd.read_csv('premier_league_data.csv')  # Reads match data from CSV
teams_df = pd.read_csv('teams_data.csv')  # Reads team data from CSV
daily_standings_df = pd.read_csv('daily_standings.csv')  # Reads daily standings data from CSV
standings_df = pd.read_csv('standings_data.csv')  # Reads standings data from CSV

# Rename "Played Games" to "P" in the standings DataFrame
standings_df = standings_df.rename(columns={"Played Games": "P"})  # Renames column for brevity

# Create a Dash application
app = dash.Dash(__name__)  # Initializes the Dash app
app.config.suppress_callback_exceptions = True  # Suppresses callback exceptions for dynamic components

# Create a Plotly figure
fig = px.line(daily_standings_df, x='Date', y='Position', title='Premier League Positions', range_y=[20, 1])  # Creates a line chart

# Define the layout of the app
app.layout = html.Div(style={'font-family': 'Arial, Helvetica, sans-serif'}, children=[
    html.H1(children='Premier League Dashboard'),  # Adds a title

    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'flex': '30%', 'padding': '10px'}, children=[
            html.H2(children='Teams'),
            html.Table([
                html.Thead(
                    html.Tr([html.Th('Team', style={'width': '70%'}), html.Th('Crest')])  # Table headers
                ),
                html.Tbody([
                    html.Tr(id=row['Name'], children=[
                        html.Td(row['Name'], style={'width': '70%'}),  # Team name column
                        html.Td(html.Img(src=row['Crest'], style={'width': '50px', 'height': '50px'}))  # Team crest column
                    ]) for _, row in teams_df.iterrows()  # Iterates over team data to create rows
                ])
            ], style={'border': 'none', 'width': '100%'})  # Styles the table
        ]),
        html.Div(style={'flex': '70%', 'padding': '10px'}, children=[
            dcc.Graph(
                id='example-graph',
                figure=fig  # Displays the line chart
            ),

            html.Div(style={'display': 'flex'}, children=[
                html.Div(style={'flex': '50%'}, children=[
                    html.H2(children='Standings'),
                    html.Table(id='standings-table')  # Placeholder for standings table
                ]),
                html.Div(style={'flex': '50%'}, children=[
                    html.H2(children='Results'),
                    html.Div(id='results-table')  # Placeholder for results table
                ])
            ])
        ])
    ])
])

# Callback to update the graph, standings table, and results table based on the selected team
@app.callback(
    [Output('example-graph', 'figure'),
     Output('standings-table', 'children'),
     Output('results-table', 'children')],
    [Input(row['Name'], 'n_clicks') for _, row in teams_df.iterrows()]  # Creates dynamic inputs for each team
)
def update_graph_and_table(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        standings_table = html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in standings_df.columns])  # Table headers
            ),
            html.Tbody([
                html.Tr([
                    html.Td(standings_df.iloc[i][col]) for col in standings_df.columns  # Table rows
                ]) for i in range(len(standings_df))
            ])
        ])
        return fig, standings_table, html.Table()  # Returns initial empty tables if no team is selected
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]  # Identifies the triggered button
        filtered_standings_df = daily_standings_df[daily_standings_df['Team'] == button_id]  # Filters data for the selected team
        filtered_standings_df = filtered_standings_df.sort_values(by='Date')  # Sorts data by date
        new_fig = px.line(filtered_standings_df, x='Date', y='Position', title=f'{button_id} League Position', range_y=[20, 1])  # Creates a new line chart

        filtered_matches_df = matches_df[(matches_df['Home Team'] == button_id) | (matches_df['Away Team'] == button_id)]  # Filters match data for the selected team
        filtered_matches_df = filtered_matches_df.sort_values(by='Date')  # Sorts data by date

        table_header = [
            html.Thead(html.Tr([html.Th(col) for col in filtered_matches_df.columns]))  # Table headers for match results
        ]
        table_body = [
            html.Tbody([
                html.Tr([
                    html.Td(filtered_matches_df.iloc[i][col]) for col in filtered_matches_df.columns  # Table rows for match results
                ]) for i in range(len(filtered_matches_df))
            ])
        ]
        results_table = html.Table(table_header + table_body)  # Combines header and body for the results table

        standings_table = html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in standings_df.columns])  # Table headers for standings
            ),
            html.Tbody([
                html.Tr(style={'background-color': 'yellow'} if standings_df.iloc[i]['Team'] == button_id else {}, children=[
                    html.Td(standings_df.iloc[i][col]) for col in standings_df.columns  # Highlights the selected team's row in standings
                ]) for i in range(len(standings_df))
            ])
        ])

        return new_fig, standings_table, results_table  # Returns the updated figures and tables

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)  # Runs the Dash app
