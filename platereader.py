#!/usr/bin/env python3

import numpy as np
import argparse
import openpyxl


parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile",required=True,default=None)
args = parser.parse_args()


data = openpyxl.load_workbook(args.infile)

print(data.get_sheet_names())

OD_start_column = 28
CFP_start_column = 59 # ['B59', 'M66']
GFP_start_column = 90 # ['B90', 'M97']
mC_start_column  = 121 # ['B121','M128']

for sheet in data:
    try:
        od  = np.array([[sheet['{}{}'.format(chr(66+i),OD_start_column  + j)].value for i in range(12)] for j in range(8) ],dtype=np.float64 )
        cfp = np.array([[sheet['{}{}'.format(chr(66+i),CFP_start_column + j)].value for i in range(12)] for j in range(8) ],dtype=np.float64 )
        gfp = np.array([[sheet['{}{}'.format(chr(66+i),GFP_start_column + j)].value for i in range(12)] for j in range(8) ],dtype=np.float64 )
        
        # rescale
        
        od = (od - np.min(od))/(np.max(od) - np.min(od))
        
        print(od)
        
        
        #mC  = np.array([[sheet['{}{}'.format(chr(66+i),mC_start_column  + j)].value for i in range(12)] for j in range(8) ],dtype=np.float64 )
        print(sheet.title)
        #print(od,cfp,gfp)
    except:
        continue
