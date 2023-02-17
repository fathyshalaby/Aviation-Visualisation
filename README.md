# ✈️ Lufthansa API - Aviation Visualisation

## General Information

This project uses the Lufthansa OpenAPI [1]. Together with the data provided by the LH Public API, this project aims to 
visualise the flight schedules for all publicly available flights of the Lufthansa Group. This includes scheduled flights 
of Lufthansa, Austrian Airlines, SWISS or Brussels Airlines.

### Remarks

This application uses official flight data and loads the data dynamically via the provided API. Since the application 
needs to load the scheduled flight information, it may take some time to display all the data and prepare everything visually.

For more information, visit https://developer.lufthansa.com/page.

### Table of Contents

1. Installation
2. Aviation Visualisation
3. References


## 1. Installation

The following section shows how to install the project dependencies and any other requirements that are necessary for 
the application to run successfully.

### 1.1 Requirements

For the application to run successfully, the following dependencies must be installed. Therefore, it is recommended to 
use `pip install` to avoid errors or other dependency problem occurrences.

```sh
pandas==1.5.3
requests~=2.28.1
plotly==5.13.0
numpy~=1.24.1
dash~=2.8.1
dash_bootstrap_components~=1.3.1
```

The following command shows you how to install all project dependencies. For your convenience, the `requirements.txt` 
file contains a list of all dependencies (as shown above) that can be easily installed with the following command.

```sh
pip install -r requirements.txt
```

### 1.2 Lufthansa API Token
Since the Lufthansa API requires a valid API token and key, it is also required by the application to provide such one.

## 2. Aviation Visualisation 

The application makes use of the OpenAPI provided by the Lufthansa Group to visualize scheduled flights for the airlines 
Lufthansa, Austrian Airlines, SWISS and Brussels Airlines. This enables the possibility to investigate on the scheduled 
flights in a more visualized way and to see the flight route connections.

`The application may need a few seconds to load the data from the API. Be aware of this!`

### 2.1 Usage Example

```bash
app.py
```
For a list of possible arguments use the `--help` option

After the successful launch of the application, a web server is started and its link is displayed in the console.
```
(missing_semester) anon@anon EX2-AviationVisualisation % python3 app.py
Dash is running on http://127.0.0.1:8050/

INFO:Aviation Visualisation:Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'Aviation Visualisation'
 * Debug mode: on
```



The application creates logs for each event that occured and shows them in the console. 

```
INFO:__main__:New search request for: LH, 2023-02-16
INFO:__main__:Lufthansa API answered with status code 200
INFO:src.flights_plot:parsing flights
INFO:src.flights_plot:parsing airports
INFO:src.flights_plot:creating map
INFO:src.flights_plot:filtering missing data
INFO:src.flights_plot:creating geomap

INFO:__main__:New search request for: OS, 2023-04-27
INFO:__main__:Lufthansa API answered with status code 200
INFO:src.flights_plot:parsing flights
INFO:src.flights_plot:parsing airports
INFO:src.flights_plot:creating map
INFO:src.flights_plot:filtering missing data
INFO:src.flights_plot:creating geomap
```

## 3. References
* [1] Lufthansa Public API https://developer.lufthansa.com/io-docs
  * This API provides Lufthansa's flight schedule information (incl. Lufthansa, Austrian Airlines, SWISS and Brussels Airlines).
* [2] OurAirports Airport Data https://ourairports.com/data/ 
  * Last Changes: 31.01.2023

## Attribution
* Airplane Favicon by [Twemoji](https://twemoji.twitter.com/)  is licensed under CC BY 4.0
