#!/usr/bin/env python3

import numpy as np
import argparse
import openpyxl
import cairo
import time
import dateutil
import sys

# ===================================================== #
# define positions of values in Excel file              #
# ===================================================== #

# row numbers for starting values
time_starting_row = 33
data_starting_row = 37
# starting column, usually B
time_starting_column = 2
data_starting_column = 2

# plate dimensions
platex = 12
platey = 8


# ===================================================== #
# helper routines                                       #
# ===================================================== #
def column_string(n):
    div=n
    string=""
    temp=0
    while div>0:
        module=(div-1)%26
        string=chr(65+module)+string
        div=int((div-module)/26)
    return string

def baseN(num,b=26,numerals="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def convert(x,y):
    return '{}{}'.format(column_string(x),y)

def AddRow(alldata,newdata):
    if alldata is None:
        r = np.array([newdata])
    else:
        r = np.concatenate([alldata,np.array([newdata])],axis = 0)
    #r[-1:0] += starttime_newdata
    return r


# ===================================================== #
# actual progam                                         #
# ===================================================== #

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--infile",required=True,default=None)
    parser.add_argument("-o","--outfile",default="out",type=str)
    args = parser.parse_args()


    # open Excel file
    try:
        data = openpyxl.load_workbook(args.infile)
    except:
        raise IOError("could not open file")

    assay = None
    for sheet in data:
        cell = convert(time_starting_column,time_starting_row)
        timestr = sheet[cell].value
        t_start = float((dateutil.parser.parse(timestr)).strftime("%s"))
        if t_start > 0:
            print("reading data from sheet '{}': starttime = {}".format(sheet.title,t_start),file=sys.stderr)
            i = 0
            while not sheet[convert(data_starting_column,data_starting_row + i)].value is None:
                newrow         = np.array([float(sheet[convert(data_starting_column + j,data_starting_row + i)].value) for j in range(platex * platey + 2)]) # +2 for time and temp columns
                newrow_time    = np.zeros(len(newrow))
                newrow_time[0] = t_start
                assay          = AddRow(assay,newrow+newrow_time)
                i += 1
    assay = np.sort(assay,axis=0)

    assay[:,0] -= np.min(assay[:,0])
    assay[:,0] /= 3600.
    np.savetxt(args.outfile,assay)
    #print(assay)

# if called from cmdline, then start here
if __name__ == "__main__":
    main()
