#!/usr/bin/python3
import sys
import sqlite3
sys.path.append('.')
from datetime import datetime
from calc_GDD import calc_GDD
from read_from_sql import read_from_sql
from check_database_first import check_database_year_only

#

def csv2sql(CSV, args):
	conn = sqlite3.connect('place_time_temp_data.sql')
	c = conn.cursor()

	c.execute('CREATE TABLE IF NOT EXISTS ptt_data(station_id INT, station_name TEXT, datastamp TEXT, \
		       year INT, month INT, day INT, t_min REAL, t_max REAL, t_mean REAL, GDD REAL, GDD_acc REAL)')

	dateformat = '%Y-%m-%d'

	station_name = read_from_sql(columns='station_name', database='stationInventory.sql', table='stationinfo', logic=('WHERE station_id=' + str(args.place)))[0][0]
	args.place_name = station_name

	Check = check_database_year_only(args.place, args.year)

	if Check == []:
		GDD_accumulated = 0
		breaker = False
		csv = CSV.decode("utf-8", errors='replace')
		
		for line in csv.split('\n')[25:]:
			splitted_line = line.split(",")
			if splitted_line[0] == '"Date/Time"':
				line_array = [0, 1, 2, 3]
				breaker = True
				if splitted_line[5] == '"Max Temp (\xb0C)"':
					line_array.append(5)
				if splitted_line[7] == '"Min Temp (\xb0C)"':
					line_array.append(7)
				if splitted_line[9] == '"Mean Temp (\xb0C)"':
					line_array.append(9)
				continue

			if breaker == True:
				if splitted_line == [""]:
					continue
				if splitted_line[5][1:-1] == "" or splitted_line[7][1:-1] == "":
					if splitted_line[9][1:-1] == "":
						continue
					else:
						GDD = calc_GDD(float(splitted_line[9][1:-1]), float(splitted_line[9][1:-1]), float(args.base_temp))
				else:
					GDD = calc_GDD(float(splitted_line[5][1:-1]), float(splitted_line[7][1:-1]), float(args.base_temp))
				GDD_accumulated += GDD
				string = 'INSERT INTO ptt_data VALUES(' + str(args.place) + ', "' + str(args.place_name) + '", "' + \
					      str(datetime.strptime(str(str(splitted_line[1][1:-1]) + '-' + str(splitted_line[2][1:-1]) + '-' + \
					      str(splitted_line[3][1:-1])), dateformat)).split(" ")[0] + '", ' + \
					      str(splitted_line[1][1:-1]) + ', ' + str(splitted_line[2][1:-1]) + ', ' + str(splitted_line[3][1:-1]) + ', ' + \
					      str(splitted_line[5][1:-1]) + ', ' + str(splitted_line[7][1:-1]) + ', ' + str(splitted_line[9][1:-1]) + ', ' + \
					      str(GDD) + ', ' + str(GDD_accumulated) + ')'
				c.execute(string)
				conn.commit()

			else:
				print("This is not a traditional input *.csv from the website: http://climate.weather.gc.ca\nPlease use .csv files for input just from that site.")
				c.close()
				conn.close()
				break
		
		c.close()
		conn.close()
	else:
		print('Data of year '+ str(args.year) + ' with strtion ID of ' + str(args.place) + ' found in database. Skipping.')
