#!/usr/bin/env python
'''

Welcome to ntuples_to_chiSq.py

Loops through ntuples of signal samples defined in get_signal_xsec()
Calculates chiSq, S/B among other observables to a CSV

Requires running plot.py once to compute YIELD file for total background counts

* Configure various aspects in other files
    - cuts.py
    - xsecs.py
    - samples.py
'''

import argparse, os, sys, math
from array import array
from ROOT import *
from cuts import *
  
# Path to the intermediate ntuples
#SIG_PATH = '/home/jesseliu/pheno/fcc/PhenoSim/data/samples/14TeV/2019mar18/all_merged_delphes/ntuples_2019mar25/merged_signals'
SIG_PATH = '/data/atlas/atlasdata/DiHiggsPheno/ntuples'
dir = '150719'

# Impose 4 b-tags as weights
do_BTagWeight = True

#____________________________________________________________________________
def main():

  mkdir('data')
  
  # -----------------------------------------------------------
  #
  # Some user configurables
  #
  # Luminosity
  lumi = 3000.0 # inverse fb
  # Analysis (defined in samples.py)
  l_samples  = ['loose']
  # Signal region (define in cuts.py)
  l_sig_regs = ['preselection'] 
  # Cut selections
  l_cut_sels = ['resolved-preselection', 'intermediate-preselection' ,'boosted-preselection',
                'resolved-commonSR',     'intermediate-commonSR',     'boosted-commonSR',
                'resolved-finalSR',      'intermediate-finalSR',      'boosted-finalSR' ] 
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

        do_selection( yield_file, save_file, lumi, analysis, sig_reg, cut_sel )

#____________________________________________________________________________
def do_selection( yield_file, save_file, lumi, analysis, sig_reg, cut_sel ):
  '''
  Given N_bkg from yield file, analysis, sig_reg, cut_sel, 
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
  # Get the cross-section file
  d_sig_xsec = get_signal_xsec()

  # Variable to plot in
  var  = 'm_hh'
  # Get cut strings from cuts.py
  unweighted_cuts, l_cuts = configure_cuts(var, cut_sel) 
  # -----------------------------------------------------------
  
  print('Background yield: {0}'.format(N_bkg) )
  print('Luminosity: {0} /fb '.format(lumi) )
  print('Unweighted cuts: {0}'.format(unweighted_cuts) )
  
  # ---------------------------------------
  # Get nominal signal yield
  # ---------------------------------------
  N_sig_nom = get_N_sig_nom( lumi, var, unweighted_cuts )

  # ---------------------------------------
  # Now loop through coupling variations
  # ---------------------------------------
  with open(save_file, 'w') as f_out:
    header  = 'TopYuk,SlfCoup,N_bkg,N_sig,N_sig_raw,'
    header += 'SoverB,SoverSqrtB,SoverSqrtBSyst1pc,SoverSqrtBSyst5pc,'
    header += 'chiSq,chiSqSyst1pc,chiSqSyst5pc,acceptance\n'
    f_out.write( header )

    for signal, xsec_sig in d_sig_xsec.iteritems():  
      out_str = compute_chiSq( f_out, signal, xsec_sig, lumi, var, unweighted_cuts, N_bkg, N_sig_nom )
      if not out_str == 'NoFile':
        f_out.write( out_str )
        print( out_str )

  print('\n------------------------------------------------------')
  print('Saved outputs to: {0}'.format(save_file) )
  print('------------------------------------------------------')

#____________________________________________________________________________
def get_N_sig_nom( lumi, var, unweighted_cuts ):
  ''' 
  Get nominal yield for chi square calculation
  '''
  
  print('\nGetting the nominal signal yield\n')
  
  root_nom = SIG_PATH + '/' + dir + '/loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0.root'
  print('Nominal root file: {0}'.format(root_nom))
  tfile = TFile( root_nom )
  N_nom_raw = tfile.Get('loose_cutflow').GetBinContent(1)
  nom_xsec = 0.016078 # Leading order MadGraph
  
  if do_BTagWeight:
    my_weight = 'h1_j1_BTagWeight * h1_j2_BTagWeight * h2_j1_BTagWeight * h2_j2_BTagWeight'
  else:
    my_weight = 1.
  cuts = '( ({0}) * (1000 * {1} * {2} * {3}) ) / {4}'.format( unweighted_cuts, nom_xsec, lumi, my_weight, N_nom_raw )
  print('Weighted signal cuts: {0}'.format(cuts) )
  
  # Project and make histogram
  Nbins = 1
  xmin = -100.0
  xmax = 10000
  th1_nom = TH1D('h_sig_nom', "", Nbins, xmin, xmax) 
  ttree_nom = tfile.Get('preselection')
  ttree_nom.Project( 'h_sig_nom', var, cuts )
  N_sig_nom =  float( th1_nom.Integral() )
  print('Nominal signal yield: {0}'.format( N_sig_nom ))

  return N_sig_nom    

#____________________________________________________________________________
def compute_chiSq( f_out, signal, xsec_sig, lumi, var, unweighted_cuts, N_bkg, N_sig_nom ):
  '''
  Perform cuts onto the signal file
  and compute various metrics like S/B, chi square etc
  ''' 
  print('\nComputing chi square for {0}'.format(signal) )
  
  d_sig_file = {}
  d_sig_hist = {}
  d_sig_tree = {}
  d_sig_yield = {}

  # ------------------------------------------------------
  # Extract coupling values from file name
  # ------------------------------------------------------
  info = signal.split('_')
  TopYuk  = float( info[5] )
  SlfCoup = float( info[7].replace('m', '-') )
  root_signal = SIG_PATH + '/' + dir + '/' + signal + '.root'
  print( 'Root file: {0}'.format( root_signal ) )
  Nbins = 1
  xmin = -100.0
  xmax = 10000
  d_sig_file[signal] = TFile( root_signal )
  d_sig_hist[signal] = TH1D('h_sig_' + signal, "", Nbins, xmin, xmax) 

  # Inititalise
  N_orig_raw = 1

  # ------------------------------------------------------
  # Get the initial number of events before any cuts
  # ------------------------------------------------------
  try:
    N_orig_raw = d_sig_file[signal].Get('loose_cutflow').GetBinContent(1)
  except AttributeError:
    return 'NoFile'
    print('{0} has no loose_cutflow histogram, skipping...'.format(d_sig_file[signal]))

  if do_BTagWeight:
    my_weight = 'h1_j1_BTagWeight * h1_j2_BTagWeight * h2_j1_BTagWeight * h2_j2_BTagWeight'
  else:
    my_weight = 1.

  # ------------------------------------------------------
  # Construct cut string for TTree.Project()
  # ------------------------------------------------------
  cuts = '( ({0}) * (1000 * {1} * {2} * {3}) ) / {4}'.format(unweighted_cuts, xsec_sig, lumi, my_weight, N_orig_raw)
  print('Weighted signal cuts: {0}'.format(cuts) )
  
  # ------------------------------------------------------
  # Project to histogram and compute yields
  # ------------------------------------------------------
  d_sig_tree[signal] = d_sig_file[signal].Get('preselection')
  d_sig_tree[signal].Project( 'h_sig_' + signal, var, cuts )

  N_sig     = float( d_sig_hist[signal].Integral() )
  N_sig_raw = int( d_sig_hist[signal].GetEntries() )
  
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
  chiSq         = ( N_sig - N_sig_nom ) ** 2 / ( N_bkg )
  chiSqSyst1pc  = ( N_sig - N_sig_nom ) ** 2 / ( N_bkg + (0.01 * N_bkg ) ** 2 )
  chiSqSyst5pc  = ( N_sig - N_sig_nom ) ** 2 / ( N_bkg + (0.05 * N_bkg ) ** 2 )
  
  # ------------------------------------------------------
  # Calculate acceptance
  # ------------------------------------------------------
  acceptance = N_sig / ( xsec_sig * lumi * 1000.)

  # ------------------------------------------------------
  # Construct string of values to output
  # ------------------------------------------------------
  out_str  = '{0},{1},{2:.4g},{3:.4g},{4:.4g},'.format( TopYuk, SlfCoup,      N_bkg,             N_sig, N_sig_raw )
  out_str += '{0:.4g},{1:.4g},{2:.4g},{3:.4g},'.format( SoverB, SoverSqrtB,   SoverSqrtBSyst1pc, SoverSqrtBSyst5pc  )
  out_str += '{0:.4g},{1:.4g},{2:.4g},{3:.4g}'.format( chiSq,  chiSqSyst1pc, chiSqSyst5pc,      acceptance )
  out_str += '\n'

  return out_str

#_________________________________________________________________________
def get_signal_xsec():
  '''
  Leading order MG cross-sections in pb
  '''
  d_xsec = {
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m20.0' : 0.51342,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m10.0' : 0.1438,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m7.0'  : 0.077355,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m5.0'  : 0.044446,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m3.0'  : 0.020674,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m2.0'  : 0.012206,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m1.0'  : 0.0060154,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_m0.5'  : 0.0037762,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_0.5'   : 0.0010049,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_1.0'   : 0.00047415,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_2.0'   : 0.0011231,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_3.0'   : 0.0040518,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_5.0'   : 0.016746,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_7.0'   : 0.038557,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_10.0'  : 0.088394,
   'loose_noGenFilt_signal_hh_TopYuk_0.5_SlfCoup_20.0'  : 0.40269,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m20.0' : 1.4078,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m10.0' : 0.41912,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m7.0'  : 0.23617,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m5.0'  : 0.14345,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m3.0'  : 0.074079,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m2.0'  : 0.048166,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m1.0'  : 0.028062,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_m0.5'  : 0.020193,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_0.5'   : 0.0088491,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_1.0'   : 0.0053661,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_2.0'   : 0.0027707,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_3.0'   : 0.0060114,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_5.0'   : 0.029995,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_7.0'   : 0.077325,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_10.0'  : 0.19209,
   'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_20.0'  : 0.95416,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m10.0' : 0.55292,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m7.0'  : 0.3161,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m5.0'  : 0.19517,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m3.0'  : 0.10379,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m2.0'  : 0.069191,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m1.0'  : 0.041957,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_m0.5'  : 0.031105,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_0.5'   : 0.01494,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_1.0'   : 0.0096347,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_2.0'   : 0.0045515,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_3.0'   : 0.0068599,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_5.0'   : 0.033622,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_7.0'   : 0.089949,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_10.0'  : 0.22978,
   'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_20.0'  : 1.1762,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m20.0' : 2.3008,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m15.0' : 1.3919,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m10.0' : 0.71114,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m9.0'  : 0.60241,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m8.0'  : 0.50274,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m7.0'  : 0.41211,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m6.0'  : 0.33079,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0'  : 0.25842,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m4.0'  : 0.19529,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m3.0'  : 0.14117,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m2.0'  : 0.096246,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m1.5'  : 0.07717,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m1.0'  : 0.060419,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m0.5'  : 0.04591,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_0.5'   : 0.023744,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_0.8'   : 0.018863,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0'   : 0.016078,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.2'   : 0.013651,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.5'   : 0.010691,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0'   : 0.0075864,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_3.0'   : 0.0082156,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_4.0'   : 0.01797,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0'   : 0.036819,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_6.0'   : 0.064829,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_7.0'   : 0.10192,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_8.0'   : 0.14813,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_9.0'   : 0.2035,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0'  : 0.26794,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_15.0'  : 0.72691,
   'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_20.0'  : 1.4143,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m20.0' : 2.8461,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m10.0' : 0.89591,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m7.0'  : 0.52603,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m5.0'  : 0.33467,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m3.0'  : 0.18749,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m2.0'  : 0.1304,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m1.0'  : 0.084344,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_m0.5'  : 0.06546,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_0.5'   : 0.035942,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_1.0'   : 0.025329,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_2.0'   : 0.012381,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_3.0'   : 0.010459,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_5.0'   : 0.03971,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_7.0'   : 0.11313,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_10.0'  : 0.30598,
   'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_20.0'  : 1.6661,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m20.0' : 3.4621,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m10.0' : 1.1095,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m7.0'  : 0.65961,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m5.0'  : 0.42544,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m3.0'  : 0.24384,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m2.0'  : 0.17275,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m1.0'  : 0.11473,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_m0.5'  : 0.090659,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_0.5'   : 0.052327,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_1.0'   : 0.038111,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_2.0'   : 0.019517,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_3.0'   : 0.014026,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_5.0'   : 0.042466,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_7.0'   : 0.12343,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_10.0'  : 0.3433,
   'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_20.0'  : 1.9299,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m20.0' : 5.7703,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m10.0' : 1.9438,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m7.0'  : 1.1967,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m5.0'  : 0.80087,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m3.0'  : 0.48725,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m2.0'  : 0.3612,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m1.0'  : 0.25562,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_m0.5'  : 0.21048,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_0.5'   : 0.13571,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_1.0'   : 0.10598,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_2.0'   : 0.061942,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_3.0'   : 0.038406,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_5.0'   : 0.052931,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_7.0'   : 0.14951,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_10.0'  : 0.44814,
   'loose_noGenFilt_signal_hh_TopYuk_1.5_SlfCoup_20.0'  : 2.7778, 
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
