#!/usr/bin/env python
'''

Welcome to combine_chiSq.py

 - This script takes in the csv files made by ntuples_to_chiSq.py.
 - This finds the chiSq values for the 2 files so we can produce a combined contour (sum SRs chi2 values)
 - Outputs a single csv file containing the combined chiSq values
'''

# So Root ignores command line inputs so we can use argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import *
import os, sys, time, argparse, math, datetime, csv

# NOTE set up to combine 2 SRs only at present!! If use more than 2 will only combine first two 

#____________________________________________________________________________
def main():
  
  t0 = time.time()
  
  # Input dir
  dir = 'loose_preselection' 

  # For shape analysis
  l_SRs = [("resolved-finalSRNNlow","resolved-finalSRNN"),("intermediate-finalSRNNlow","intermediate-finalSRNN"),("boosted-finalSRNNlow","boosted-finalSRNN")]
  l_SRs = [("resolved-finalSRNNlam10low","resolved-finalSRNNlam10"),("intermediate-finalSRNNlam10low","intermediate-finalSRNNlam10"),("boosted-finalSRNNlam10low","boosted-finalSRNNlam10")]

  # Signal regions definition
  #l_SRs = [("resolved-finalSR","intermediate-finalSR"),("boosted-finalSR","resolved-finalSR_AND_intermediate-finalSR_combined")]
  #l_SRs = [("resolved-finalSRNNQCD","intermediate-finalSRNNQCD"),("boosted-finalSRNNQCD","resolved-finalSRNNQCD_AND_intermediate-finalSRNNQCD_combined")]
  #l_SRs = [("resolved-finalSRNNQCDTop","intermediate-finalSRNNQCDTop"),("boosted-finalSRNNQCDTop","resolved-finalSRNNQCDTop_AND_intermediate-finalSRNNQCDTop_combined")]
  #l_SRs = [("resolved-finalSRNN","intermediate-finalSRNN"),("boosted-finalSRNN","resolved-finalSRNN_AND_intermediate-finalSRNN_combined")]
  #l_SRs = [("resolved-finalSRNN","intermediate-finalSRNN"),("boosted-finalSRNN","resolved-finalSRNN_AND_intermediate-finalSRNN_combined")]
  #l_SRs = [("resolved-finalSRNNlow_AND_resolved-finalSRNN_combined","intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined"),("boosted-finalSRNNlow_AND_boosted-finalSRNN_combined","resolved-finalSRNNlow_AND_resolved-finalSRNN_combined_AND_intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined_combined")]
  l_SRs = [("resolved-finalSRNNlam10low_AND_resolved-finalSRNNlam10_combined","intermediate-finalSRNNlam10low_AND_intermediate-finalSRNNlam10_combined"),("boosted-finalSRNNlam10low_AND_boosted-finalSRNNlam10_combined","resolved-finalSRNNlam10low_AND_resolved-finalSRNNlam10_combined_AND_intermediate-finalSRNNlam10low_AND_intermediate-finalSRNNlam10_combined_combined")]
  # ------------------------------------------------------
  # Loop over pairs of signal regions
  # ------------------------------------------------------
  for SRpair in l_SRs:
  
    # list of csv dictionaries for this pair
    l_d_csv = []

    out_file = 'data/CHISQ_{0}_{1}_AND_{2}_combined.csv'.format(dir,SRpair[0],SRpair[1])
 
    # ------------------------------------------------------
    # Loop over signal region in pair 
    # ------------------------------------------------------ 
    for SR in SRpair:

      in_file = 'data/CHISQ_{0}_{1}.csv'.format(dir,SR)
  

      # ------------------------------------------------------
      # First Convert the csv into lists 
      # where column header is key of dictionary, values as list
      # ------------------------------------------------------
      d_csv = csv_to_lists( in_file )

      # ------------------------------------------------------
      # Save list of d_csv 
      # ------------------------------------------------------
      l_d_csv.append(d_csv)

    #print l_d_csv

    # ------------------------------------------------------
    #
    # Now commence combination of chiSq
    #
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Loop over zCols 
    # ------------------------------------------------------
    
    d_zCol_combined_chiSq = {}
    
    xCol, yCol, l_zCols = 'TopYuk', 'SlfCoup', ['chiSq','chiSqSyst1pc'] 
 
    for zCol in l_zCols:
            
      print( '--------------------------------------------------------------' )
      print( '\nWelcome to combine_chiSq.py\n' )
      print( 'Input: {0}'.format(in_file) )  
      print( 'Using the column headers: {0} {1} {2}'.format(xCol, yCol, zCol))
      print( 'Saving combined chiSq csv to file:\n  {0}\n'.format(out_file) )
      print( '-----------------------------------------------------------------\n' )

      # ------------------------------------------------------
      # loop over dictionaries in d_csv and save zCol for each
      # l_zCol is list containing zCol from each of the SRs 
      # ------------------------------------------------------
      l_zCol = [] 
      for d_csv in l_d_csv:
        l_zCol.append(d_csv[zCol])

      # ------------------------------------------------------
      # Sum chi2 index wise value for list of zCol
      # i.e. for each mass point in two signal regions sum both chi2 
      #------------------------------------------------------
  
      a,b = l_zCol[0], l_zCol[1]
 
      a = map(float,a)
      b = map(float,b) 
      from operator import add
      l_combined_chiSq = list(map(add, a,b))

      d_zCol_combined_chiSq[zCol] = l_combined_chiSq

    # ------------------------------------------------------
    # Rebuild combined csv file with xCol, yCol and combined zCol
    # ------------------------------------------------------
    #print 'dict'
    #print d_zCol_combined_chiSq

    keys = []
    values = []

    for key,value in d_zCol_combined_chiSq.iteritems():
      keys.append(key)
      values.append(value) 
     
    with open(out_file, 'w') as f_out: 
      f_out.write('{0},{1},{2}\n'.format(xCol, yCol, ','.join(keys)))
      for count, ( x_val, y_val) in enumerate( zip( l_d_csv[0][xCol], l_d_csv[0][yCol]) ) :
        # make list of quad combined chi2 values for specified zCols for this signal point (count)
        combined_chiSq = list(zip(*values)[count])
        # turn list entries from float to string so can join with comma
        for i in range(len(combined_chiSq)): combined_chiSq[i]=str(combined_chiSq[i])
        # make into comma separated list 
        str_combined_chiSq=','.join(combined_chiSq)
        f_out.write('{0},{1},{2}\n'.format(x_val, y_val, str_combined_chiSq))
    
#__________________________________________
def csv_to_lists(csv_file):
  '''
  converts csv to dictionary of lists containing columns
  the dictionary keys is the header
  '''
  with open(csv_file) as input_file:
      reader = csv.reader(input_file)
      col_names = next(reader)
      #print col_names
      data = {name: [] for name in col_names}
      for line in reader:
        for pos, name in enumerate(col_names):
          data[name].append(line[pos])
  
  return data

if __name__ == "__main__":
  main()
