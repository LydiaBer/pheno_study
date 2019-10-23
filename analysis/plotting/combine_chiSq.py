#!/usr/bin/env python
'''

Welcome to combine_chiSq.py

 - This script takes in the csv files made by ntuples_to_chiSq.py.
 - Once the signal regions are specified, the script combines the chiSqs from their corresponding files.
 - Currently combines by evaluating the sum and maximum of the given chiSqSyst1pc
 - Outputs a single csv file containing the combined chiSq values
'''

# So Root ignores command line inputs so we can use argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import *
import os, sys, time, argparse, math, datetime, csv
from pprint import pprint
import pandas as pd


#____________________________________________________________________________
def main():
  
  t0 = time.time()

  print('\nCombine chi squares script\n')
  
  # ------------------------------------------------------
  # Input dir
  my_dir = 'loose_preselection' 
  #
  # ------------------------------------------------------
  # Input SRs to combine
  l_SR        = ['resolved-finalSR','intermediate-finalSR','boosted-finalSR']
  l_SRNN      = ['resolved-finalSRNN','intermediate-finalSRNN','boosted-finalSRNN']
  l_SRNNlam10 = ['resolved-finalSRNNlam10','intermediate-finalSRNNlam10','boosted-finalSRNNlam10']
  #
  # Column header whose value we want to combine
  #
  l_to_sum_vars = ['chiSq', 'chiSqSyst0p5pc', 'chiSqSyst1pc']

  for var in l_to_sum_vars:
    combine_set_of_SRs( l_SR,        var, my_dir )
    combine_set_of_SRs( l_SRNN,      var, my_dir )
    combine_set_of_SRs( l_SRNNlam10, var, my_dir )
  
  combine_set_of_SRs( l_SR,        'chiSq_ij_Sys1pc', my_dir, True )
  combine_set_of_SRs( l_SRNN,      'chiSq_ij_Sys1pc', my_dir, True )
  combine_set_of_SRs( l_SRNNlam10, 'chiSq_ij_Sys1pc', my_dir, True )

#____________________________________________________________________________
def combine_set_of_SRs(l_SRs, to_sum_var, my_dir, do_2dlambda=False):
  
  # Join SRs as the combined name output
  if do_2dlambda:
    out_file = 'data/CHISQ_2Dlambda_{0}_{1}_combined_{2}.csv'.format(my_dir, '_'.join(l_SRs), to_sum_var)
  else:
    out_file = 'data/CHISQ_{0}_{1}_combined_{2}.csv'.format(my_dir, '_'.join(l_SRs), to_sum_var)

  #
  # Columns to delete in new dataframe 
  l_del = ['N_bkg','N_sig','N_sig_raw',
    'SoverB','SoverSqrtB','SoverSqrtBSyst1pc','SoverSqrtBSyst5pc',
    'chiSq','chiSqSyst1pc','chiSqSyst0p5pc','acceptance','xsec'] 
  #  
  # ------------------------------------------------------
  
  print('-----------------------------------\n')
  print('List of SRs to combine:')
  pprint(l_SRs)
  print('Variable to combine: {0}'.format(to_sum_var) ) 
  print('\n-----------------------------------\n')
  
  # ------------------------------------------------------
  # Import data files for each SR into pandas dataframe
  # ------------------------------------------------------
  d_df = {}
  for SR in l_SRs:
    print( 'Processing {0}'.format(SR) )
    
    # Input CSV file
    if do_2dlambda:
      in_file = 'data/CHISQ_2Dlambda_{0}_{1}.csv'.format(my_dir, SR)
    else:
      in_file = 'data/CHISQ_{0}_{1}.csv'.format(my_dir,SR)
    
    # Read in CSV as pandas dataframe (like an excel spreadsheet but python-able)
    d_df[SR] = pd.read_csv( in_file )
    #print(d_df[SR])

  # ------------------------------------------------------
  # Clone the first dataframe into a new dataframe
  # ------------------------------------------------------
  combo_df = d_df[l_SRs[0]].copy()

  if not do_2dlambda:
    for var in l_del:
      del combo_df[var]

  # ------------------------------------------------------
  # Import chiSq from other dataframes and add to combo_df
  # ------------------------------------------------------
  for SR in l_SRs:
    new_col_name = SR + '_' + to_sum_var
    combo_df[new_col_name] = d_df[SR][to_sum_var]

  # ------------------------------------------------------
  # List the columns we want to sum by header name
  # ------------------------------------------------------
  l_cols_to_combine = [SR + '_' + to_sum_var for SR in l_SRs]

  # ------------------------------------------------------
  # Perform the combination of the values as new column
  # ------------------------------------------------------
  combo_sum = 'sum_' + to_sum_var
  combo_max = 'max_' + to_sum_var
  # Sum the chiSqs
  combo_df[combo_sum] = combo_df[l_cols_to_combine].astype(float).sum(axis=1)
  # Find the maximum of the chiSqs
  combo_df[combo_max] = combo_df[l_cols_to_combine].astype(float).max(axis=1)

  # ------------------------------------------------------
  # Save new combined dataframe as 
  # ------------------------------------------------------
  #print(combo_df)
  print('Saving as: {0}'.format(out_file))
  combo_df.to_csv(out_file, float_format='%g', index=False)

if __name__ == "__main__":
  main()
