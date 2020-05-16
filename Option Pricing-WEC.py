# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 17:47:13 2019

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

start_data = datetime.now() - relativedelta(years=5)
today = datetime.now()
ticker = 'WEC'
date_6mo = datetime.now() - relativedelta(months=6)

stock = pdr.get_data_yahoo(ticker, start_data , today)
stock = stock['Close']
stock_returns = stock.pct_change()                  #all values below in % form
stock_corr_21d = stock_returns.rolling(21).std()
stock_corr_21d_ann = stock_corr_21d.multiply(sqrt(252))*100
stock_corr_10d = stock_returns.rolling(10).std()
stock_corr_10d_ann = stock_corr_10d.multiply(sqrt(252))*100
stock_corr_5d = stock_returns.rolling(5).std()
stock_corr_5d_ann = stock_corr_5d.multiply(sqrt(255))*100

##########################################################################################

# WEC X=$95, C=#0.35, Exp = 10/18
X = 95
exp_date = datetime(2019, 10, 18)
days_to_exp = (exp_date - today).days
purchase_date = datetime(2019, 6, 20)
purchase_days_to_exp = (exp_date-purchase_date).days
cost = 0.35
S_purchase = stock[purchase_date]

calls = options.get_calls(ticker, exp_date)
V_market = pd.to_numeric(calls.loc[calls['Strike']==X, 'Last Price'].iloc[0])
IV_exp_yahoo = pd.to_numeric(calls.loc[calls['Strike']==X, 'Implied Volatility'].iloc[0].rstrip('%'))/100

##Implied Volatility - CALL
#def implied_vol_call(S,X,T,r,c):
#    from scipy import log, exp, sqrt, stats
#    for i in range(20000):
#        sigma=0.005*(i+1)
#        d1=(log(S/X)+(r+sigma*sigma/2.)*T)/(sigma*sqrt(T))
#        d2=d1-sigma*sqrt(T)
#        diff=c-(S*stats.norm.cdf(d1)-X*exp(-r*T)*stats.norm.cdf(d2))
#        if abs(diff)<=0.02:
#            return i,sigma,diff
##implied_vol_call(40,40,0.5,.05,3.3)
#implied_vol_call(90.42, 95, days_to_exp/365, 0, .96)


from scipy.stats import norm
n = norm.pdf
N = norm.cdf

def bs_price(cp_flag,S,K,T,r,v,q=0.0):
    d1 = (log(S/K)+(r+v*v/2.)*T)/(v*sqrt(T))
    d2 = d1-v*sqrt(T)
    if cp_flag == 'c':
        price = S*exp(-q*T)*N(d1)-K*exp(-r*T)*N(d2)
    else:
        price = K*exp(-r*T)*N(-d2)-S*exp(-q*T)*N(-d1)
    return price

def bs_vega(cp_flag,S,K,T,r,v,q=0.0):
    d1 = (log(S/K)+(r+v*v/2.)*T)/(v*sqrt(T))
    return S * sqrt(T)*n(d1)

def find_vol(target_value, call_put, S, K, T, r):
    MAX_ITERATIONS = 100
    PRECISION = 1.0e-5

    sigma = 0.5
    for i in range(0, MAX_ITERATIONS):
        price = bs_price(call_put, S, K, T, r, sigma)
        vega = bs_vega(call_put, S, K, T, r, sigma)

        price = price
        diff = target_value - price  # our root

        print( i, sigma, diff)

        if (abs(diff) < PRECISION):
            return sigma
        sigma = sigma + diff/vega # f(x) / f'(x)

    # value wasn't found, return best guess so far
    return sigma

# At Purchase
V_market = cost
K = 95
T = purchase_days_to_exp/365
S = S_purchase
r = 0
cp = 'c' # call option
implied_vol_purchase = find_vol(V_market, cp, S, K, T, r)

# WEC X=$95, cost=$0.35, Exp = 10/18
V_market = V_market
K = 95
T = days_to_exp/365
S = stock[-1]
r = 0
cp = 'c' # call option

implied_vol = find_vol(V_market, cp, S, K, T, r)

print('Implied vol: %.2f%%' % (implied_vol * 100))
print('YahooFinance Implied vol: %.2f%%' % (IV_exp_yahoo*100))
print('Implied vol at Purchase: %.2f%%' % (implied_vol_purchase * 100))
print('Market price = %.2f' % V_market)
print('Model price = %.2f' % bs_price(cp, S, K, T, r, implied_vol))

import py_vollib.black_scholes.greeks.analytical

S = S
K = K
r = 0
t = T
sigma = implied_vol
flag = cp

py_vollib.black_scholes.greeks.analytical.delta(flag, S, K, t, r, sigma)



#############################################################################################

## Inputs
plt.style.use('ggplot')
xlim_start = datetime.now() - relativedelta(months=3)
xlim_end = today + relativedelta(days=3)
line1_Laxis_color = 'red'
line2_Laxis_color = 'blue'
line3_Laxis_color = 'green'
linewidth = 3
title1 = 'WEC Rolling Historical Volatility'
title_fontsize = 30
y1_label_text = ''
y2_label_text= ''
x1_label_text = ''
y1_label_fontsize = 25
x1_label_fontsize = 25
y1_tick_min = 0
y1_tick_max = 30
y1_tick_break = 5
#y2_tick_min = 
#y2_tick_max = 
#y2_tick_break = 
xtick_label_fontsize = 20
ytick_label_fontsize = 20
#text1 = ''
##'Latest: '+ end.strftime("%m-%d-%Y")
#text1_x = stock_corr_21d_ann.index[-15]
#text1_y = stock_corr_5d_ann.max()
#text1_fontsize = 20
annotate_text1 = 'IV: WEC c$95 10/18/19 | Days to Expiration: ' + str(days_to_exp)
annotate_text2 = 'IV at Purchase Date | Days to Expiration: ' + str(purchase_days_to_exp)

fig, ax1 = plt.subplots(figsize=(20,10))
ax1.plot(stock_corr_21d_ann[xlim_start:today], color=line1_Laxis_color , linewidth=linewidth, linestyle='-')
ax1.plot(stock_corr_10d_ann[xlim_start:today], color=line2_Laxis_color , linewidth=linewidth, linestyle='-')
ax1.plot(stock_corr_5d_ann[xlim_start:today], color=line3_Laxis_color , linewidth=linewidth, linestyle='-')

# Labels
ax1.set_title(title1, fontsize=title_fontsize, loc='center', color = 'black', pad = 12, fontweight ='bold')
ax1.axhline(y=implied_vol*100, color='black', linestyle='-', linewidth=2)
ax1.axhline(y=implied_vol_purchase*100, color='black', linestyle='-', linewidth=2)

ax1.annotate(annotate_text1,
             xytext=(xlim_start+ relativedelta(days=3),
                     stock_corr_5d_ann[xlim_start:today].max()),   #text
             fontsize=26, color = 'black', horizontalalignment='left',             
             xy=(xlim_start+ relativedelta(days=3),
                 implied_vol*100),     #end of arrow point
             arrowprops=dict(color='black',
                             linewidth=2, mutation_scale=10))
             
ax1.annotate(annotate_text2,
             xytext=(xlim_start + relativedelta(days=7),
                     stock_corr_5d_ann[xlim_start:today].max()-3),   #text
             fontsize=26, color = 'black', horizontalalignment='left',             
             xy=(xlim_start + relativedelta(days=7), implied_vol_purchase*100),     #end of arrow point
             arrowprops=dict(color='black',
                             linewidth=2, mutation_scale=10))

# Y-axis
ax1.set_yticks(np.arange(y1_tick_min, y1_tick_max, y1_tick_break))
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = ytick_label_fontsize, labelcolor = 'black')
ax1.set_ylabel(y1_label_text, fontsize=y1_label_fontsize, labelpad=20, color = 'black')
ax1.yaxis.set_major_formatter(PercentFormatter(decimals=1))

# X-axis
ax1.set_xlim(xlim_start, xlim_end)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=15))
ax1.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=45, labelcolor = 'black')
ax1.tick_params(axis = 'x', which='minor',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')
# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

ax1.legend(['21-day','10-day','5-day'],
                 framealpha = 50, loc = 'lower left', ncol = 3,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=15,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = .5)

##########################################################

stock = S
strike = K
time = T
risk_free_rate = r
sigma = stock_corr_21d_ann.iloc[[-1]].item()/100

d1 = ((log(stock / strike) + (risk_free_rate + 0.5 * sigma *sigma) * time) / (sigma * sqrt (time)))

d1num = (log(stock / strike) + (risk_free_rate + 0.5 * sigma *sigma) * time)

d2 = d1 - sigma * sqrt(time)

def delta_call_europe(d1):
    return norm.cdf(d1)
def delta_put_europe(d1):
    return -(norm.cdf(-d1))

delta_call_europe(d1)

#########################################################################

oil = DataReader('DCOILWTICO', 'fred', start_data, today)
oil.columns = ['WTI']
wec = pdr.get_data_yahoo('WEC', start_data , today)
wec = wec['Close']
wec = pd.DataFrame(wec)

wec_oil_df = wec.join(oil['WTI'], how='left')
wec_oil_df = wec_oil_df[wec_oil_df['WTI'].notnull()]   # drop rows with NaN
wec_oil_df['SP500_PctReturn'] = wec_oil_df['Close'].pct_change()
wec_oil_df['Oil_PctReturn'] = wec_oil_df['WTI'].pct_change()
wec_oil_df['SP500_LogReturn'] = np.log(1+wec_oil_df['SP500_PctReturn'])
wec_oil_df['Oil_LogReturn'] = np.log(1+wec_oil_df['Oil_PctReturn'])

wec_oil_df['1MoCorr_Prices'] = wec_oil_df['Close'].rolling(22).corr(wec_oil_df['WTI'])
wec_oil_df['1MoCorr_PctReturn'] = wec_oil_df['SP500_PctReturn'].rolling(22).corr(wec_oil_df['Oil_PctReturn'])
wec_oil_df['1MoCorr_LogReturn'] = wec_oil_df['SP500_LogReturn'].rolling(22).corr(wec_oil_df['Oil_LogReturn'])

## Inputs
plt.style.use('ggplot')
xlim_start = date(2019,1,1)
xlim_end = datetime.now()
line1_Laxis_color = 'red'
line2_Laxis_color = 'blue'
line3_Laxis_color = 'green'
linewidth = 3
title1 = 'WEC/WTI Correlation'
title_fontsize = 30
y1_label_text = ''
y2_label_text= ''
x1_label_text = ''
y1_label_fontsize = 25
x1_label_fontsize = 25
y1_tick_min = -1
y1_tick_max = 1
y1_tick_break = .2
#y2_tick_min = 
#y2_tick_max = 
#y2_tick_break = 
xtick_label_fontsize = 20
ytick_label_fontsize = 20
#text1 = ''
##'Latest: '+ end.strftime("%m-%d-%Y")
#text1_x = stock_corr_21d_ann.index[-15]
#text1_y = stock_corr_5d_ann.max()
#text1_fontsize = 20

fig, ax1 = plt.subplots(figsize=(20,10))
ax1.plot(wec_oil_df['1MoCorr_Prices'][xlim_start:today], color=line1_Laxis_color , linewidth=linewidth, linestyle='-')
ax1.plot(wec_oil_df['1MoCorr_PctReturn'][xlim_start:today], color=line2_Laxis_color , linewidth=linewidth, linestyle='-')
ax1.plot(wec_oil_df['1MoCorr_LogReturn'][xlim_start:today], color=line3_Laxis_color , linewidth=linewidth, linestyle='-')

# Labels
ax1.set_title(title1, fontsize=title_fontsize, loc='center', color = 'black', pad = 12, fontweight ='bold')
ax1.axhline(y=0, color='black', linestyle='-', linewidth=2)

# Y-axis
ax1.set_yticks(np.arange(y1_tick_min, y1_tick_max, y1_tick_break))
ax1.tick_params(axis = 'y', which='major', # Options for both major and minor ticks
                left='on', right='off', labelsize = ytick_label_fontsize, labelcolor = 'black')
ax1.set_ylabel(y1_label_text, fontsize=y1_label_fontsize, labelpad=20, color = 'black')
ax1.yaxis.set_major_formatter(PercentFormatter(decimals=1))

# X-axis
ax1.set_xlim(xlim_start, xlim_end)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=15))
ax1.tick_params(axis = 'x', which='major',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=45, labelcolor = 'black')
ax1.tick_params(axis = 'x', which='minor',
                top='off', bottom='on',
                labelsize = xtick_label_fontsize, rotation=0, labelcolor = 'black')
# Grid
ax1.grid(which='minor', linestyle='-', linewidth=1, color='white', alpha=1)
ax1.grid(which='major', linestyle='-', linewidth=1, color='white', alpha=1)

ax1.legend(['Prices','PctReturn','LogReturn'],
                 framealpha = 50, loc = 'lower left', ncol = 3,
                 labelspacing = 1,
                 handlelength = 3,
                 fontsize=15,
                 edgecolor = 'black',
                 facecolor = 'white',
                 handletextpad=1,
                 borderpad = .5)



