import logging
import random
import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

warnings.simplefilter(action='ignore', category=FutureWarning)


def create_flights_df(flights_list):
    logger.info("parsing flights")

    # Create an empty DataFrame
    flights_df = pd.DataFrame(columns=['origin', 'destination', 'legs'])

    for flight in flights_list:
        legs = flight['legs']
        stops = [leg['destination'] for leg in legs[:-1]]
        origin = legs[0]['origin']
        destination = legs[-1]['destination']
        airline = flight["airline"]
        flight_number = flight["flightNumber"]

        # Append the extracted data to the DataFrame
        flights_df = flights_df.append(
            {"airline": airline, "flight_number": flight_number, 'origin': origin, 'destination': destination,
             'stops': stops, 'legs': legs}, ignore_index=True)

    # look if the length of stops is more than 0 if so create new row for each stop

    for i, row in flights_df.iterrows():
        if len(row["stops"]) > 1:
            # create new row for each stop but if the stops are multi stops then create a new row for each stop where the origin is the previous stop
            for stop in row["stops"]:
                if stop == row["stops"][0]:
                    flights_df = flights_df.append(
                        {"airline": row["airline"], "flight_number": row["flight_number"], 'origin': row["origin"],
                         'destination': stop, 'stops': [], 'legs': row["legs"]}, ignore_index=True)
                else:
                    flights_df = flights_df.append(
                        {"airline": row["airline"], "flight_number": row["flight_number"], 'origin': stop,
                         'destination': stop, 'stops': [], 'legs': row["legs"]}, ignore_index=True)
        elif len(row["stops"]) == 1:
            flights_df = flights_df.append(
                {"airline": row["airline"], "flight_number": row["flight_number"], 'origin': row["stops"][0],
                 'destination': row["destination"], 'stops': [], 'legs': row["legs"]}, ignore_index=True)
        else:
            pass

    # remove the rows where the origin and destination are the same
    flights_df = flights_df[flights_df["origin"] != flights_df["destination"]]
    # if the origin is not nan
    flights_df = flights_df[flights_df["origin"].notna()]
    # if the destination is not nan
    flights_df = flights_df[flights_df["destination"].notna()]

    flights_df = flights_df[flights_df["origin"] != "nan"]
    flights_df = flights_df[flights_df["destination"] != "nan"]

    flights_df = flights_df.reset_index(drop=True)

    # return the DataFrame
    return flights_df


def filter_flights(flights_df, airports):
    """Remove Missing Data, which includes:
    - Flights with no destination
    - Flights with airports that are not in the airport database
    """
    logger.info("filtering missing data")

    lat_orgs = []
    lon_orgs = []
    lat_dests = []
    lon_dests = []
    missing = []
    flights_df = flights_df.reset_index(drop=True)
    for i in range(len(flights_df)):
        try:
            lat_org = airports[airports['iata'] == flights_df['origin'][i]]['latitude'].values[0]
            lon_org = airports[airports['iata'] == flights_df['origin'][i]]['longitude'].values[0]
        except:

            missing.append(flights_df['origin'][i])
        try:
            lat_dest = airports[airports['iata'] == flights_df['destination'][i]]['latitude'].values[0]
            lon_dest = airports[airports['iata'] == flights_df['destination'][i]]['longitude'].values[0]
            lat_orgs.append(lat_org)
            lon_orgs.append(lon_org)
            lat_dests.append(lat_dest)
            lon_dests.append(lon_dest)
        except:

            missing.append(flights_df['destination'][i])

    missings = np.unique(missing)
    flights_df = flights_df[~flights_df['origin'].isin(missings)]
    flights_df = flights_df[~flights_df['destination'].isin(missings)]
    flights_df = flights_df.reset_index(drop=True)

    lat_orgs = []
    lon_orgs = []
    lat_dests = []
    lon_dests = []
    city_orgs = []
    city_dests = []
    country_orgs = []
    country_dests = []
    missing = []

    for i in range(len(flights_df)):
        try:
            lat_org = airports[airports['iata'] == flights_df['origin'][i]]['latitude'].values[0]
            lon_org = airports[airports['iata'] == flights_df['origin'][i]]['longitude'].values[0]
            city_org = airports[airports['iata'] == flights_df['origin'][i]]['city'].values[0]
            country_org = airports[airports['iata'] == flights_df['origin'][i]]['country'].values[0]

        except:
            missing.append(flights_df['origin'][i])

        try:
            lat_dest = airports[airports['iata'] == flights_df['destination'][i]]['latitude'].values[0]
            lon_dest = airports[airports['iata'] == flights_df['destination'][i]]['longitude'].values[0]
            city_dest = airports[airports['iata'] == flights_df['destination'][i]]['city'].values[0]
            country_dest = airports[airports['iata'] == flights_df['destination'][i]]['country'].values[0]
            city_orgs.append(city_org)
            city_dests.append(city_dest)
            country_orgs.append(country_org)
            country_dests.append(country_dest)
            lat_orgs.append(lat_org)
            lon_orgs.append(lon_org)
            lat_dests.append(lat_dest)
            lon_dests.append(lon_dest)

        except:
            missing.append(flights_df['destination'][i])

        flights_df = flights_df[~flights_df['origin'].isin(missing)]
        flights_df = flights_df[~flights_df['destination'].isin(missing)]

    flights_df['lat_org'] = lat_orgs
    flights_df['lon_org'] = lon_orgs
    flights_df['lat_dest'] = lat_dests
    flights_df['lon_dest'] = lon_dests
    flights_df['city_org'] = city_orgs
    flights_df['city_dest'] = city_dests
    flights_df['country_org'] = country_orgs
    flights_df['country_dest'] = country_dests

    table = go.Figure(data=[go.Table(
        header=dict(values=list(flights_df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[flights_df.origin, flights_df.destination, flights_df.legs],
                   fill_color='lavender',
                   align='left'))
    ])

    return flights_df


def create_map(flights_df, airports):
    logger.info("creating map")
    df = filter_flights(flights_df, airports)
    logger.info("creating geomap")
    fig = px.scatter_geo(df,
                         lat='lat_org',
                         lon='lon_org',
                         hover_name='city_org',
                         hover_data=['airline', 'flight_number'],
                         title='Flight Connection Map',
                         scope='world',
                         projection='natural earth',
                         height=900,
                         width=1800)

    # Create the lines
    hover_text = []
    for index, row in df.iterrows():
        hover_text.append(('Origin: {origin}<br>' +
                           'Destination: {dest}<br>' +
                           'Airline: {airline}<br>' +
                           'Flight Number: {flight_number}<br>'
                           ).format(origin=row['city_org'],
                                    dest=row['city_dest'],
                                    airline=row['airline'],
                                    flight_number=format(row['flight_number'], '.0f')
                                    )
                          )
    colors = ['red', 'blue', 'green', 'orange']
    for i, row in df.iterrows():
        fig.add_trace(go.Scattergeo(
            showlegend=False,
            lon=[row['lon_org'], row['lon_dest']],
            lat=[row['lat_org'], row['lat_dest']],
            mode='lines',
            line=dict(width=1.5, color=random.choice(colors)),
            opacity=0.6,
            text=hover_text[i]
        ))
    return fig


def get_airports():
    logger.info("parsing airports")
    airports = pd.read_csv('resources/airports_ourairports.csv')
    airports = airports[['iata_code', 'name', 'municipality', 'iso_country', 'latitude_deg', 'longitude_deg']]
    airports = pd.DataFrame(airports[airports['iata_code'] != '\\N'])
    airports = airports.rename(
        columns={'iata_code': 'iata', 'municipality': 'city', 'iso_country': 'country', 'latitude_deg': 'latitude',
                 'longitude_deg': 'longitude'})
    return airports


def create_connection_map(response):
    flights_df = create_flights_df(response)
    airports = get_airports()
    return create_map(flights_df, airports)
