from datetime import date

import dash_bootstrap_components as dbc
from dash import html, dcc

NAVBAR_STYLE = {
    "display": "flex",
    "justify-content": "space-between",
    "vertical-align": "middle"
}

navbar = dbc.NavbarSimple(
    children=[
        dcc.Dropdown(
            id='airline-search',
            options=[
                {'label': 'Lufthansa', 'value': 'LH'},
                {'label': 'Austrian Airlines', 'value': 'OS'},
                {'label': 'SWISS', 'value': 'LX'},
                {'label': 'Brussels Airlines', 'value': 'SN'},
            ],
            value='OS',
            style={
                'width': '250px',
                'padding-top': '5px'
            }
        ),
        dcc.DatePickerSingle(
            id='date-search',
            min_date_allowed=date(2020, 1, 1),
            max_date_allowed=date(2025, 1, 1),
            initial_visible_month=date.today(),
            date=date.today(),
            style={
                'padding-left': '20px',
                'padding-right': '20px'
            }
        ),
        dbc.Button("Search", id='submit-button', size="lg", n_clicks=0),
    ],
    brand="Aviation Visualisation",
    brand_href="https://sourcery.im.jku.at/missing-semester-2022/EX2-AviationVisualisation",
    color="primary",
    dark=True,
    style=NAVBAR_STYLE
)

layout = html.Div([
    navbar,
    html.Div([], id="map-figure",
             style={
                 "display": "flex",
                 "justify - content": "center"
             })
], style={"height": "100vh"})


def get_layout():
    return layout
