#!/usr/bin/env python
#
#Copyright 2019 Elmwood Electronics
#Permission is hereby granted, free of charge, to any person obtaining a copy of this crappy software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sqlite3
import pandas as pd
import json
from datetime import datetime,time
from time import mktime

##def to_json_dict(dict_format_string):
##    
##    d = {}
##    elems  = filter(str.isalnum,dict_format_string.split("'"))
##    values = elems[1::2]
##    keys   = elems[0::2]
##    d.update(zip(keys,values))
##
##    return d


simplified_json = json.load(open('/run/dump1090-fa/aircraft.json'))


##simplified_json = simplified_json.filter(["aircraft"])

hexes = []
flights = []
latitudes = []
longitudes = []
navigations = []
nics = []


for event in simplified_json['aircraft']:

##    for element in event:
##        dictionary = to_json_dict(str(element))
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

the_dataframe = pd.DataFrame({
    'hexes': hexes,
    'flights': flights,
    'latitudes': latitudes,
    'longitudes' : longitudes,
    'navigations' : navigations,
    'nics' : nics
    })

print(the_dataframe)
        
# hex_, flight, lat, lon, nav_altitude_mcp, nic

 
