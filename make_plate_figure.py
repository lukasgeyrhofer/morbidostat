#!/usr/bin/env python

import numpy as np
import argparse
import sys,math

def hextodec(hexval):
    return 0

def dectohex(decval):
    return "0"

def getColor(value,c0,c1):
    r = int(value * hextodec(c0[0:1]) + (1-value) * hextodec(c1[0:1]))
    g = int(value * hextodec(c0[2:3]) + (1-value) * hextodec(c1[2:3]))
    b = int(value * hextodec(c0[4:5]) + (1-value) * hextodec(c1[4:5]))
    return (r,g,b)

parser = argparse.ArgumentParser()
parser.add_argument("-i","--infiles",nargs="*")
parser.add_argument("-S","--pixelsize",type=int,default=20)
parser.add_argument("-C","--basecolor1",type=str,default="FFFFFF")
parser.add_argument("-c","--basecolor0",type=str,default="000000")
parser.add_argument("-o","--outfilebase",type=str,default="")
args = parser.parse_args()


for fn in args.infiles:
    try:
        data = np.genfromtxt(fn)
    except:
        continue

    control = data[:,-1]
    data -= np.mean(control)
    
    data += np.min(data)
    data /= np.max(data)

    xsize = data.shape[0]
    ysize = data.shape[1]

    fp = open(args.outfilebase + fn + ".OUT","w")
    fp.write("R6")
    fp.write("256")
    fp.write("{:d} {:d}".format(xsize * args.pixelsize, ysize * args.pixelsize))
    
    for y in range(ysize):
        for j in range(args.pixelsize
            for x in range(xsize):
                for i in range(args.pixelsize):
                    fp.write("{:3d} {:3d} {:3d}".format(getColor(data[x,y],args.basecolor0,args.basecolor1)),end = ' ')
            fp.write('')
            
        
        
    fp.close()
    




