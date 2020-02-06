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
  #
  # Column header whose value we want to combine
  #
  #l_to_sum_vars = ['chiSq', 'chiSqSyst0p3pc', 'chiSqSyst1pc', 'chiSqSyst1p5pc', 'chiSqSyst2pc', 'chiSqSyst5pc']

  chiSqLabel = 'chiSqSystMix'
    
  d_SRvar_sets = {

    # Inclusive baselines 
    'SR'        : ['SR-res:chiSqSyst0p3pc',
                   'SR-int:chiSqSyst1pc',
                   'SR-bst:chiSqSyst5pc'],

    'SRNN-lam1'   : ['SRNN-res-lam1:chiSqSyst0p3pc',
                     'SRNN-int-lam1:chiSqSyst1pc',
                     'SRNN-bst-lam1:chiSqSyst5pc'],

    'SRNN-lam5'   : ['SRNN-res-lam5:chiSqSyst0p3pc',
                     'SRNN-int-lam5:chiSqSyst1pc',
                     'SRNN-bst-lam5:chiSqSyst5pc'],

    # Multibin baseline (no DNN)
    'SR_res_multibin' : [
                'SR-res-200mHH250:chiSqSyst0p3pc',
                'SR-res-250mHH300:chiSqSyst0p3pc',
                'SR-res-300mHH350:chiSqSyst0p3pc',
                'SR-res-350mHH400:chiSqSyst0p3pc',
                'SR-res-400mHH500:chiSqSyst0p3pc',
                'SR-res-500mHH:chiSqSyst0p3pc',
    ],

    'SR_int_multibin' : [
                'SR-int-200mHH500:chiSqSyst1pc',
                'SR-int-500mHH600:chiSqSyst1pc',
                'SR-int-600mHH:chiSqSyst1pc',
    ],
                
    'SR_bst_multibin' : [
                'SR-bst-500mHH800:chiSqSyst5pc',
                'SR-bst-800mHH:chiSqSyst5pc',
               ],

    'SR_all_multibin' : [
                'SR-res-200mHH250:chiSqSyst0p3pc',
                'SR-res-250mHH300:chiSqSyst0p3pc',
                'SR-res-300mHH350:chiSqSyst0p3pc',
                'SR-res-350mHH400:chiSqSyst0p3pc',
                'SR-res-400mHH500:chiSqSyst0p3pc',
                'SR-res-500mHH:chiSqSyst0p3pc',
                
                'SR-int-200mHH500:chiSqSyst1pc',
                'SR-int-500mHH600:chiSqSyst1pc',
                'SR-int-600mHH:chiSqSyst1pc',
                
                'SR-bst-500mHH800:chiSqSyst5pc',
                'SR-bst-800mHH:chiSqSyst5pc',
               ],
                
    # Multibin baseline with DNN cut trained on k(lambda)=1
    'SRNN_res_multibin_lam1' : [
                'SRNN-res-200mHH250-lam1:chiSqSyst0p3pc',
                'SRNN-res-250mHH300-lam1:chiSqSyst0p3pc',
                'SRNN-res-300mHH350-lam1:chiSqSyst0p3pc',
                'SRNN-res-350mHH400-lam1:chiSqSyst0p3pc',
                'SRNN-res-400mHH500-lam1:chiSqSyst0p3pc',
                'SRNN-res-500mHH-lam1:chiSqSyst0p3pc',
    ],
                
    'SRNN_int_multibin_lam1' : [
                'SRNN-int-200mHH500-lam1:chiSqSyst1pc',
                'SRNN-int-500mHH600-lam1:chiSqSyst1pc',
                'SRNN-int-600mHH-lam1:chiSqSyst1pc',
    ],

    'SRNN_bst_multibin_lam1' : [
                'SRNN-bst-500mHH800-lam1:chiSqSyst5pc',
                'SRNN-bst-800mHH-lam1:chiSqSyst5pc', 
                ],
    
    
    'SRNN_all_multibin_lam1' : [
                'SRNN-res-200mHH250-lam1:chiSqSyst0p3pc',
                'SRNN-res-250mHH300-lam1:chiSqSyst0p3pc',
                'SRNN-res-300mHH350-lam1:chiSqSyst0p3pc',
                'SRNN-res-350mHH400-lam1:chiSqSyst0p3pc',
                'SRNN-res-400mHH500-lam1:chiSqSyst0p3pc',
                'SRNN-res-500mHH-lam1:chiSqSyst0p3pc',

                'SRNN-int-200mHH500-lam1:chiSqSyst1pc',
                'SRNN-int-500mHH600-lam1:chiSqSyst1pc',
                'SRNN-int-600mHH-lam1:chiSqSyst1pc',

                'SRNN-bst-500mHH800-lam1:chiSqSyst5pc',
                'SRNN-bst-800mHH-lam1:chiSqSyst5pc', 
                ],

    # Multibin baseline with DNN cut trained on k(lambda)=5
    'SRNN_res_multibin_lam5' : [
                'SRNN-res-200mHH250-lam5:chiSqSyst0p3pc',
                'SRNN-res-250mHH300-lam5:chiSqSyst0p3pc',
                'SRNN-res-300mHH350-lam5:chiSqSyst0p3pc',
                'SRNN-res-350mHH400-lam5:chiSqSyst0p3pc',
                'SRNN-res-400mHH500-lam5:chiSqSyst0p3pc',
                'SRNN-res-500mHH-lam5:chiSqSyst0p3pc',
    ],
                
    'SRNN_int_multibin_lam5' : [
                'SRNN-int-200mHH500-lam5:chiSqSyst1pc',
                'SRNN-int-500mHH600-lam5:chiSqSyst1pc',
                'SRNN-int-600mHH-lam5:chiSqSyst1pc',
    ],

    'SRNN_bst_multibin_lam5' : [
                'SRNN-bst-500mHH800-lam5:chiSqSyst5pc',
                'SRNN-bst-800mHH-lam5:chiSqSyst5pc', 
                ],   
    
    'SRNN_all_multibin_lam5' : [
                'SRNN-res-200mHH250-lam5:chiSqSyst0p3pc',
                'SRNN-res-250mHH300-lam5:chiSqSyst0p3pc',
                'SRNN-res-300mHH350-lam5:chiSqSyst0p3pc',
                'SRNN-res-350mHH400-lam5:chiSqSyst0p3pc',
                'SRNN-res-400mHH500-lam5:chiSqSyst0p3pc',
                'SRNN-res-500mHH-lam5:chiSqSyst0p3pc',
    
                'SRNN-int-200mHH500-lam5:chiSqSyst1pc',
                'SRNN-int-500mHH600-lam5:chiSqSyst1pc',
                'SRNN-int-600mHH-lam5:chiSqSyst1pc',
    
                'SRNN-bst-500mHH800-lam5:chiSqSyst5pc',
                'SRNN-bst-800mHH-lam5:chiSqSyst5pc', 
                ],


    # Multibin baseline with DNN cut trained on k(lambda)=7
    'SRNN_res_multibin_lam7' : [
                'SRNN-res-200mHH250-lam7:chiSqSyst0p3pc',
                'SRNN-res-250mHH300-lam7:chiSqSyst0p3pc',
                'SRNN-res-300mHH350-lam7:chiSqSyst0p3pc',
                'SRNN-res-350mHH400-lam7:chiSqSyst0p3pc',
                'SRNN-res-400mHH500-lam7:chiSqSyst0p3pc',
                'SRNN-res-500mHH-lam7:chiSqSyst0p3pc',
    ],

    'SRNN_int_multibin_lam7' : [
                'SRNN-int-200mHH500-lam7:chiSqSyst1pc',
                'SRNN-int-500mHH600-lam7:chiSqSyst1pc',
                'SRNN-int-600mHH-lam7:chiSqSyst1pc',
    ],

    'SRNN_bst_multibin_lam7' : [
                'SRNN-bst-500mHH800-lam7:chiSqSyst5pc',
                'SRNN-bst-800mHH-lam7:chiSqSyst5pc', 
                ],   
    
    'SRNN_all_multibin_lam7' : [
                'SRNN-res-200mHH250-lam7:chiSqSyst0p3pc',
                'SRNN-res-250mHH300-lam7:chiSqSyst0p3pc',
                'SRNN-res-300mHH350-lam7:chiSqSyst0p3pc',
                'SRNN-res-350mHH400-lam7:chiSqSyst0p3pc',
                'SRNN-res-400mHH500-lam7:chiSqSyst0p3pc',
                'SRNN-res-500mHH-lam7:chiSqSyst0p3pc',
    
                'SRNN-int-200mHH500-lam7:chiSqSyst1pc',
                'SRNN-int-500mHH600-lam7:chiSqSyst1pc',
                'SRNN-int-600mHH-lam7:chiSqSyst1pc',
    
                'SRNN-bst-500mHH800-lam7:chiSqSyst5pc',
                'SRNN-bst-800mHH-lam7:chiSqSyst5pc', 
                ],
  }


  for SRvar_set in d_SRvar_sets:
    # TODO combine_set_of_SRs( SRvar_set, d_SRvar_sets, 'chiSq_ij_Sys0p3pc', my_dir, chiSqLabel, True )
    combine_set_of_SRs( SRvar_set, d_SRvar_sets, my_dir, chiSqLabel)
  
#____________________________________________________________________________
def combine_set_of_SRs(SRvar_set, d_SRvar_sets, my_dir, chiSqLabel, do_2dlambda=False):

  #
  # Columns to delete in new dataframe 
  l_del = ['N_bkg','N_sig','N_sig_raw',
    'SoverB','SoverSqrtB','SoverSqrtBSyst5pc','SoverSqrtBSyst2pc','SoverSqrtBSyst1p5pc','SoverSqrtBSyst1pc','SoverSqrtBSyst0p3pc',
    'chiSq','chiSqSyst5pc','chiSqSyst2pc','chiSqSyst1p5pc','chiSqSyst1pc','chiSqSyst0p3pc','acceptance','xsec'] 
  
  # Get the list of SRs and vars to combine
  l_SRvars = d_SRvar_sets[SRvar_set]
 
  # Join SRs and vars as the combined name output
  #SRvar_names = '_'.join(l_SRvars).replace(':','_') 

  if do_2dlambda:
    #TODO 
    out_file = 'data/CHISQ_2Dlambda_{0}_{1}_combined_{2}.csv'.format(my_dir, SR_set, to_sum_var)
  else:
    out_file = 'data/CHISQ_{0}_{1}_combined_{2}.csv'.format(my_dir, SRvar_set, chiSqLabel)
  
  print('-----------------------------------\n')
  print('List of SR var combos to combine:')
  pprint(l_SRvars)
  print('\n-----------------------------------\n')
 
  # ------------------------------------------------------
  # Import data files for each SR into pandas dataframe
  # ------------------------------------------------------
  d_df = {}
  for SRvar in l_SRvars:
    print( 'Processing {0}'.format(SRvar) )

    # Extract SR from SRvar   
    SR = SRvar.split(":")[0] 

    # Input CSV file
    if do_2dlambda:
      # TODO
      in_file = 'data/CHISQ_2Dlambda_{0}_{1}.csv'.format(my_dir, SR)
    else:
      in_file = 'data/CHISQ_{0}_{1}.csv'.format(my_dir,SR)
    
    # Read in CSV as pandas dataframe (like an excel spreadsheet but python-able)
    d_df[SR] = pd.read_csv( in_file )
    #print(d_df[SR])

  # ------------------------------------------------------
  # Clone the first dataframe into a new dataframe
  # ------------------------------------------------------
  SR_0 = l_SRvars[0].split(":")[0] 
  combo_df = d_df[SR_0].copy()

  if not do_2dlambda:
    for var in l_del:
      del combo_df[var]

  # ------------------------------------------------------
  # Import chiSq from other dataframes and add to combo_df
  # ------------------------------------------------------
  l_cols_to_combine = []

  for SRvar in l_SRvars:

    # Extract SR and var from SRvar   
    SR  = SRvar.split(":")[0] 
    to_sum_var = SRvar.split(":")[1] 

    new_col_name = SR + '_' + to_sum_var
    combo_df[new_col_name] = d_df[SR][to_sum_var]

    # ------------------------------------------------------
    # List the columns we want to sum by header name
    # ------------------------------------------------------
    l_cols_to_combine.append(SR + '_' + to_sum_var)

  # ------------------------------------------------------
  # Perform the combination of the values as new column
  # ------------------------------------------------------
  combo_sum = 'sum_' + chiSqLabel
  combo_max = 'max_' + chiSqLabel
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
