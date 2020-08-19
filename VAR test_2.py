# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:16:48 2020

@author: miclo
"""

#import required packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from datetime import date, datetime
from scipy import log, exp, sqrt, stats

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter, FormatStrFormatter
import matplotlib.dates as mdates
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib import rc, rcParams

from dateutil.relativedelta import relativedelta

#############################################################################
# UYS Consumer Spending
start_data = datetime.now() - relativedelta(years=66)
today = datetime.now()

# y1: consumer spending (Fred: PCE)
# y2: consumer confidence (Fred: UMCSENT - from Jan 1978)
# y3: unemployment (Fred: UNRATE)
# y4: hourly earnings, manufaac (Fred: LCEAMN01USM189S)
# y5: total consumer credit (Fred: TOTALSL)
# y6: retail sales (Fred: MRTSSM44X72USS - from Jan 1992)
# y8: housing starts (Fred: HOUST)
# autos
# healthcare
#avg hourly earnings (Fred: CES0500000003 - from Mar 2006)

from statsmodels.tsa.vector_ar.vecm import select_order
from statsmodels.tsa.vector_ar.vecm import select_coint_rank
from statsmodels.tsa.vector_ar.vecm import VECM

from dateutil.relativedelta import relativedelta
start_data = datetime.now() - relativedelta(years=66)
today = datetime.now()

from pandas_datareader.data import DataReader
consumer_df = DataReader(['PCE','UMCSENT','UNRATE','LCEAMN01USM189S',
                          'TOTALSL', 'MRTSSM44X72USS','HOUST'], 'fred', start_data, today)
consumer_df = consumer_df.dropna()
consumer_df.columns = ['PCE','ConConf','Unempl','HourlyEarning',
                    'CCredit','RetSales','HouseStarts']
consumer_df = consumer_df.resample('1M').mean()
type(consumer_df)

# lag order selection
lag_order = select_order(data=consumer_df, maxlags=10, deterministic="ci", seasons=12)
print(lag_order.summary())
print(lag_order)

# Cointegration rank
rank_test = select_coint_rank(consumer_df, 0, 2, method="trace", signif=0.05)
rank_test.rank
print(rank_test.summary())
print(rank_test)

# Parameter Estimation
model = VECM(consumer_df, deterministic="ci", seasons=12,
             k_ar_diff=lag_order.aic,  
             coint_rank=rank_test.rank)  
vecm_res = model.fit()
vecm_res.summary()

vecm_res.predict(steps=5)
vecm_res.predict(steps=5, alpha=0.05)
for text, vaĺues in zip(("forecast", "lower", "upper"), vecm_res.predict(steps=5, alpha=0.05)):
    print(text+":", vaĺues, sep="\n")
    
vecm_res.plot_forecast(steps=12, n_last_obs=6)


































