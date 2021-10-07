def auto_corr(b,max_len=60):
    """ (ac_f,lag) = auto_corr(x,max_len = .5*len(x)).  calculate the autocorrelation function for a vector x to a max lag of max_len.  
    Returns a vector of lag time and a vector of autocorrelation at that lag. """
    import numpy;
    import scipy;
    import pdb;
    ac_f = numpy.ones(max_len);
    lag = numpy.arange(max_len);
    for i in range(max_len):
        stab = b[0:len(x)-i];
        lag = b[i:len(x)];
        ac_im = numpy.corrcoef(stab,lag);
        ac_i = ac_im[1,1];
        ac_f[i]=ac_i;
    return (ac_f,lag)
