#!/usr/bin/env python3

import numpy as np
import argparse
import openpyxl
import cairo



# ===================================================== #
# define positions of values in Excel file              #
# ===================================================== #

# rows for starting values
OD_start_row  = 28
CFP_start_row = 59 
GFP_start_row = 90 
mC_start_row  = 121

# starting column, usually B
starting_column = ord('B')

# plate dimensions
platex = 12
platey = 8


# ===================================================== #
# helper routines                                       #
# ===================================================== #

def setOVERtoMAX(value):
    if value == "OVER":
        return 65536
    else:
        return value

def rescale(values,log = False):
    if log:
        return (np.log(values) - np.min(np.log(values)))/(np.max(np.log(values)) - np.min(np.log(values)))
    else:
        return (values - np.min(values))/(np.max(values) - np.min(values))


# ===================================================== #
# actual progam                                         #
# ===================================================== #

def main():
    # parse parameters from command line
    # simplest usage:
    #      ./platereader.py -i EXCELFILE
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--infile",required=True,default=None)
    parser.add_argument("-S","--sheets",nargs="*",default=None)
    parser.add_argument("-o","--outbasename",type=str,default="")
    parser.add_argument("-p","--pixelsize",type=int,default = 20)
    parser.add_argument("-L","--logarithmic",default=False,action="store_true")
    args = parser.parse_args()


    # open Excel file
    try:
        data = openpyxl.load_workbook(args.infile)
    except:
        raise IOError("could not open file")

    # iterate over all sheets in the Excel file
    for sheet in data:
        # only use sheets that are specified, or if none is specified then use all of them
        if (args.sheets is None) or (sheet.title in args.sheets):
            
            # some feedback for the user
            print(sheet.title)
            
            # read data from Excel file and generate numpy array
            # values are accessed by 'sheet["B28"].value' (where CellID "B28", ... is generated in for loops)
            OD  = np.array([[setOVERtoMAX(sheet['{}{}'.format(chr(starting_column+i),OD_start_row  + j)].value) for i in range(platex)] for j in range(platey) ],dtype=np.float64 )
            CFP = np.array([[setOVERtoMAX(sheet['{}{}'.format(chr(starting_column+i),CFP_start_row + j)].value) for i in range(platex)] for j in range(platey) ],dtype=np.float64 )
            GFP = np.array([[setOVERtoMAX(sheet['{}{}'.format(chr(starting_column+i),GFP_start_row + j)].value) for i in range(platex)] for j in range(platey) ],dtype=np.float64 )
            mC  = np.array([[setOVERtoMAX(sheet['{}{}'.format(chr(starting_column+i),mC_start_row  + j)].value) for i in range(platex)] for j in range(platey) ],dtype=np.float64 )
            
            # rescale, range is now [0:1]
            ODr  = rescale(OD,  log = args.logarithmic)
            CFPr = rescale(CFP, log = args.logarithmic)
            GFPr = rescale(GFP, log = args.logarithmic)
            mCr  = rescale(mC,  log = args.logarithmic)
            
            # initialize graphics generation
            CairoImage = cairo.ImageSurface(cairo.FORMAT_ARGB32,platex * args.pixelsize,4 * platey * args.pixelsize)
            context    = cairo.Context(CairoImage)
            
            # set the color blobs
            for x in range(platex):
                for y in range(platey):
                    context.set_source_rgb(ODr[y,x],ODr[y,x],ODr[y,x])
                    context.rectangle(x*args.pixelsize,(y + 0 * platey) * args.pixelsize,args.pixelsize,args.pixelsize)
                    context.fill()
                    
                    context.set_source_rgb(0,0,CFPr[y,x])
                    context.rectangle(x*args.pixelsize,(y + 1 * platey) * args.pixelsize,args.pixelsize,args.pixelsize)
                    context.fill()
                    
                    context.set_source_rgb(0,GFPr[y,x],0)
                    context.rectangle(x*args.pixelsize,(y + 2 * platey) * args.pixelsize,args.pixelsize,args.pixelsize)
                    context.fill()
                    
                    context.set_source_rgb(mCr[y,x],0,0)
                    context.rectangle(x*args.pixelsize,(y + 3 * platey) * args.pixelsize,args.pixelsize,args.pixelsize)
                    context.fill()
            
            # write graphics to file
            CairoImage.write_to_png(args.outbasename + sheet.title + '.png')
            

# if called from cmdline, then start here
if __name__ == "__main__":
    main()
