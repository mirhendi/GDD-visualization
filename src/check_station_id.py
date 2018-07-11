#!/usr/bin/python3
import sys
sys.path.append('.')
import sqlite3
from read_from_sql import read_from_sql

def check_station_id(station_id):
	reading = read_from_sql(database='stationInventory.sql', table='stationinfo', logic="WHERE station_id=" + str(station_id))
	if reading == []:
		return False
	else:
		return True