# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 19:27:28 2019

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

#####################################################################################
## VIX racker
## Data
start_data = date(2019, 7, 1)
today = datetime.now()

vix = pdr.get_data_yahoo('^VIX', start_data, today)

#####################################################################################

## Inputs
start = start_data
end = date(2019, 8, 30)
line1_1_color = 'blue'
linewidth = 3
title1 = 'CBOE VIX (July - August 2019)'
title_fontsize = 30
y1_label_text = ''
x1_label_text = ''
y1_label_fontsize = 25
x1_label_fontsize = 25
y1_tick_min = 10
y1_tick_max = 28
y1_tick_break = 2
xtick_label_fontsize = 25
ytick_label_fontsize = 25
xlim_start = start_data
xlim_end = end

fig, ax1 = plt.subplots(nrows=1, ncols=1)
plt.style.use('ggplot')

ax1.plot(vix['Close']['2019-7-1':'2019-8-30'], color=line1_1_color , linewidth=linewidth, linestyle='-')

# Labels
ax1.set_title(title1, fontsize=title_fontsize, loc='center', color = 'black', pad = 12, fontweight ='bold')

ax1.annotate('FOMC rate cut',
             xytext=('2019-7-23', vix['Close']['2019-7-31']), # text
             fontsize=26, color = 'black',              
             xy=('2019-07-31', vix['Close']['2019-7-31']),     #end of arrow point
             arrowprops=dict(color='black',
                             linewidth=2, mutation_scale=10))

ax1.annotate('Trump Tweet',
             xytext=('2019-7-24', vix['Close']['2019-08-1']+2), # text
             fontsize=26, color = 'black',              
             xy=('2019-08-1', vix['Close']['2019-08-1']),     #end of arrow point
             arrowprops=dict(color='black',
                             linewidth=2, mutation_scale=10))

ax1.annotate('Yuan Devaluation',
             xytext=('2019-7-24', vix['Close']['2019-08-2']), # text
             fontsize=26, color = 'black',               
             xy=('2019-08-2', vix['Close']['2019-08-2']),     #end of arrow point
             arrowprops=dict(color='black',
                             linewidth=2, mutation_scale=10))

ax1.annotate('U.S. 10yr-2yr inverts',
             xytext=('2019-08-10', vix['Close']['2019-08-14']), # text
             fontsize=26, color = 'black', horizontalalignment='right',          
             xy=('2019-08-14', vix['Close']['2019-08-14']),     #end of arrow point
             arrowprops=dict(color='black',
                             linewidth=2, mutation_scale=10))

ax1.annotate('China $75B tariff announcement',
             xytext=('2019-8-20', vix['Close']['2019-08-23']+1), # text
             fontsize=26, color = 'black', horizontalalignment='right',          
             xy=('2019-08-23', vix['Close']['2019-08-23']),     #end of arrow point
             arrowprops=dict(color='black',
                             linewidth=2, mutation_scale=10))


# Y-axis
ax1.set_yticks(np.arange(y1_tick_min, y1_tick_max, y1_tick_break))
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = ytick_label_fontsize, labelcolor = 'black')
#ax1.yaxis.set_minor_locator(MultipleLocator(5))

# X-axis
ax1.set_xlim(xlim_start, xlim_end)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=45, labelcolor = 'black')
ax1.tick_params(axis = 'x', which='minor',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')

# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)