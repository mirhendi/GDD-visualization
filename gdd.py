#!/usr/bin/env python

import io
import os
import sys
import argparse
sys.path.append('src/')
sys.path.append('.')
#sys.path.append('/usr/local/lib/python3.4/dist-packages/tornado')
from getfile import getURL
from getfile import getURL_link
from read_from_sql import read_from_sql
from stationcsv2sql import csv2sql
from check_station_id import check_station_id
from station_id_by_province import station_id_by_province
import codecs
from codecs import open as uopen
import time

#This function will check the number of arguments that are passed in by the user when running this code
#First argument will decide the kind of job the user want's (like in git for examample)
#If there is no first argument the interactive code will run that will ask for the data step by step.
#Examples for the first argument:
#
#gdd data # #
#gdd plot # #
#gdd ...
#
#There might be other options that the user can set in the command line by the second, third, ... arguments
#Most of the main options will need some if these arguments, like -y 2015 for example, year is usually needed, -p --place also

parser = argparse.ArgumentParser()
parser.add_argument('task', nargs='?', choices=['data', 'lin_reg', 'plot_min_max', 'plot_acc_gdd', 'plot_min_max_gdd', 'station', 
	                'province', 'map', 'interactive', 'examples'], help='task to  be done (string)')
parser.add_argument('-y', '--year', type=int, help='year of interest (integer)')
parser.add_argument('-Y', '--Years', type=argparse.FileType('r'), help='file that contains a list of desired years \n(integer\n, integer\n, ...)')
parser.add_argument('-m', '--month', type=int, help='month of interest (integer)')
parser.add_argument('-d', '--day', type=int, help='day of interest (integer)')
parser.add_argument('-p', '--place', type=int, help='station_id of the place of interest (integer)')
parser.add_argument('-P', '--Places', type=argparse.FileType('r'), help='file that contains a list of desired station_id\'s \n(integer\n, integer\n, ...)')
parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='file name to output to (string)')
parser.add_argument('-b', '--base_temp', nargs='+', type=float, help='value(s) of base temperature', default='10.0')
parser.add_argument('-g', '--get_station_id', type=str, help='name of the desired station, prints all station name results with that name and their id\'s')
parser.add_argument('-n', '--place_name', type=str, help='name of the station. Should not be given. Will be generated using the station_id.')
parser.add_argument('-r', '--province', type=str, help='name of the province.')


global args
args = parser.parse_args()

YEARS = []
PLACES = []

if args.task == 'examples':
	print('Examples:')
	print('python3 gdd.py interactive')
	print('python3 gdd.py station -g toronto')
	print("python3 gdd.py station -g st\.\ john\\'s")
	print('python3 gdd.py province -r newfoundland')
	print("python3 gdd.py province -r nova\ scotia")
	print("python3 gdd.py data -y 2004 -m 5 -d 3 -p 5051")
	print("python3 gdd.py data -Y TESTS/example_Years.txt -m 5 -d 3 -p 5051")
	print("python3 gdd.py data -y 2004 -m 5 -d 3 -P TESTS/NEWFOUNDLAND.txt")
	print("python3 gdd.py data -Y TESTS/example_Years.txt -P TESTS/IDS.txt")
	print('python3 gdd.py plot_min_max')
	print('python3 gdd.py plot_acc_gdd')
	print('python3 gdd.py plot_min_max_gdd')
	sys.exit("Try one of these if you're clueless")

if args.task=='data' or args.task=='map' or args.task=='lin_reg':
	if args.year:
		if 1800 < args.year < 2016:
			pass
		else:
			sys.exit('Please provide a year that is in between 1800 and 2016.')
	elif args.Years:
		for line in args.Years.readlines():
			line = line.strip()
			if line == "":
				line.next()
			if 1800 < int(line) < 2016:
				YEARS.append(int(line))
				continue
			else:
				sys.exit('Year ' + str(line) + ' is not a valid year. Please choose one between 1800 and 2016.')
	else:
		sys.exit('Year has to be provided for - ' + str(args.task) + ' - option.')

	if args.place:
		check = check_station_id(int(args.place))
		if check == True:
			pass
		else:
			sys.exit('Please provide a valid station_id. ' + str(args.place) + ' is not a valid one (see readme for help).')
	elif args.Places:
		for line in args.Places.readlines():
			line = line.strip()
			if line == "" or line == None:
				line.next()

			check = check_station_id(int(line))
			if check == True:
				PLACES.append(int(line))
				continue
			else:
				sys.exit('Station_id ' + str(line) + ' is not a valid one (see readme for help).')
	else:
		sys.exit('Station_id has to be provided for - ' + str(args.task) + ' - option.')
	

#################################################################################################################################
if args.task == 'interactive':
	args = getURL(args)
	climate_data, args = getURL_link(args)
	csv2sql(climate_data, args)


#################################################################################################################################
elif args.task == 'lin_reg':
	args.month = 1
	args.day = 1
	Acc_Gdd_year_pair = []
	lin_reg_save_file = open('TESTS/linear_regression.txt', 'w')
	if args.Years:
		for yeaR in YEARS:
			reading = read_from_sql(columns='GDD_acc', logic=('WHERE station_id=' + str(args.place) + ' AND year=' + str(yeaR)))
			
			Acc_count = 0
			for i in reading:
				if i[0] > Acc_count:
					Acc_count = i[0]
				else:
					continue
			Acc_Gdd_year_pair.append([yeaR, Acc_count])
		for l in range(len(Acc_Gdd_year_pair)):
			if Acc_Gdd_year_pair[l][1] == 0:
				continue
			else:
				lin_reg_save_file.write('{},{}\n'.format(Acc_Gdd_year_pair[l][0], Acc_Gdd_year_pair[l][1]))

	else:
		sys.exit('Please provide a file for the -Y option with the years.')
	lin_reg_save_file.close()
	time.sleep(1)
	os.popen("java src/SGD_linearRegression >SGD_linearRegression_out_put.txt")

#################################################################################################################################
elif args.task == 'data':
	if args.month == None:
		args.month = 1
	if args.day == None:
		args.day = 1

	if args.Places:
		if args.Years:
			for place in PLACES:
				for year in YEARS:
					args.year = year
					args.place = place
					climate_data, args = getURL_link(args)
					csv2sql(climate_data, args)
					print("Year: " + str(args.year) + "    Station ID: " + str(args.place))
		else:
			for place in PLACES:
				args.place = place
				climate_data, args = getURL_link(args)
				csv2sql(climate_data, args)
				print("Year: " + str(args.year) + "    Station ID: " + str(args.place))
	else:
		if args.Years:
			for year in YEARS:
				args.year = year
				climate_data, args = getURL_link(args)
				csv2sql(climate_data, args)
				print("Year: " + str(args.year) + "    Station ID: " + str(args.place))
		else:
			climate_data, args = getURL_link(args)
			csv2sql(climate_data, args)
			print("Year: " + str(args.year) + "    Station ID: " + str(args.place))


#################################################################################################################################
elif args.task == 'plot_min_max':
	os.popen("cd src")
	os.popen("bokeh serve --show min_max_plot.py")
	os.popen("cd ..")

#################################################################################################################################
elif args.task == 'plot_acc_gdd':
	os.popen("cd src")
	os.popen("bokeh serve --show acc_gdd_plot.py")
	os.popen("cd ..")

#################################################################################################################################
elif args.task == 'plot_min_max_gdd':
	os.popen("cd src")
	os.popen("bokeh serve --show min_max_gdd_plot.py")
	os.popen("cd ..")

#################################################################################################################################
elif args.task == 'station':
	if args.get_station_id:
		#This will print all values where the selected name was found in the station name
		stations = read_from_sql(columns='station_name, station_id', database='stationInventory.sql', table='stationinfo', 
								logic='WHERE instr(station_name, "' + str(args.get_station_id.upper()) + '") > 0')
		for name in stations:
			if len(name[0].strip()) < 7:
				tabs = 5
			elif len(name[0].strip()) < 15:
				tabs = 4
			elif len(name[0].strip()) < 23:
				tabs = 3
			elif len(name[0].strip()) < 31:
				tabs = 2
			else:
				tabs = 1
			print(name[0].strip(), '\t'*tabs, name[1])
	else:
		print("Usage: gdd station -g 'station_name'")
#################################################################################################################################

elif args.task == 'province':
	if args.province:
		args.province = str(args.province).upper()
		station_id_by_province(args.province)
	else:
		sys.exit('Argument -r or --province followed by the province name is needed.')

#################################################################################################################################

elif args.task == 'map':
	print('Map')

# This is the function that is run first - it decides what the user wants to do, and then passes
# the results onto the other functions as necessary

def gdd():
    """ The master file that grabs data from the user to decide firstly what actions they want to take, 
    and secondly passes all the relevant information to the relevant functions """

# Get filename from getURL
# Pass filename to the SQL database function to generate the DB
# Pass the DB filename through to the calculator to calculate the GDDs
# Pass the GDDs to the plotting program to make plots
# Etc...
