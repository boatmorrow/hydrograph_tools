# -*- coding: utf-8 -*-
"""
split_hydrograph.py
"""

import numpy
#import pylab
#import scipy.io
import pdb
import datetime

def hyd_split(filename='inputfile.txt'):
    """reads in a daily flow file from the USGS water data for the nation.  Separates out each years hydrograph.
    For that years hydrograph pulls out the recession returns a dictionary keyed by the year with each years 
    annual mean daily hydrograph. """
    #
    curyear = 1901;
    qq_year = [];
    dd_year = [];
    qq_dict = {};
    #import the text file
    D = numpy.loadtxt(filename,dtype='str',delimiter='\t',usecols=(2,3)); # column 2 is the date and 3 is th flow files need to be opened in wordpad and saved to get right line endings.  Make sure the record is complete for the whole segment being analyzed
    D = D[2:len(D[:,0])-1,:]; #get rid of headers
    dd = [];
    #convert to time series vectors...
    for i in range(len( D[:,1])):
        dd.append(datetime.datetime.strptime(D[i,0],'%Y-%m-%d'));
        
    qq = map(float,D[:,1]);
    #now split the hydrographs
    for i in range(len(dd)):
        if i == 0:
            curyear = dd[i].year;
            if dd[i] > datetime.datetime(curyear,9,30):
                curyear = curyear +1;
        wye = datetime.datetime(curyear,9,30);  # USGS water year ends at the end of september but going to try it on the data set out january...
        #wye = datetime.datetime(curyear+1,1,1);
        if dd[i] < wye:
            qq_year.append(qq[i]);
            dd_year.append(dd[i]);
        if dd[i] == wye:
            qq_year.append(qq[i]);
            dd_year.append(dd[i]);
            qq_year = numpy.array(qq_year);
            dd_year = numpy.array(dd_year);
            dq_year = numpy.transpose(numpy.vstack((dd_year,qq_year)));
            qq_dict[curyear]=dq_year;
            curyear = curyear + 1;
            qq_year = [];
            dd_year = [];
        if i == len(dd)-1:  #probably only need this for going to years end...
            #pdb.set_trace();
            qq_year.append(qq[i]);
            dd_year.append(dd[i]);
            qq_year = numpy.array(qq_year);
            dd_year = numpy.array(dd_year);
            dq_year = numpy.transpose(numpy.vstack((dd_year,qq_year)));
            qq_dict[curyear]=dq_year;
    
    return qq_dict, dd, qq