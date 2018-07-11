
# coding: utf-8

# In[45]:

import pandas as pd
import numpy as np

import pandas.io.sql as psql
import sqlite3 as sql

from bokeh.plotting import Figure, show
from bokeh.models import ColumnDataSource, HoverTool, DataRange1d, CrosshairTool
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc, output_notebook, output_file
from datetime import datetime
from bokeh.models import DatetimeTickFormatter
from bokeh.layouts import column


import os
import sys
os.getcwd()
sys.path.extend([ os.getcwd() ])

from read_from_sql import read_from_sql
from get_new_data import get_new_data
from check_station_id import check_station_id

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(min_GDD=[], max_GDD=[], mean_GDD=[],
                                    q1_GDD=[], q3_GDD=[],
                                    time=[], timer=[], timel=[], 
                                    date_str=[]))

# Create Input controls
current_year = datetime.today().year
min_year = Slider(title="Year Start", start=1900, end=current_year, value=1900, step=1)
max_year = Slider(title="Year End", start=1900, end=current_year, value=current_year, step=1)
station_IDs_str = TextInput(title="Station ID", value='6551')
base_temp = Slider(title="Base Temperature (C)", start=0, end=25, value=10, step=1)

# Create Figure and Plot
hover = HoverTool(tooltips=[
    ("Date","@date_str")])
p = Figure(x_axis_type="datetime", plot_width=800, tools=[hover])
p.quad(top='max_GDD', bottom='min_GDD', left='timel', right='timer', source=source, alpha=0.5, color='mediumslateblue', line_color="black", line_alpha=0.5, legend='Min/Max')
p.quad(top='q3_GDD', bottom='q1_GDD', left='timel', right='timer', source=source, alpha=0.5, color='black', line_color="black", line_alpha=0.5, legend='25-75 Percentile')
p.line(x='time', y='mean_GDD', source = source, color='red', line_width = 2, alpha=0.8, legend='Average' )
p.x_range = DataRange1d(range_padding=0, bounds=None)
p.yaxis.axis_label = "GDD"
p.xaxis.axis_label = 'Month'
# p.xaxis[0].formatter = DatetimeTickFormatter(formats=dict(days=["%B %d"], months=["%B"], years=["%Y"]))


# Select Data based on input info             
def select_data():
    # p.title = p.title + str(' (Wait..)')
    global station_IDs
    # Make Stations ID's as a list
    station_IDs=[]
    [station_IDs.append(int(n)) for n in station_IDs_str.value.split()]
    
    # Select Data based on input info             
    logic_str = ('WHERE year>=' + str(min_year.value) 
                 + ' AND year<=' + str(max_year.value)
                 + ' AND station_id=' + str(station_IDs[0]))
    selected_data = read_from_sql(columns='station_id, t_min, t_max, t_mean, month, day, datastamp', logic = logic_str)
    selected_data = pd.DataFrame(selected_data)
    old_names = np.arange(7) 
    new_names = ['ID', 'Min', 'Max', 'Mean', 'Month', 'Day', 'Time']
    selected_data.rename(columns=dict(zip(old_names, new_names)), inplace=True)
    return selected_data

#Update function
def update(attrname, old, new):
    df = select_data()
    if len(df)==0:
        p.title = "No Data Availabe!"
        
    else:
        # Change DateTime Format
        df['Time'] = pd.to_datetime(df['Time'])   
        
        # Calculate GDDs
        temp=[]
        for i, each_day in enumerate(pd.date_range('2000-1-1','2000-12-29')):
            same_time=df[pd.Series(df.Month==each_day.month) & pd.Series(df.Day==each_day.day)]
            GDD_same_time = same_time.Mean - base_temp.value
            GDD_same_time [GDD_same_time<0] = 0
            temp.append([min(GDD_same_time),
                         max(GDD_same_time),
                         np.mean(GDD_same_time),
                         np.percentile(GDD_same_time,25),
                         np.percentile(GDD_same_time,75)])
        
        df_calc = pd.DataFrame(temp, columns = ['Min_GDD', 'Max_GDD', 'Mean_GDD', 'Q1_GDD', 'Q3_GDD'])                     
        df_calc['Time'] = pd.date_range('2000-1-1','2000-12-29')
        
        # Update plot data source      
        #p.title = "Annual Cycle of Min/Max Daily Growing Degree Days"
        source.data = dict(
            min_GDD=df_calc['Min_GDD'],
            max_GDD=df_calc['Max_GDD'],
            mean_GDD=df_calc['Mean_GDD'],
            q1_GDD=df_calc['Q1_GDD'],
            q3_GDD=df_calc['Q3_GDD'],
            timel=df_calc['Time']- pd.DateOffset(days=.5),
            timer=df_calc['Time']+ pd.DateOffset(days=.5),
            time=df_calc['Time'],
            date_str=[[str(each_row.month)+'/'+str(each_row.day)] for each_row in df_calc['Time']],
            )
    
# Making plot visual and make updates
controls = [base_temp, min_year, max_year, station_IDs_str]
for control in controls:
    control.on_change('value', update)
# inputs = HBox(VBoxForm(*controls), width=300)
update(None, None, None) # initial load of the data
# curdoc().add_root(HBox(inputs, p))
curdoc().add_root(column(p))


# In[ ]:



