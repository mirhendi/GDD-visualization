#!/usr/bin/python3
#This code will only test weather the user has these packages working

import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt
import bokeh
import io
import os
import fileinput
import re
import datetime
import urllib.request
import difflib
import sqlite3
import argparse
import pandas as pd
import numpy as np
import codecs
from codecs import open as uopen

from bokeh.models.widgets import Slider, Select, TextInput

import pandas.io.sql as psql

from bokeh.plotting import Figure, show
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBoxForm, DataRange1d
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc, output_notebook, output_file
from datetime import datetime


#Now lets try to import our modules
from calc_GDD import calc_GDD

print("All modules are OK!")
