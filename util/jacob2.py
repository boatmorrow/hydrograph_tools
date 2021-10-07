#####################################################################################################
# Jacobian.py - calculated the Jacobian of the residual, as a measure of the sensitivity of the inversion.
####################################################################################################
from pylab import *;
#import pdb;
from numpy import *;

def jacob(A,m,d,num_res):
    ''' Calculates the jacobian of the residual given inverted data (A_i), inversion results (m), and observed
    data (d) (J) = jacobian(A_i,m,d).  For 2 reservior hydrograph inversion only right now.'''
    R_ini = linalg.norm(A-d);
    m_o = m;
    error = .1; #error level
    print 'error level =' +str(error);
    ll = len(d);
    t = arange(0,ll);
    #num_res = 1;
    J = ones(len(m));

    for i in range(len(m)):
        m_step = error*m[i];
        m_i = m_o.copy();
        m_i[i] = m_i[i] + m_step;
        A_i = calc_j(ll,t,m_i,num_res); 
        R_i = linalg.norm(A_i-d);
        dR_dm_i = abs((R_i - R_ini)/m_step);
        J[i] = dR_dm_i; 
# I'm going to divide by m_step to give me a signal to step ratio, I think this is a good measure of how much we change our measure of the error with a change in model params.  If its greater that one, that means I can definately see this stepsize.
        
    return(J);

def calc_j(ll,t,m_i,num_res):
    """Calculates A_i(m) the modeled data for a given set of model parameters."""
    A_i = ones((ll,));
    for i in range(ll):
        # for three expotentials
        # build the Frechet for time t[i,0];
        # for three decays change commented lines accordingly
        if num_res == 1:
            A_i[i] = m_i[0]*exp(-1*m_i[1]*t[i]);
        if num_res == 2:
            A_i[i] = m_i[0]*exp(-1*m_i[1]*t[i]) + m_i[2]*exp(-1*m_i[3]*t[i]);
        if num_res == 3:
            A_i[i] = m_i[0]*exp(-1*m_i[1]*t[i]) + m_i[2]*exp(-1*m_i[3]*t[i])  + m_i[4]*exp(-1*m_i[5]*t[i]);
    return(A_i)
