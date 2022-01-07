#Title: Arc-Angel Aircraft tracking project
#Authors: Nickolas Gadomski, Samuel Njenga, Ben Deleuze, Colby Nicoletti, Neel Patel
#Purpose: Utilize local aircraft data recieved by ADS-B antenna to calculate the distance of the closest
#aircraft compared to the users gps location.


import pandas as pd
import json
import requests
import numpy as np
import math

class AircraftFilter:

#Initilize Aircraft Distance, Altitude, and Tail Number
    def __init__(self, distance = 0, altitude = 0):
        self.tail_number = ''
        self.my_distance = distance
        self.altitude = altitude
        
    
#Retrieve Local Aircraft Data: Altitude, Distance, and Tail Number from data set
    def get_distance(self):
        return self.my_distance
    def get_altitude(self):
        return self.altitude
    def get_tail_number(self):
        return self.tail_number

#Method to calculate distance between user and aircraft coordinates
    def aircraft_dist_calc(self):
        res = requests.get('https://ipinfo.io/')
        data = res.json()

		#Initilze User Longitude and Latitude coordinates in float
        myDevicelocation = data['loc'].split(',')
        my_lat = float(myDevicelocation[0])
        my_lon = float(myDevicelocation[1])

        print("My Latitude : ", my_lat)
        print("My Longitude : ", my_lon)

		#Load and open Local Aircraft data file from dump1090 Package
        simplified_json = json.load(open('/run/dump1090-fa/aircraft.json'))

#Initialize lists/arrays to hold aircraft data in DataFrame
        hexes = []
        flights = []
        latitudes = []
        longitudes = []
        navigations = []
        nics = []

#For loop of Try/Catch to append/organize aircraft data into a DataFrame
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

#Pandas DataFrame for Local Aircraft: simplified_json
        my_df = pd.DataFrame({
            'hexes': hexes,
            'flights': flights,
            'latitudes': latitudes,
            'longitudes' : longitudes,
            'nav_altitude' : navigations,
            'nics' : nics
        })

#New DataFrame to select specific data from DataFrame Tables
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

#Initialize Variables for Haversine Calculation
        s = [[],[]]
        index = new_df.index
        distance = 0.0
        final_df = pd.DataFrame()
        R = 6373.0

#Nested For Loop to calculate local aircraft Longitude and Latitude coordinates compared to User location
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

				#Haversine Algorithm
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

        try:
            self.tail_number = my_df.loc['flights']
        except:
            self.tail_number = 'Anonymous'
        self.my_distance = my_df.loc['distance']
        self.altitude = my_df.loc['nav_altitude']
        print('\n', self.tail_number)
        print('\n', self.my_distance)
        print('\n', self.altitude)


        
# hex_, flight, lat, lon, nav_altitude_mcp, nic

 
