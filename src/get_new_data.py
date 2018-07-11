import sys
sys.path.append('.')
from getfile import getURL_link
from stationcsv2sql import csv2sql

def get_new_data(year, station):
	global args	
	args.station_id = station
	args.year = year
	args.month = 1
	args.day = 1
	climate_data, args = getURL_link(args)
	csv2sql(climate_data, args)