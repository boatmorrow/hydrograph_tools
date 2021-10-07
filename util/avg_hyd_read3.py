#%##########################################################################
# Hydrograph Analysis
# reads in a USGS mean daily statistics discharge file, pulls out the time series data.
# returns the mean qq_mean- daily hydrograph, and qq_med- median daily hydrgraphy.
# neads a daily statistics disharge tab separated file from the USGS water data 
# page.  Call (qq_mean,qq_med,qq_mean_rec,qq_med_rec) = avg_hyd_read(filename). 
# Inputs should be strings. 
############################################################################
import numpy
#import pylab
import datetime
#import scipy.io
import pdb

def avg_hyd_read(filename):
    """reads in a average daily flow statistics file from the USGS water data for the nation.  This version plots from the day of 
    peak flow, plus a week.  Call (qq_mean,dd) = avg_hyd_read(filename). 
    Inputs should be strings."""
    #
    # pdb.set_trace();
    #import the text file
    #D = scipy.io.read_array(filename,separator='\t',columns=(4,5,13,18)); 
    D = numpy.loadtxt(filename,dtype=object,delimiter='\t',usecols=(4,5,13));
    D = D[2:len(D[:,0])-1,:];
    # a = numpy.loadtxt(filename,dtype=object,comments='#',skiprows=66);
    # pull out the time series
    dd = [];
    year = 2008;
    for i in range(len( D[:,1])):
        dday = int(D[i,1]);
        dmonth = int(D[i,0]);
        #pdb.set_trace();
        dd.append(datetime.datetime(year,dmonth,dday));
    qq_mean = numpy.array(map(float,D[:,2]));
    #qq_med = numpy.array(map(float,D[:,3]));
    #cut_off = pylab.find(qq_mean==max(qq_mean));
    #cutoff_index = cut_off[0]+20;
    #qq_mean_rec = qq_mean[slice(cutoff_index,len(qq_mean))];
    #qq_med_rec = qq_med[slice(cutoff_index,len(qq_med))];
    dd = numpy.array(dd);
    return(qq_mean,dd);
