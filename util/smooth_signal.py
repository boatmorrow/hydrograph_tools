# -*- coding: utf-8 -*-
import numpy
import pylab

def smooth(qq,window_len,type='mean'):
    """
    qq_smooth = smooth(qq,type='mean') returns a smoothed vector of length qq smoothed with
    window length of 'window_len'.  Can smooth with the average, blackman or hanning weights over
    the interval.
    """
    #create the signal, reflects the signal at each end
    s = numpy.r_[2*qq[0]-qq[window_len:1:-1],qq,2*qq[-1]-qq[-1:-window_len:-1]];
    #different windows
    if type == 'mean': #average
        w = numpy.ones(window_len,'d');
    if type == 'blackman': #blackman window
        w = numpy.blackman(window_len);
    if type == 'hanning':  #hanning window
        w = numpy.hanning(window_len);
    
    #convolve
    qq_smooth = numpy.convolve(w/w.sum(),s,mode='same');
    qq_smooth = qq_smooth[window_len-1:-window_len+1];
    return qq_smooth;

def smooth_all(qq,dd,window_len):
    """ qq_smooth_av,qq_smooth_bk,qq_smooth_hn = smooth_all(qq,dd,window_len) returns smoothed
    signals of length qq with mean, blackman and hanning weightings.  Plots all them on a single plot.  
    Useful for testing which type of smoothing works the best wonders."""
    
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
    pylab.plot(dd,qq,'b-');
    #hold();
    pylab.plot_date(dd,q_bf_av,'r-');
    pylab.plot_date(dd,q_bf_b,'g-');
    pylab.plot_date(dd,q_bf_h,'y-');
    pylab.xlabel('date')
    pylab.ylabel('discharge (cfs)')
    pylab.legend(('discharge','average','blackman','hanning'));
    pylab.show();