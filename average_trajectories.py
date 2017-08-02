#!/usr/bin/env python

import argparse
import numpy as np
import sys,math

parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile")
parser.add_argument("-n","--averagepoints",default=30,type=int)
parser.add_argument("-c","--channels",default=15,type=int)
parser.add_argument("-V","--computevariance",default=False,action="store_true")
args = parser.parse_args()


try:
    data = np.genfromtxt(args.infile)
except:
    raise IOError

t = data[:,0]
od = data[:,1:]

dataindex = 0
while dataindex + args.averagepoints < len(t):
    print "{:f}".format(np.mean(t[dataindex:dataindex+args.averagepoints])),
    for c in range(args.channels):
        print " {:11.4e}".format(np.mean(od[dataindex:dataindex + args.averagepoints,c])),
        if args.computevariance:
            print " {:11.4e}".format(np.var(od[dataindex:dataindex + args.averagepoints,c])),
    print
    dataindex += args.averagepoints

