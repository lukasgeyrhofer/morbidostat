#!/usr/bin/env python

import argparse
import numpy as np
import sys,math


from scipy.optimize import curve_fit

def logisticgrowth(x,a,b,c):
    return a/(1 + np.exp(-b*(x-c)))


parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile")
parser.add_argument("-M","--maxfev",default=5000,type=int)
parser.add_argument("-l","--lowercutoff",default=None,type=float)
args = parser.parse_args()

try:
    data = np.genfromtxt(args.infile)
except:
    raise IOError

t = data[:,0] # / args.timerescale
od = data[:,1:]


for c in range(len(od[0])):
    p0 = np.array([1,.5,6])
    odc = od[:,c]
    fit,cov = curve_fit(logisticgrowth,t,odc,p0=p0,maxfev = args.maxfev)
    if not args.lowercutoff is None:
        tc  = t  [odc >= args.lowercutoff]
        odc = odc[odc >= args.lowercutoff]
        if len(odc) > 0:
            fitc,covc = curve_fit(logisticgrowth,tc,odc,p0=p0,maxfev = args.maxfev)
        else:
            fitc = np.zeros(3)
            covc = np.zeros((3,3))
        np.savetxt("log{:03d}".format(c),np.transpose([t,od[:,c],logisticgrowth(t,fit[0],fit[1],fit[2]),logisticgrowth(t,fitc[0],fitc[1],fitc[2]) ]))
    else:
        np.savetxt("log{:03d}".format(c),np.transpose([t,od[:,c],logisticgrowth(t,fit[0],fit[1],fit[2])]))
    
    print "{:2d} {:6.4f} {:6.4f}".format(c+1,fit[1],np.sqrt(cov[1,1])),
    if not args.lowercutoff is None:
        print " {:6.4f} {:6.4f}".format(fitc[1],np.sqrt(covc[1,1])),
    print
