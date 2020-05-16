# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 01:06:26 2019

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

# Data
start_data = date(1970, 1, 1)
today = datetime.now()  
US10Yr = DataReader(['DGS10'], 'fred', start_data, today)
US3Mo = DataReader(['DGS3MO'], 'fred', start_data, today)
US2Yr = DataReader(['DGS2'], 'fred', start_data, today)
USFedFundsRate = DataReader(['DFF'], 'fred', start_data, today)
TSpread_df = US10Yr.join(US3Mo, how = 'left')
TSpread_df = TSpread_df.join(US2Yr, how = 'left')
TSpread_df = TSpread_df.join(USFedFundsRate, how = 'left')
TSpread_df = TSpread_df.ffill()
TSpread_df.columns = ['US10Yr', 'US3Mo', 'US2Yr', 'USFedFundsRate']
TSpread_df.loc[:,['US10Yr', 'US3Mo', 'US2Yr', 'USFedFundsRate']] = TSpread_df.loc[:,['US10Yr', 'US3Mo', 'US2Yr', 'USFedFundsRate']].ffill()
TSpread_df['10Yr_3Yr'] = TSpread_df['US10Yr'] - TSpread_df['US3Mo']
TSpread_df['10Yr_FFR'] = TSpread_df['US10Yr'] - TSpread_df['USFedFundsRate']
TSpread_df['10Yr_2Yr'] = TSpread_df['US10Yr'] - TSpread_df['US2Yr']

## Inputs
start = date(1975, 1, 1)
end = datetime.now()
line1_color = 'blue'
line2_color = 'red'
line3_color = 'purple'
linewidth = 2
title1 = '10-Year - 3-Month'
title2 = '10-Year - Effective Federal Funds Rate'
title3 = '10-Year - 2-Year'
title_fontsize = 20
y1_label_text = ''
y1_label_fontsize = 15
x1_label_text = ''
x1_label_fontsize = 15
y1_tick_min = -1
y1_tick_max = 1
y1_tick_break = .1
y2_label_text = ''
y2_label_fontsize = 15
xtick_label_fontsize = 18

plt.style.use('ggplot')
fig, [[ax1, ax2], [ax3, ax4], [ax5, ax6]] = plt.subplots(nrows=3, ncols=2)
# 10Yr - 3Mo (1) ########################################################################
ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax1.plot(TSpread_df['US10Yr'], color=line1_color, linewidth=linewidth, linestyle='-')
ax1.plot(TSpread_df['US3Mo'], color=line2_color, linewidth=linewidth, linestyle='-')
ax1.plot(TSpread_df['10Yr_3Yr'], color=line3_color, linewidth=linewidth, linestyle='-')

# Lines and Shading
ax1.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
ax1.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)
ax1.axvspan('1990-07-01', '1991-03-01', color='gray', alpha=0.5)
ax1.axvspan('1981-07-01', '1982-11-01', color='gray', alpha=0.5)
ax1.axvspan('1980-01-01', '1980-07-01', color='gray', alpha=0.5)

ax1.fill_between(TSpread_df.index, 0, TSpread_df['10Yr_3Yr'],
                 where=TSpread_df['10Yr_3Yr'] <= 0, facecolor='red', alpha = .5)

# Labels
ax1.set_title(title1, fontsize=title_fontsize, loc='left', color = 'black', pad = 10, fontweight ='bold')

# Y-axis
ax1.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = 15, rotation=0, labelcolor = 'black')

# X-axis
ax1.xaxis.set_major_locator(mdates.YearLocator(5))
ax1.tick_params(axis = 'x', which='major', # Options for both major and minor ticks
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')

# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

# Legend
ax1.legend(['10-Year','3-Month', 'Spread'],
                 framealpha = 50, loc = 'upper right', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=15,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = .5)
leg = ax1.get_legend()
leg.legendHandles[0].set_color('blue')
leg.legendHandles[1].set_color('red')
leg.legendHandles[2].set_color('purple')
leg.legendHandles[0].set_linewidth(linewidth)


# 10Yr - 3Mo (2) ############################################################################
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2.plot(TSpread_df['US10Yr'].loc['2019-01-01':], color=line1_color, linewidth=linewidth, linestyle='-')
ax2.plot(TSpread_df['US3Mo'].loc['2019-01-01':], color=line2_color, linewidth=linewidth, linestyle='-')
ax2.plot(TSpread_df['10Yr_3Yr'].loc['2019-01-01':], color=line3_color, linewidth=linewidth, linestyle='-')

# Lines and Shading
ax2.fill_between(TSpread_df.index, 0, TSpread_df['10Yr_3Yr'],
                 where=TSpread_df['10Yr_3Yr'] <= 0, facecolor='red', alpha = .5)

# Labels
ax2.text(TSpread_df.index[-1], 3.1, today.strftime("%m/%d/%Y"),
         fontsize=20, color = 'black', horizontalalignment='right')
# Y-axis
ax2.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax2.yaxis.set_minor_locator(MultipleLocator(.5))
ax2.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = 15, rotation=0, labelcolor = 'black')
ax2.set_yticks(np.arange(-1, 3, 1))

# X-axis
ax2.set_xlim([date(2020, 1, 1), today])
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax2.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')
ax2.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

# Grid
ax2.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax2.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)


# 10Yr - FFR (3) ############################################################################
ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax3.plot(TSpread_df['US10Yr'], color=line1_color, linewidth=linewidth, linestyle='-')
ax3.plot(TSpread_df['USFedFundsRate'], color=line2_color, linewidth=linewidth, linestyle='-')
ax3.plot(TSpread_df['10Yr_FFR'], color=line3_color, linewidth=linewidth, linestyle='-')

# Lines and Shading
ax3.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
ax3.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)
ax3.axvspan('1990-07-01', '1991-03-01', color='gray', alpha=0.5)
ax3.axvspan('1981-07-01', '1982-11-01', color='gray', alpha=0.5)
ax3.axvspan('1980-01-01', '1980-07-01', color='gray', alpha=0.5)

ax3.fill_between(TSpread_df.index, 0, TSpread_df['10Yr_FFR'],
                 where=TSpread_df['10Yr_FFR'] <= 0, facecolor='red', alpha = .5)

# Labels
ax3.set_title(title2, fontsize=title_fontsize, loc='left', color = 'black', pad = 10, fontweight ='bold')

# Y-axis
ax3.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax3.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = 15, rotation=0, labelcolor = 'black')

# X-axis
ax3.xaxis.set_major_locator(mdates.YearLocator(5))
ax3.tick_params(axis = 'x', which='major', # Options for both major and minor ticks
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')

# Grid
ax3.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax3.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

ax3.legend(['10-Year','Fed Funds Rate', 'Spread'],
                 framealpha = 50, loc = 'upper right', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=15,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = .5)
leg = ax3.get_legend()
leg.legendHandles[0].set_color('blue')
leg.legendHandles[1].set_color('red')
leg.legendHandles[2].set_color('purple')
leg.legendHandles[0].set_linewidth(linewidth)

# 10Yr - FFR (4) ############################################################################
ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax4.plot(TSpread_df['US10Yr'].loc['2019-01-01':], color=line1_color, linewidth=linewidth, linestyle='-')
ax4.plot(TSpread_df['USFedFundsRate'].loc['2019-01-01':], color=line2_color, linewidth=linewidth, linestyle='-')
ax4.plot(TSpread_df['10Yr_FFR'].loc['2019-01-01':], color=line3_color, linewidth=linewidth, linestyle='-')

# Lines and Shading
ax4.fill_between(TSpread_df.index, 0, TSpread_df['10Yr_3Yr'],
                 where=TSpread_df['10Yr_3Yr'] <= 0, facecolor='red', alpha = .5)

# Y-axis
ax4.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax4.yaxis.set_minor_locator(MultipleLocator(.5))
ax4.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = 15, rotation=0, labelcolor = 'black')
ax4.set_yticks(np.arange(-1, 3, 1))

# X-axis
ax4.set_xlim([date(2020, 1, 1), today])
ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax4.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')

# Grid
ax4.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax4.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

# 10Yr - 2Yr (5) ############################################################################
ax5.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax5.plot(TSpread_df['US10Yr'], color=line1_color, linewidth=linewidth, linestyle='-')
ax5.plot(TSpread_df['US2Yr'], color=line2_color, linewidth=linewidth, linestyle='-')
ax5.plot(TSpread_df['10Yr_2Yr'], color=line3_color, linewidth=linewidth, linestyle='-')

# Lines and Shading
ax5.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
ax5.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)
ax5.axvspan('1990-07-01', '1991-03-01', color='gray', alpha=0.5)
ax5.axvspan('1981-07-01', '1982-11-01', color='gray', alpha=0.5)
ax5.axvspan('1980-01-01', '1980-07-01', color='gray', alpha=0.5)

ax5.fill_between(TSpread_df.index, 0, TSpread_df['10Yr_2Yr'],
                 where=TSpread_df['10Yr_2Yr'] <= 0, facecolor='red', alpha = .5)

# Labels
ax5.set_title(title3, fontsize=title_fontsize, loc='left', color = 'black', pad = 10, fontweight ='bold')

# Y-axis
ax5.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax5.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = 15, rotation=0, labelcolor = 'black')

# X-axis
ax5.xaxis.set_major_locator(mdates.YearLocator(5))
ax5.tick_params(axis = 'x', which='major', # Options for both major and minor ticks
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')

# Grid
ax5.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax5.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

ax5.legend(['10-Year','2-Year', 'Spread'],
                 framealpha = 50, loc = 'upper right', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=15,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = .5)
leg = ax5.get_legend()
leg.legendHandles[0].set_color('blue')
leg.legendHandles[1].set_color('red')
leg.legendHandles[2].set_color('purple')
leg.legendHandles[0].set_linewidth(linewidth)

# 10Yr - 2Yr (6) ############################################################################
ax6.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax6.plot(TSpread_df['US10Yr'].loc['2019-01-01':], color=line1_color, linewidth=linewidth, linestyle='-')
ax6.plot(TSpread_df['US2Yr'].loc['2019-01-01':], color=line2_color, linewidth=linewidth, linestyle='-')
ax6.plot(TSpread_df['10Yr_2Yr'].loc['2019-01-01':], color=line3_color, linewidth=linewidth, linestyle='-')

## Lines and Shading
#ax6.fill_between(TSpread_df.index, 0, TSpread_df['10Yr_3Yr'],
#                 where=TSpread_df['10Yr_3Yr'] <= 0, facecolor='red', alpha = .5)

# Y-axis
ax6.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax6.yaxis.set_minor_locator(MultipleLocator(.5))
ax6.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = 15, rotation=0, labelcolor = 'black')
ax6.set_yticks(np.arange(-1, 3, 1))

# X-axis
ax6.set_xlim([date(2020, 1, 1), today])
ax6.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax6.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax6.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')

# Grid
ax6.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax6.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

##########################################################################################
# Corporate Spreads

start_data = date(2018, 1, 1)
today = datetime.now()  
#corporate_spread_df = DataReader(['AAA10Y','BAA10Y'], 'fred', start_data, today)

## Inputs
plt.style.use('ggplot')
xlim_start = start_data
xlim_end = today
line1_Laxis_color = 'blue'
line2_Laxis_color = 'red'
linewidth = 3
title1 = 'Moodys Seasoned Corporate Bond Yields Relative to U.S. 10-Year'
title_fontsize = 30
y1_label_text = ''
y2_label_text= ''
x1_label_text = ''
y1_label_fontsize = 25
x1_label_fontsize = 25
y1_tick_min = 1.5
y1_tick_max = 3
y1_tick_break = .5
#y2_tick_min = 
#y2_tick_max = 
#y2_tick_break = 
xtick_label_fontsize = 20
ytick_label_fontsize = 20
text1 = 'Latest: '+ xlim_end.strftime("%m-%d-%Y")
text1_x = corporate_spread_df.index[-1]
text1_y = 1.7
text1_fontsize = 20


fig, ax1 = plt.subplots(figsize=(20,10))
ax1.plot(corporate_spread_df['AAA10Y'], color=line1_Laxis_color , linewidth=linewidth, linestyle='-')
ax1.plot(corporate_spread_df['BAA10Y'], color=line2_Laxis_color , linewidth=linewidth, linestyle='-')

# Labels
ax1.set_title(title1, fontsize=title_fontsize, loc='center', color = 'black', pad = 12, fontweight ='bold')
ax1.text(text1_x, text1_y, text1, fontsize = text1_fontsize, color = 'black', horizontalalignment='right')


# Y-axis
ax1.set_yticks(np.arange(y1_tick_min, y1_tick_max, y1_tick_break))
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = ytick_label_fontsize, labelcolor = 'black')
ax1.set_ylabel(y1_label_text, fontsize=y1_label_fontsize, labelpad=20, color = 'black')
ax1.yaxis.set_major_formatter(PercentFormatter(decimals=1))

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

ax1.legend(['Aaa','Baa'],
                 framealpha = 50, loc = 'upper left', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=15,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = .5)


















