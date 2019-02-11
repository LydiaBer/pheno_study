#!/usr/bin/env python
'''

Welcome to ntuples_to_chiSq.py

Loops through ntuples of signal samples and calculates chiSq, S/B among other things to a CSV
Depends on cuts defined in cuts.py
Needs an estimate of background yield

TODO: Lots of work needed 
e.g. let user give input, output, signal region selection using argparse
extend to resolved, intermediate

'''

import argparse, os, sys, math
from array import array
from ROOT import *
from cuts import *

#____________________________________________________________________________
def main():

  # Path to the intermediate ntuples
  sig_path = '/home/jesseliu/pheno/fcc/PhenoSim/data/samples/14TeV/2018nov26/all_merged_delphes/ntuples/merged_signals'

  mkdir('data')
  
  # Output path to save CSV
  #save_file = 'data/SR-1ibsmall-2ibtrk-Mass_300invfb_5pcSyst.txt'
  save_file = 'data/SR-1ibsmall-2ibtrk_300invfb_5pcSyst.txt'
  
  # -----------------------------------------------------------
  #
  # Some user configurables
  #
  # Luminosity
  lumi = 300.0 # inverse fb
  # Signal region (define in cuts.py)
  sig_reg  = 'SR-1ibsmall-2ibtrk'
  # Fractional systematic
  syst = 0.05
  # Insert background yield (calculate from plot.py)
  N_bkg = 2023.5 * float(lumi)
  # normalised to 1/fb SR-1ibsmall-2ibtrk-Mass
  #N_bkg = 343.565 * float(lumi)
  # -----------------------------------------------------------

 
  # -----------------------------------------------------------
  # 
  # Prepare the signals and cuts
  #
  # Get the cross-section file
  d_xsec = get_xsec()
  # Get the list of signals
  l_sig  = get_list_signals()
  # Variable to plot in
  var  = 'm_h2'
  # Dummy cut to use cuts.py
  add_cuts = 'm_h2 > 0'
  # Get cut strings from cuts.py
  unweighted_cuts, l_cuts = configure_cuts(var, add_cuts, sig_reg) 
  # -----------------------------------------------------------
  
  print('Background yield: {0}'.format(N_bkg) )
  print('Luminosity: {0} /fb '.format(lumi) )
  print('Unweighted cuts: {0}'.format(unweighted_cuts) )

  Nbins = 1
  xmin = 0.0
  xmax = 10000
  
  # ---------------------------------------
  # Calculate signal yields & sensitivity
  # ---------------------------------------
  d_sig_file = {}
  d_sig_hist = {}
  d_sig_tree = {}
  d_sig_yield = {}

  # ---------------------------------------
  # Get nominal yield for chi square calculation
  # ---------------------------------------
  root_nom = sig_path + '/intermediate_TopYuk_1.0_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM.root'
  print('Nominal root file: {0}'.format(root_nom))
  tfile = TFile( root_nom )
  N_nom_raw = tfile.Get('intermediate_cutflow').GetBinContent(1)
  nom_xsec = 0.016078
  cuts = '( {0} * (1000 * {1} * {2}) ) / {3}'.format(unweighted_cuts, nom_xsec, lumi, N_nom_raw)
  print('Weighted signal cuts: {0}'.format(cuts) )
  
  # Project and make histogram
  ttree_nom = tfile.Get('preselection')
  ttree_nom.Project( 'h_sig_nom', var, cuts )
  th1_nom = TH1D('h_sig_nom', "", Nbins, xmin, xmax) 
  yield_nom =  th1_nom.Integral()
  print('Nominal signal yield: {0}'.format(yield_nom))

  # ---------------------------------------
  # Now loop through coupling variations
  # ---------------------------------------
  with open(save_file, 'w') as f_out: 
    f_out.write('TopYuk,SlfCoup,N_bkg,N_sig,N_sig_raw,SoverB,SoverSqrtB,SoverSqrtBSyst,chiSq,chiSqSyst,chiSqSyst1pc,acc\n')

    for signal in l_sig:
      
      print('\nProcessing {0}'.format(signal) )

      info = signal.split('.root')[0].split('_')
      TopYuk  = float(info[2])
      SlfCoup = float(info[4].replace('m', '-'))

      root_signal = sig_path + '/' + signal
      print('Root file: {0}'.format(root_signal) )

      d_sig_file[signal] = TFile( root_signal )
      d_sig_hist[signal] = TH1D('h_sig_' + signal, "", Nbins, xmin, xmax) 

      # Inititalise
      xsec_sig = 1.0 
      N_orig_raw = 10 

      # Get the signal cross-section
      try:
        xsec_sig = float( d_xsec[signal.split('.root')[0]] )
        print('Cross-section [pb]: {0} '.format(xsec_sig) )
      except KeyError:
        print('signal {0} has no cross-section, skipping...\n'.format(signal))
        continue
      
      # Get the initial number of events before any cuts
      try:
        N_orig_raw = d_sig_file[signal].Get('intermediate_cutflow').GetBinContent(1)
      except AttributeError:
        print('{0} has no intermediate_cutflow histogram, skipping...'.format(d_sig_file[signal]))
        continue
      cuts = '( ({0}) * (1000 * {1} * {2}) ) / {3}'.format(unweighted_cuts, xsec_sig, lumi, N_orig_raw)
      print('Weighted signal cuts: {0}'.format(cuts) )
      
      # Project and make histogram
      d_sig_tree[signal] = d_sig_file[signal].Get('preselection')
      d_sig_tree[signal].Project( 'h_sig_' + signal, var, cuts )

      N_sig = d_sig_hist[signal].Integral()
      N_sig_raw = d_sig_hist[signal].GetEntries()
      print('Signal {0} yield: {1}, raw: {2}'.format(signal, N_sig, N_sig_raw))

      # Calculate purity S / B and significance S / sqrt(B)
      SoverB         = float(N_sig) / float(N_bkg)
      SoverSqrtB     = float(N_sig) / math.sqrt( float(N_bkg) )
      SoverSqrtBSyst = float(N_sig) / math.sqrt( float(N_bkg) + (syst * float(N_bkg) ) ** 2 )
      
      # Calculate the chi squares
      chiSq         = ( float(N_sig) - float(yield_nom) ) ** 2 / float(N_bkg) 
      chiSqSyst     = ( float(N_sig) - float(yield_nom) ) ** 2 / ( float(N_bkg) + (syst * float(N_bkg) ) ** 2 )
      chiSqSyst1pc  = ( float(N_sig) - float(yield_nom) ) ** 2 / ( float(N_bkg) + (0.01 * float(N_bkg) ) ** 2 )
      
      # Calculate acceptance
      acc = d_sig_hist[signal].GetEntries() / float( N_orig_raw )

      print( 'Signal {0}: {1}, {2}, {3}, {4}'.format( signal, N_bkg, N_sig, SoverSqrtB, SoverSqrtBSyst ) )
      f_out.write('{0},{1},{2:.3g},{3:.3g},{4:.3g},{5:.3g},{6:.3g},{7:.3g},{8:.3g},{9:.3g},{10:.3g},{11:.3g}\n'.format(TopYuk, SlfCoup, N_bkg, N_sig, N_sig_raw, SoverB, SoverSqrtB, SoverSqrtBSyst, chiSq, chiSqSyst, chiSqSyst1pc, acc ) )

  print('\n------------------------------------------------------')
  print('Finished. Saved outputs to: {0}'.format(save_file) )
  print('------------------------------------------------------')

#_________________________________________________________________________
def get_list_signals():
  
  l_sig = [
    'intermediate_TopYuk_0.5_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.5_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_0.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.8_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_0.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_0.9_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_0.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.0_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_0.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.1_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_0.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.2_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_0.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM.root',
    'intermediate_TopYuk_1.5_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM.root' 
    ]

  return l_sig

#_________________________________________________________________________
def get_xsec():
  
  d_xsec = {
   'intermediate_TopYuk_0.5_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM' : 0.51342,
   'intermediate_TopYuk_0.5_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM' : 0.1438,
   'intermediate_TopYuk_0.5_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM' : 0.077355,
   'intermediate_TopYuk_0.5_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM' : 0.044446,
   'intermediate_TopYuk_0.5_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM' : 0.020674,
   'intermediate_TopYuk_0.5_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM' : 0.012206,
   'intermediate_TopYuk_0.5_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM' : 0.0060154,
   'intermediate_TopYuk_0.5_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM' : 0.0037762,
   'intermediate_TopYuk_0.5_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM' : 0.0010049,
   'intermediate_TopYuk_0.5_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM' : 0.00047415,
   'intermediate_TopYuk_0.5_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM' : 0.0011231,
   'intermediate_TopYuk_0.5_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM' : 0.0040518,
   'intermediate_TopYuk_0.5_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM' : 0.016746,
   'intermediate_TopYuk_0.5_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM' : 0.038557,
   'intermediate_TopYuk_0.5_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM' : 0.088394,
   'intermediate_TopYuk_0.5_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM' : 0.40269,
   'intermediate_TopYuk_0.8_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM' : 1.4078,
   'intermediate_TopYuk_0.8_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM' : 0.41912,
   'intermediate_TopYuk_0.8_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM' : 0.23617,
   'intermediate_TopYuk_0.8_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM' : 0.14345,
   'intermediate_TopYuk_0.8_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM' : 0.074079,
   'intermediate_TopYuk_0.8_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM' : 0.048166,
   'intermediate_TopYuk_0.8_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM' : 0.028062,
   'intermediate_TopYuk_0.8_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM' : 0.020193,
   'intermediate_TopYuk_0.8_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM' : 0.0088491,
   'intermediate_TopYuk_0.8_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM' : 0.0053661,
   'intermediate_TopYuk_0.8_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM' : 0.0027707,
   'intermediate_TopYuk_0.8_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM' : 0.0060114,
   'intermediate_TopYuk_0.8_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM' : 0.029995,
   'intermediate_TopYuk_0.8_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM' : 0.077325,
   'intermediate_TopYuk_0.8_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM' : 0.19209,
   'intermediate_TopYuk_0.8_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM' : 0.95416,
   'intermediate_TopYuk_0.9_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM' : 0.55292,
   'intermediate_TopYuk_0.9_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM' : 0.3161,
   'intermediate_TopYuk_0.9_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM' : 0.19517,
   'intermediate_TopYuk_0.9_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM' : 0.10379,
   'intermediate_TopYuk_0.9_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM' : 0.069191,
   'intermediate_TopYuk_0.9_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM' : 0.041957,
   'intermediate_TopYuk_0.9_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM' : 0.031105,
   'intermediate_TopYuk_0.9_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM' : 0.01494,
   'intermediate_TopYuk_0.9_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM' : 0.0096347,
   'intermediate_TopYuk_0.9_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM' : 0.0045515,
   'intermediate_TopYuk_0.9_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM' : 0.0068599,
   'intermediate_TopYuk_0.9_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM' : 0.033622,
   'intermediate_TopYuk_0.9_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM' : 0.089949,
   'intermediate_TopYuk_0.9_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM' : 0.22978,
   'intermediate_TopYuk_0.9_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM' : 1.1762,
   'intermediate_TopYuk_1.0_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM' : 2.3008,
   'intermediate_TopYuk_1.0_SlfCoup_m15.0_pp2hh_HeavyHiggsTHDM' : 1.3919,
   'intermediate_TopYuk_1.0_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM' : 0.71114,
   'intermediate_TopYuk_1.0_SlfCoup_m9.0_pp2hh_HeavyHiggsTHDM' : 0.60241,
   'intermediate_TopYuk_1.0_SlfCoup_m8.0_pp2hh_HeavyHiggsTHDM' : 0.50274,
   'intermediate_TopYuk_1.0_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM' : 0.41211,
   'intermediate_TopYuk_1.0_SlfCoup_m6.0_pp2hh_HeavyHiggsTHDM' : 0.33079,
   'intermediate_TopYuk_1.0_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM' : 0.25842,
   'intermediate_TopYuk_1.0_SlfCoup_m4.0_pp2hh_HeavyHiggsTHDM' : 0.19529,
   'intermediate_TopYuk_1.0_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM' : 0.14117,
   'intermediate_TopYuk_1.0_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM' : 0.096246,
   'intermediate_TopYuk_1.0_SlfCoup_m1.5_pp2hh_HeavyHiggsTHDM' : 0.07717,
   'intermediate_TopYuk_1.0_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM' : 0.060419,
   'intermediate_TopYuk_1.0_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM' : 0.04591,
   'intermediate_TopYuk_1.0_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM' : 0.023744,
   'intermediate_TopYuk_1.0_SlfCoup_0.8_pp2hh_HeavyHiggsTHDM' : 0.018863,
   'intermediate_TopYuk_1.0_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM' : 0.016078,
   'intermediate_TopYuk_1.0_SlfCoup_1.2_pp2hh_HeavyHiggsTHDM' : 0.013651,
   'intermediate_TopYuk_1.0_SlfCoup_1.5_pp2hh_HeavyHiggsTHDM' : 0.010691,
   'intermediate_TopYuk_1.0_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM' : 0.0075864,
   'intermediate_TopYuk_1.0_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM' : 0.0082156,
   'intermediate_TopYuk_1.0_SlfCoup_4.0_pp2hh_HeavyHiggsTHDM' : 0.01797,
   'intermediate_TopYuk_1.0_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM' : 0.036819,
   'intermediate_TopYuk_1.0_SlfCoup_6.0_pp2hh_HeavyHiggsTHDM' : 0.064829,
   'intermediate_TopYuk_1.0_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM' : 0.10192,
   'intermediate_TopYuk_1.0_SlfCoup_8.0_pp2hh_HeavyHiggsTHDM' : 0.14813,
   'intermediate_TopYuk_1.0_SlfCoup_9.0_pp2hh_HeavyHiggsTHDM' : 0.2035,
   'intermediate_TopYuk_1.0_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM' : 0.26794,
   'intermediate_TopYuk_1.0_SlfCoup_15.0_pp2hh_HeavyHiggsTHDM' : 0.72691,
   'intermediate_TopYuk_1.0_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM' : 1.4143,
   'intermediate_TopYuk_1.1_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM' : 2.8461,
   'intermediate_TopYuk_1.1_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM' : 0.89591,
   'intermediate_TopYuk_1.1_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM' : 0.52603,
   'intermediate_TopYuk_1.1_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM' : 0.33467,
   'intermediate_TopYuk_1.1_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM' : 0.18749,
   'intermediate_TopYuk_1.1_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM' : 0.1304,
   'intermediate_TopYuk_1.1_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM' : 0.084344,
   'intermediate_TopYuk_1.1_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM' : 0.06546,
   'intermediate_TopYuk_1.1_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM' : 0.035942,
   'intermediate_TopYuk_1.1_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM' : 0.025329,
   'intermediate_TopYuk_1.1_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM' : 0.012381,
   'intermediate_TopYuk_1.1_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM' : 0.010459,
   'intermediate_TopYuk_1.1_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM' : 0.03971,
   'intermediate_TopYuk_1.1_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM' : 0.11313,
   'intermediate_TopYuk_1.1_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM' : 0.30598,
   'intermediate_TopYuk_1.1_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM' : 1.6661,
   'intermediate_TopYuk_1.2_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM' : 3.4621,
   'intermediate_TopYuk_1.2_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM' : 1.1095,
   'intermediate_TopYuk_1.2_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM' : 0.65961,
   'intermediate_TopYuk_1.2_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM' : 0.42544,
   'intermediate_TopYuk_1.2_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM' : 0.24384,
   'intermediate_TopYuk_1.2_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM' : 0.17275,
   'intermediate_TopYuk_1.2_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM' : 0.11473,
   'intermediate_TopYuk_1.2_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM' : 0.090659,
   'intermediate_TopYuk_1.2_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM' : 0.052327,
   'intermediate_TopYuk_1.2_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM' : 0.038111,
   'intermediate_TopYuk_1.2_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM' : 0.019517,
   'intermediate_TopYuk_1.2_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM' : 0.014026,
   'intermediate_TopYuk_1.2_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM' : 0.042466,
   'intermediate_TopYuk_1.2_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM' : 0.12343,
   'intermediate_TopYuk_1.2_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM' : 0.3433,
   'intermediate_TopYuk_1.2_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM' : 1.9299,
   'intermediate_TopYuk_1.5_SlfCoup_m20.0_pp2hh_HeavyHiggsTHDM' : 5.7703,
   'intermediate_TopYuk_1.5_SlfCoup_m10.0_pp2hh_HeavyHiggsTHDM' : 1.9438,
   'intermediate_TopYuk_1.5_SlfCoup_m7.0_pp2hh_HeavyHiggsTHDM' : 1.1967,
   'intermediate_TopYuk_1.5_SlfCoup_m5.0_pp2hh_HeavyHiggsTHDM' : 0.80087,
   'intermediate_TopYuk_1.5_SlfCoup_m3.0_pp2hh_HeavyHiggsTHDM' : 0.48725,
   'intermediate_TopYuk_1.5_SlfCoup_m2.0_pp2hh_HeavyHiggsTHDM' : 0.3612,
   'intermediate_TopYuk_1.5_SlfCoup_m1.0_pp2hh_HeavyHiggsTHDM' : 0.25562,
   'intermediate_TopYuk_1.5_SlfCoup_m0.5_pp2hh_HeavyHiggsTHDM' : 0.21048,
   'intermediate_TopYuk_1.5_SlfCoup_0.5_pp2hh_HeavyHiggsTHDM' : 0.13571,
   'intermediate_TopYuk_1.5_SlfCoup_1.0_pp2hh_HeavyHiggsTHDM' : 0.10598,
   'intermediate_TopYuk_1.5_SlfCoup_2.0_pp2hh_HeavyHiggsTHDM' : 0.061942,
   'intermediate_TopYuk_1.5_SlfCoup_3.0_pp2hh_HeavyHiggsTHDM' : 0.038406,
   'intermediate_TopYuk_1.5_SlfCoup_5.0_pp2hh_HeavyHiggsTHDM' : 0.052931,
   'intermediate_TopYuk_1.5_SlfCoup_7.0_pp2hh_HeavyHiggsTHDM' : 0.14951,
   'intermediate_TopYuk_1.5_SlfCoup_10.0_pp2hh_HeavyHiggsTHDM' : 0.44814,
   'intermediate_TopYuk_1.5_SlfCoup_20.0_pp2hh_HeavyHiggsTHDM' : 2.7778, 
  }

  return d_xsec

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
