# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 15:07:58 2017

@author: wpgardner
"""

import ulmo
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import pdb
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from climata.snotel import StationDailyDataIO

def ImportUsgsSiteDailyValues(siteno):
    sitename = {}
    sitename = ulmo.usgs.nwis.get_site_data(siteno, service="daily", period="all")
    siteinfo = sitename['00060:00003']['site']
    sitename = pd.DataFrame(sitename['00060:00003']['values'])
    sitename['dates'] = pd.to_datetime(pd.Series(sitename['datetime']))
    sitename.set_index(['dates'],inplace=True)
    sitename['value'] = sitename['value'].astype(float)
    sitename = sitename.replace('-999999',np.NAN)
    sitename = sitename.dropna()
    return sitename,siteinfo

def ImportSnotel(stationid,start_date='1950-1-1',end_date='2016-12-31'):
    '''wrapper for climata.  returns a date indexed dataframe of snow water equivalent'''
    print 'downloading snotel station data.'
    params = StationDailyDataIO(station=stationid,start_date='1966-1-1',end_date='2016-12-31')   
    print 'snotel download done.'
    df = params.as_dataframe()
#    swe=df.data[8].as_dataframe()
    swe = df.data[df.index[df.element_name=='SNOW WATER EQUIVALENT'].values[0]].as_dataframe()
    swe['date']=pd.to_datetime(swe.date)
    swe.set_index('date',inplace=True)
    swe=swe.dropna()
    return swe

def GetDailyStats(df,type='median',parameter='value',quantile=.5,water_year=True):
    grouped = df.groupby(df.index.dayofyear)
    if type == 'median':
        dfg = pd.DataFrame(grouped[parameter].median())
        try:
            dfg = dfg.drop(366) #get rid of leap day...
        except KeyError:
            dfg = dfg
        dfg['date']=dfg.index.map(dt.datetime.fromordinal)
        dfg.date=dfg.date+relativedelta(years=2015)
        dfg.date=pd.to_datetime(dfg.date)
    if type == 'mean':
        dfg = pd.DataFrame(grouped[parameter].mean())
        try:
            dfg = dfg.drop(366) #get rid of leap day...
        except KeyError:
            dfg = dfg
        dfg['date']=dfg.index.map(dt.datetime.fromordinal)
        dfg.date=dfg.date+relativedelta(years=2015)
        dfg.date=pd.to_datetime(dfg.date)
    if type == 'quantile':
        dfg = pd.DataFrame(grouped[parameter].quantile(q=quantile))
        try:
            dfg = dfg.drop(366) #get rid of leap day...
        except KeyError:
            dfg = dfg
        dfg['date']=dfg.index.map(dt.datetime.fromordinal)
        dfg.date=dfg.date+relativedelta(years=2015)
        dfg.date=pd.to_datetime(dfg.date)
        
    else:
        print 'type =', type, ' not recognized'
        print 'add stat type'
    if water_year:
        for i in dfg.index:
            if dfg.date[i].month >= 10:
                dfg.date[i] = dfg.date[i]-relativedelta(years=1)
        dfg.set_index('date',inplace=True)
        dfg=dfg.sort_index()
    else:
        dfg.set_index('date',inplace=True)
    return dfg


def GetMonthlyStats(df,type='median',parameter='value',quantile=.5,water_year=True):
    grouped = df.groupby(df.index.month)
    if type == 'median':
        dfg = pd.DataFrame(grouped[parameter].median())
        dfg['date']=pd.to_datetime('2015-' + dfg.index.astype(str) + '-15', format = '%Y-%m')
    if type == 'mean':
        dfg = pd.DataFrame(grouped[parameter].mean())
        dfg['date']=pd.to_datetime('2015-' + dfg.index.astype(str) + '-15', format = '%Y-%m')
    if type == 'quantile':
        dfg = pd.DataFrame(grouped[parameter].quantile(q=quantile))
        dfg['date']=pd.to_datetime('2015-' + dfg.index.astype(str) + '-15', format = '%Y-%m')
    if type == 'variance':
        dfg = pd.DataFrame(grouped[parameter].var())
        dfg['date']=pd.to_datetime('2015-' + dfg.index.astype(str) + '-15', format = '%Y-%m')
    if type == 'std':
        dfg = pd.DataFrame(grouped[parameter].std())
        dfg['date']=pd.to_datetime('2015-' + dfg.index.astype(str) + '-15', format = '%Y-%m')
    #else:
    #    print 'type =', type, ' not recognized'
    #    print 'add stat type'
    if water_year:
        for i in dfg.index:
            if dfg.date[i].month >= 10:
                dfg.date[i] = dfg.date[i]-relativedelta(years=1)
        dfg.set_index('date',inplace=True)
        dfg=dfg.sort_index()
    else:
        dfg.set_index('date',inplace=True)
    return dfg

def MakeAnAvHydrograph(siteno,parameter='value',quants='True',logdisch=True):
    fig, ax = plt.subplots()
    try:
        num = len(siteno)
    except TypeError:
        siteno = [siteno]
    for i in xrange(len(siteno)):    
        df,siteinfo = ImportUsgsSiteDailyValues(siteno[i])
        dvstat = GetDailyStats(df,parameter=parameter)
        if logdisch:
            lname = ax.semilogy(dvstat.index, dvstat[parameter],'b-',lw=2,label=siteinfo['name'])
        if logdisch == False:   
            lname = ax.plot(dvstat.index, dvstat[parameter],'b-',lw=2,label=siteinfo['name'])
        if quants:
            dvu = GetDailyStats(df,parameter=parameter,type='quantile',quantile=.75)
            dvl = GetDailyStats(df,parameter=parameter,type='quantile',quantile=.25)
            lname1 = ax.plot(dvu.index, dvu[parameter],'g-',lw=2,label='75th percentile')
            lname2 = ax.plot(dvl.index, dvl[parameter],'r-',lw=2,label='25th percentile')
            lns = lname + lname1 + lname2
            labs = [l.get_label() for l in lns]
            
    months = mdates.MonthLocator()   # every month
    monthsFmt = mdates.DateFormatter('%b')
    ## format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    # set limits
    datemin = dt.date(dvstat.index.min().year, 10, 1)
    datemax = dt.date(dvstat.index.max().year, 9, 30)
    ax.set_xlim(datemin, datemax)

    # format the coords message box
    def cfs(x):
        return '%1.2f' % x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = cfs
    ax.grid(True)
    ax.legend(lns,labs,loc='best')
    ax.set_ylabel('Discharge (cfs)')
    fig.autofmt_xdate()
    plt.show()
    plt.savefig(siteinfo['name']+'.png',dpi=200)

def MakeAnAvHydrographDF(df,parameter='value',quants='True',logdisch=False):
    fig, ax = plt.subplots()
    dvstat = GetDailyStats(df,parameter=parameter)
    if logdisch:
        lname = ax.semilogy(dvstat.index, dvstat[parameter],'b-',lw=2,label='median')
    if logdisch == False:   
        lname = ax.plot(dvstat.index, dvstat[parameter],'b-',lw=2,label='median')
    if quants:
        dvu = GetDailyStats(df,parameter=parameter,type='quantile',quantile=.75)
        dvl = GetDailyStats(df,parameter=parameter,type='quantile',quantile=.25)
        lname1 = ax.plot(dvu.index, dvu[parameter],'g-',lw=2,label='75th percentile')
        lname2 = ax.plot(dvl.index, dvl[parameter],'r-',lw=2,label='25th percentile')
        lns = lname + lname1 + lname2
        labs = [l.get_label() for l in lns]
            
    months = mdates.MonthLocator()   # every month
    monthsFmt = mdates.DateFormatter('%b')
    ## format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    # set limits
    datemin = dt.date(dvstat.index.min().year, 10, 1)
    datemax = dt.date(dvstat.index.max().year, 9, 30)
    ax.set_xlim(datemin, datemax)

    # format the coords message box
    def cfs(x):
        return '%1.2f' % x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = cfs
    ax.grid(True)
    ax.legend(lns,labs,loc='best')
    ax.set_ylabel('Discharge (cfs)')
    fig.autofmt_xdate()
    plt.show()
    plt.savefig(parameter+'.png',dpi=200)

def PlotMonthlyStd(df,parameter='value'):
    fig, ax = plt.subplots()
    dvstat = GetMonthlyStats(df,type='std',parameter=parameter)
    lname = ax.plot(dvstat.index, dvstat[parameter],'b-',lw=2,label=parameter)
    months = mdates.MonthLocator()   # every month
    monthsFmt = mdates.DateFormatter('%b')
    ## format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    # set limits
    datemin = dt.date(dvstat.index.min().year, 10, 1)
    datemax = dt.date(dvstat.index.max().year, 9, 30)
    ax.set_xlim(datemin, datemax)

    # format the coords message box
    def cfs(x):
        return '%1.2f' % x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = cfs
    ax.grid(True)
    ax.legend(loc='best')
    ax.set_ylabel('St. Dev.')
    fig.autofmt_xdate()
    plt.savefig(parameter+'Monthly_STD.png',dpi=200)
    plt.show()
