# -*- coding: utf-8 -*-
"""
Utility functions for working with hydrologic timeseries data and doing some common tasks.  Utilizes ulmo
climata (for now), and pandas.  

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
    '''sitname,siteinfo = ImportUsgsSiteDailyValues(siteno)
        Wraps ulmo.nwis functions.  returns a dictionary of site information (siteinfo) 
        and a pandas dataframe of daily values (sitename) for a given USGS site number.'''
    sitename = {}
    sitename = ulmo.usgs.nwis.get_site_data(siteno, service="daily", period="all",methods="all")
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
    print('downloading snotel station data.')
    params = StationDailyDataIO(station=stationid,start_date='1966-1-1',end_date='2016-12-31')   
    print('snotel download done.')
    df = params.as_dataframe()
#    swe=df.data[8].as_dataframe()
    swe = df.data[df.index[df.element_name=='SNOW WATER EQUIVALENT'].values[0]].as_dataframe()
    swe['date']=pd.to_datetime(swe.date)
    swe.set_index('date',inplace=True)
    swe=swe.dropna()
    return swe

def WaterYear(df): 
    '''dfwy = WaterYear(df).  Changes a time index to have years start and stop on the water year.
        keeps the original date in a new column.  Keeps M and D from old date.  Requres df to have
        a date time index.'''
    dfg = df.copy()
    dfg['date']=dfg.index.copy()
    dfg['wy_date']=dfg.index.copy()
    for i in range(len(dfg.index)):
        if dfg.date[i].month >= 10:
            dfg.iloc[i,dfg.columns.get_loc('wy_date')] = dfg.date.iloc[i]+relativedelta(years=1)
        else:
            continue
    dfg.set_index('wy_date',inplace=True)
    return dfg

def GetDailyStats(df,type='median',parameter='value',quantile=.5,water_year=True):
    '''dfg = GetDailyStats(df,type='median',parameter='value',quantile=.5,water_year=True) - return a dataframe dfg
        with the given statistic for each day of year.  If water year is true, index will be given by water year.
        Pick the parameter in the dataframe you want the stats for.'''
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
    if type == 'min':
        dfg = pd.DataFrame(grouped[parameter].min())
        try:
            dfg = dfg.drop(366) #get rid of leap day...
        except KeyError:
            dfg = dfg
        dfg['date']=dfg.index.map(dt.datetime.fromordinal)
        dfg.date=dfg.date+relativedelta(years=2015)
        dfg.date=pd.to_datetime(dfg.date)
    if type == 'max':
        dfg = pd.DataFrame(grouped[parameter].max())
        try:
            dfg = dfg.drop(366) #get rid of leap day...
        except KeyError:
            dfg = dfg
        dfg['date']=dfg.index.map(dt.datetime.fromordinal)
        dfg.date=dfg.date+relativedelta(years=2015)
        dfg.date=pd.to_datetime(dfg.date)
    else:
        print('type =', type, ' not recognized')
        print('add stat type')
        
    if water_year:
        dfg = WaterYear(dfg)
    else:
        dfg.set_index('date',inplace=True)
    return dfg

def GetDailyStatsSummary(df,parameter='value',water_year=True):
    '''dfg = GetDailyStats(df,type='median',parameter='value',quantile=.5,water_year=True) - return a dataframe dfg
        with the given statistic for each day of year.  If water year is true, index will be given by water year.
        Pick the parameter in the dataframe you want the stats for.'''
    grouped = df.groupby(df.index.dayofyear)
    stats = ['count','min','max','mean','std','median','mad']
    dfg = pd.DataFrame(grouped[parameter].agg(stat_list))
    if water_year:
        dfg = WaterYear(dfg)
    else:
        dfg.set_index('date',inplace=True)
    return dfg

#
#def GetDailyStats(df,type='median',parameter='value',quantile=.5,water_year=True):
#    grouped = df.groupby(df.index.dayofyear)
#    '''GetDailyStats(df,type='median',parameter='value',quantile=.5,water_year=True) - return a dataframe dfg
#        with the given statistic for each day of year.  If water year is true, index will be given by water year.
#        Pick the parameter in the dataframe you want the stats for.'''
#    if type == 'median':
#        dfg = pd.DataFrame(grouped[parameter].median())
#        try:
#            dfg = dfg.drop(366) #get rid of leap day...
#        except KeyError:
#            dfg = dfg
#        dfg['date']=dfg.index.map(dt.datetime.fromordinal)
#        dfg.date=dfg.date+relativedelta(years=2015)
#        dfg.date=pd.to_datetime(dfg.date)
#    if type == 'mean':
#        dfg = pd.DataFrame(grouped[parameter].mean())
#        try:
#            dfg = dfg.drop(366) #get rid of leap day...
#        except KeyError:
#            dfg = dfg
#        dfg['date']=dfg.index.map(dt.datetime.fromordinal)
#        dfg.date=dfg.date+relativedelta(years=2015)
#        dfg.date=pd.to_datetime(dfg.date)
#    if type == 'quantile':
#        dfg = pd.DataFrame(grouped[parameter].quantile(q=quantile))
#        try:
#            dfg = dfg.drop(366) #get rid of leap day...
#        except KeyError:
#            dfg = dfg
#        dfg['date']=dfg.index.map(dt.datetime.fromordinal)
#        dfg.date=dfg.date+relativedelta(years=2015)
#        dfg.date=pd.to_datetime(dfg.date)
#        
#    else:
#        print('type =', type, ' not recognized')
#        print('add stat type')
#    if water_year:
#        for i in dfg.index:
#            if dfg.date[i].month >= 10:
#                dfg.date[i] = dfg.date[i]-relativedelta(years=1)
#        dfg.set_index('date',inplace=True)
#        dfg=dfg.sort_index()
#    else:
#        dfg.set_index('date',inplace=True)
#    return dfg
#

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
    for i in range(len(siteno)):    
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
    #plt.show()
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

def MakeMonthlyAvHydrographDF(df,parameter='value',quants='True',logdisch=False):
    fig, ax = plt.subplots()
    dvstat = GetMonthlyStats(df,parameter=parameter)
    if logdisch:
        lname = ax.semilogy(dvstat.index, dvstat[parameter],'bo',lw=2,label='median')
    if logdisch == False:   
        lname = ax.plot(dvstat.index, dvstat[parameter],'bo',lw=2,label='median')
    if quants:
        dvu = GetMonthlyStats(df,parameter=parameter,type='quantile',quantile=.75)
        dvl = GetMonthlyStats(df,parameter=parameter,type='quantile',quantile=.25)
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
    plt.savefig(parameter+'monthly.png',dpi=200)
