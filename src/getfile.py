#!/usr/bin/env python

import io
import re
import os
import urllib.request
import datetime
from difflib import SequenceMatcher

def getURL(args):
    """Acquires a data file (csv) of the lowest and highest temperatures at a selected station in Canada, over a given \
        timescale"""
    
    #Before we even do anything, make sure that the user has entered valid information
    print ("Please enter the follwoing information:\n\"Station,Year,Month\" where:\n \
        Station = Name of City (must be plaintext)\n \
        Year = The year you wish to look at (format yyyy; must be type(int))\n \
        Month = The month you wish to look at (format m (so 4 or 11, but not 04); must be type(int))")
    
    #Arbitrary input checking flags
    if args.place == None:
        get_dgd_region_flag = False
    else:
        get_dgd_region_flag = True

    if args.year == None:
        get_dgd_year_flag = False
    else:
        get_dgd_year_flag = True

    if args.month == None:
        get_dgd_month_flag = False
    else:
        get_dgd_month_flag = True

    #Changed variable dgd_region to args.place(), similarly dgd_year to args.year() and dgd_month to args.month()
    
    while get_dgd_region_flag == False:
        get_dgd_region = input ("First, type the name of the Station you want data for:\n ")
        if get_dgd_region != "":
            dgd_region = get_dgd_region.upper()
            get_dgd_region_flag = True
        else:
            print("Please type something. Anything. Ideally a Station name.")
        
    while get_dgd_year_flag == False:
        get_dgd_year = input ("Next, please type what year you want data for:\n")
        if get_dgd_year != "":
            if int(get_dgd_year) not in range (1800, int(str(datetime.date.today())[:4])):
                print("Please ensure the year is between 1800 and "+ str(datetime.date.today())[:4])
            else:
                args.year = get_dgd_year
                get_dgd_year_flag = True
            
    while get_dgd_month_flag == False:
        get_dgd_month = input("Finally, what month do you want data for, if applicable? (OPTIONAL)\n")
        if get_dgd_month != "":
            if int(get_dgd_month) not in range (1,13):
                print("Please ensure the month is within the range of 1-12, inclusive. Them's all the months there are!")
            else:
                args.month = get_dgd_month
                get_dgd_month_flag = True
        
# The steps below acquire the raw data from "http://climate.weather.gc.ca", and then builds a new list of all stations that are
# similar in name (by use of the SequenceMatcher function), in case of typos or similarly named stations.
# This then gives the user the ability to manually select the exact station they want
    
    # First of all, check to see if a file called "stationinventory-<todays_date>.csv" exists. If it does not, download it.
    
    todays_temperature_data = str("stationinventory-"+str(datetime.date.today())[:10]+".csv")
    
    if not (os.path.isfile(todays_temperature_data)):
        print ("FILE NOT FOUND")
        daily_temp_data = "ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv"
        
        print ("Downloading File...")
        stationID = urllib.request.urlretrieve (daily_temp_data, todays_temperature_data)
        #while os.path.getsize(todays_temperature_data) < 1792000:
        #    print (os.path.getsize(todays_temperature_data))
        #    if os.path.getsize(todays_temperature_data) % 89600 == 0:
        #        print("#", end="")            
            
        print("100% - FILE DOWNLOADED!")
    else:
        print("A file containing today's temperature data already exists on this system. Skipping download.\n\n")
    
    with open(todays_temperature_data,mode="r") as stationID:
        station_list = []
        for line in stationID:
            newline = re.sub("\"", "",line)
            station_list.append(newline.rstrip().split(","))
 
    new_ctr = 0
    similar_stations = []
    
    # Iterate from 4 to maxlength because the first 4 lines (0,1,2,3) are not relevant data
    for ctr_i in range (4,len(station_list)):
        if not (station_list[ctr_i][11] == '' or station_list[ctr_i][12]== ''):
            if SequenceMatcher(None,dgd_region,str(station_list[ctr_i][0])).ratio() > 0.6:
                if int(args.year) in range (int(station_list[ctr_i][11]),int(station_list[ctr_i][12])):
                    new_ctr += 1
                    similar_stations.append(station_list[ctr_i])
    
    if new_ctr == 0:
        print ("There were no matches based on your string search! Please try again")
        return
    elif new_ctr > 1:
        print ("You typed {0}, and the following entries matched:\n".format(dgd_region))
        for ctr_j in range (0,len(similar_stations)):
            print (str(int(ctr_j) + 1) + ": {0} (Has data from {1} to {2})".format(\
                    similar_stations[ctr_j][0],similar_stations[ctr_j][11],similar_stations[ctr_j][12]))
    
    if new_ctr == 1:
        station_id = similar_stations[0][1]
    else:
        selected_a_station = False
        station_id = ""
        while selected_a_station == False:
            get_station_id = input("Please type in the number of the station you want to use from the list above:\n")
            try:
                get_station_id = int(get_station_id)
            except ValueError:
                print("You must input a number, not a string.")
                break
            
            if int(get_station_id) > 0 and int(get_station_id) < (len(similar_stations)+1):
                args.place = similar_stations[int(get_station_id) - 1][3]
                selected_a_station = True
            else:
                print("Please select from the list above. Just type in the number.")
    return(args)

def getURL_link(args):
    
# The steps below acquire the temperature data pertaining to the requested station, then saves this as a new CSV

    url_of_climate_data = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID="\
    + str(args.place) + "&Year=" + str(args.year) + "&Month=" + str(args.month) + "&Day=1&timeframe=2&submit=Download+Data"
    
    # Timeframe (2) does something - changing from 2 to 1/3/4 seems to affect the type of result - maybe
    # incorporate this as an alternative selector? IE, do you want monthly/hourly/etc data?

    climate_data = urllib.request.urlopen(url_of_climate_data).read()
    
    #Format the filename to display the station, what yr/mth the data is for, and what date/time the data was acquired
    #station_data = str(args.place)+'-'+str(args.year)+'-'+str(args.month)+'_acquired_on_'+str(datetime.date.today())+\
    #re.sub(r"\:","-",str(datetime.datetime.now().time()))[:8]+'.csv'
    
    #with open(station_data, 'wb') as csv_of_station_data:
    #    csv_of_station_data.write(climate_data)
    return (climate_data, args)
