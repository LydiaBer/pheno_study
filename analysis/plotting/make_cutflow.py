#!/usr/bin/env python
'''

Welcome to make_cutflow.py

Generates publication ready cutflow LaTeX tables (booktabs).
  - User configures list samples (in 'sample set') to analyse
  - User configures list of efficiency weights to append to cutflow
  - User configures dictionary of cutflow sets
  - Run script to make a cutflow table per sample set 

  - get_latex_maps() is where the map from sample/cut name to LaTeX lives 

* Configure various aspects in other files
    - cuts.py
    - xsecs.py
    - samples.py
'''

# So Root ignores command line inputs so we can use argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
from math import sqrt
import os, sys, time, argparse
from pprint import pprint

from cuts       import *
from xsecs      import *
from samples    import *

#------------------------------------
# Global options

# Impose 4 b-tags as weights
do_BTagWeight = True

# Save rounded values in TeX tables 
savePDG_rounding = False 

# Show the raw yields in tables
# TODO: can only show either raw counts or S / sqrt(B), not both right now
show_raw_counts = False
  
# Show S / sqrt(B), please specify which sample to use as background
show_SoverSqrtB = False
bkg_samp_for_SoverSqrtB = ''

# Luminosity in 1/fb  
lumi = 3000.0 

# Tag to add to name of output cutflow
tag = 'cf_2019aug06_hh4b'

# Directory samples are in
dir = '150719' 

#____________________________________________________________________________
def main():
  
  t0 = time.time()
  
  #--------------------------------------------
  # User configures list sample sets to analyse
  #--------------------------------------------
  l_samp_set = ['all','smallbkgs','mainbkgs','signals']
  d_samp_set = get_samp_set() 
  
  #--------------------------------------------
  # User configures list of cuts to in cutflow
  #--------------------------------------------
  l_cutflow_set = ['resolved-finalSR', 'intermediate-finalSR' ,'boosted-finalSR', 'resolved-preselection', 'intermediate-preselection' ,'boosted-preselection'] 

  #-------------------------------------------
  # Where to save cutflow
  #-------------------------------------------
  savedir = 'cutflows'
  mkdir(savedir)
 
  #================================================
  # -------------------------------------------------------------
  # Argument parser
  parser = argparse.ArgumentParser(description='Analyse background/signal TTrees and make plots.')
  parser.add_argument('-s', '--cut_sel', type=str, nargs='?', help='Selection cuts considered.')
  parser.add_argument('-o', '--onesample', type=str, nargs='?', help='Sample name.')
 
  args = parser.parse_args()
  if args.cut_sel:
    l_cutflow_set = [ args.cut_sel ] 
  if args.onesample:
    l_samp_set = [ args.onesample ] 

  print('------------------------------------------')
  print(' Welcome to make_cutflow.py')
  print('------------------------------------------')
  
  #-------------------------------------------
  # Make a cutflow table per sample set and cutflow set
  #-------------------------------------------
  for samp_set in l_samp_set:
    # To make one cutflow file per samp_set 
    #save_name = '{0}/cutflow_{1}_{2}.tex'.format(savedir, samp_set, tag) 
    #open(save_name, 'w') # Open new cutflow file & overwrite existing one
    for cutflow_set in l_cutflow_set: 
      # To make one cutflow file per cutflow_set per samp_set
      save_name = '{0}/cutflow_{1}_{2}_{3}.tex'.format(savedir, samp_set, cutflow_set, tag) 
      open(save_name, 'w') # Open new cutflow file & overwrite existing one
      make_cutflow(samp_set, d_samp_set, cutflow_set, savedir, save_name)

  tfinish = time.time()
  telapse = tfinish - t0
  print( '\nFinished in {0:.3f}s'.format(telapse))

#____________________________________________________________________________
def make_cutflow(samp_set, d_samp_set, cutflow_set, savedir, save_name):
  '''
  Make the cutflow given samples and dict of cuts 
  '''

  var = 'm_hh'
  d_samp_cutflow = {}
  
  l_samp = d_samp_set[samp_set] 

  # Get cuts to apply from cuts.py 
  cut_string, l_cuts = configure_cuts(cutflow_set) 

  l_cutflow = l_cuts
  
  for count, samp in enumerate( l_samp ):
    # Initialise the cutflow dictionary
    d_samp_cutflow[(samp,cutflow_set)] = { 'yield' : [], 
                                           'unc' : [], 
                                           'raw' : [],
                                           'rounded_yield' : [],
                                           'rounded_yieldUnc' : [],
                                         }
    
    l_cutflow_common = []
   
    #------------------------------------------
    # Now run over each cut 
    #------------------------------------------
    for cut in l_cutflow:

      # Add each successive cut with AND operation
      l_cutflow_common.append(cut)
      add_cut = ' && '.join(l_cutflow_common)
      
      #------------------------------------------
      # Get the yields from the selection
      #------------------------------------------
      nYield, yieldUnc, nRaw, rounded_nYield, rounded_yieldUnc = calc_selections(samp, var, add_cut, lumi, dir)
      # Assign it to the dictionary
      d_samp_cutflow[(samp,cutflow_set)]['yield'].append(nYield)
      d_samp_cutflow[(samp,cutflow_set)]['unc'].append(yieldUnc)
      d_samp_cutflow[(samp,cutflow_set)]['raw'].append(nRaw)
      d_samp_cutflow[(samp,cutflow_set)]['rounded_yield'].append(rounded_nYield)
      d_samp_cutflow[(samp,cutflow_set)]['rounded_yieldUnc'].append(rounded_yieldUnc)
    
  # Debug print 
  pprint(d_samp_cutflow)

  #------------------------------------------
  # Make LaTeX cutflow table and save to file
  #------------------------------------------
  print('\nCutflow dictionary complete, now making LaTeX cutflow table')
  make_latex(samp_set, l_samp, cutflow_set, l_cutflow, d_samp_cutflow, savedir, save_name)

#____________________________________________________________________________
def calc_selections(samp, var, add_cuts, lumi, dir):
  '''
  Extract trees given a relevant variable
  ''' 

  #----------------------------------------------------
  # 
  # Get various configurations from other python files
  #
  #----------------------------------------------------
  #
  # Get the sample paths from samples.py
  bkg_path, sig_path, bkg_suffix, sig_suffix = get_sample_paths(dir)

  #---------------------------------------------------------
  # Prepare information and objects for analysis and plots
  #---------------------------------------------------------
  # obtain cut to apply (string)
  d_files = {}
  d_hists = {}
  
  if 'TopYuk' in samp: 
    full_path = sig_path + '/' + samp + sig_suffix
  else: 
    full_path = bkg_path + '/' + samp + bkg_suffix
  
  unweighted_cuts = add_cuts 

  print('cuts to apply: {0}'.format(unweighted_cuts))     
  # assign TFile to a dictionary entry
  d_files[samp] = TFile(full_path)

  # obtain histogram from file and store to dictionary entry
  hNbins = 1
  hXmin  = 0
  hXmax  = 100000
  d_hists[samp] = apply_cuts_weights_to_tree( d_files[samp], samp, var, lumi, unweighted_cuts, hNbins, hXmin, hXmax )

  # extract key outputs of histogram 
  nYield, nYieldErr, nRaw, rounded_nYield, rounded_nYieldErr = d_hists[samp]
  print('In cut: {0},{1},{2}'.format(nYield, nYieldErr, nRaw)) 
   
  return nYield, nYieldErr, nRaw, rounded_nYield, rounded_nYieldErr

#_______________________________________________________
def apply_cuts_weights_to_tree(f, hname, var, lumifb, unweighted_cuts='', Nbins=100, xmin=0, xmax=100000):
  '''
  Obtain yields by performing TTree.Project() to impose cuts & apply weights
  '''

  h_AfterCut   = TH1D(hname, "", Nbins, xmin, xmax)
  t = f.Get('preselection')
  lumi     = lumifb * 1000 # convert to [pb^{-1}]
  
  d_xsecs = configure_xsecs()
  xsec = d_xsecs[hname]

  #-----------------------------------------------------
  # Normalise to xsec * lumi, apply cuts & weights
  #-----------------------------------------------------
  xsec_times_lumi = xsec * lumi
  
  # Inititalise
  N_orig_raw = 1

  # ------------------------------------------------------
  # Get the initial number of events before any cuts
  # ------------------------------------------------------
  try:
    N_orig_raw = f.Get('loose_cutflow').GetBinContent(1)
  except AttributeError:
    return 'NoFile'
    print('{0} has no loose_cutflow histogram, skipping...'.format(d_sig_file[signal]))

  weights = xsec_times_lumi / float(N_orig_raw)

  if do_BTagWeight:
    my_weight = 'h1_j1_BTagWeight * h1_j2_BTagWeight * h2_j1_BTagWeight * h2_j2_BTagWeight'
  else:
    my_weight = 1.

  # ------------------------------------------------------
  # Construct cut string for TTree.Project()
  # ------------------------------------------------------
  cuts = '(({0}) * {1} * {2})'.format(unweighted_cuts, weights, my_weight)

  print('\nCross-section applied: {0}'.format( xsec ) )
  print('N_orig_raw in tree: {0}'.format(N_orig_raw) )
  print('xsec * lumi / N_orig_raw applied: {0}'.format( weights ) )
  print('Weighted signal cuts: {0}'.format(cuts) )
 
  t.Project( hname,           var, cuts )
  
  # Perform integrals to find total yield
  nYieldErr = ROOT.Double(0)
  nYield    = h_AfterCut.IntegralAndError(0, Nbins+1, nYieldErr)
 
  rounded_nYield, rounded_nYieldErr = pdgRound(nYield, nYieldErr)

  print( 'Sample {0} has integral {1:.3f} +/- {2:.3f}, PDG rounded to {3} +/- {4}'.format( hname, nYield, nYieldErr, rounded_nYield, rounded_nYieldErr ) )
  # =========================================================
  
  nRaw = h_AfterCut.GetEntries()
  
  return nYield, nYieldErr, nRaw, rounded_nYield, rounded_nYieldErr

#____________________________________________________________________________
def make_latex(samp_set, l_samp, cutflow_set, l_cuts, d_samp_cutflow, savedir, save_name):
  '''
  Produce the LaTeX table
  '''

  # Map TCut strings and sample file names to beautiful LaTeX entries
  d_cuts_latex, d_samp_latex = get_latex_maps()

  # ------------------------------------------
  # Top of table using LaTeX booktabs
  # ------------------------------------------
  tab_head = r'''
\begin{table}[H]
\scriptsize
\begin{center}
\renewcommand{\arraystretch}{1.1}
  '''

  tab_top_line = r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l'
  tab_samp_header   = r'''
  \toprule
  Requirement '''
  tab_count_header = r''
  
  # ------------------------------------------
  # Add column headings with sample names
  # ------------------------------------------
  for samp in l_samp:
    if show_raw_counts or show_SoverSqrtB:
      if show_SoverSqrtB and bkg_samp_for_SoverSqrtB in samp:
        tab_top_line += 'r'
        tab_samp_header += r' & \multicolumn{1}{c}{' + d_samp_latex[samp] + '} \n '
      else:
        tab_top_line += 'rr'
        tab_samp_header += r' & \multicolumn{2}{c}{' + d_samp_latex[samp] + '} \n '
      if show_raw_counts:
        tab_count_header += r' & Wgt & Raw '
      elif show_SoverSqrtB:
        # Don't print S/sqrt(B) for the background sample
        if bkg_samp_for_SoverSqrtB in samp:
          tab_count_header += r' & Yield '
        else:
          tab_count_header += r' & Yield & $S / \sqrt{B}$ '
    else:
      tab_top_line += 'r'
      tab_samp_header += r' & ' + d_samp_latex[samp] + ' \n'
    
  tab_top_line += r'}'
  if show_raw_counts or show_SoverSqrtB:
    tab_samp_header += r'\\' 
  tab_count_header += r'''\\ 
  \midrule
  '''
  
  # ------------------------------------------
  # Each cut is new horizontal entry in table
  # ------------------------------------------
  tab_line = ''
  for count, cut in enumerate(l_cuts):
    # Retrieve the LaTeX corresponding to the cut
    try:
      tab_line += d_cuts_latex[cut]
    except KeyError:
      print( '  \nKeyError: Make sure the cut %s is in the d_cuts_latex = {} dictionary of the function get_latex_maps()'%(cut) ) 
      sys.exit()
    for samp in l_samp:
      # Retrieve the yields
      my_yield         = d_samp_cutflow[(samp,cutflow_set)]['yield'][count]
      my_unc           = d_samp_cutflow[(samp,cutflow_set)]['unc'][count]
      my_raw           = d_samp_cutflow[(samp,cutflow_set)]['raw'][count]
      my_rounded_yield = d_samp_cutflow[(samp,cutflow_set)]['rounded_yield'][count]
      my_rounded_unc   = d_samp_cutflow[(samp,cutflow_set)]['rounded_yieldUnc'][count]
      
      # Format the yields with or without rounding
      if savePDG_rounding:
        #tab_line += r' & ${0} \pm {1}$ ({2})     '.format(my_rounded_yield, my_rounded_unc, int(my_raw) )
        if show_raw_counts:
          tab_line += r' & ${0}$ & ${1}$   '.format(my_rounded_yield, int(my_raw) ) 
        else:
          tab_line += r' & ${0}$ '.format(my_rounded_yield )
  
      else:
        if show_raw_counts:
          tab_line += r' & ${0:.1f}$ & ${1:.0f}$ '.format(my_yield, int(my_raw) )
        elif show_SoverSqrtB:
          my_bkg = d_samp_cutflow[(bkg_samp_for_SoverSqrtB,cutflow_set)]['yield'][count]
          # Don't print S/sqrt(B) for the background sample
          if bkg_samp_for_SoverSqrtB in samp:
            tab_line += r' & ${0:.1f}$'.format(my_yield)
          else:
            tab_line += r' & ${0:.1f}$ & ${1:.1f}$ '.format(my_yield, my_yield / my_bkg )
        else:
          tab_line += r' & ${0:.1f}$ '.format(my_yield )
  
    tab_line += r'''\\ 
    '''
  
  # ------------------------------------------
  # Bottom of table with placeholder caption
  # ------------------------------------------
  if show_SoverSqrtB:
    add_txt = r'Also displayed for each signal is the $S/\sqrt{B}$ using the {0} yield as $B$.'.format(bkg_samp_for_SoverSqrtB)
  elif show_raw_counts:
    add_txt = r'Also displayed for each process are the raw counts generated for this study.'
  else:
    add_txt = ''
 
  if cutflow_set == 'leplep':
    cutflow_set_for_caption = '$2\ell$' 
  elif cutflow_set == 'lep1prong':
    cutflow_set_for_caption = '$1\ell$ plus 1 track' 
  elif cutflow_set == 'lep2prong':
    cutflow_set_for_caption = '$1\ell$ plus 2 tracks' 
  elif cutflow_set == 'lep3prong':
    cutflow_set_for_caption = '$1\ell$ plus 3 tracks' 
  elif cutflow_set == 'lep2or3prong':
    cutflow_set_for_caption = '$1\ell$ plus 2 or 3 tracks' 
  else:
    cutflow_set_for_caption = cutflow_set

  tab_foot = r'''
  \bottomrule
  \end{tabular*}
\end{center}
\caption{Signal region %s. Cutflow of yields after each requirement applied sequentially, normalised to $\mathcal{L} = %s$~nb$^{-1}$. %s 
}
\label{tab:cutflow_%s_%s}
\end{table} 
  ''' % ( cutflow_set_for_caption, lumi, add_txt, samp_set, cutflow_set )
 
  # ------------------------------------------
  # Construct the table 
  # ------------------------------------------
  final_tab = tab_head + tab_top_line + tab_samp_header + tab_count_header +  tab_line + tab_foot
  
  # ------------------------------------------
  # Save the table to file
  # ------------------------------------------
  with open(save_name, 'a+') as f_out:
    print('\n-----------------------------------------------')
    print('Saving LaTeX cutflow table to: \n   {0}'.format(save_name))
    print('--------------------------------------------------')
    f_out.write(final_tab)

#_________________________________________________________________________
def pdgRound(value, error) :
# This class implements the pdg rounding rules indicated in
# section 5.3 of doi:10.1088/0954-3899/33/1/001
#
# Note: because it uses round (and in general floats), it is affected
# by the limitations described in
# http://docs.python.org/library/functions.html#round
#  and
# http://dx.doi.org/10.1145/103162.103163
#
# davide.gerbaudo@gmail.com
# September 2012

  "Given a value and an error, round and format them according to the PDG rules for significant digits"
  def threeDigits(value) :
    "extract the three most significant digits and return them as an int"
    return int(("%.2e"%float(error)).split('e')[0].replace('.','').replace('+','').replace('-',''))
  def nSignificantDigits(threeDigits) :
    assert threeDigits<1000,"three digits (%d) cannot be larger than 10^3"%threeDigits
    if threeDigits<101 : return 2 # not sure
    elif threeDigits<356 : return 2
    elif threeDigits<950 : return 1
    else : return 2
  def frexp10(value) :
    "convert to mantissa+exp representation (same as frex, but in base 10)"
    valueStr = ("%e"%float(value)).split('e')
    return float(valueStr[0]), int(valueStr[1])
  def nDigitsValue(expVal, expErr, nDigitsErr) :
    "compute the number of digits we want for the value, assuming we keep nDigitsErr for the error"
    return expVal-expErr+nDigitsErr
  def formatValue(value, exponent, nDigits, extraRound=0) :
    "Format the value; extraRound is meant for the special case of threeDigits>950"
    roundAt = nDigits-1-exponent - extraRound
    nDec = roundAt if exponent<nDigits else 0
    nDec = max([nDec, 0])
    return ('%.'+str(nDec)+'f')%round(value,roundAt)
  tD = threeDigits(error)
  nD = nSignificantDigits(tD)
  expVal, expErr = frexp10(value)[1], frexp10(error)[1]
  extraRound = 1 if tD>=950 else 0
  return (formatValue(value, expVal, nDigitsValue(expVal, expErr, nD), extraRound),
          formatValue(error,expErr, nD, extraRound))

#____________________________________________________________________________
def get_latex_maps():
  '''
  Map TCut strings and sample file names to beautiful LaTeX entries
  '''

  # ------------------------------------------
  # Mapping ntuple selections to LaTeX
  # ------------------------------------------
  d_cuts_latex = {
    'met_Et < 150'  : r'$E_\text{T}^\text{miss} < 150$~GeV',
    'nElec == 0'    : r'$N_{\rm{e}} = 0$',
    'nMuon == 0'    : r'$N_{\mu} = 0$',
    'dEta_hh < 1.5' : r'$|\eta(h_1, h_2)| < 1.5',
    'h1_M > 50'     : r'$m(h_1) > 50$~GeV',
    'h2_M > 50'     : r'$m(h_2) > 50$~GeV',

    'n_large_jets == 0' : r'$N(j_L) = 0$',
    'n_large_jets == 1' : r'$N(j_L) = 1$',
    'n_large_jets == 2' : r'$N(j_L) = 2$',
    
    'n_small_jets >= 2' : r'$N(j_S) \geq 2$',
    'n_small_jets >= 4' : r'$N(j_S) \geq 4$',
    
    'h1_M > 90 && h1_M < 140' : r'$m(h_1)$~GeV~$[90, 140]$',
    'h2_M > 80 && h2_M < 130' : r'$m(h_2)$~GeV~$[80, 130]$',
    'h2_M > 90 && h2_M < 140' : r'$m(h_2)$~GeV~$[90, 140]$',
  }
  
  
  # ------------------------------------------
  # Mapping short sample name to LaTeX
  # ------------------------------------------
  d_samp_latex = {
                  'loose_noGenFilt_wh'    : r'\thead{$Wh$\\}',
                  'loose_noGenFilt_zh'    : r'\thead{$Zh$\\}',
                  'loose_noGenFilt_zz'    : r'\thead{$ZZ$\\}',
                  'loose_noGenFilt_bbh'   : r'\thead{$b\bar{b}h$\\}',
                  'loose_noGenFilt_tth'   : r'\thead{$t\bar{t}h$\\}',
                  'loose_noGenFilt_ttbb'  : r'\thead{$t\bar{t}+b\bar{b}$\\}',
                  'loose_noGenFilt_ttbar' : r'\thead{$t\bar{t}$\\}',
                  'loose_ptj1_1000_to_infty_4b': r'\thead{$4b$\\$ > 1000$}',
                  'loose_ptj1_500_to_1000_4b'  : r'\thead{$4b$\\$ [500, 1000]$}',
                  'loose_ptj1_200_to_500_4b'   : r'\thead{$4b$\\$ [200, 500]$}',
                  'loose_ptj1_20_to_200_4b'    : r'\thead{$4b$\\$ [20, 200]$}',
                  'loose_ptj1_1000_to_infty_2b2j': r'\thead{$2b2j$\\$ > 1000$$}',
                  'loose_ptj1_500_to_1000_2b2j'  : r'\thead{$2b2j$\\$ [500, 1000]$}',
                  'loose_ptj1_200_to_500_2b2j'   : r'\thead{$2b2j$\\$ [200, 500]$}',
                  'loose_ptj1_20_to_200_2b2j'    : r'\thead{$2b2j$\\$ [20, 200]$}',
                  'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0': r'\thead{hh $\kappa(\lambda_{hhh}) = 1,$\\$\kappa(y_\text{top}) = 1$}', 
                  'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0': r'\thead{hh $\kappa(\lambda_{hhh}) = 2,$\\$ \kappa(y_\text{top}) = 1$}', 
                  'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0': r'\thead{hh $\kappa(\lambda_{hhh}) = 5,$\\$ \kappa(y_\text{top}) = 1$}', 
                  'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0': r'\thead{hh $\kappa(\lambda_{hhh}) = -5,$\\$ \kappa(y_\text{top}) = 1$}',  
                  'loose_noGenFilt_signal_hh_TopYuk_0.9_SlfCoup_1.0': r'\thead{hh $\kappa(\lambda_{hhh}) = 1,$\\$ \kappa(y_\text{top}) = 0.9$}', 
                  'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_1.0': r'\thead{hh $\kappa(\lambda_{hhh}) = 1,$\\$ \kappa(y_\text{top}) = 1.1$}', 

    }

  return d_cuts_latex, d_samp_latex 
 

#_________________________________________________________________________
def get_samp_set():

  d_samp_sets = {

    'test'          : ['loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0'],

    'all'          : ['loose_noGenFilt_wh',
                       'loose_noGenFilt_zh',
                       'loose_noGenFilt_zz',
                       'loose_noGenFilt_bbh',
                       'loose_noGenFilt_tth',
                       'loose_noGenFilt_ttbb',
                       'loose_noGenFilt_ttbar',
                       'loose_ptj1_1000_to_infty_4b',
                       'loose_ptj1_500_to_1000_4b',
                       'loose_ptj1_200_to_500_4b',
                       'loose_ptj1_20_to_200_4b',
                       'loose_ptj1_1000_to_infty_2b2j',
                       'loose_ptj1_500_to_1000_2b2j',
                       'loose_ptj1_200_to_500_2b2j',
                       'loose_ptj1_20_to_200_2b2j',
                       'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                       'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0', 
                       'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0', 
                       'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0', 
                       'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_1.0', 
                      ],

    'smallbkgs'     : ['loose_noGenFilt_wh',
                       'loose_noGenFilt_zh',
                       'loose_noGenFilt_zz',
                       'loose_noGenFilt_bbh',
                       'loose_noGenFilt_tth',
                       'loose_noGenFilt_ttbb'],

    'mainbkgs'      : ['loose_noGenFilt_ttbar',
                       'loose_ptj1_1000_to_infty_4b',
                       'loose_ptj1_500_to_1000_4b',
                       'loose_ptj1_200_to_500_4b',
                       'loose_ptj1_20_to_200_4b',
                       'loose_ptj1_1000_to_infty_2b2j',
                       'loose_ptj1_500_to_1000_2b2j',
                       'loose_ptj1_200_to_500_2b2j',
                       'loose_ptj1_20_to_200_2b2j'],

    'signals'       : ['loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                       'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0', 
                       'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0', 
                       'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0', 
                       'loose_noGenFilt_signal_hh_TopYuk_1.1_SlfCoup_1.0', 
                      ]
  }
  return d_samp_sets

#_________________________________________________________________________
def mkdir(dirPath):
  '''
  make directory for given input path
  '''
  try:
    os.makedirs(dirPath)
    print 'Successfully made new directory ' + dirPath
  except OSError:
    pass
 
if __name__ == "__main__":
  #main(sys.argv)
  main()
