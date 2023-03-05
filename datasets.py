import requests
import os
from math import sin, cos, sqrt, atan2, radians

'''
Doc: https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted
Token: https://www.ncdc.noaa.gov/cdo-web/token
'''
# Set up the request headers with the token included
#To generate toke visit https://www.ncdc.noaa.gov/cdo-web/token
headers = {
    "token": os.environ.get('NOAA_TOKEN'),
}

# define API endpoint and parameters
endpoint = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
params = {'limit': 25, 'datasetid': 'GHCND'}

# get closest station using longitude and latitude
# Read more about extent https://www.ncdc.noaa.gov/cdo-web/webservices/v2#stations
def get_closest_stations(longitude, latitude,extent=30):
    params['extent'] = f'{longitude-extent},{latitude-extent},{longitude+extent},{latitude+extent}'
    print(f'extent={extent}')
    response = requests.get(endpoint, params=params, headers=headers)

    if len(response.json()) > 0:
        return response.json()
    else:
        raise Exception('Could not find station within specified extent')

# get weather data for closest station
def get_weather_data(longitude, latitude):
    stations = get_closest_stations(longitude, latitude)
    stations = sort_stations_by_distance(longitude, latitude, stations['results'])
    for station in stations:
        #print(station)
        station_id = station['id']
        endpoint = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
        params = {
            'datasetid': 'GHCND',
            'stationid': station_id,
            'startdate': '2023-02-01', #YYYY-MM-DD
            'enddate': '2023-02-01', #YYYY-MM-DD
            'units' : 'metric',
            'datatypeid': 'TMAX,TMIN,PRCP,VISIB,AWND,AWDR,RELHUM'
        }
        response = requests.get(endpoint, params=params, headers=headers)


        print(response.json())

    #data = response.json()
    #return data

def sort_stations_by_distance(longitude, latitude, stations):
    """
    Sorts an array of coordinates by their distance from a given longitude and latitude.

    Args:
        longitude (float): The longitude of the reference point.
        latitude (float): The latitude of the reference point.
        stations (list): An array of stations tuples, where each tuple contains longitude and latitude.

    Returns:
        list: An array of stations tuples, sorted by their distance from the reference point.
    """

    # Define a function to calculate the distance between two coordinates using the haversine formula
    def calculate_distance(coord1, coord2):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(coord1[1])
        lon1 = radians(coord1[0])
        lat2 = radians(coord2[1])
        lon2 = radians(coord2[0])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

    # Calculate the distance of each coordinate from the reference point
    for station in stations:
        distance = calculate_distance((longitude, latitude), (station['longitude'], station['latitude']))
        station['distance'] = distance

    # Sort the coordinates by their distance from the reference point
    sorted_stations = sorted(stations, key=lambda x: x['distance'])

    return sorted_stations

#51.7905732,-1.3467806
# example usage
longitude = -1.285010
latitude = 51.670071
# longitude = -75.1652
# latitude = 39.9526
weather_data = get_weather_data(longitude, latitude)

#print(weather_data)