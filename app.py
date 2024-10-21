from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objs as go
from datetime import datetime, timedelta
from sklearn.ensemble import AdaBoostRegressor
import warnings
import json
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the trained model
model = joblib.load('models/model.pkl')

# Load the future data for prediction
future_data1 = pd.read_csv('data/afcon.csv')

# Get the required columns for prediction
prediction_features = ['home_score', 'away_score', 'goal_difference', 'neutral']
future_data = future_data1[prediction_features]

# Make predictions on the future data
predictions = model.predict(future_data)

# Add the 'winner' column to the future_data DataFrame
future_data['winner'] = predictions

# Get the names of the home and away teams from the original future_data DataFrame
team_names = future_data1.merge(
    pd.DataFrame(future_data.index),
    left_index=True,
    right_index=True
)[['date', 'home_team', 'away_team']]

# Replace values in the 'winner' column based on the specified conditions
future_data.loc[future_data['winner'] == 2, 'winner'] = team_names['away_team']
future_data.loc[future_data['winner'] == 1, 'winner'] = team_names['home_team']
future_data.loc[future_data['winner'] == 0, 'winner'] = 'Draw'

output = pd.concat([future_data, team_names], axis=1)

# Rearrange the columns
column_order = ['date', 'home_team', 'home_score', 'away_score', 'away_team', 'winner']
output = output[column_order]

# Count the occurrences of each team in the 'winner' column, excluding 'Draw' values
winner_counts = future_data.loc[future_data['winner'] != 'Draw', 'winner'].value_counts()

# Get all unique team names from the 'winner' column
all_teams = pd.unique(future_data['winner'])

# Create a DataFrame with the team names and their counts
team_counts = pd.DataFrame({'Team': winner_counts.index, 'Wins': winner_counts.values})

# Sort the DataFrame in descending order based on the number of wins
team_counts = team_counts.sort_values('Wins', ascending=False)

# Reset the index of the DataFrame and set it to start counting from 1
team_counts.index = range(1, len(team_counts) + 1)

# Calculate the total number of appearances for each team
total_appearances = output['home_team'].value_counts() + output['away_team'].value_counts()

# Calculate the Win Rate (%) for each team
team_counts['Appearances'] = total_appearances[team_counts['Team']].values
team_counts['Win Rate (%)'] = round((team_counts['Wins'] / team_counts['Appearances']) * 100, 2)

# Calculate the weighted average Win Rate (%)
max_appearances = team_counts['Appearances'].max()
team_counts['Weighted Win Rate (%)'] = round(((team_counts['Wins'] / team_counts['Appearances']) * (team_counts['Appearances'] / max_appearances)) * 100, 2)

# Sort the DataFrame in descending order based on the Weighted Win Rate (%)
team_counts = team_counts.sort_values('Weighted Win Rate (%)', ascending=False)

# Reset the index of the DataFrame and set it to start counting from 1
team_counts.index = range(1, len(team_counts) + 1)

# Create a new instance of the AdaBoostRegressor class
model = AdaBoostRegressor()

# Set the start date and end date for the forecast
years = 30
start_date = datetime.now().replace(day=1, month=1) + timedelta(days=365)
end_date = datetime.strptime(output['date'].max(), '%Y-%m-%d') + timedelta(days=365 * years)

# Create a date range between the start date and end date with a frequency of 1 month
date_range = pd.date_range(start=start_date, end=end_date, freq='MS')

# Create an empty DataFrame to store the forecasted values
forecast = pd.DataFrame(index=date_range)

# Iterate over each team in the team_counts DataFrame
for team in team_counts['Team']:
    # Get the historical data for the current team
    historical_data = output.loc[(output['home_team'] == team) | (output['away_team'] == team)]
    
    # Convert the 'date' column to a datetime object
    historical_data['date'] = pd.to_datetime(historical_data['date'])
    
    # Set the 'date' column as the index of the DataFrame
    historical_data = historical_data.set_index('date')
    
    # Resample the historical data to a monthly frequency and count the number of wins for each month
    historical_data = historical_data.resample('MS')['winner'].apply(lambda x: (x == team).sum())
    
    # Check if there are at least two values in the historical data
    if len(historical_data) > 1:
        # Create a DataFrame with the historical data and a column of ones
        X = pd.DataFrame({'ones': 1, 'x': range(len(historical_data))})
        y = historical_data.values
        
        # Fit a random forest regressor to the historical data
        model = AdaBoostRegressor()
        model.fit(X, y)

        # Create a DataFrame with the date range and a column of ones
        X_new = pd.DataFrame({'ones': 1, 'x': range(len(date_range))})
        
        # Forecast the number of wins for each month in the date range
        forecast[team] = model.predict(X_new)
    else:
        # Set all forecasted values to zero if there are not enough observations
        forecast[team] = 0

@app.route('/')
def index():
    # Create a list of years from 2024 to 2050
    years = list(range(2024, 2051))

    # Set the start year to the first year in the list of years
    start_year = years[0]

    # Create an HTML view of the year slider
    year_slider_html = f'<input type="range" min="{years[0]}" max="{years[-1]}" value="{years[0]}" class="slider" id="year-slider">'

    # Create an HTML view for the forecast line chart
    forecast_fig_html = '<div id="forecast-fig"></div>'

    # Create an HTML view for the team wins bubble map
    team_wins_fig_html = '<div id="team-wins-fig"></div>'

    # Create an HTML view for the top countries table
    top_countries_html = '<div id="top-countries-table"></div>'

    return render_template('index.html', years=years, year_slider_html=year_slider_html,
                           forecast_fig_html=forecast_fig_html, team_wins_fig_html=team_wins_fig_html,
                           top_countries_html=top_countries_html)

@app.route('/update_dashboard')
def update_dashboard():
    year = int(request.args.get('year'))
    years = list(range(2024, 2051))
    
    # Calculate the end date for the forecast based on the selected year
    start_year = years[0]
    end_date = start_date + timedelta(days=365 * (year - start_year))
    
    # Filter the forecast DataFrame based on the end date
    forecast_filtered = forecast.loc[forecast.index <= end_date]
    
    # Sum the forecasted wins for each team
    total_wins = forecast_filtered.sum()

    # Create a DataFrame with the team names and their forecasted wins
    team_wins = pd.DataFrame({'Team': total_wins.index, 'Wins': total_wins.values})

    # Sort the DataFrame in descending order based on the number of wins
    team_wins = team_wins.sort_values('Wins', ascending=False)

    # Reset the index of the DataFrame and set it to start counting from 1
    team_wins.reset_index(drop=True, inplace=True)
    team_wins.index += 1

    # Create a list of traces for the forecast line chart
    forecast_traces = []
    excluded_teams = ['Rwanda', 'Equatorial Guinea', 'Zimbabwe', 'Cape Verde', 'Madagascar']
    for col in forecast_filtered.columns:
        if col not in excluded_teams:
            trace = go.Scatter(x=forecast_filtered.index, y=forecast_filtered[col], name=col)
            forecast_traces.append(trace)
    
    # Create a trace for the team wins bubble map
    team_wins_trace = go.Scattergeo(
        locations=team_wins.loc[~team_wins['Team'].isin(excluded_teams), 'Team'],
        locationmode='country names',
        marker=dict(
            size=team_wins.loc[~team_wins['Team'].isin(excluded_teams), 'Wins'],
            sizemode='diameter',
            color=team_wins.loc[~team_wins['Team'].isin(excluded_teams), 'Wins'],
            colorscale='Viridis',
            showscale=True
        ),
        text=team_wins.loc[~team_wins['Team'].isin(excluded_teams), 'Team'] + ': ' + team_wins.loc[~team_wins['Team'].isin(excluded_teams), 'Wins'].round().astype(int).astype(str) + ' Wins',
        hoverinfo='text'
    )
    
    top_countries = team_wins.loc[~team_wins['Team'].isin(excluded_teams)].head(5)
    top_countries.insert(0, 'Rank', range(1, len(top_countries) + 1))
    top_countries['Wins'] = top_countries['Wins'].round().astype(int)
    top_countries_html = '<table style="width:95%;height:500px;text-align:center"><tr style="background-color:#00008b;color:white"><th style="text-align:center">RANK</th><th style="text-align:center">TEAM</th><th style="text-align:center">WINS</th></tr>' + ''.join(['<tr class="table-row"><td class="table-cell" style="text-align:center">{}</td><td class="table-cell" style="text-align:center">{}</td><td class="table-cell" style="text-align:center">{}</td></tr>'.format(row['Rank'], row['Team'], row['Wins']) for _, row in top_countries.iterrows()]) + '</table>'

    def default(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return str(obj)

    return jsonify({
        'forecast_traces': [json.loads(json.dumps(trace.to_plotly_json(), default=default)) for trace in forecast_traces],
        'team_wins_trace': json.loads(json.dumps(team_wins_trace.to_plotly_json(), default=default)),
        'top_countries_html': top_countries_html
    })

if __name__ == '__main__':
    app.run(debug=True)
