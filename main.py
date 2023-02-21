# Author: William Brandow
# Date: 2023-02-21

from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from dash.dependencies import Input, Output, State

import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps
import base64
from animal_shelter import AnimalShelter


###########################
# Data Manipulation / Model
###########################

username = 'aacuser'
password = '96724_Two!'
shelter = AnimalShelter(username, password)


# class read method must support return of cursor object 
df = pd.DataFrame.from_records(shelter.read())


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

# Grazioso Salvare’s logo
image_filename = 'Grazioso_Salvare_Logo.png' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Img(
        src='data:image/png;base64,{}'.format(encoded_image.decode()), 
        style={'width': '20%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}
    ),
    html.Center(html.B(html.H3('William Brandow'))),
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
    html.Hr(),
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
        page_current= 0,
        page_size= 10,
        style_table={'overflowX': 'scroll'}
    ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

# Filter datatable based on rescue_type selected with dropdown
@app.callback(
    Output('datatable-id', 'data'),
    [Input('rescue_type', 'value')]
)    
def update_data_table(rescue_type):
    # Water Rescue selected
    if rescue_type == 'Water Rescue':
        query_result_df = pd.DataFrame.from_records(shelter.read({
            '$and':[
                # age must be greater than 26 AND less than 156 weeks
                {'age_upon_outcome_in_weeks': {'$gte': 26}}, 
                {'age_upon_outcome_in_weeks': {'$lte': 156}},
                # must be one of the preferred breeds
                {'breed': {'$in': [
                    'Labrador Retriever Mix', 
                    'Chesapeake Bay Retriever', 
                    'Newfoundland'
                ]}},
                # must be preferred sex
                {'sex_upon_outcome': 'Intact Female'}
            ]
        }))
    # Mountain Rescue selected    
    elif rescue_type == 'Mountain Rescue':
        query_result_df = pd.DataFrame.from_records(shelter.read({
            '$and':[
                # age must be greater than 26 AND less than 156 weeks
                {'age_upon_outcome_in_weeks': {'$gte': 26}}, 
                {'age_upon_outcome_in_weeks': {'$lte': 156}},
                # must be one of the preferred breeds
                {'breed': {'$in': [
                    'German Shepherd', 
                    'Alaskan Malamute', 
                    'Old English Sheepdog',
                    'Siberian Husky',
                    'Rottweiler'
                ]}},
                # must be preferred sex
                {'sex_upon_outcome': 'Intact Male'}
            ]
        }))  
    # Disaster Rescue selected    
    elif rescue_type == 'Disaster Rescue':
        query_result_df = pd.DataFrame.from_records(shelter.read({
            '$and':[
                # age must be greater than 20 AND less than 300 weeks
                {'age_upon_outcome_in_weeks': {'$gte': 20}}, 
                {'age_upon_outcome_in_weeks': {'$lte': 300}},
                # must be one of the preferred breeds
                {'breed': {'$in':[
                    'German Shepherd', 
                    'Doberman Pinscher', 
                    'Golden Retriever',
                    'Bloodhound',
                    'Rottweiler'
                ]}},
                # must be preferred sex
                {'sex_upon_outcome': 'Intact Male'}
            ]
        }))
    # reset to non-filtered view    
    elif rescue_type == 'Reset':
        query_result_df = pd.DataFrame.from_records(shelter.read())
        
    return query_result_df.to_dict('records')


# highlight selected row in datatable
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_rows')]
)
def update_styles(selected_rows):
    return [{
        'if': { 'row_index': i },
        'background_color': '#D2F3FF'
    } for i in selected_rows]

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "data")])
def update_graphs(currentData):
    dff = pd.DataFrame.from_dict(currentData)
    df_pie = dff.loc[dff['animal_type'] == 'Dog', 'breed']
    fig = px.pie(df_pie, names='breed', title='Dog Breeds')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    
    return [
        dcc.Graph(            
            figure = fig
        )    
    ]


# Display information of animal in selected row on map. If no row selected, displays row_index 1
@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', 'derived_viewport_data'),
    Input('datatable-id', 'selected_rows')]
)
def update_map(viewData, selected_rows):
    dff = pd.DataFrame.from_dict(viewData)
        
    # if any row is selected return info for that animal
    if selected_rows:       
        resulting_map = [
            dl.Map(
                style={'width': '1000px', 'height': '500px'}, 
                center=[30.75,-97.48], 
                zoom=10, 
                children=[
                    dl.TileLayer(id="base-layer-id"),
                    # Marker with tool tip and popup
                    dl.Marker(
                        position=[
                            dff.iloc[selected_rows[0]]['location_lat'],
                            dff.iloc[selected_rows[0]]['location_long']
                        ], 
                        children=[
                            dl.Tooltip(dff.iloc[selected_rows[0]][4]),
                            dl.Popup([
                                html.H1("Animal Name"),
                                html.P(dff.iloc[selected_rows[0]][9])
                            ])
                        ]
                    )
                ]
            )
        ]
    # if no row is selected return info for animal at row_index 1    
    else:
        resulting_map = [
            dl.Map(
                style={'width': '1000px', 'height': '500px'}, 
                center=[30.75,-97.48], 
                zoom=10, 
                children=[
                    dl.TileLayer(id="base-layer-id"),
                    # Marker with tool tip and popup
                    dl.Marker(
                        position=[
                            dff.iloc[1]['location_lat'],
                            dff.iloc[1]['location_long']
                        ], 
                        children=[
                            dl.Tooltip(dff.iloc[1,4]),
                            dl.Popup([
                                html.H1("Animal Name"),
                                html.P(dff.iloc[1,9])
                            ])
                        ]
                    )
                ]
            )
        ]        
    return resulting_map


app
