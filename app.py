# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import functions_app as fa
import plots as pl
from datetime import datetime as dt
import requests
import json
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


def get_station_dict():
    availiblestations = json.loads(requests.get('https://dataset.api.hub.zamg.ac.at/v1/station/historical/klima-v1-1d/metadata').content)["stations"]

    station_dict = {}
    for dicti in availiblestations:
        station_dict[dicti['id']] = ', '.join([dicti['name'],dicti['state']])

    return station_dict
station_dictioniary = get_station_dict()

app.layout = html.Div([
    html.H1("Elisabeth's Weather App", style={'textAlign': 'center'}),
    html.Div([
    'Pick a date range: ',
    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        #calendar_orientation='horizontal',  # vertical or horizontal
        #day_size=39,  # size of calendar image. Default is 39
        end_date_placeholder_text="Return",  # text that appears when no end date chosen
        with_portal=False,  # if True calendar will open in a full screen overlay portal
        first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
        reopen_calendar_on_clear=True,
        is_RTL=False,  # True or False for direction of calendar
        clearable=True,  # whether or not the user can clear the dropdown
        number_of_months_shown=2,  # number of months shown when calendar is open
        min_date_allowed=dt(2015, 1, 1),  # minimum date allowed on the DatePickerRange component
        max_date_allowed=dt.now().date(),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=dt.now().date(),  # the month initially presented when the user opens the calendar
        start_date=dt(2020, 12, 4).date(),
        end_date=dt.now().date(),
        display_format='D/M/YYYY',  # how selected dates are displayed in the DatePickerRange component.
        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
        #minimum_nights=2,  # minimum number of days between start and end date

        persistence=True,
        persisted_props=['start_date'],
        persistence_type='session',  # session, local, or memory. Default is 'local'

        updatemode='bothdates',  # singledate or bothdates. Determines when callback is triggered
        style={'display': 'inline-block' }
    )]),
    # html.Br(),
    #     html.Label('Text Input'),
    #     dcc.Input(value='5904', type='text'),
        
    html.Div([
        "station ID: ",
        dcc.Input(id='my-input', value='5904', type='text',debounce=True,style={'display': 'inline-block'})
    ]),
    html.Br(),
    html.Div(id='my-output'),

    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download-dataframe-csv"),

    #html.H3("Elisabeth's Weather App", style={'textAlign': 'center'}),
    dcc.Graph(id='mymap'),

    
    
    
])



@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('my-input', 'value')
    ],
    prevent_initial_call=True,
)
def func(n_clicks,start_date, end_date, value):
    if n_clicks is None:
        raise PreventUpdate
    elif value not in station_dictioniary:
        raise ValueError('station not in list')
    else:
        zamg = fa.Zamg_Data(start_date,end_date,station = value)
        data = zamg.zamg_data()
        name = station_dictioniary[value]
        return dcc.send_data_frame(data.to_csv, f"weather_{name}.csv")

@app.callback(
    Output('mymap', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('my-input', 'value')]
)
def update_output(start_date, end_date, value):
    if value not in station_dictioniary:
        zamg = fa.Zamg_Data(start_date,end_date)
    else:
        zamg = fa.Zamg_Data(start_date,end_date,station = value)
    data = zamg.zamg_data()

    fig = pl.subplots(data)
    return fig


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    if input_value in station_dictioniary:
        return f'station: {station_dictioniary[str(input_value)]}'
    else:
        return 'station ID not found, return to default "WIEN-HOHE WARTE, Wien"'



if __name__ == '__main__':
    app.run_server(debug=True)
