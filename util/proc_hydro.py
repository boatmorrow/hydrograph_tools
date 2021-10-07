#from avg_hyd_read import avg_hyd_read
from newton import newton
from cg import cg
from jacob2 import jacob
import pylab

def proc_hydro(qq):
    ''' (A,m,d,J,error_flag) = proc_hydro(qq) - 
    wants qq an annual hydrograph.  Returns the modeled data A, the model paramters m, and J
    the Jacobian for snowmelt hydrograph interpretation'''

    #(qq_mean,qq_med,qq_mean_rec,qq_med_rec) = avg_hyd_read(inputfile);
    cut_off = pylab.find(qq==max(qq));
    cutoff_index = cut_off[0]+20;
    qq_mean_rec = qq[slice(cutoff_index,len(qq))];
    d = qq_mean_rec.copy();
    (A,m,error_flag) = cg(qq_mean_rec,2);
    (J) = jacob(A,m,qq_mean_rec,2);
    return(A,m,d,J,error_flag);
