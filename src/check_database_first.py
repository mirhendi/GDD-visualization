
#!/usr/bin/python3
import sys
sys.path.append('.')
import sqlite3
from read_from_sql import read_from_sql

def check_database_first(station_id, year, month, day):
	reading = read_from_sql(logic="WHERE station_id=" + str(station_id) + ' AND year=' + str(year) + ' AND month=' 
		+ str(month) + ' AND day=' + str(day))
	return(reading)

#Calls read_from_sql function, and check weather there is data already or not, you have to check for each day separately because
#I will remove empty rows from the database once new data is added, so if you just check for one day, let's say 1st of january
#there might not be any data, but there might be for 12-th, or for the rest of the month. If there is data for at least one day from the month
#you can stop searching, we have all the data that was available from the site for that moth, usually for the whole year.
#if it returns [] there was nothing found

#A simplified version is:

def check_database_year_only(station_id, year):
	reading = read_from_sql(logic="WHERE station_id=" + str(station_id) + ' AND year=' + str(year))
	return(reading)

#now if this function returns [] it means there is no data in the database for that station_id and that year
#this might be better to use