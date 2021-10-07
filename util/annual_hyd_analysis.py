# -*- coding: utf-8 -*-
"""
annual_hyd_analysis.py
"""

from proc_hydro import proc_hydro
from split_hydrograph import hyd_split
from numpy import mean,std
import pdb
from smooth_signal import smooth
#import file

filename = 'inputfile.txt';
#filename = 'Fireriv.txt';
sm_flag = 1;
qq_dict,dd,qq = hyd_split(filename);
hyd_mod_dict = {};
Q_sm = [];
alpha_sm = [];
Q_gw = [];
alpha_gw = [];
bf_index = [];


for k,v in qq_dict.iteritems():
    error_flag = 1;
    hyd_i = qq_dict[k][:,1];
    if len(hyd_i) >= 365:
        hyd_i = smooth(hyd_i,14);
        #pdb.set_trace();
        (A,m,d,J,error_flag) = proc_hydro(hyd_i);
        if error_flag == 0:
            q_GW_q_max = m[2]/max(hyd_i);
            hyd_mod_dict[k]=(A,m,d,J,q_GW_q_max);

for k,v in hyd_mod_dict.iteritems():
    #pdb.set_trace();
    Q_sm.append(hyd_mod_dict[k][1][0]);
    alpha_sm.append(hyd_mod_dict[k][1][1]);
    Q_gw.append(hyd_mod_dict[k][1][2]);
    alpha_gw.append(hyd_mod_dict[k][1][3]);
    bf_index.append(hyd_mod_dict[k][4]);
    
avg_Q_sm = '%.2f' %mean(Q_sm);
std_Q_sm = '%.2f' %std(Q_sm);
avg_alpha_sm = '%1.1e' %mean(alpha_sm);
std_alpha_sm = '%1.1e' %std(alpha_sm);
avg_Q_gw = '%.2f' %mean(Q_gw);
std_Q_gw = '%.2f' %std(Q_gw);
avg_alpha_gw = '%1.1e' %mean(alpha_gw);
std_alpha_gw = '%1.1e' %std(alpha_gw);
avg_bf_index = '%.1g' %mean(bf_index);
std_bf_index = '%.2f' %std(bf_index);
f = open('out.txt','w');
line = '&'+ str(avg_Q_sm) +'&'+ str(std_Q_sm) +'&'+ str(avg_alpha_sm) +'&'+ str(std_alpha_sm) +'&'+ str(avg_Q_gw) +'&'+ str(std_Q_gw) +'&'+ str(avg_alpha_gw) +'&'+ str(std_alpha_gw) +'&'+ str(avg_bf_index) +'&'+ str(std_bf_index) +'\\'
f.write(line);
f.close();
print 'avg_Q_sm =' + str(avg_Q_sm) 
print 'std_Q_sm =' + str(std_Q_sm)
print 'avg_alpha_sm =' + str(avg_alpha_sm)
print 'std_alpha_sm =' + str(std_alpha_sm)
print 'avg_Q_gw =' + str(avg_Q_gw) 
print 'std_Q_gw =' + str(std_Q_gw)
print 'avg_alpha_gw =' + str(avg_alpha_gw)
print 'std_alpha_gw =' + str(std_alpha_gw)
print 'avg_bf_index =' + str(avg_bf_index)
print 'std_bf_index =' + str(std_bf_index)