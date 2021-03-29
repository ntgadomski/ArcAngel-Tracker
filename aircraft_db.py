
import sqlite3
import pandas as pd
import json
from datetime import datetime,time
from time import mktime

now = datetime.now()
hour_now = now.strftime('%H')
time_now = datetime.today()

sec_since_epoch = int(mktime(now.timetuple()) + now.microsecond/1000000.0)  #using this to have a "unique" counter for each entry, should make the database easier to search

counter_int = sec_since_epoch - 1576179322  #1576179322 was the epoch when we made this program, just put this line in to make a lower number for our counter

print (counter_int)


conn = sqlite3.connect('/home/pi/aircraft.db') 
cur = conn.cursor()

#creating the database tables here:

#aircraft_json = json.load(open('/run/dump1090-fa/aircraft.json'))   #load the JSON file from the default location

read_aircraft_json = pd.read_json('/run/dump1090-fa/aircraft.json')
read_aircraft_json.to_csv('/home/pi/Desktop/aircraft.csv', index = None, header = True)
get_csv = pd.read_csv('/home/pi/Desktop/aircraft.csv')
get_csv.to_sql('all_aircraft', conn, if_exists='append', index=False)
