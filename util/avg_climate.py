# -*- coding: utf-8 -*-
"""
split_hydrograph.py
"""

import numpy
import pylab
#import scipy.io
import pdb
import datetime

def avg_clim(filename='Canyon_all.txt'):
    """reads in a daily observation file from a snowtell site.  Calculates the average daily value
   for each day over the period of record, return tav,pav,dav the average temperature,precip,date.  The
  date has an arbitrary year of 2000 """
    prcp = [];
    dd = [];
    tavg = [];
    p_dict = {};
    t_dict = {};
    tav = [];
    pav = [];
    dav = [];
    #qq_dict = {};
    #import the text file
    D = numpy.loadtxt('Canyon_all.txt',dtype=object,delimiter='\t'); # column 2 is the date and 3 is th flow files need to be opened in wordpad and saved to get right line endings.  Make sure the record is complete for the whole segment being analyzed
    #D = D[2:len(D[:,0])-1,:]; #get rid of headers
    dd = [];
    #convert to time series vectors...
    for i in range(len(D)):
        if len(D[i])==7:
            prcp.append(float(D[i][6]));
            dd.append(datetime.datetime.strptime(D[i][0],'%m%d%y'));
            tavg.append(float(D[i][5]));
        
    for i in range(len(prcp)):
        #key = str(dd[i].day) + str(dd[i].month);
        key = datetime.datetime(2000,dd[i].month,dd[i].day);
        #if t_dict.has_key(key)==True:
         #   
        if t_dict.has_key(key)==False:
            t_dict[key]=numpy.array([[],datetime.date.today()],dtype=object);
            p_dict[key]=numpy.array([[],datetime.date.today()],dtype=object);
        t_dict[key][0].append(tavg[i]);
        t_dict[key][1]=datetime.datetime(2000,dd[i].month,dd[i].day);
        p_dict[key][0].append(prcp[i]);
        p_dict[key][1]=datetime.datetime(2000,dd[i].month,dd[i].day);
    keys_sort = numpy.sort(t_dict.keys());
    #pdb.set_trace();
    for i in range(len(keys_sort)):
        k = keys_sort[i];
        tav.append(numpy.mean(numpy.array(t_dict[k][0])));
        pav.append(numpy.mean(numpy.array(p_dict[k][0])));
        dav.append(t_dict[k][1]);
    tav = numpy.array(tav);
    pav = numpy.array(pav);
    dav = numpy.array(dav);
    return (tav, pav, dav);

#make figures
# some figure parameters.  If you don't want to use latex then don't use these...
#mpl.rcParams['text.usetex'] = True;
#mpl.rcParams['font.family'] = 'serif';
#mpl.rcParams['font.serif'] = 'Times, Palatino, New Century Schoolbook, Bookman, Computer Modern Roman';
#mpl.rcParams['font.sans-serif'] = 'Helvetica, Avant Garde, Computer Modern Sans serif';
#mpl.rcParams['font.cursive'] = 'Zapf Chancery';
#mpl.rcParams['font.monospace'] = 'Courier, Computer Modern Typewriter';
#mpl.rcParams['font.size'] = 18;
#mpl.rcParams['axes.labelsize'] = 18;
#mpl.rcParams['xtick.labelsize'] = 16;
#mpl.rcParams['ytick.labelsize'] = 16;
#mpl.rcParams['axes.titlesize']= 20;
#mpl.rcParams['text.dvipnghack'] = 'False';
#mpl.rcParams['figure.figsize'] = 13, 11;


#ax1 = subplot(111); #make a set of axes and name them
#line1 = plot(dav, tav, 'ro',label=r'T$_{avg}^o$C'); #make first plot
#ylim(0.0,1); #change the y limits
#ax2 = twinx(); # now make the second set of axes and name them
#line4 = plot(dav, pav, 'r--',label=r'Precip. (in)'); #plot on the second set of axes
#xlim(1.0001,0.90); #set x limits on second set of axes
#ylim(-.5,0.0); #set y limits on second set of axes
#xlabel(r'Day');
#ax1.set_ylabel(r'\begin{center}$\chi$\\ (residual Xenon concentration)\end{center}');
#ax2.set_ylabel(r'$\delta_{ws}$D - $\delta_{wi}$D');
#title(r'\begin{center}Effect of boiling on noble gas content\\and isotopic compostion of water\\-continuous steam removal\end{center}');
#savefig('boil_fig_cont.png');
#pylab.show();
        
#now split the hydrographs
#for i in range(len(dd)):
#    if i == 0:
#        curyear = dd[i].year;
#        if dd[i] > datetime.datetime(curyear,9,30):
#            curyear = curyear +1;
#    wye = datetime.datetime(curyear,9,30);  # USGS water year ends at the end of september but going to try it on the data set out january...
    #wye = datetime.datetime(curyear+1,1,1);
#    if dd[i] < wye:
#        qq_year.append(qq[i]);
#        dd_year.append(dd[i]);
#    if dd[i] == wye:
#        qq_year.append(qq[i]);
#        dd_year.append(dd[i]);
#        qq_year = numpy.array(qq_year);
#        dd_year = numpy.array(dd_year);
#        dq_year = numpy.transpose(numpy.vstack((dd_year,qq_year)));
#        qq_dict[curyear]=dq_year;
#        curyear = curyear + 1;
#        qq_year = [];
#        dd_year = [];
#    if i == len(dd)-1:  #probably only need this for going to years end...
        #pdb.set_trace();
#        qq_year.append(qq[i]);
#        dd_year.append(dd[i]);
#        qq_year = numpy.array(qq_year);
#        dd_year = numpy.array(dd_year);
#        dq_year = numpy.transpose(numpy.vstack((dd_year,qq_year)));
#        qq_dict[curyear]=dq_year;

#return qq_dict, dd, qq