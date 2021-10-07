def calc_var(a,window_len):
    """ calculate the variance in a sliding window. input should be a 1d array and window_len  is the window length.  
    Uses mirror symmetric projections at boundary ends. Returns a 1d array of length a which is the variance within the
    window as it moves along the signal."""
    import numpy;
    import scipy;
    import pdb;
    # create the extended signal 
    aa = numpy.r_[2*a[0]-a[.5*window_len:1:-1],a,2*a[-1]-a[-1:-.5*window_len:-1]];
    sig_var = numpy.ones(len(a));
    for i in range(len(a)):
        #pdb.set_trace();
        index = i + .5*window_len;
        win = aa[index-.5*window_len:index+.5*window_len];
        var_i = numpy.var(win);
        sig_var[i]=var_i;
        
    return sig_var
