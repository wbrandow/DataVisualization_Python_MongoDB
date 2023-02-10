from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
from dash import dcc, html, dash_table
import plotly.express as px
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

from animal_shelter import AnimalShelter

###########################
# Data Manipulation / Model
###########################

username = 'aacuser'
password = '96724_Two!'
shelter = AnimalShelter(username, password)

# class read method must support return of cursor object and accept projection json input
df = pd.DataFrame.from_records(shelter.read())

#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    dcc.Dropdown(
        options=[
            {'label': 'Water Rescue', 'value': 'Water Rescue'},
            {'label': 'Mountain Rescue', 'value': 'Mountain Rescue'},
            {'label': 'Disaster Rescue', 'value': 'Disaster Rescue'},
            {'label': 'Reset', 'value': 'Reset'}
        ],
        value='Reset',
        id='rescue_type'
    ),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {'name': i, 'id': i, 'deletable': False, 'selectable': True} for i in df.columns
        ],
        data=df.to_dict('records'),
        sort_action='native',
        sort_mode='multi',
        filter_action='native',
        row_selectable='single',
        selected_rows=[],
        page_action='native',
        page_current=0,
        page_size=10,
        style_table={'overflowX': 'scroll'}
    ),
    html.Br(),
    html.Hr(),
    html.Div(
        className='col s12 m6',
        children=dl.Map(
            id='map-id',
            style={'width': '1000px', 'height': '500px'},
            center=[30, -97],
            zoom=10,
            children=[
                dl.TileLayer(id="base-layer-id"),
                # Marker with tool tip and popup
                dl.Marker(
                    id='marker-id',
                    position=[30, -97],
                    children=[
                        dl.Tooltip(id='breed'),
                        dl.Popup([
                            html.H1("Animal Name"),
                            html.P(id='name')
                        ])
                    ]
                )
            ]
        )
    )
])


#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(
    [Output('breed', 'children'),
     Output('name', 'children')],
    [Input('datatable-id', 'derived_viewport_data'),
     Input('datatable-id', 'selected_rows')]
)
def update_map(viewData, selected_rows):
    dff = pd.DataFrame.from_dict(viewData)

    # get info for selected animal
    if selected_rows:
        name = dff.iloc[selected_rows]['name']
        breed = dff.iloc[selected_rows]['breed']
        lat = dff.iloc[selected_rows]['location_lat']
        long = dff.iloc[selected_rows]['location_long']
    else:
        name = dff.iloc[0]['name']
        breed = dff.iloc[0]['breed']
        lat = dff.iloc[0]['location_lat']
        long = dff.iloc[0]['location_long']

    center = [lat, long]
    position = [lat, long]

    return [
        breed,
        name
    ]


@app.callback(
    Output('datatable-id', 'data'),
    [Input('rescue_type', 'value')]
)
def update_data_table(rescue_type):
    # Water Rescue selected
    if rescue_type == 'Water Rescue':
        query_result_df = pd.DataFrame.from_records(shelter.read({
            '$and': [
                # age between 26 and 156 weeks
                {'$and': [
                    {'age_upon_outcome_in_weeks': {'$gte': 26}},
                    {'age_upon_outcome_in_weeks': {'$lte': 156}}
                ]},
                # preferred breeds
                {'$or': [
                    {'breed': 'Labrador Retriever Mix'},
                    {'breed': 'Chesapeake Bay Retriever'},
                    {'breed': 'Newfoundland'}
                ]},
                # preferred sex
                {'sex_upon_outcome': 'Intact Female'}
            ]
        }))
    # Mountain Rescue selected
    elif rescue_type == 'Mountain Rescue':
        query_result_df = pd.DataFrame.from_records(shelter.read({
            '$and': [
                # age between 26 and 156 weeks
                {'$and': [
                    {'age_upon_outcome_in_weeks': {'$gte': 26}},
                    {'age_upon_outcome_in_weeks': {'$lte': 156}}
                ]},
                # preferred breeds
                {'$or': [
                    {'breed': 'German Shepherd'},
                    {'breed': 'Alaskan Malamute'},
                    {'breed': 'Old English Sheepdog'},
                    {'breed': 'Siberian Husky'},
                    {'breed': 'Rottweiler'}
                ]},
                # preferred sex
                {'sex_upon_outcome': 'Intact Male'}
            ]
        }))
        # Disaster Rescue selected
    elif rescue_type == 'Disaster Rescue':
        query_result_df = pd.DataFrame.from_records(shelter.read({
            '$and': [
                # age between 20 and 300 weeks
                {'$and': [
                    {'age_upon_outcome_in_weeks': {'$gte': 20}},
                    {'age_upon_outcome_in_weeks': {'$lte': 300}}
                ]},
                # preferred breeds
                {'$or': [
                    {'breed': 'German Shepherd'},
                    {'breed': 'Doberman Pinscher'},
                    {'breed': 'Golden Retriever'},
                    {'breed': 'Bloodhound'},
                    {'breed': 'Rottweiler'}
                ]},
                # preferred sex
                {'sex_upon_outcome': 'Intact Male'}
            ]
        }))
    # reset to non-filtered view
    elif rescue_type == 'Reset':
        query_result_df = pd.DataFrame.from_records(shelter.read())

    return query_result_df.to_dict('records')


app
