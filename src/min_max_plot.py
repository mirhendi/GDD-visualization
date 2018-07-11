
# coding: utf-8

# In[20]:

import pandas as pd
import numpy as np

import pandas.io.sql as psql
import sqlite3 as sql

from bokeh.plotting import Figure, show
from bokeh.models import ColumnDataSource, HoverTool,  DataRange1d, CrosshairTool
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc, output_notebook, output_file
from datetime import datetime
from bokeh.layouts import column

import os
import sys
os.getcwd()
sys.path.extend([ os.getcwd() ])

from read_from_sql import read_from_sql
from get_new_data import get_new_data
from check_station_id import check_station_id

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(min_t=[], max_t=[], mean_t=[], time=[], station_id=[], timer=[], timel=[], date_str=[]))

# Create Input controls
current_year = datetime.today().year
selected_year = Slider(title="Year", start=1900, end=current_year, value=2008, step=1)
station_IDs_str = TextInput(title="Station ID", value='6551')

# Create Figure and Plot
hover = HoverTool(tooltips=[
    ("Date","@date_str"),
    ("Station ID", "@station_id") ])
p = Figure(x_axis_type="datetime", plot_width=800, tools=[hover])
p.quad(top='max_t', bottom='min_t', left='timel', right='timer', source=source, alpha=0.5, color='RoyalBlue', line_color="black", line_alpha=0.5, legend='Min/Max')
p.line(x='time', y='mean_t', source = source, color='red', line_width = 1.5, alpha=0.8, legend='Average')
p.x_range = DataRange1d(range_padding=0, bounds=None)
p.yaxis.axis_label = "Temperature (C)"
p.xaxis.axis_label = 'Month'


# Select Data based on input info             
def select_data():
    #p.title = p.title + str(' (Wait..)')
    global station_IDs
    # Make Stations ID's as a list
    station_IDs=[]
    [station_IDs.append(int(n)) for n in station_IDs_str.value.split()]
    
    # Select Data based on input info             
    logic_str = ('WHERE year=' + str(selected_year.value) 
                 + ' AND station_id=' + str(station_IDs[0]))
    selected_data = read_from_sql(columns='station_id, t_min, t_max, t_mean, datastamp', logic = logic_str)
    selected_data = pd.DataFrame(selected_data)
    old_names = np.arange(7) 
    new_names = ['ID', 'Min', 'Max', 'Mean', 'Time']
    selected_data.rename(columns=dict(zip(old_names, new_names)), inplace=True)
    return selected_data

#Update function
def update(attrname, old, new):
    df = select_data()
    if len(df)==0:
        p.title = "No Data Availabe!"
        source.data = dict(min_t=0)
    else:
        # Change DateTime Format
        df['Time'] = pd.to_datetime(df['Time'])        
        
        # Update plot data source      
        #p.title = "Annual Cycle of Min/Max Daily Temperatures"
        source.data = dict(
            min_t=df['Min'],
            max_t=df['Max'],
            mean_t=df['Mean'],
            timel=df['Time']- pd.DateOffset(days=.5),
            timer=df['Time']+ pd.DateOffset(days=.5),
            time=df['Time'],
            date_str=[str(each_row.date()) for each_row in df['Time']],
            station_id=df['ID']
            )
    
# Making plot visual and make updates
controls = [selected_year, station_IDs_str]
for control in controls:
    control.on_change('value', update)
#inputs = HBox(VBoxForm(*controls), width=300)
update(None, None, None) # initial load of the data
#curdoc().add_root(HBox(inputs, p))
curdoc().add_root(column(p))


# In[ ]:



