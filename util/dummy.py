from pylab import *;
import pdb;
from numpy import *;
def dummy(m):
    m_o = m;
    pdb.set_trace();
    m_step  = 100;
    m_i = m_o;
    dummy = m;
    dummy2 = m_o;
    dummy3 = m_o;
    i = 0;
    m_i[i] = m_i[i] + m_step;
    return(m_i);

