import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Fetch data
matches_df = pd.read_csv('premier_league_data.csv')
teams_df = pd.read_csv('teams_data.csv')
daily_standings_df = pd.read_csv('daily_standings.csv')
standings_df = pd.read_csv('standings_data.csv')

# Create a Dash application
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Create a Plotly figure
fig = px.line(daily_standings_df, x='Date', y='Position', title='Premier League Positions', range_y=[20, 1])

# Define the layout of the app
app.layout = html.Div(style={'font-family': 'Arial, Helvetica, sans-serif'}, children=[
    html.H1(children='Premier League Dashboard'),

    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'flex': '25%', 'padding': '10px'}, children=[
            html.H2(children='Teams'),
            html.Table([
                html.Thead(
                    html.Tr([html.Th('Team'), html.Th('Crest')])
                ),
                html.Tbody([
                    html.Tr(id=row['Name'], children=[
                        html.Td(row['Name']),
                        html.Td(html.Img(src=row['Crest'], style={'width': '50px', 'height': '50px'}))
                    ]) for _, row in teams_df.iterrows()
                ])
            ], style={'border': 'none', 'width': '100%'})
        ]),
        html.Div(style={'flex': '75%', 'padding': '10px'}, children=[
            dcc.Graph(
                id='example-graph',
                figure=fig
            ),

            html.Div(style={'display': 'flex'}, children=[
                html.Div(style={'flex': '50%'}, children=[
                    html.H2(children='Standings'),
                    html.Table([
                        html.Thead(
                            html.Tr([html.Th(col) for col in standings_df.columns])
                        ),
                        html.Tbody([
                            html.Tr([
                                html.Td(standings_df.iloc[i][col]) for col in standings_df.columns
                            ]) for i in range(len(standings_df))
                        ])
                    ])
                ]),
                html.Div(style={'flex': '50%'}, children=[
                    html.H2(children='Results'),
                    html.Div(id='results-table')
                ])
            ])
        ])
    ])
])

# Callback to update the graph and results table based on the selected team
@app.callback(
    [Output('example-graph', 'figure'),
     Output('results-table', 'children')],
    [Input(row['Name'], 'n_clicks') for _, row in teams_df.iterrows()]
)
def update_graph_and_table(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return fig, html.Table()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        filtered_standings_df = daily_standings_df[daily_standings_df['Team'] == button_id]
        filtered_standings_df = filtered_standings_df.sort_values(by='Date')
        new_fig = px.line(filtered_standings_df, x='Date', y='Position', title=f'{button_id} League Position', range_y=[20, 1])

        filtered_matches_df = matches_df[(matches_df['Home Team'] == button_id) | (matches_df['Away Team'] == button_id)]
        filtered_matches_df = filtered_matches_df.sort_values(by='Date')

        table_header = [
            html.Thead(html.Tr([html.Th(col) for col in filtered_matches_df.columns]))
        ]
        table_body = [
            html.Tbody([
                html.Tr([
                    html.Td(filtered_matches_df.iloc[i][col]) for col in filtered_matches_df.columns
                ]) for i in range(len(filtered_matches_df))
            ])
        ]
        table = html.Table(table_header + table_body)

        return new_fig, table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)