#!/usr/bin/env python
'''

Welcome to ntuples_to_chiSq.py

Loops through ntuples of signal samples defined in get_signal_xsec()
Calculates chiSq, S/B among other observables to a CSV

Requires running plot.py once to compute YIELD file for total background counts

* Configure various aspects in other files
    - cuts.py
    - samples.py
    - xsecs.py
'''

import argparse, os, sys, math
from array import array
import ROOT
from ROOT import *
from cuts import *
from samples import *
from xsecs import *

# Directory samples and in and will also be used in output names etc  
#dir = 'original_full_stats'
dir = '150719'
dir = '150719/merged_nn_score_ntuples'

# Get the sample paths from samples.py
bkg_path, sig_path, bkg_suffix, sig_suffix = get_sample_paths(dir)
 
# Impose 4 b-tags as weights
do_BTagWeight = True

# nominal signal name
samp_nom = 'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0'

# Do lambda_i vs lambda_j scan
do_lambda_ij = True

#____________________________________________________________________________
def main():

  mkdir('data')
  
  # -----------------------------------------------------------
  #
  # Some user configurables
  #
  # Luminosity
  lumi = 3000.0 # inverse fb
  # Analysis 
  l_samples  = ['loose']
  # Signal region (define in cuts.py)
  l_sig_regs = ['preselection'] 
  # Cut selections
  l_cut_sels = ['resolved-preselection', 'intermediate-preselection' ,'boosted-preselection',
                'resolved-commonSR',     'intermediate-commonSR',     'boosted-commonSR',
                'resolved-finalSR',      'intermediate-finalSR',      'boosted-finalSR', 
                'resolved-finalSRNN',      'intermediate-finalSRNN',      'boosted-finalSRNN' ] 

  l_cut_sels = [
          'resolved-finalSRNNlam_m20', 
          'intermediate-finalSRNNlam_m20',    
          'boosted-finalSRNNlam_m20', 
          'resolved-finalSRNNlam_m10', 
          'intermediate-finalSRNNlam_m10',    
          'boosted-finalSRNNlam_m10',
          'resolved-finalSRNNlam_m7', 
          'intermediate-finalSRNNlam_m7',    
          'boosted-finalSRNNlam_m7',
          'resolved-finalSRNNlam_m5', 
          'intermediate-finalSRNNlam_m5',    
          'boosted-finalSRNNlam_m5', 
          'resolved-finalSRNNlam_m2', 
          'intermediate-finalSRNNlam_m2',    
          'boosted-finalSRNNlam_m2', 
          'resolved-finalSRNNlam_m1', 
          'intermediate-finalSRNNlam_m1',    
          'boosted-finalSRNNlam_m1',
          'resolved-finalSRNNlam_m0p5', 
          'intermediate-finalSRNNlam_m0p5',    
          'boosted-finalSRNNlam_m0p5', 
          'resolved-finalSRNNlam0p5', 
          'intermediate-finalSRNNlam0p5',    
          'boosted-finalSRNNlam0p5', 
          'resolved-finalSRNN', 
          'intermediate-finalSRNN',    
          'boosted-finalSRNN',
          'resolved-finalSRNNlam2', 
          'intermediate-finalSRNNlam2',    
          'boosted-finalSRNNlam2',
          'resolved-finalSRNNlam3', 
          'intermediate-finalSRNNlam3',    
          'boosted-finalSRNNlam3', 
          'resolved-finalSRNNlam5', 
          'intermediate-finalSRNNlam5',    
          'boosted-finalSRNNlam5', 
          'resolved-finalSRNNlam7', 
          'intermediate-finalSRNNlam7',    
          'boosted-finalSRNNlam7', 
          'resolved-finalSRNNlam10', 
          'intermediate-finalSRNNlam10',    
          'boosted-finalSRNNlam10', 
          'resolved-finalSRNNlam20', 
          'intermediate-finalSRNNlam20',    
          'boosted-finalSRNNlam20'
  ]

  l_cut_sels = ['resolved-finalSR',      'intermediate-finalSR',      'boosted-finalSR',
                'resolved-finalSRNN',    'intermediate-finalSRNN',    'boosted-finalSRNN', 
                'resolved-finalSRNNlam10', 'intermediate-finalSRNNlam10',    'boosted-finalSRNNlam10' ] 
  #================================================
  
  # -------------------------------------------------------------
  # Argument parser
  parser = argparse.ArgumentParser(description='Analyse background/signal TTrees and make plots.')
  parser.add_argument('-s', '--cut_sel', type=str, nargs='?', help='Selection cuts considered.')
 
  args = parser.parse_args()
  if args.cut_sel:
    l_cut_sels = [ args.cut_sel ] 
  #
  # -----------------------------------------------------------

  for analysis in l_samples:
    for sig_reg in l_sig_regs:
      for cut_sel in l_cut_sels:
  
        print( 'Analysis: {0}'.format(analysis) )
        print( 'Signal region: {0}'.format(sig_reg) )
        print( 'Cut selection: {0}'.format(cut_sel) )
        
        # Yield file is the input file with the background yield from plot.py
        yield_file = 'figs/{0}/YIELD_{1}_{2}_{3}.txt'.format(dir, analysis, sig_reg, cut_sel)

        # Save file is where we will store the outputs
        save_file  = 'data/CHISQ_{0}_{1}_{2}.csv'.format(analysis, sig_reg, cut_sel)
        
        print('Input file with background yield: {0}'.format( yield_file ) )
        print('Output file to store chi squares: {0}'.format( save_file  ) )

        do_selection( yield_file, save_file, lumi, sig_reg, cut_sel, samp_nom)

#____________________________________________________________________________
def do_selection( yield_file, save_file, lumi, sig_reg, cut_sel, samp_nom):
  '''
  Given N_bkg from yield file, sig_reg, cut_sel, 
  will loop over signals and output the chi squares into save_file
  '''
    
  # Extract background yield
  try:
    with open( yield_file, 'r' ) as f_in:
      for line in f_in:
        if 'TotBkg' not in line: continue
        N_bkg = float( line.split(',')[2] )
  except:
    print('No YIELD file, please run plot.py. Will take N_bkg as 1000. for now')
    N_bkg = 1000.
  # -----------------------------------------------------------
  # 
  # Prepare the signals and cuts
  #
  # Get the signal list 
  l_sig_list = get_signal_list()

  # Variable to plot in
  var  = 'm_hh'
  # Get cut strings from cuts.py
  unweighted_cuts, l_cuts = configure_cuts(cut_sel) 
  # -----------------------------------------------------------
  
  print('Background yield: {0}'.format(N_bkg) )
  print('Luminosity: {0} /fb '.format(lumi) )
  print('Unweighted cuts: {0}'.format(unweighted_cuts) )
  
  # ---------------------------------------
  # Get nominal signal yield
  # ---------------------------------------
  N_sig_nom = get_N_sig_nom( lumi, var, unweighted_cuts, samp_nom)

  # ---------------------------------------
  # Now loop through coupling variations
  # ---------------------------------------
  with open(save_file, 'w') as f_out:
    header  = 'TopYuk,SlfCoup,N_bkg,N_sig,N_sig_raw,'
    header += 'SoverB,SoverSqrtB,SoverSqrtBSyst1pc,SoverSqrtBSyst5pc,'
    header += 'chiSq,chiSqSyst1pc,chiSqSyst0p5pc,acceptance,xsec\n'
    f_out.write( header )

    for signal in l_sig_list:  
      out_str = compute_chiSq( f_out, signal, lumi, var, unweighted_cuts, N_bkg, N_sig_nom )
      if not out_str == 'NoFile':
        f_out.write( out_str )
        print( out_str )

  # ---------------------------------------
  # Compare 2d lambda discrimination power
  # i.e. compare chiSq vs lambda_i vs lambda_j
  # Not just chiSq wrt SM value
  # ---------------------------------------

  if do_lambda_ij:

    print('\n-----------------------------------------------')
    print('Performing 2D chiSq(i,j) vs lambda_i vs lambda_j')
    print('-------------------------------------------------')

    save_file_2d = save_file.replace('CHISQ_', 'CHISQ_2Dlambda_')
    with open(save_file_2d, 'w') as f_out2d:
      header2d = 'lambda_i,lambda_j,chiSq_ij_Sys1pc,chiSq_ij\n'
      f_out2d.write( header2d )

      for signal_i in l_sig_list:
        # For simplicity do this for ytop = 1.0
        if 'TopYuk_1.0' not in signal_i: continue 
        N_sig_nom_i = get_N_sig_nom( lumi, var, unweighted_cuts, signal_i)
        for signal_j in l_sig_list:
          if 'TopYuk_1.0' not in signal_j: continue 
          long_out = compute_chiSq( f_out, signal_j, lumi, var, unweighted_cuts, N_bkg, N_sig_nom_i )
        
          # Extract the lambdas
          lambda_i = float( signal_i.split('_')[7].replace('m', '-') )
          lambda_j = float( signal_j.split('_')[7].replace('m', '-') )
          
          # Extract chi squares
          chiSq       = float(long_out.split(',')[9])
          chiSqSys1pc = float(long_out.split(',')[10])
      
          out_str = '{0:.1f},{1:.1f},{2:.4g},{3:.4g}\n'.format(lambda_i, lambda_j, chiSqSys1pc, chiSq)
          f_out2d.write(out_str)

  print('\n------------------------------------------------------')
  print('Saved outputs to: {0}'.format(save_file) )
  print('------------------------------------------------------')

#____________________________________________________________________________
def get_N_sig_nom( lumi, var, unweighted_cuts, samp_nom):
  ''' 
  Get nominal yield for chi square calculation
  '''
  
  print('\nGetting the nominal signal yield\n')
  
  root_nom = sig_path + '/' +  samp_nom + '.root'
  print('Nominal root file: {0}'.format(root_nom))

  tfile = TFile( root_nom )

  # dictionary to store histogram info 
  d_hists = {}
  
  # obtain histogram from file and store to dictionary entry
  Nbins = 1
  xmin = -100.0
  xmax = 10000
  d_hists[samp_nom] = apply_cuts_weights_to_tree( tfile, samp_nom, var, lumi, unweighted_cuts, Nbins, xmin, xmax)

  # extract key outputs of histogram 
  nYield, nYieldErr, nRaw, xsec = d_hists[samp_nom]
  print('In cut: {0},{1},{2},{3}'.format(nYield, nYieldErr, nRaw,xsec)) 
    
  N_sig_nom = nYield
  print('Nominal signal yield: {0}'.format( N_sig_nom ))

  return N_sig_nom    

#_______________________________________________________
def apply_cuts_weights_to_tree(f, hname, var, lumi, unweighted_cuts='', Nbins=100, xmin=0, xmax=100000):
  '''
  Obtain yields by performing TTree.Project() to impose cuts & apply weights
  '''
  th1 = TH1D('h_sig', "", Nbins, xmin, xmax) 
  ttree = f.Get('preselection')

  N_raw = f.Get('loose_cutflow').GetBinContent(1)

  d_xsecs = configure_xsecs()
  xsec = d_xsecs[hname]
  
  if do_BTagWeight:
    my_weight = 'h1_j1_BTagWeight * h1_j2_BTagWeight * h2_j1_BTagWeight * h2_j2_BTagWeight'
  else:
    my_weight = 1.

  cuts = '( ({0}) * (1000 * {1} * {2} * {3}) ) / {4}'.format( unweighted_cuts, xsec, lumi, my_weight, N_raw ) # Factor of 1000 to convert xsec from ifb to ipb

  print('Weighted signal cuts: {0}'.format(cuts) )
  
  ttree.Project( 'h_sig', var, cuts )
  
  # Perform integrals to find total yield
  nYieldErr = ROOT.Double(0)
  nYield    = th1.IntegralAndError(0, Nbins+1, nYieldErr)

  print( 'Sample {0} has integral {1:.3f} +/- {2:.3f}'.format( hname, nYield, nYieldErr))
  # =========================================================
  
  nRaw = th1.GetEntries()
  
  return nYield, nYieldErr, nRaw, xsec

#____________________________________________________________________________
def compute_chiSq( f_out, signal, lumi, var, unweighted_cuts, N_bkg, N_sig_nom ):
  '''
  Perform cuts onto the signal file
  and compute various metrics like S/B, chi square etc
  ''' 
  print('\nComputing chi square for {0}'.format(signal) )
  
  # ------------------------------------------------------
  # Extract coupling values from file name
  # ------------------------------------------------------
  info = signal.split('_')
  TopYuk  = float( info[5] )
  SlfCoup = float( info[7].replace('m', '-') )
  root_signal = sig_path + '/' + signal + '.root'
  print( 'Root file: {0}'.format( root_signal ) )

  tfile = TFile( root_signal )

  # dictionary to store histogram info 
  d_sig_hists = {}
  
  # obtain histogram from file and store to dictionary entry
  Nbins = 1
  xmin = -100.0
  xmax = 10000
  d_sig_hists[signal] = apply_cuts_weights_to_tree( tfile, signal, var, lumi, unweighted_cuts, Nbins, xmin, xmax)

  # extract key outputs of histogram 
  nYield, nYieldErr, nRaw, xsec = d_sig_hists[signal]
  print('In cut: {0},{1},{2},{3}'.format(nYield, nYieldErr, nRaw, xsec)) 

  N_sig     = nYield 
  N_sig_raw = nRaw 
  print('Signal {0} yield: {1:.3g}, raw: {2}'.format(signal, N_sig, N_sig_raw))

  # ------------------------------------------------------
  # Calculate purity S / B and significance S / sqrt(B)
  # ------------------------------------------------------
  SoverB            = N_sig / N_bkg
  SoverSqrtB        = N_sig / math.sqrt( N_bkg )
  SoverSqrtBSyst1pc = N_sig / math.sqrt( N_bkg + (0.01 * N_bkg ) ** 2 )
  SoverSqrtBSyst5pc = N_sig / math.sqrt( N_bkg + (0.05 * N_bkg ) ** 2 )
  
  # ------------------------------------------------------
  # Calculate the chi squares
  # ------------------------------------------------------
  chiSq          = ( N_sig - N_sig_nom ) ** 2 / ( N_bkg )
  chiSqSyst1pc   = ( N_sig - N_sig_nom ) ** 2 / ( N_bkg + (0.01 * N_bkg ) ** 2 )
  chiSqSyst0p5pc = ( N_sig - N_sig_nom ) ** 2 / ( N_bkg + (0.005 * N_bkg ) ** 2 )
  
  # ------------------------------------------------------
  # Calculate acceptance
  # ------------------------------------------------------
  acceptance = N_sig / ( xsec * lumi * 1000.)

  # ------------------------------------------------------
  # Construct string of values to output
  # ------------------------------------------------------
  out_str  = '{0},{1},{2:.4g},{3:.4g},{4:.4g},'.format( TopYuk, SlfCoup,      N_bkg,             N_sig, N_sig_raw )
  out_str += '{0:.4g},{1:.4g},{2:.4g},{3:.4g},'.format( SoverB, SoverSqrtB,   SoverSqrtBSyst1pc, SoverSqrtBSyst5pc  )
  out_str += '{0:.4g},{1:.4g},{2:.4g},{3:.4g},{4}'.format( chiSq,  chiSqSyst1pc, chiSqSyst0p5pc, acceptance, xsec )
  out_str += '\n'

  return out_str

#_________________________________________________________________________
def get_signal_list():
  '''
  Get list of signals to consider 
  '''
  l_sig_list = [
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m20.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m10.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m7.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m5.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m3.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m2.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m1.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m0.5',
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_0.5',  
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_1.0',   
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_2.0',  
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_5.0',   
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_7.0',  
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_10.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_20.0',  
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m20.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m10.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m7.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m5.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m2.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m1.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_0.5',  
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_1.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_2.0',  
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_3.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_5.0',  
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_7.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_10.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_20.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m10.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m7.0',  
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m5.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m2.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m1.0',  
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_1.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_2.0',   
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_3.0',  
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_5.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_7.0',
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_10.0', 
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_20.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m20.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m15.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m10.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m9.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m8.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m7.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m6.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m4.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m2.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m1.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m1.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_0.8',  
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.2', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_4.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_6.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_7.0',   
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_8.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_9.0',   
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_15.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_20.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m20.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m10.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m7.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m5.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m2.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m1.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_1.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_2.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_3.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_5.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_7.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_10.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_20.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m20.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m10.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m7.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m5.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m2.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m1.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_1.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_2.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_3.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_5.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_7.0',  
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_10.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_20.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m20.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m10.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m7.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m5.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m2.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m1.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m0.5',
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_0.5', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_1.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_2.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_3.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_5.0', 
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_7.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_10.0',
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_20.0',
  ]

  return l_sig_list

#_________________________________________________________________________
def mkdir(dirPath):

  # Makes new directory @dirPath

  try:
    os.makedirs(dirPath)
    print 'Successfully made new directory ' + dirPath
  except OSError:
    pass

if __name__ == "__main__":
  main()
