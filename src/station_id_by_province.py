#!/usr/bin/python3
import sys
sys.path.append('.')
import sqlite3
from read_from_sql import read_from_sql
import datetime

def station_id_by_province(province):
	reading = read_from_sql(columns = 'station_id', database='stationInventory.sql', table='stationinfo', logic="WHERE province='" + str(province) + "'")
	filename = str(datetime.date.today()) + "-" + str(province) + ".txt"
	File = open(filename, 'a')
	for r in range(len(reading)):
		File.write('{}\n'.format(reading[r][0]))
	