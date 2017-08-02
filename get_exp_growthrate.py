#!/usr/bin/env python

import argparse
import numpy as np
import sys,math


from scipy.optimize import curve_fit

def logisticgrowth(x,a,b,c):
    return a/(1 + np.exp(-b*(x-c)))

def expgrowth(x,a,b):
    return a*np.exp(b*x)


parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile")
parser.add_argument("-M","--maxfev",default=5000,type=int)
parser.add_argument("-l","--lowercutoff",default=.04,type=float)
parser.add_argument("-L","--uppercutoff",default=.15,type=float)
args = parser.parse_args()

try:
    data = np.genfromtxt(args.infile)
except:
    raise IOError

t = data[:,0] # / args.timerescale
od = data[:,1:]

l = list()
for c in range(len(od[0])):
    p0 = np.array([1,.5,6])
    odc = od[:,c]
    tc  = t  [odc >= args.lowercutoff]
    odc = odc[odc >= args.lowercutoff]
    
    tc  = tc [odc <= args.uppercutoff]
    odc = odc[odc <= args.uppercutoff]
    
    p0  = np.array([1e-3,1])
    
    try:
        fit,cov = curve_fit(expgrowth,tc,odc,p0=p0,maxfev=args.maxfev)
    
    
    
        print "{:2d} {:6.4f} {:6.4f} {:6.4e} {:6.4e}".format(c+1,fit[1],np.sqrt(cov[1,1]),fit[0],np.sqrt(cov[0,0]))
        l.append(fit[1])
    except:
        continue


print >> sys.stderr,np.mean(l),np.std(l)
