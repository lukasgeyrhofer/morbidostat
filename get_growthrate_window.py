#!/usr/bin/env python

import argparse
import numpy as np
import sys,math


from scipy.optimize import curve_fit

def log_increase1(time,signal):
    time   = time[signal > 0]
    signal = signal[signal > 0]
    st  = np.sum(time)
    stt = np.sum(time*time)
    sst = np.sum(time * np.log(signal))
    ss  = np.sum(np.log(signal))
    n   = len(time)
    return (n*sst - st * ss)/(n*stt - st*st)


def expgrowth(x,a,b,c):
    return b*np.exp(a*x)+c

def log_increase2(time,signal):
    p0 = np.array([0,signal[0],0])
    try:
        f,c = curve_fit(expgrowth,time,signal,p0 = p0,maxfev = 5000)
    except:
        f = np.zeros(2)
    return f[0]

def logisticgrowth(x,a,b,c):
    return a/(1 + np.exp(-b*(x-c)))


parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile")
parser.add_argument("-w","--windowsize",type=float,default=.5)
parser.add_argument("-c","--channels",type=int,default=15)
parser.add_argument("-t","--timechannel",type=int,default=16)
parser.add_argument("-T","--timestep",type=float,default=.1)
parser.add_argument("-B","--backgroundaverage",type=int,default=300)
parser.add_argument("-b","--removebackground",default=False,action="store_true")
args = parser.parse_args()


try:
    data = np.genfromtxt(args.infile)
except:
    raise IOError

t = data[:,0] # / args.timerescale
od = data[:,1:]

if args.removebackground:
    for c in range(args.channels):
        b = np.median(od[:args.backgroundaverage,c])
        od[:,c] -= b

curtime = 0

while curtime + args.windowsize < t[-1]:
    firstindex = len(t[t <= curtime])
    lastindex  = len(t[t <= curtime + args.windowsize])
    cur_t = t[firstindex:lastindex]

    print "{:8f}".format((curtime + 0.5*args.windowsize)),
    for c in range(args.channels):
        cur_od = od[firstindex:lastindex,c]
        cur_growthrate = log_increase1(cur_t,cur_od)
        print " {:11.4e} ".format(cur_growthrate),
    print
    curtime += args.timestep
