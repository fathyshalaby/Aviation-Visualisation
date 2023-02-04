#!/usr/bin/env python3

import argparse
import datetime
import logging
import time

import dash_bootstrap_components as dbc
import requests
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

from src import dash_page, flights_plot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog='Aviation Visualisation',
    description='A Dash app that visualises airline flights',
    epilog='Written for Special Topics Missing Semester 921CSPTST2K13'
)

parser.add_argument('-p', '--port')
parser.add_argument('-d', '--debug', choices=['true', 'false'])

app = Dash("Aviation Visualisation", external_stylesheets=[dbc.themes.SANDSTONE])
app.title = "Aviation Visualisation"
app.layout = dash_page.get_layout()
app.config.suppress_callback_exceptions = True

# global variables relevant for token
client_id = ""
client_secret = ""
access_token = ""
token_expiration_timestamp = 0

enable_debug = False
port = 8050


def handle_arguments():
    args = parser.parse_args()
    if args.port is not None:
        if not args.port.isdigit() or not 1 <= int(args.port) <= 65535:
            message = f"{args.port} is not a valid port number"
            raise ValueError(message)
        global port
        port = int(args.port)

    if args.debug is not None:
        global enable_debug
        enable_debug = bool(args.debug)


# converts a YYY-MM-DD date string to the SSIM format
def convert_date(date_string):
    date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return date_object.strftime("%d%b%y").upper()


def get_token():
    global access_token, token_expiration_timestamp

    # if there is no token or the token is expired, get new oauth access token
    if access_token == "" or token_expiration_timestamp < int(time.time()):
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': "client_credentials"
        }
        response = requests.post("https://api.lufthansa.com/v1/oauth/token", data=data).json()
        access_token = response["access_token"]
        token_expiration_timestamp = int(time.time()) + response['expires_in']

    return access_token


@app.callback(Output('map-figure', 'children'),
              Input('submit-button', 'n_clicks'),
              State('airline-search', 'value'),
              State('date-search', 'date'),
              State('map-figure', 'children'), )
def search(n_clicks, airline_search, date_search, children):
    if n_clicks < 1 or airline_search is None:
        return

    logger.info("New search request for: %s, %s", airline_search, date_search)

    headers = {
        'Authorization': 'Bearer {}'.format(get_token()),
        'Accept': 'application/json'
    }

    query_params = {
        'airlines': airline_search,
        'startDate': convert_date(date_search),
        'endDate': convert_date(date_search),
        'daysOfOperation': '1234567',
        'timeMode': 'UTC',
    }

    retry_counter = 0
    while True:
        response = requests.get(url='https://api.lufthansa.com/v1/flight-schedules/flightschedules/passenger',
                                params=query_params, headers=headers)
        logger.info("Lufthansa API answered with status code %s", response.status_code)
        if response.status_code == 200:
            break

        time.sleep(5)
        retry_counter += 1
        if retry_counter > 5:
            raise ConnectionError("Unable to get proper Response from Lufthansa API")

    json = response.json()
    if len(json) == 0:
        return [html.H2("No flights have been found for the given search parameters.")]

    figure = flights_plot.create_connection_map(response.json())
    figure.to_html("test.html")

    return [dcc.Graph(figure=figure)]


handle_arguments()

if __name__ == '__main__':
    app.run(debug=enable_debug, port=port)
