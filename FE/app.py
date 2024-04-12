# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests as r
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
from datetime import datetime

app = Dash(__name__)
#%%
all_data_url="http://localhost:8080/cities-pollution-all-historical-data"
res = r.get(all_data_url)
df = pd.DataFrame(res.json())
#%%
index_col= ['pm2_5',
 'pm10',
 'aqi',
 'co',
 'no',
 'no2',
 'o3',
 'so2',
 'nh3',]
#%%

# PM10 mean per city
city_mean = df[index_col+['city']].groupby('city').mean()

# Select first 5 cities with highest col param
def order_by_col(col_name:str)->pd.DataFrame:
    return city_mean.sort_values(col_name,ascending=False)[col_name].head(5)


# Personalized style
colors = {
    'background': '#f2f2f2',
    'text': '#333333',
    'accent': '#3498db'
}

# Layout dell'app
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '50px'}, children=[
    html.H1(children='Air quality analysis', style={'color': colors['accent'], 'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}),

    html.Div([
        html.H3(children='Top 10 cities for PM10 presence', style={'color': colors['text'], 'fontFamily': 'Arial, sans-serif'}),
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=df['date'].min(),
            max_date_allowed=df['date'].max(),
            initial_visible_month=df['date'].max(),
            date=df['date'].max()
        ),

        dcc.Graph(id='top-10-pm10-graph')
    ], style={'marginBottom': '50px'}),
                html.Hr(style={'borderWidth': "0.3vh", "color": "#FEC700"}),

    html.Div([
        html.H3(children='PM10 trend per city', style={'color': colors['text'], 'fontFamily': 'Arial, sans-serif'}),
        html.Label('Select a city:', style={'color': colors['text'], 'fontFamily': 'Arial, sans-serif'}),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in df['city'].unique()],
            value=df['city'].unique()[0]
        ),

        dcc.Graph(id='pm10-line-chart')
    ]),

                html.Hr(style={'borderWidth': "0.3vh", "color": "#FEC700"}),

html.Div([
        dcc.Graph(
            id='top-5-pm2.5-average-graph',
            figure={
                'data': [
                    {'x': order_by_col(index_col[0]).index, 'y': order_by_col(index_col[0]).values, 'type': 'bar', 'marker': {'color': colors['accent']}}
                ],
                'layout': {
                    'title': 'Top 5 cities per PM 2.5 (Average)',
                    'xaxis': {'title': 'city'},
                    'yaxis': {'title': 'Average PM2.5'}
                }
            }
        ) ],style={'width': '50%', 'display': 'inline-block','border':'10px'}),
           html.Div([     dcc.Graph(
            id='top-5-pm10-average-graph',
            figure={
                'data': [
                    {'x': order_by_col(index_col[1]).index, 'y': order_by_col(index_col[1]).values, 'type': 'bar', 'marker': {'color': colors['accent']}}
                ],
                'layout': {
                    'title': 'Top 5 cities per PM10 (Average)',
                    'xaxis': {'title': 'city'},
                    'yaxis': {'title': 'Average PM10'}
                }
            }
        )
           ],style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([     dcc.Graph(
            id='top-5-o3-average-graph',
            figure={
                'data': [
                    {'x': order_by_col(index_col[6]).index, 'y': order_by_col(index_col[6]).values, 'type': 'bar', 'marker': {'color': colors['accent']}}
                ],
                'layout': {
                    'title': 'Top 5 cities per 03 (Average)',
                    'xaxis': {'title': 'city'},
                    'yaxis': {'title': 'Average 03'}
                }
            }
        )
           ],style={'width': '50%', 'display': 'inline-block'}),

            html.Div([     dcc.Graph(
            id='top-5-NO2-average-graph',
            figure={
                'data': [
                    {'x': order_by_col(index_col[5]).index, 'y': order_by_col(index_col[5]).values, 'type': 'bar', 'marker': {'color': colors['accent']}}
                ],
                'layout': {
                    'title': 'Top 5 cities per NO2 (Average)',
                    'xaxis': {'title': 'city'},
                    'yaxis': {'title': 'Average NO2'}
                }
            }
        )
           ],style={'width': '50%', 'display': 'inline-block'}),
  
            html.Hr(style={'borderWidth': "0.3vh", "color": "#FEC700"})


        
    
])



@app.callback(
    Output('top-10-pm10-graph', 'figure'),
    [Input('date-picker', 'date')]
)
def update_figure(selected_date):
    #selected_date = datetime.strptime(selected_date, '%Y-%m-%d')

    # Filtra il DataFrame per la data selezionata
    filtered_df = df[df['date'] == selected_date]

    # Seleziona le prime 10 città per PM10
    top_10_cities_pm10 = filtered_df.sort_values(by='pm10', ascending=False).head(10)

    # Crea il grafico
    figure = {
        'data': [
            {'x': top_10_cities_pm10['city'], 'y': top_10_cities_pm10['pm10'], 'type': 'bar', 'name': 'PM10'}
        ],
         'layout': {
            'title': f'Selected date: {selected_date}',
            'xaxis': {'title': 'City', 'tickfont': {'family': 'Roboto, sans-serif'}, 'color': colors['text']},
            'yaxis': {'title': 'PM10', 'tickfont': {'family': 'Roboto, sans-serif'}, 'color': colors['text']},
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {'color': colors['text'], 'family': 'Roboto, sans-serif'}
        }
    }

    return figure

@app.callback(
    Output('pm10-line-chart', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_line_chart(selected_city):
    # Filter dataframe per city
    filtered_df = df[df['city'] == selected_city]

    # Create line chart
    figure = {
        'data': [
            {'x': filtered_df['date'], 'y': filtered_df['pm10'], 'type': 'line', 'name': 'PM10'}
        ],
         'layout': {
            'title': f'Trend of PM10 over time in: {selected_city}',
            'xaxis': {'title': 'Data', 'tickfont': {'family': 'Roboto, sans-serif'}, 'color': colors['text']},
            'yaxis': {'title': 'PM10', 'tickfont': {'family': 'Roboto, sans-serif'}, 'color': colors['text']},
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {'color': colors['text'], 'family': 'Roboto, sans-serif'}
        }
    }

    return figure

if __name__ == '__main__':
    app.run(debug=True,port=8080)
