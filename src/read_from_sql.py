#!/usr/bin/python
import sys
sys.path.append('.')
import sqlite3

def read_from_sql(columns='*', database='place_time_temp_data.sql', table='ptt_data', logic=''):
	conn = sqlite3.connect(database)
	c = conn.cursor()

	c.execute("SELECT " + columns + " FROM " + table + " " + logic)
	selection = c.fetchall()

	c.close()
	conn.close()
	return(selection)

#Usage
#array = read_from_sql()		#will select all the data in the sql database and return it in a 2D array
#specific_array = read_from_sql(columns='station_id, t_min, t_max, t_mean, year, month, day', logic='WHERE year=1995 AND station_id=5050')
#
#!!!
#sqlite IS case sensitive (MySQL is not but they are still working on mysql to work under python3, currently it only works under python2 so we use sqlite)
#
#the column names in the database are like this:
#
#station_id station_name datestamp year month day t_min t_max t_mean GDD GDD_acc
#
#Please feel free to ask for other columns if needed or question on how to use this function
