#################################################################################################
#  newton.py -
#  Newton's method inversion to find model parameters for a description
#  of the snowmelt recession as a sum of expotentials.  Q(t) = \sum{i=1}{N}Q_{o}^{i}e^{-\alpha t}.
#  In this model I assume 3 reserviors 1) snowmelt/runoff 2) interflow 3) baseflow
#  so I have a sum of three expotenials.  This script will use newtons methods to find the 
#  the best fit model parameters.
#  needs a data set (the snowmelt decrease for now).
##################################################################################################

#import some modules
from pylab import *;
import pdb;
from numpy import *;
from numpy.linalg import  pinv,norm;
close('all');

def newton(dd,num_res):
    """ Newton's method inversion to find model parameters for a multiple reservour model of a snowmelt decay hydrograph.
        Needs d the decay data and the number 1-3 of the reserviors, returns A the modeled data and m the best fit parameters.
        For a three reservior model - m = [Q_1,alpa_1,Q_2,alpha_2,Q_3,alpha_3]."""
    # initalialize arrays and starting model.  The starting model probably needs a better treatment
    global ll;
    global t;
    ll = len(dd);
    dd = dd.reshape(ll,);
# for regularization
    alpha = 1;
    t = arange(0,ll);
    if num_res > 3:
        print 'No more than three reserviors please.';
        return();
    # for a single reservior
    if num_res == 1:
        # the initial guess - call m =  build_m_i(dd,t,num_res,alpha): 
        m = build_m_i(dd,t,num_res,alpha);
        #nneed to offset the decay i think
    if num_res ==2:
        # for two decays only
        m = build_m_i(dd,t,num_res,alpha);
    if num_res  == 3:
        # for three reserviors uncomment
        m = array([100,.1e-5,100,.1e-5,100,.1e-5]);
    #build A(m) and F intially
    m_apr = m;
    (F,A_ini) = calc(ll,t,m,num_res);
    e_i = norm(A_ini-dd);
    #call the inversion routine
    (A,m,error_flag) = invert(F,m,m_apr,A_ini,dd,alpha,num_res);
    
    figure();
    plot(dd,'ro');
    plot(A_ini);
    title('Initial model');
    xlabel('elapsed time (days)');
    ylabel('Discharge (cfs)');
    
    figure();
    plot(dd,'ro');
    plot(A);
    title('Best fit model');
    legend(('Mean Recession','model'));
    xlabel('elapsed time (days)');
    ylabel('Discharge (cfs)');
    show();
    return(A,m,error_flag);

def invert(F,m,m_apr,A,dd,alpha,num_res):
    """start newton iterations.  Uses regularized  newton method with line search for weighting of one."""
    count = 0;
    maxit = 50;
    etol = 10e-5;
    iflag = 1;
    error_flag = 0;
    e_i = norm(A-dd);
    while iflag:
        close('all');
        Hess = 2*(dot(transpose(F),F) + alpha);
        H_inv  = pinv(Hess);
        r_n = A - dd;
        l_n = dot(transpose(F),r_n) + alpha*(m-m_apr);
        m_step = dot(H_inv,l_n);
        g_n = dot(dot(F,H_inv),l_n);
        k_n = (dot(dot(H_inv,l_n),l_n))/(dot(g_n,g_n));
        #pdb.set_trace();
        #m = m - k_n*m_step;
        m = m - m_step;
        (F,A) = calc(ll,t,m,num_res);
        e_2 = norm(A-dd);
        delt_e = abs(e_i-e_2);
        if e_2 > e_i:
            iflag = 0;
            error_flag = 1;
            print'error increasing.';
        if count > maxit:
            iflag = 0;
            print'failed to converge';
        if delt_e < etol:
            iflag = 0;
            print'convergnce of rms';
        # to be uncommented when I'm done debugging.
        #else:
        #    A = A2;
        #    F = F2;
        count = count+1;
        #pdb.set_trace();
        e_i = e_2; 
        
    return(A,m,error_flag);

def calc(ll,t,m,num_res):
    """Calculates A(m) the modeled data and the Freschet for a given set of model parameters.  Freschet
    can be calculated analytically in this case."""
    A = ones((ll,));
    for i in range(ll):
        # for three expotentials
        # build the Frechet for time t[i,0];
        # for three decays change commented lines accordingly
        if num_res == 1:
            A[i] = m[0]*exp(-1*m[1]*t[i]);
            dAdm1 = exp(-1*m[1]*t[i]);
            dAdm2 = m[0]*-1*t[i]*exp(-1*m[1]*t[i]);
            F_i = array([dAdm1,dAdm2]);
        if num_res == 2:
            A[i] = m[0]*exp(-1*m[1]*t[i]) + m[2]*exp(-1*m[3]*t[i]);
            dAdm1 = exp(-1*m[1]*t[i]);
            dAdm2 = m[0]*-1*t[i]*exp(-1*m[1]*t[i]);
            dAdm3 = exp(-1*m[3]*t[i]);
            dAdm4 = m[2]*-1*t[i]*exp(-1*m[3]*t[i]);
            F_i = array([dAdm1,dAdm2,dAdm3,dAdm4]);
        if num_res == 3:
            A[i] = m[0]*exp(-1*m[1]*t[i]) + m[2]*exp(-1*m[3]*t[i])  + m[4]*exp(-1*m[5]*t[i]);
            dAdm1 = exp(-1*m[1]*t[i]);
            dAdm2 = m[0]*-1*t[i]*exp(-1*m[1]*t[i]);
            dAdm3 = exp(-1*m[3]*t[i]);
            dAdm4 = m[2]*-1*t[i]*exp(-1*m[3]*t[i]);
            dAdm5 = exp(-1*m[5]*t[i]);
            dAdm6 = m[4]*-1*t[i]*exp(-1*m[5]*t[i]);
            F_i = array([dAdm1,dAdm2,dAdm3,dAdm4,dAdm5,dAdm6]);
        if i == 0:
            F = F_i;
        else:
            F = vstack((F,F_i));
    return(F,A)

def build_m_i(dd,t,num_res,alpha):
    """ Builds in the initial model, and the apriori model. For a one and two reservior model only.  For first reservior 
        takes the O_o_1 = max(dd) - min(dd).  Then fits a discharge shifted data set with a one reservior model to get decay for snow melt
        reservior.  For gw reservior, takes med(dd) for Q_o_i and assumes a small decay of -10. Needs data, time, number of reserviors,
        alpha for inversion.  Return m_i the model parameter array."""
    # fit a discharge shifted decay for first reservior model parameters
    print('building initial model');
    dd_shift = dd - min(dd);
    Q_o_1 = max(dd) - min(dd);
    alpha_i_1 = 1e-2;
    m_i = array([ Q_o_1 , alpha_i_1]); 
    (F,A) = calc(len(dd),t,m_i,1);
    # fit 1 reservior model call invert(F,m,m_apr,A,dd,alpha):
    (A,m_1,error_flag) = invert(F,m_i,m_i,A,dd_shift,alpha,1);
    figure();
    plot(A);
    plot(dd_shift);
    show();
    #pdb.set_trace();
    if num_res == 1:
        m_1[0]=m_1[0]+min(dd);
        return (m_1);
    if num_res == 2:
        m_2 = array([min(dd),1e-10]);
        m = concatenate( (m_1,m_2) );
        return(m);

