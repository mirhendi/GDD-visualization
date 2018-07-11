import pandas as pd
import numpy as np

import pandas.io.sql as psql
import sqlite3 as sql

from bokeh.palettes import Spectral11
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.plotting import Figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, DataRange1d, CrosshairTool
from bokeh.io import curdoc, output_notebook, output_file
from datetime import datetime
from bokeh.models import DatetimeTickFormatter
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import column
from bokeh.layouts import row, widgetbox

import os
import sys
os.getcwd()
sys.path.extend([ os.getcwd() ])

from read_from_sql import read_from_sql
from get_new_data import get_new_data
from check_station_id import check_station_id

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data = dict(x = [], y = [], station_id = [], color = [], plot_year = []))

# Create Input controls
current_year = datetime.today().year
min_year = Slider(title="Year Start", start=1900, end=current_year, value=1900, step=1)
max_year = Slider(title="Year End", start=1900, end=current_year, value=current_year, step=1)
min_month = Slider(title="Month Start", start=1, end=12, value=1, step=1)
max_month = Slider(title="Month End", start=1, end=12, value=12, step=1)
base_temp = Slider(title="Base Temperature (C)", start=0, end=25, value=10, step=1)
station_IDs_str = TextInput(title="Station IDs", value='6720 6551')

# Create Figure and Plot
hover = HoverTool(tooltips=[("Station ID", "@station_id"), ("Year", "@year")])
p = Figure(plot_height=600, plot_width=800, title="", tools=[hover], x_axis_type="datetime")
p.multi_line(xs = 'x',ys = 'y', line_color = 'color', source = source, line_width = 2, )
p.x_range = DataRange1d(range_padding = 0.0, bounds = None)
#p.xaxis[0].formatter = DatetimeTickFormatter(formats=dict(days=["%B %d"], months=["%B"], years=["%Y"]))
p.yaxis.axis_label = 'Cumulative GDD'
p.xaxis.axis_label = 'Month'

# Select Data based on input info             
def select_data():
    #p.title = p.title + str(' (Wait..)')
    global station_IDs
    # Make Stations ID's as a list
    station_IDs=[]
    [station_IDs.append(int(n)) for n in station_IDs_str.value.split()]
    
    # Select Data based on input info             
    logic_str = ('WHERE year>=' + str(min_year.value) 
                 + ' AND year<=' + str(max_year.value)
                 + ' AND month>=' + str(min_month.value)
                 + ' AND month<=' + str(max_month.value)
                 + ' AND station_id IN (' + str(station_IDs)[1:-1:1]+')')
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
        
        # This section is for separating data base on station ID and year/
        # Each part of data that have a identical station ID and year will be presented as a line in plot
        df_identical_emp=[]
        for ID in station_IDs:
            for year in range (min_year.value, max_year.value + 1):
                df_identical_emp.append(df[(df.ID == ID) &
                                     (df.Time >= datetime(year,1,1)) &
                                     (df.Time <= datetime(year,12,28))])
        df_identical=[]
        
        #Remove empty parts
        for each_df in df_identical_emp:
            if not(each_df.empty):
                df_identical.append(each_df)
        
        # Store year of each part of data and assign an identical year on all data 
        # to be able to show them in the same time line.
        real_years=[]
        for i, each_df in enumerate(df_identical):
            real_years.append(df_identical[i].Time.iloc[0].year)
            time_edited = [each_row.replace(year=2000) for each_row in each_df.Time]
            df_identical[i].Time = time_edited

        # Calculate GDD 
        df_identical_mean = [each_df['Mean'] for each_df in df_identical]        
        GDD = [each_df-base_temp.value for each_df in df_identical_mean]
        for each_df_GDD in GDD:
            each_df_GDD[each_df_GDD<0]=0
        
        # Update plot data source
        source.data = dict(
            x = [each_df['Time'] for each_df in df_identical], # Prepare time stamp for X axes
            y = [np.cumsum(each_GDD) for each_GDD in GDD], # Cumulative GDD for Y axes
            color = Spectral11[0:len(df_identical)],
            plot_year = real_years
            )
        #p.title = "Accumulated Growing Degree Days"

# Making plot visual and make updates
controls = [base_temp, min_year, max_year, min_month, max_month, station_IDs_str ]
for control in controls:
    control.on_change('value', update)
#inputs = HBox(VBoxForm(*controls), width=300)
inputs = row(widgetbox(*controls), width=300)

update(None, None, None) # initial load of the data
#curdoc().add_root(HBox(inputs, p, width=1100))
#curdoc().add_root(column(p))
curdoc().add_root(row(inputs, p, width=1100))


html = file_html(p, CDN, "gdd_plot")
