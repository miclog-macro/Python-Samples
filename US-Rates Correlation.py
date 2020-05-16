# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 20:55:21 2019

@author: miclo
"""


# Modules
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import pandas_datareader.data as web
from pandas_datareader.data import DataReader

import datetime
from datetime import date, datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter, FormatStrFormatter
import matplotlib.dates as mdates
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib import rc, rcParams
from dateutil.relativedelta import relativedelta

## Stock Market capitalization vs GDP
## Data
start_data = datetime.now() - relativedelta(months=3)
today = datetime.now()

rates_df = DataReader(['DGS3MO','DGS6MO','DGS1','DGS2','DGS5','DGS10','DGS20','DGS30'], 'fred', start_data, today)
rates_df = rates_df.dropna()
rates_df.columns = ['3mo','6mo','1yr','2yr','5yr','10yr','20yr','30yr']

df_corr = rates_df.corr(method ='pearson')
df_corr.to_csv('ratescorr.csv')


data1 = df_corr.values
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)
fig1.colorbar(heatmap1)
ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)
ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)
ax1.invert_yaxis()
ax1.xaxis.tick_top()
#column_labels = df_corr.columns
#row_labels = df_corr.index

column_labels = ['3mo','6mo','1yr','2yr','5yr','10yr','20yr','30yr']
row_labels = ['3mo','6mo','1yr','2yr','5yr','10yr','20yr','30yr']

ax1.set_xticklabels(column_labels)
ax1.set_yticklabels(row_labels)

ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = 25, labelcolor = 'black')

ax1.tick_params(axis = 'x', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = 25, labelcolor = 'black')

plt.xticks(rotation=90)
heatmap1.set_clim(-1,1)
plt.tight_layout()
#plt.savefig("correlations.png", dpi = (300))
plt.show()






