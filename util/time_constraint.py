# -*- coding: utf-8 -*-
"""
time_constraint.py
"""
import numpy
import pylab 
from numpy import pi
K =.0002
h_o = 100
L = 1000
S_y = .1
n = numpy.arange(1,5000,2);
t = numpy.arange(1,10000000,100000);
exp_lt_vec=[];
sum_exp_vec=[];
for i in range(len(t)):
    #calculate sum
    sum_exp = 0;
    exp_lt = numpy.exp((-pi**2*K*h_o*t[i])/(4*L**2*S_y));
   #print 'time =' + str(t[i]);
    #print 'exp_lt =' + str(exp_lt);
    for j in range(len(n)):
        exp_j = numpy.exp((-n[j]**2*pi**2*K*h_o*t[i])/(4*L**2*S_y));
        sum_exp = sum_exp + exp_j;
    #print 'sum_exp =' + str(sum_exp);
    sum_exp_vec.append(sum_exp);
    exp_lt_vec.append(exp_lt);

pylab.hold(True);
pylab.plot(t,exp_lt_vec);
pylab.plot(t,sum_exp_vec);
pylab.show();