#Aircraft tracking project


import pandas as pd
import json
import requests
import numpy as np
import math
from datetime import datetime,time
from time import mktime

#tail_number = ''
my_distance = 0.0
altitude = 0.0

def get_distance():
    return my_distance
def get_altitude():
    return altitude

def aircraft_dist_calc():
    res = requests.get('https://ipinfo.io/')
    data = res.json()

    myDevicelocation = data['loc'].split(',')
    my_lat = float(myDevicelocation[0])
    my_lon = float(myDevicelocation[1])

    print("My Latitude : ", my_lat)
    print("My Longitude : ", my_lon)


    simplified_json = json.load(open('/run/dump1090-fa/aircraft.json'))


    hexes = []
    flights = []
    latitudes = []
    longitudes = []
    navigations = []
    nics = []


    for event in simplified_json['aircraft']:
        try:
            hexes.append(event['hex'])
        except:
            hexes.append(None)
        try:
            flights.append(event['flight'])
        except:
            flights.append(None)
        try:
            latitudes.append(event['lat'])
        except:
            latitudes.append(None)
        try:
            longitudes.append(event['lon'])
        except:
            longitudes.append(None)
        try:
            navigations.append(event['nav_altitude_mcp'])
        except:
            navigations.append(None)
        try:
            nics.append(event['nic'])
        except:
            nics.append(None)


    my_df = pd.DataFrame({
        'hexes': hexes,
        'flights': flights,
        'latitudes': latitudes,
        'longitudes' : longitudes,
        'nav_altitude' : navigations,
        'nics' : nics
    })


    new_df = my_df.loc[(my_df['flights'] != None)&
                       (my_df['latitudes'] != None )&
                       (my_df['longitudes'] != None)&
                       (my_df['nav_altitude'] < 10000)]
    flight_longitudes = []
    flight_latitudes = []

    try:
        flight_longitudes = np.array(new_df.longitudes)
    except:
        flight_longitudes.append(None)
    try:
        flight_latitudes = np.array(new_df.latitudes)
    except:
        flight_latitudes.append(None)


    print('\n', new_df)
    print('\n Flight Longitudes: \n', flight_longitudes)
    print('\n Flight Latitudes: \n', flight_latitudes)

    s = [[],[]]
    index = new_df.index
    distance = 0.0
    final_df = pd.DataFrame()
    R = 6373.0

    for flight_lon in flight_longitudes:
        for flight_lat in flight_latitudes:
          
            #coordinates
            lat1 = math.radians(my_lat)
            lon1 = math.radians(my_lon)
            lat2 = math.radians(flight_lat)
            lon2 = math.radians(flight_lon)

            #change in coordinates
            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c
        s[0].append(distance)
    s[1].append(index)

    for distance_index in s[1]:
        final_df = new_df.loc[distance_index,:]
        final_df['distance'] = s[0]
        final_df.sort_values('distance', ascending = True)

    print('\nDistance Calculations: \n', s)
    print('\n', final_df)

    my_df = final_df.min()
    print('\n', my_df)

    #tail_number = my_df.loc['flights']
    my_distance = my_df.loc['distance']
    altitude = my_df.loc['nav_altitude']
    #print('\n', tail_number)
    print('\n', my_distance)
    print('\n', altitude)


        
# hex_, flight, lat, lon, nav_altitude_mcp, nic

 
