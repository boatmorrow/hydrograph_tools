#%##########################################################################
# read_avg_disc - A hydrograph input function.
# reads in a USGS discharge file, pulls out the time series data and then
# applies various low pass filters of length window_len
# plots em up
############################################################################
import numpy
import pylab
import pdb

#import the text file
a = numpy.loadtxt('soda_butte_avg_decay.txt',dtype=object,comments='#',skiprows=28);
# pull out the time series
dd = pylab.datestr2num(a[:,2]);
qq = numpy.array(map(float,a[:,3]));

#low pass filter interval
window_len = 45;

#create the signal, reflects the signal at each end
s = numpy.r_[2*qq[0]-qq[window_len:1:-1],qq,2*qq[-1]-qq[-1:-window_len:-1]];

#different windows
#average
w = numpy.ones(window_len,'d');
#blackman window
w_b = numpy.blackman(window_len);
#hanning window
w_h = numpy.hanning(window_len);

#convolve
#average
q_bf_av = numpy.convolve(w/w.sum(),s,mode='same');
q_bf_av = q_bf_av[window_len-1:-window_len+1];
#blackman
q_bf_b = numpy.convolve(w_b/w_b.sum(),s,mode='same');
q_bf_b = q_bf_b[window_len-1:-window_len+1];
#hanning
q_bf_h = numpy.convolve(w_h/w_h.sum(),s,mode='same');
q_bf_h = q_bf_h[window_len-1:-window_len+1];

#vizualize
#pdb.set_trace();
pylab.plot_date(dd,qq,'b-');
#hold();
pylab.plot_date(dd,q_bf_av,'r-');
pylab.plot_date(dd,q_bf_b,'g-');
pylab.plot_date(dd,q_bf_h,'y-');
pylab.xlabel('date')
pylab.ylabel('discharge (cfs)')
pylab.legend(('discharge','average','blackman','hanning'));
pylab.show();
