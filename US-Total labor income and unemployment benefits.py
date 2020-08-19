# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 16:07:46 2020

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
from scipy import log, exp, sqrt, stats

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter, FormatStrFormatter
import matplotlib.dates as mdates
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib import rc, rcParams

from dateutil.relativedelta import relativedelta
from yahoo_fin import options

#############################################################################################
start_data = datetime.now() - relativedelta(years=80)
today = datetime.now()

ticker = ['W209RC1','W825RC1','CPALTT01USM657N']
LaborComp_data_pull = DataReader(ticker, 'fred', start_data, today)
LaborComp = LaborComp_data_pull
LaborComp.columns = ['EC','UI','CPI_1']    #EC=Employee compensation   UI=Unemployment insurance
LaborComp['CPI_1'] = LaborComp['CPI_1']/100
LaborComp['Total'] = LaborComp['EC']+LaborComp['UI']

LaborComp = LaborComp[12:]   # DROPPING FIRST ROWS
#Dropping Rows https://chrisalbon.com/python/data_wrangling/pandas_dropping_column_and_rows/

LaborComp['CPI_1'].iloc[-1] = LaborComp['CPI_1'].iloc[-5:-2].mean()



CPI_1_index=[]
CPI_1_index.append(100)
for i in range(len(LaborComp['CPI_1'])):
    CPI_1_index.append(
        CPI_1_index[i]*(1+LaborComp['CPI_1'].values[i])
        )

CPI_1_index_df = pd.DataFrame(CPI_1_index,columns=['CPI_1_index'])

type(CPI_1_index_df)

CPI_1_index_df = pd.DataFrame({'Date': LaborComp.index, 'CPI_1_index': CPI_1_index[1:]})
CPI_1_index_df = CPI_1_index_df.set_index('Date')

LaborComp['CPI_1_index']=CPI_1_index_df['CPI_1_index']

LaborComp['Total_real1960'] = LaborComp['Total']/CPI_1_index_df['CPI_1_index']*100

LaborComp['Total_real1960_12moPctChng'] = ((LaborComp['Total_real1960']/LaborComp['Total_real1960'].shift(12))-1)

#sp500_d = DataReader('SP500', 'fred', start_data, today)
#sp500_d.resample('1M').mean()                            #CONVERTING TO MONTHLY (AVG)

sp500_m = pd.read_csv('MacroTrends_Data_Download.csv')
sp500_m["date"] = pd.to_datetime(sp500_m["date"]).dt.strftime('%Y-%m-%d')
sp500_m = sp500_m.set_index(sp500_m['date'])

sp500_m['sp500_m_real1969'] = sp500_m['nominal'][385:-2]/CPI_1_index_df['CPI_1_index']*100

sp500_m['sp500_m_real1969_pctret'] = (sp500_m['sp500_m_real1969']/sp500_m['sp500_m_real1969'].shift(12)-1)

# Adjust S&P for same inflation
# take 12 mo return
# then 12mo log return = log(today) - log(today.shift(12))


#############################################################################################

## Inputs
plt.style.use('ggplot')
xlim_start = LaborComp['Total_real1960_12moPctChng'].notna().idxmax().to_pydatetime()
xlim_end = today
line1_Laxis_color = 'black'
linewidth = 3
title1 = 'Total Labor Income and Unemployment Benefits\nNet Yearly % Change in real 1960 Index USD'
title_fontsize = 20
y1_label_text = 'Real 1-yr Change'
y2_label_text= 'Log(S&P500)'
x1_label_text = ''
y1_label_fontsize = 25
x1_label_fontsize = 28
y1_tick_min = -.05
y1_tick_max = .09
y1_tick_break =.01
xtick_label_fontsize = 20
ytick_label_fontsize = 20

plt.style.use('ggplot')
fig, ax1 = plt.subplots(figsize=(20,8))
widths = [d.days for d in np.diff(LaborComp.index.tolist())]
ax1.bar(LaborComp.index, LaborComp['Total_real1960_12moPctChng'],width=.8*widths[0],
         color=(LaborComp['Total_real1960_12moPctChng'] > 0).map({True: 'g', False: 'r'}))

# X-axis
#ax1.xlim(xlim_start, xlim_end)
ax1.xaxis.set_major_formatter(DateFormatter('%Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=60))
ax1.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')
ax1.tick_params(axis = 'x', which='minor',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')
ax1.margins(x=0.02)
#Data
#LaborComp['Total_real1960_12moPctChng'][xlim_start:today].plot(kind='bar',
#         color=(LaborComp['Total_real1960_12moPctChng'] > 0).map({True: 'g', False: 'r'}))

# Labels
plt.title(title1, fontsize=title_fontsize, loc='center', color = 'black', pad = 12, fontweight ='bold')
plt.xlabel('')

# Shading
ax1.axvspan('2020-02-01', today, color='gray', alpha=0.5)
ax1.axvspan('2007-12-01', '2009-06-01', color='gray', alpha=0.5)
ax1.axvspan('2001-03-01', '2001-11-01', color='gray', alpha=0.5)
ax1.axvspan('1990-07-01', '1991-03-01', color='gray', alpha=0.5)
ax1.axvspan('1981-07-01', '1982-11-01', color='gray', alpha=0.5)
ax1.axvspan('1980-01-01', '1980-07-01', color='gray', alpha=0.5)
ax1.axvspan('1973-11-01', '1975-03-01', color='gray', alpha=0.5)
ax1.axvspan('1969-12-01', '1970-11-01', color='gray', alpha=0.5)
#ax1.axvspan('1960-04-01', '1961-02-01', color='gray', alpha=0.5)

# Y-axis
plt.yticks(np.arange(y1_tick_min, y1_tick_max, y1_tick_break))
plt.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = ytick_label_fontsize, labelcolor = 'black')
plt.ylabel(y1_label_text, fontsize=y1_label_fontsize, labelpad=20, color = 'black')

# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

#ax2 = ax1.twinx()
##plt.style.use('ggplot')
##fig, ax2 = plt.subplots(figsize=(20,10))
##ax2.xaxis.set_major_formatter(DateFormatter('%Y'))
##ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=60))
#ax2.set_ylabel(y2_label_text, fontsize=y1_label_fontsize, labelpad=20, color = 'green')
#ax2.plot(LaborComp.index,
#         sp500_m['sp500_m_real1969_pctret'][385:-2],
#         color='yellow', linewidth=4, linestyle='solid')
#ax2.grid(b=False)
#ax2.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
#                labelsize = 20, labelcolor = 'black')
#fig.tight_layout()


#############################################################################################