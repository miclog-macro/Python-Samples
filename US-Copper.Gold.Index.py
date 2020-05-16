# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 19:29:32 2019

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

### Copper/Gold Index vs US 10-Year #################################
## Data
start_data = date(2018, 1, 1)
today = datetime.now()

copper_gold_df = DataReader(['GOLDAMGBD228NLBM','DGS10'], 'fred', start_data, today)
copper_gold_df.columns = ['Gold','U.S. 10-Year']

copper = DataReader('CHRIS/CME_HG1', 'quandl', start_data, today ,access_key="h8vqKTPis9Jf25z6woGz")
copper = copper['Last']*100
copper = pd.DataFrame(copper)
copper.columns = ['copper']
copper_gold_df = copper_gold_df.join(copper, how='left')
copper_gold_df['C.G.Index'] = copper_gold_df['copper']/copper_gold_df['Gold']
copper_gold_df.ffill()

## Inputs
start = start_data
end = today
line1_1_color = 'red'
line2_1_color = 'blue'
linewidth = 3
title1 = 'Copper-Gold vs U.S. 10-Year'
title_fontsize = 30
y1_label_text = 'Copper-Gold Ratio'
y2_label_text= 'U.S. 10-Year Yield'
x1_label_text = ''
y1_label_fontsize = 20
x1_label_fontsize = 20
y1_tick_min = copper_gold_df['C.G.Index'].min().round(2)
y1_tick_max = copper_gold_df['C.G.Index'].max().round(2)
y1_tick_break = .01
y2_tick_min = copper_gold_df['U.S. 10-Year'].min().round(2)
y2_tick_max = copper_gold_df['U.S. 10-Year'].min().round(2)
y2_tick_break = .2
xtick_label_fontsize = 20
ytick_label_fontsize = 20
xlim_start = start_data
xlim_end = today + relativedelta(days=14)
text1 = 'Latest: '+ end.strftime("%m-%d-%Y")
text1_x = copper_gold_df.index[-1]
text1_y = copper_gold_df['C.G.Index'].max().round(2)
text1_fontsize = 20

plt.style.use('ggplot')
fig, ax1 = plt.subplots(figsize=(20,10))
ax1.plot(copper_gold_df['C.G.Index'], color=line1_1_color , linewidth=linewidth, linestyle='-')

# Labels
ax1.set_title(title1, fontsize=title_fontsize, loc='center', color = 'black', pad = 12, fontweight ='bold')
ax1.text(text1_x, text1_y, text1, fontsize = text1_fontsize, color = 'black', horizontalalignment='right')

# Y-axis
ax1.set_yticks(np.arange(y1_tick_min, y1_tick_max, y1_tick_break))
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = ytick_label_fontsize, labelcolor = 'black')
ax1.set_ylabel(y1_label_text, fontsize=y1_label_fontsize, labelpad=20, color = line1_1_color)

# X-axis
ax1.set_xlim(xlim_start, xlim_end)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax1.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=45, labelcolor = 'black')
ax1.tick_params(axis = 'x', which='minor',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')
# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

ax2 = ax1.twinx()
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax1.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=45, labelcolor = 'black')
ax1.tick_params(axis = 'x', which='minor',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')
ax2.set_ylabel(y2_label_text, fontsize=y1_label_fontsize, labelpad=20, color = line2_1_color)
ax2.plot(copper_gold_df['U.S. 10-Year'], color=line2_1_color, linewidth=linewidth, linestyle='solid')
ax2.grid(which='both',axis='y', b=None)
ax2.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                labelsize = ytick_label_fontsize, labelcolor = 'black')
fig.tight_layout()