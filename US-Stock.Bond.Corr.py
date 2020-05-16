# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 08:52:24 2019

@author: miclo
"""

# Clear variable explorer: %reset
# help(function) -- shows arguments

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
#
#pip uninstall iexfinance
#pip install iexfinance --upgrade
#from iexfinance.stocks import Stock
#from iexfinance.stocks import get_historical_data

## Dates
start = date(1990, 1, 1)
end = date(2019, 6, 1)
today = datetime.now()

## Data Pulls
sp500 = pdr.get_data_yahoo('^GSPC', start, today)
US6mo = DataReader(['DGS6MO'], 'fred', start, today)
SP500_US6mo_df = sp500.join(US6mo, how = 'left')
SP500_US6mo_df = SP500_US6mo_df.drop(columns=['High','Low','Open','Volume','Adj Close'])
dxy = pdr.get_data_yahoo('DX-Y.NYB', start, today)
dxy = pd.DataFrame(dxy.Close)
dxy.columns = ['DXY']
SP500_US6mo_df = SP500_US6mo_df.join(dxy, how = 'left')
effectiveFFR = DataReader('DFF', 'fred', start, today)
SP500_US6mo_df = SP500_US6mo_df.join(effectiveFFR, how = 'left')

SP500_US6mo_df['Close_PctChng'] = SP500_US6mo_df['Close'].pct_change()
SP500_US6mo_df['Close_LogRtn'] = np.log(1+SP500_US6mo_df['Close_PctChng'])
SP500_US6mo_df['DGS6MO'] = SP500_US6mo_df['DGS6MO'].ffill()
SP500_US6mo_df['1-Year Correlation'] = SP500_US6mo_df['Close'].rolling(252).corr(SP500_US6mo_df['DGS6MO'])
SP500_US6mo_df['2-Year Correlation'] = SP500_US6mo_df['Close'].rolling(504).corr(SP500_US6mo_df['DGS6MO'])
SP500_US6mo_df['5-Year Correlation'] = SP500_US6mo_df['Close'].rolling(1260).corr(SP500_US6mo_df['DGS6MO'])
# Day count - see number of rows: SP500_US6mo_df.loc['2018-08-02':'2019-08-02']
SP500_US6mo_df = SP500_US6mo_df.resample('1M').mean()

## Chart
plt.style.use('ggplot')
SP500_US6mo_df['1-Year Correlation'].plot(color='blue', linewidth=5, linestyle=':', x_compat=True)
SP500_US6mo_df['2-Year Correlation'].plot(color='red',linewidth=5, linestyle='--', x_compat=True)
SP500_US6mo_df['5-Year Correlation'].plot(color='purple', linewidth=5, linestyle='solid',x_compat=True)

# Lines and Shading
plt.axhline(y=0, color='black', linestyle='-', linewidth=3)
plt.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
plt.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)

# Labels
plt.title('S&P500 Return vs 6-Month Treasury Constant Maturity Rate',
          fontsize=40, loc='left', color = 'black', pad = 20)
plt.xlabel('', fontsize=20, labelpad=20)
plt.text(SP500_US6mo_df.index[-10], .98, today.strftime("%m/%d/%Y"),
         fontsize=18, color = 'black', horizontalalignment='right')

# Y-axis
plt.yticks(np.arange(-1, 1, .1))   #plt.xticks(tick_val, tick_lab) - 2nd argument for tick labels
#plt.axes().yaxis.set_minor_locator(MultipleLocator(.125))
plt.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='on', labelright = False,
                labelsize = 20,rotation=0,labelcolor = 'black')

# X-axis
plt.xlim([date(1995, 1, 1), today])
plt.axes().xaxis.set_major_locator(mdates.MonthLocator(interval=12))
plt.axes().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.tick_params(axis = 'x', which='major', # Options for both major and minor ticks
                top='off', bottom='on',
                labelsize = 15, rotation=45, labelcolor = 'black')

# Both axes
plt.tick_params(axis = 'both', which='minor',
                top='off', left='on', right='off', bottom='on', labelsize = 8)

# Grid
plt.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
plt.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

# Legend
leg = plt.legend(['1-Year','2-Year', '5-Year'],
                 framealpha = 50, loc = 'lower left', ncol = 3,
                 labelspacing = 1,
                 handlelength = 3,
                 edgecolor = 'black',
                 facecolor = 'white',
#                 bbox_to_anchor=(.1, -.2, 0, 0),    #(x0, y0, width, height)
                 handletextpad=1,
                 borderpad = 3)
for text in leg.get_texts():
    plt.setp(text, color = 'black', fontsize=30)

## Recessions
#plt.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
#plt.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)
#plt.axvspan('1990-07-01', '1991-03-01', color='gray', alpha=0.5)
#plt.axvspan('1981-07-01', '1982-11-01', color='gray', alpha=0.5)
#plt.axvspan('1980-01-01', '1980-07-01', color='gray', alpha=0.5)


plt.style.use('ggplot')
fig, ax1 = plt.subplots()
ax1.plot(SP500_US6mo_df['1-Year Correlation'], color='blue', linewidth=3, linestyle=':')
ax1.plot(SP500_US6mo_df['2-Year Correlation'], color='red', linewidth=3, linestyle='-.')
ax1.plot(SP500_US6mo_df['5-Year Correlation'], color='purple', linewidth=3, linestyle='solid')

# Lines and Shading
ax1.axhline(y=0, color='black', linestyle='-', linewidth=3)
ax1.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
ax1.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)

# Labels
ax1.set_title('Correlation[S&P500 Return, 6-Month Treasury Constant Maturity Rate] vs DXY',
          fontsize=40, loc='left', color = 'black', pad = 20)
ax1.set_ylabel('Correlation', fontsize=20, labelpad=20, color = 'black')
ax1.set_xlabel('', fontsize=20, labelpad=20)
ax1.text(SP500_US6mo_df.index[-10], .98, today.strftime("%m/%d/%Y"),
         fontsize=18, color = 'black', horizontalalignment='right')

# Y-axis
ax1.set_yticks(np.arange(-1, 1, .1))   #plt.xticks(tick_val, tick_lab) - 2nd argument for tick labels
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='on', labelright = False,
                labelsize = 20,rotation=0,labelcolor = 'black')

# X-axis
ax1.set_xlim([date(2000, 1, 1), today])
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=12))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.tick_params(axis = 'x', which='major', # Options for both major and minor ticks
                top='off', bottom='on',
                labelsize = 20, rotation=45, labelcolor = 'black')

# Both axes
ax1.tick_params(axis = 'both', which='minor',
                top='off', left='on', right='off', bottom='on', labelsize = 8)

# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

# 2nd Axis
ax2 = ax1.twinx()
ax2.set_ylabel('DXY', fontsize=20, labelpad=20, color = 'black')
ax2.plot(SP500_US6mo_df['DXY'], color='green', linewidth=4, linestyle='solid')
ax2.grid(which='both',axis='y', b=None)
ax2.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                labelsize = 20, labelcolor = 'black')
fig.tight_layout()
# Legend
ax1.legend(['1-Year','2-Year', '5-Year'],
                 framealpha = 50, loc = 'lower left', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=20,
                 title="Correlation:",
                 title_fontsize = 20,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = 1)
ax2.legend(['DXY'],
                 framealpha = 50, loc = 'lower right', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=20,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = 1)


#################################################################################


plt.style.use('ggplot')
fig, ax1 = plt.subplots()
ax1.plot(SP500_US6mo_df['1-Year Correlation'], color='blue', linewidth=3, linestyle=':')
ax1.plot(SP500_US6mo_df['2-Year Correlation'], color='red', linewidth=3, linestyle='-.')
ax1.plot(SP500_US6mo_df['5-Year Correlation'], color='purple', linewidth=3, linestyle='solid')

# Lines and Shading
ax1.axhline(y=0, color='black', linestyle='-', linewidth=3)
ax1.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
ax1.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)

# Labels
ax1.set_title('Correlation[S&P500 Return, 6-Month Treasury Constant Maturity Rate] vs Fed Funds Rate',
          fontsize=40, loc='left', color = 'black', pad = 20)
ax1.set_ylabel('Correlation', fontsize=20, labelpad=20, color = 'black')
ax1.set_xlabel('', fontsize=20, labelpad=20)
ax1.text(SP500_US6mo_df.index[-10], .98, today.strftime("%m/%d/%Y"),
         fontsize=18, color = 'black', horizontalalignment='right')

# Y-axis
ax1.set_yticks(np.arange(-1, 1, .1))   #plt.xticks(tick_val, tick_lab) - 2nd argument for tick labels
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='on', labelright = False,
                labelsize = 20,rotation=0,labelcolor = 'black')

# X-axis
ax1.set_xlim([date(2000, 1, 1), today])
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=12))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.tick_params(axis = 'x', which='major', # Options for both major and minor ticks
                top='off', bottom='on',
                labelsize = 20, rotation=45, labelcolor = 'black')

# Both axes
ax1.tick_params(axis = 'both', which='minor',
                top='off', left='on', right='off', bottom='on', labelsize = 8)

# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

# 2nd Axis
ax2 = ax1.twinx()
ax2.set_ylabel('DFF', fontsize=20, labelpad=20, color = 'black')
ax2.plot(SP500_US6mo_df['DFF'], color='green', linewidth=4, linestyle='solid')
ax2.grid(which='both',axis='y', b=None)
ax2.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                labelsize = 20, labelcolor = 'black')
fig.tight_layout()
# Legend
ax1.legend(['1-Year','2-Year', '5-Year'],
                 framealpha = 50, loc = 'lower left', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=20,
                 title="Correlation:",
                 title_fontsize = 20,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = 1)
ax2.legend(['DFF'],
                 framealpha = 50, loc = 'lower right', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=20,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = 1)


####################################################################################

## Inputs
start = date(1990, 1, 1)
end = date(2019, 6, 1)
today = datetime.now()
line1_color = 'blue'
line2_color = 'red'
line3_color = 'purple'
line4_color = 'green'
linewidth = 3
title = 'Correlation[S&P500 Return, 6-Month Treasury Constant Maturity Rate] vs Fed Funds Rate'
title_fontsize = 40
y1_label_text = 'Correlation'
y1_label_fontsize = 20
x1_label_text = ''
x1_label_fontsize = 20
y1_tick_min = -1
y1_tick_max = 1
y1_tick_break = .1
y2_label_text = 'DFF'
y2_label_fontsize = 20

# Chart
plt.style.use('ggplot')
fig, ax1 = plt.subplots()
ax1.plot(SP500_US6mo_df['1-Year Correlation'], color=line1_color, linewidth=linewidth, linestyle=':')
ax1.plot(SP500_US6mo_df['2-Year Correlation'], color=line2_color, linewidth=linewidth, linestyle='-.')
ax1.plot(SP500_US6mo_df['5-Year Correlation'], color=line3_color, linewidth=linewidth, linestyle='solid')

# Lines and Shading
ax1.axhline(y=0, color='black', linestyle='-', linewidth=3)
ax1.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
ax1.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)

# Labels
ax1.set_title(title, fontsize=title_fontsize, loc='left', color = 'black', pad = 20)
ax1.set_ylabel(y1_label_text, fontsize=y1_label_fontsize, labelpad=20, color = 'black')
ax1.set_xlabel(x1_label_text, fontsize=x1_label_fontsize, labelpad=20)
ax1.text(SP500_US6mo_df.index[-10], .98, today.strftime("%m/%d/%Y"),
         fontsize=18, color = 'black', horizontalalignment='right')

# Y-axis
ax1.set_yticks(np.arange(y1_tick_min, y1_tick_max, y1_tick_break))   #plt.xticks(tick_val, tick_lab) - 2nd argument for tick labels
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='on', labelright = False,
                labelsize = 20,rotation=0,labelcolor = 'black')

# X-axis
ax1.set_xlim([date(2000, 1, 1), today])
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=12))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.tick_params(axis = 'x', which='major', # Options for both major and minor ticks
                top='off', bottom='on',
                labelsize = 20, rotation=45, labelcolor = 'black')

# Both axes
ax1.tick_params(axis = 'both', which='minor',
                top='off', left='on', right='off', bottom='on', labelsize = 8)

# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

# 2nd Axis
ax2 = ax1.twinx()
ax2.set_ylabel(y2_label_text, fontsize=y2_label_fontsize, labelpad=20, color = 'black')
ax2.plot(SP500_US6mo_df['DFF'], color=line4_color, linewidth=linewidth, linestyle='solid')
ax2.grid(which='both',axis='y', b=None)
ax2.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                labelsize = 20, labelcolor = 'black')
fig.tight_layout()
# Legend
ax1.legend(['1-Year','2-Year', '5-Year'],
                 framealpha = 50, loc = 'lower left', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=20,
                 title="Correlation:",
                 title_fontsize = 20,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = 1)
ax2.legend(['DFF'],
                 framealpha = 50, loc = 'lower right', ncol = 1,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=20,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = 1)


