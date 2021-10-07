# make_date_plot.py - makes a date plot with only the abbreviated months in x axis.
from pylab import figure, show;
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter;
import datetime;
import pdb;
def make_date_plot(dates,discharge,plot_no=1):
    ''' make_data_plot(dates,discharge,plot_no) makes a date plot with abbreviated months
    for discharge and dates times series. plots to a one column subplot with row number 
      given by plot_no.'''
    # pdb.set_trace();
    fig = figure(1);
    #ax = fig.add_subplot(2,1,plot_no);
    ax = fig.add_subplot(1,1,1);
    #ax.plot(dates,discharge,'ko'); #plot to the current axes
    if plot_no == 1:
      ax.plot(dates,discharge,'ko',mfc='k'); #plot to the current axes
    if plot_no == 2:
      ax.plot(dates,discharge,'wo');
    # now to make the date plot the way we want.
    months = MonthLocator();
    ax.xaxis.set_major_locator(months);
    Fmt = DateFormatter('%b'); #abbreviated months
    ax.xaxis.set_major_formatter(Fmt);
    ax.autoscale_view();
    show();

