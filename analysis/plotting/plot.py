#!/usr/bin/env python
'''

Welcome to plot.py for 4b Pheno studies

Plotting script by Lydia Beresford and Jesse Liu

* This is a script to efficiently make 1-dimensional plots from ntuples 
* Configure various aspects in other files
    - xsecs.py
    - cuts.py
    - samples.py
    - variables.py
    - beautify.py

'''

# So Root ignores command line inputs so we can use argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(1)
from ROOT import *

import time 
import os, sys, time, argparse
from math       import sqrt
from random     import gauss
from array      import array

from xsecs      import *
from cuts       import *
from samples    import *
from variables  import *
from beautify   import *

#--------------------------------------------------
# TODO Could add back in significance scan

# Global settings

# Labels
GROUP_status = ''
NTUP_status = ""#Samples: 13 Sep 2018"
ENERGY_status = '14 TeV'

# text size as percentage
text_size = 0.045

# When lots of samples, put leg outside plot so less crowded
legend_outside_plot = False
# Whether to show yields in legend for validation purposes
show_yields_in_leg = False
# Show slices in legend for validation purposes
show_legend_slices = False

# Do b-tag weighting rather than cutting away events
# Impose 4 b-tags as weight rather than cutting away events 
# (TODO: do 2 or 3-tag as options)
do_BTagWeight = True

# b-tagging improvement factor for 4 b-quarks (hh4b signal, 4b bkg) 
bTagImprove_4b = 1.36

# 2 b-quarks (2b2j, ttbar bkg)
bTagImprove_2b = 1.17

#
#--------------------------------------------------

#____________________________________________________________________________
def main():
  
  t0 = time.time()
  
  #================================================
  # user set values
  #dir = 'jesse_linked_delphes' # directory input files to plot are in
  #dir = 'compare_shape_280119_cross_check_jesse_linked_delphes_ATLAScuts'
  #dir = '280119' # directory input files to plot are in
  #dir = 'original_full_stats'
  dir = '150719'
  dir = '150719/merged_nn_score_ntuples'

  ### Loose analysis plotting
  l_samples  = ['loose']
  
  l_sig_regs = ['preselection']   # gets specific region from input ROOT file

  # plots for paper
  '''
  l_vars     = ['m_hh', 'h1_M', 'h2_M', 'h1_Pt', 'h2_Pt', 'pT_hh', 'nnscore_SlfCoup_1.0_sig', 'nnscore_SlfCoup_5.0_sig'] #, 'nnscore_SlfCoup_1.0_top', 'nnscore_SlfCoup_1.0_qcd']
  
  
  l_cut_sels = [
                # Inclusive analyses (no multibin)
                'SR-res',
                'SR-int',
                'SR-bst',
  ]
  '''
 
  # computes rest of yields for paper limits  
  l_vars     = ['m_hh']
  
  l_cut_sels = [
                # Inclusive analyses (no multibin)
                'SRNN-res-lam1',
                'SRNN-int-lam1',
                'SRNN-bst-lam1',
 
                'SRNN-res-lam5',
                'SRNN-int-lam5',
                'SRNN-bst-lam5',
 
                # Multibin baseline (no DNN)
                'SR-res-200mHH250',
                'SR-res-250mHH300',
                'SR-res-300mHH350',
                'SR-res-350mHH400',
                'SR-res-400mHH500',
                'SR-res-500mHH',
                'SR-int-200mHH500',
                'SR-int-500mHH600',
                'SR-int-600mHH',
                'SR-bst-500mHH800',
                'SR-bst-800mHH',

                # Multibin baseline with DNN cut trained on k(lambda) = 1
                'SRNN-res-200mHH250-lam1',
                'SRNN-res-250mHH300-lam1',
                'SRNN-res-300mHH350-lam1',
                'SRNN-res-350mHH400-lam1',
                'SRNN-res-400mHH500-lam1',
                'SRNN-res-500mHH-lam1',
                'SRNN-int-200mHH500-lam1',
                'SRNN-int-500mHH600-lam1',
                'SRNN-int-600mHH-lam1',
                'SRNN-bst-500mHH800-lam1',
                'SRNN-bst-800mHH-lam1',

                # Multibin baseline with DNN cut trained on k(lambda) = 5
                'SRNN-res-200mHH250-lam5',
                'SRNN-res-250mHH300-lam5',
                'SRNN-res-300mHH350-lam5',
                'SRNN-res-350mHH400-lam5',
                'SRNN-res-400mHH500-lam5',
                'SRNN-res-500mHH-lam5',
                'SRNN-int-200mHH500-lam5',
                'SRNN-int-500mHH600-lam5',
                'SRNN-int-600mHH-lam5',
                'SRNN-bst-500mHH800-lam5',
                'SRNN-bst-800mHH-lam5',

                # Multibin baseline with DNN cut trained on k(lambda) = 7
                'SRNN-res-200mHH250-lam7',
                'SRNN-res-250mHH300-lam7',
                'SRNN-res-300mHH350-lam7',
                'SRNN-res-350mHH400-lam7',
                'SRNN-res-400mHH500-lam7',
                'SRNN-res-500mHH-lam7',
                'SRNN-int-200mHH500-lam7',
                'SRNN-int-500mHH600-lam7',
                'SRNN-int-600mHH-lam7',
                'SRNN-bst-500mHH800-lam7',
                'SRNN-bst-800mHH-lam7',
               ] 

  '''
  # computes yields for additional limits  
  l_cut_sels = [
                # Inclusive analyses (no multibin)
                'SRNN-res-lam7',
                'SRNN-int-lam7',
                'SRNN-bst-lam7',
 
                'SRNN-res-lam10',
                'SRNN-int-lam10',
                'SRNN-bst-lam10',

                'SRNN-res-lamM1',
                'SRNN-int-lamM1',
                'SRNN-bst-lamM1',

                'SRNN-res-lamM2',
                'SRNN-int-lamM2',
                'SRNN-bst-lamM2',

                'SRNN-res-lamM5',
                'SRNN-int-lamM5',
                'SRNN-bst-lamM5',
 
                # Multibin baseline with DNN cut trained on k(lambda) = 7
                'SRNN-res-200mHH250-lam7',
                'SRNN-res-250mHH300-lam7',
                'SRNN-res-300mHH350-lam7',
                'SRNN-res-350mHH400-lam7',
                'SRNN-res-400mHH500-lam7',
                'SRNN-res-500mHH-lam7',
                'SRNN-int-200mHH500-lam7',
                'SRNN-int-500mHH600-lam7',
                'SRNN-int-600mHH-lam7',
                'SRNN-bst-500mHH800-lam7',
                'SRNN-bst-800mHH-lam7',

                # Multibin baseline with DNN cut trained on k(lambda) = 10
                'SRNN-res-200mHH250-lam10',
                'SRNN-res-250mHH300-lam10',
                'SRNN-res-300mHH350-lam10',
                'SRNN-res-350mHH400-lam10',
                'SRNN-res-400mHH500-lam10',
                'SRNN-res-500mHH-lam10',
                'SRNN-int-200mHH500-lam10',
                'SRNN-int-500mHH600-lam10',
                'SRNN-int-600mHH-lam10',
                'SRNN-bst-500mHH800-lam10',
                'SRNN-bst-800mHH-lam10',

                # Multibin baseline with DNN cut trained on k(lambda) = -1
                'SRNN-res-200mHH250-lamM1',
                'SRNN-res-250mHH300-lamM1',
                'SRNN-res-300mHH350-lamM1',
                'SRNN-res-350mHH400-lamM1',
                'SRNN-res-400mHH500-lamM1',
                'SRNN-res-500mHH-lamM1',
                'SRNN-int-200mHH500-lamM1',
                'SRNN-int-500mHH600-lamM1',
                'SRNN-int-600mHH-lamM1',
                'SRNN-bst-500mHH800-lamM1',
                'SRNN-bst-800mHH-lamM1',

                # Multibin baseline with DNN cut trained on k(lambda) = -2
                'SRNN-res-200mHH250-lamM2',
                'SRNN-res-250mHH300-lamM2',
                'SRNN-res-300mHH350-lamM2',
                'SRNN-res-350mHH400-lamM2',
                'SRNN-res-400mHH500-lamM2',
                'SRNN-res-500mHH-lamM2',
                'SRNN-int-200mHH500-lamM2',
                'SRNN-int-500mHH600-lamM2',
                'SRNN-int-600mHH-lamM2',
                'SRNN-bst-500mHH800-lamM2',
                'SRNN-bst-800mHH-lamM2',

                # Multibin baseline with DNN cut trained on k(lambda) = -5
                'SRNN-res-200mHH250-lamM5',
                'SRNN-res-250mHH300-lamM5',
                'SRNN-res-300mHH350-lamM5',
                'SRNN-res-350mHH400-lamM5',
                'SRNN-res-400mHH500-lamM5',
                'SRNN-res-500mHH-lamM5',
                'SRNN-int-200mHH500-lamM5',
                'SRNN-int-500mHH600-lamM5',
                'SRNN-int-600mHH-lamM5',
                'SRNN-bst-500mHH800-lamM5',
                'SRNN-bst-800mHH-lamM5',
               ] 
  ''' 
  # additional score distributions
  '''l_vars = [
            'nnscore_SlfCoup_m20.0_sig',
            'nnscore_SlfCoup_m10.0_sig',
            'nnscore_SlfCoup_m7.0_sig',
            'nnscore_SlfCoup_m5.0_sig',
            'nnscore_SlfCoup_m2.0_sig',
            'nnscore_SlfCoup_m1.0_sig',
            'nnscore_SlfCoup_m0.5_sig',
            'nnscore_SlfCoup_0.5_sig',
            'nnscore_SlfCoup_1.0_sig',
            'nnscore_SlfCoup_2.0_sig',
            'nnscore_SlfCoup_3.0_sig',
            'nnscore_SlfCoup_5.0_sig',
            'nnscore_SlfCoup_7.0_sig',
            'nnscore_SlfCoup_10.0_sig',
            'nnscore_SlfCoup_20.0_sig']
  '''
  ### ATLAS analysis xcheck (old)
  #l_vars     = ['m_hh']     # corresponds to variable in variables.py
  #l_samples  = ['resolved'] #,'resolved_kl','resolved_kt','boosted','boosted_kl','boosted_kt'] # corresponds to sets of files in samples.py 
  #cut_sel    = ['ntag4']     # corresponds to set of cuts in cuts.py 
  ###

  lumi    =  3000.0 #24.3 
  yield_var = "m_hh" # Will plot multiple variables but only want to save yield file for a single variable

  UnitNorm = False
  IsLogY   = True

  annotate_text = ''
  savedir = os.getcwd()+'/figs'+"/"+dir

  #================================================
  
  # -------------------------------------------------------------
  # Argument parser
  parser = argparse.ArgumentParser(description='Analyse background/signal TTrees and make plots.')
  parser.add_argument('-l', '--lumi',    type=str, nargs='?', help='Float of integrated luminosity to normalise MC to.', default=lumi)
  parser.add_argument('-n', '--noLogY',  action='store_true', help='Do not draw log Y axis.')
  parser.add_argument('-s', '--cut_sel', type=str, nargs='?', help='Selection cuts considered.')
  parser.add_argument('-v', '--var',     type=str, nargs='?', help='Variable to plot.')
 
  args = parser.parse_args()
  if args.lumi:
    lumi = args.lumi
  if args.noLogY:
    IsLogY = False
  if args.cut_sel:
    l_cut_sels = [ args.cut_sel ] 
  if args.var:
    l_vars = [ args.var ] 
  
  # -------------------------------------------------------------
  # --------------
  # LOOP over list of samples l_samples
  # --------------
  
  for analysis in l_samples:
  
    # --------------
    # LOOP over list of signal regions l_sig_regs:
    # --------------
    
    for sig_reg in l_sig_regs:
  
      # --------------
      # LOOP over list of cut selections in l_cut_sel:
      # --------------
    
      for cut_sel in l_cut_sels:
    
        # --------------
        # LOOP over list of variables l_var
        # --------------
      
        for var in l_vars:
          # Convert maths characters in variables to valid file names
          save_var = var
          if '/' in var:
            save_var = var.replace('/', 'Over', 1)
          if '(' in var:
            save_var = save_var.replace('(', '', 1)
          if ')' in var:
            save_var = save_var.replace(')', '', 1)
          
          print( '--------------------------------------------' )
          print( '\nWelcome to plot.py\n' )
          print( 'Plotting variable: {0}'.format(var) )
          print( 'Selection region: {0}'.format(sig_reg) )
          print( 'Kinematic regime: {0}'.format(cut_sel) )
          print( 'Normalising luminosity: {0}'.format(lumi) )
          print( '\n--------------------------------------------\n' )
          
          mkdir(savedir) 
    
          if cut_sel is '': 
            save_name = savedir + '/{0}_{1}_{2}'.format(analysis, sig_reg, save_var)
          else:
            save_name = savedir + '/{0}_{1}_{2}_{3}'.format(analysis, sig_reg, save_var, cut_sel)
     
          if IsLogY: save_name += '_LogY'
          if UnitNorm: save_name += '_UnitNorm'
    
          print_lumi = lumi # [1/fb]
          print('Lumi to print: {0}'.format(print_lumi))
        
          calc_selections(var, yield_var, dir, savedir, analysis, lumi, save_name, sig_reg, cut_sel, print_lumi, annotate_text, IsLogY, UnitNorm)
  
  tfinish = time.time()
  telapse = tfinish - t0
    
  print('\n--------------------------------------------------')
  print('Finished plotting in {0:.1f}s'.format(telapse) )
  print('Have a lovely day :) ')
  print('--------------------------------------------------')

#____________________________________________________________________________
def calc_selections(var, yield_var, dir, savedir, analysis, lumi, save_name, sig_reg, cut_sel, print_lumi, annotate_text='', IsLogY=True, UnitNorm = False, l_print_cuts=[]):
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
  #
  # Get samples to plot from samples.py
  l_samp_bkg, l_sampOther = get_samples_to_plot(analysis)
  #
  # Get dictionary defining sample properties from samples.py
  d_samp = configure_samples()
  #
  # Get dictionary of histogram configurations from variables.py
  d_vars = configure_vars(cut_sel)
  
  cut_string, l_cuts = configure_cuts(cut_sel) 
  #
  #----------------------------------------------------

  l_samp = l_samp_bkg + l_sampOther

  print('\n----------------------------------')
  print('Samples to plot:')
  for samp in l_samp: print(samp)
  print('----------------------------------\n')
  
  #----------------------------------------------------
  # 
  # Initialise objects for analysis
  #
  #----------------------------------------------------

  # obtain the number of bins with their xmin and xmax
  hNbins = d_vars[var]['hXNbins']
  hXmin  = d_vars[var]['hXmin']
  hXmax  = d_vars[var]['hXmax']

  variable_bin = False
  hXarray = []
  if hNbins == 'var':
    variable_bin = True
    hXarray = d_vars[var]['binsLowE']  
    hNbins = len(hXarray) - 1

  # Initialise stacked background  
  hs = THStack('','')
  hs_bkg_frac  = THStack('','') # Another stack normalised so displays fraction of processes
 
  # Initialise objects to fill in loop 
  d_files = {}
  d_hists = {}
  d_yield = {}
  d_yieldErr = {}
  d_raw = {}
  nTotBkg = 0 # yield of background
  nTotBkgRaw = 0 # raw yield of background
  nVarBkg = 0 # variance of background
 
  l_bkg = []
  l_sig = []
  
  l_styles = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  Nsignal_count = 0

  # ----------------------------------------------------------------- 
  # set up yields file before sample loop 
  # ----------------------------------------------------------------- 

  # Total yields file: sample, sig/bkg, yield, yieldErr, raw
  yield_file = savedir + '/YIELD_{0}_{1}_{2}.txt'.format(analysis, sig_reg, cut_sel)
  if UnitNorm: 
    yield_file = savedir + '/YIELD_{0}_{1}_{2}_UnitNorm.txt'.format(analysis, sig_reg, cut_sel)
  if var == yield_var:
    print('Opening yield file: '+yield_file)
    open(yield_file, 'w') # Open new yield file & overwrite existing one
    with open(yield_file, 'a+') as f_out: 
      print("Writing headings to yield file: "+yield_file)
      f_out.write('sample,sample_type,yield,yieldErr,raw\n')

  # ----------------------------------------------------------------- 
  #
  # Loop through samples, fill histograms
  #
  # ----------------------------------------------------------------- 
  
  for samp in l_samp:
    
    print( 'Processing {0}'.format(samp) )
    # obtain sample attributes 
    sample_type = d_samp[samp]['type']
  
    #lChoose full path of sample by its type  
    full_path = ''
    if sample_type == 'sig':
      l_color     = d_samp[samp]['l_color']
      full_path = '{0}/{1}{2}'.format(sig_path, samp, sig_suffix) 
      l_sig.append(samp)
    elif sample_type == 'bkg':
      f_color     = d_samp[samp]['f_color']
      full_path = '{0}/{1}{2}'.format(bkg_path, samp, bkg_suffix) 
      l_bkg.append(samp)
    else:
      print('Please set a sample type in samples.py for sample {0}'.format(samp) )

    cutsAfter = cut_string 

    # assign TFile to a dictionary entry
    d_files[samp] = TFile(full_path)
   
    # Get TH1F histogram from the TTree in the TFile and store to dictionary entry
    d_hists[samp] = tree_get_th1f( d_files[samp], samp, var, sig_reg, cutsAfter, hNbins, hXmin, hXmax, lumi, variable_bin, hXarray)

    # ---------------------------------------------------- 
    # Stacked histogram: construct and format
    # ---------------------------------------------------- 
    # extract key outputs of histogram 
    hist        = d_hists[samp][0]
    nYield      = d_hists[samp][1]
    nYieldErr   = d_hists[samp][2]
    nRaw        = d_hists[samp][3]
    
    # samp : nYield number of events for each sample
    d_yield[samp]    = nYield
    d_yieldErr[samp] = nYieldErr
    d_raw[samp]      = nRaw
    
    # add background to stacked histograms
    if sample_type == 'bkg':
      hs.Add(hist)
      
      format_hist(hist, 1, 0, 1, f_color, 1001, 0)
      nTotBkg  += nYield
      nTotBkgRaw  += nRaw
      nVarBkg  += nYieldErr ** 2
    
    if sample_type == 'sig':
      format_hist(hist, 3, l_color, l_styles[Nsignal_count], f_color=0)
      Nsignal_count += 1

    # ----------------------------------------------------------------- 
    # save yields file 
    # sample sig/bkg yield yieldErr raw
    # ----------------------------------------------------------------- 
 
    # Total yields file: sample, sig/bkg, yield, yieldErr, raw
    if var == yield_var:
      print('Writing to yield file: '+yield_file)
      with open(yield_file, 'a') as f_out: 
        f_out.write('{0},{1},{2},{3},{4}\n'.format(samp,sample_type,d_yield[samp],d_yieldErr[samp],d_raw[samp]))
        #print '{0},{1},{2},{3},{4}\n'.format(samp,sample_type,d_yield[samp],d_yieldErr[samp],d_raw[samp])
 
  errStatBkg = sqrt( nVarBkg ) # treat total statistical error as sum in quadrature of sample stat errors
  errTotBkg  = sqrt( errStatBkg**2 + (0.2 * nTotBkg) ** 2 )
    
  if var == yield_var:
    with open(yield_file, 'a') as f_out: 
      print('Writing total background count')
      f_out.write( 'TotBkg,bkg,{0},{1},{2}\n'.format( nTotBkg, errTotBkg, nTotBkgRaw ) )
  
  print('errStatBkg: {0:.3f}, sqrtB: {1:.3f}, errTotBkg: {2:.3f}'.format(errStatBkg, sqrt(nTotBkg), errTotBkg))

  print('==============================================')
  print('----------------------------------------------')
  print('{0}, Total bkg, {1:.3f}, {2:.3f}'.format(cut_sel, nTotBkg, errTotBkg))
  print('----------------------------------------------')
 
  # ----------------------------------------------------------------- 
  # Legend for bkg, signals and total bkg yield
  # ----------------------------------------------------------------- 
  #leg = mk_leg(0.57, 0.7, 0.95, 0.98, cut_sel, l_sampOther, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.03)
  # legend with breakdown of background by sample
  d_bkg_leg = {}
  l_bkg_leg = ['samp1']
  if legend_outside_plot:
    # Legend for signals
    leg = mk_leg(0.64, 0.20, 0.88, 0.37, cut_sel, l_sampOther, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.03)
    # Legend for backgrounds
    d_bkg_leg['samp1'] = mk_leg(0.64, 0.38, 0.88, 0.90, cut_sel, l_samp_bkg, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.03)
  else:
    # Legend for signals
    leg = mk_leg(0.57, 0.70, 0.95, 0.91, cut_sel, l_sampOther, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.045)
    # Legend for backgrounds
    d_bkg_leg['samp1'] = mk_leg(0.77, 0.40, 0.93, 0.69, cut_sel, l_samp_bkg, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.045, Ncols=1)
  #d_bkg_leg['samp1'] = mk_leg(0.57, 0.28, 0.95, 0.7, cut_sel, l_samp_bkg, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.03)

  print('==============================================')
  # ----------------------------------------------------------------- 
  #
  # Make MC error histogram (background uncertainty hatching) if bkg samples not empty
  #
  pc_sys = 0 # percentage systematic uncertainty
  h_mcErr = hs
  if nTotBkg > 0.:
    h_mcErr = mk_mcErr(hs, pc_sys, hNbins, hXmin, hXmax, variable_bin, hXarray)
    h_mcErr.SetFillStyle(3245) # hatching 
    h_mcErr.SetFillColor(kGray+2)
    h_mcErr.SetLineWidth(2)
    # make other markings invisible
    #h_mcErr.SetLineColorAlpha(kWhite, 0)
    h_mcErr.SetLineColorAlpha(kGray+2, 1.0)
    h_mcErr.SetMarkerColorAlpha(kWhite, 0)
    h_mcErr.SetMarkerSize(0)
    #h_mcErr.SetMarkerColorAlpha(kWhite, 0)
    if show_yields_in_leg:
      leg.AddEntry(h_mcErr, 'Bkg ({0:.3g}, {1})'.format(nTotBkg, int(nTotBkgRaw)), 'lf')
    else:
      leg.AddEntry(h_mcErr, 'Total background')
  # ----------------------------------------------------------------- 
  
  # ----------------------------------------------------------------- 
  #
  # Now all background histogram and signals obtained
  # Proceed to make significance scan
  #
  # ----------------------------------------------------------------- 
 
  # Dicitonary for histograms and its significance plots
  # in format {samp_name : histogram}
  d_hsig = {}
  
  # calculate significances for signals only
  for samp in l_samp:
    sample_type = d_samp[samp]['type']
    if sample_type == 'sig':
      d_hsig[samp] = d_hists[samp][0]
  
  # ----------------------------------------------------------------- 
  # Proceed to plot
  plot_selections(var, hs, d_hsig, h_mcErr, leg, l_bkg_leg, d_bkg_leg, lumi, save_name, pc_sys, analysis, sig_reg, cut_sel, nTotBkg, l_sig, cutsAfter
, annotate_text ,variable_bin, l_cuts, print_lumi, IsLogY, UnitNorm)
  # ----------------------------------------------------------------- 
  
  return nTotBkg


#_______________________________________________________
def tree_get_th1f(f, hname, var, sig_reg, unweighted_cuts='', Nbins=100, xmin=0, xmax=100, lumifb=0, variable_bin=False, hXarray=0):
  '''
  from a TTree, project a leaf 'var' and return a TH1F
  '''
  if variable_bin:
    h_AfterCut   = TH1D(hname + '_hist', "", Nbins, array('d', hXarray) )
  else:
    h_AfterCut   = TH1D(hname + '_hist', "", Nbins, xmin, xmax)
 
  h_AfterCut.Sumw2()
  
  # Normalising number of raw events
  N_raw = f.Get('loose_cutflow').GetBinContent(1)

  # Obtain cross-sections
  d_xsecs = configure_xsecs()
  xsec = d_xsecs[hname]

  # Hard-coded k-factors and b-tagging improvement factors
  kfactor = 1.
  if 'ttbar' in hname:
    kfactor = 1.4  * bTagImprove_2b # NLO / LO
  if '2b2j' in hname:
    kfactor = 1.3  * bTagImprove_2b # NLO / LO
  if '4b' in hname:
    kfactor = 1.6  * bTagImprove_4b  # NLO / LO
  if 'signal_hh' in hname:
    kfactor = 1.45 * bTagImprove_4b # (NNLO+NNLL) / NLO
  
  # Impose 4 b-tags as weight 
  if do_BTagWeight:
    bTagWeight = 'h1_j1_BTagWeight * h1_j2_BTagWeight * h2_j1_BTagWeight * h2_j2_BTagWeight'
  else:
    bTagWeight = 1.

  # Construct weight string
  my_weight = '{0} * {1}'.format(bTagWeight, kfactor)

  # Construct final TCut string
  cuts = '( ({0}) * (1000 * {1} * {2} * {3}) ) / {4}'.format( unweighted_cuts, xsec, lumifb, my_weight, N_raw ) # Factor of 1000 to convert xsec from ifb to ipb
  
  print('---------------------------------')
  print('Final weighted cut string: ')
  print(cuts)
  print('---------------------------------')

  # ========================================================= 
  t = f.Get(sig_reg)
  t.Project(hname + '_hist', var, cuts)
  
  # =========================================================
  # perform integrals to find 
  # total yield, one-sided lower and upper cumulative histos
  nYieldErr = ROOT.Double(0)
  nYield    = h_AfterCut.IntegralAndError(0, Nbins+1, nYieldErr)
  
  for my_bin in range( h_AfterCut.GetXaxis().GetNbins() + 1 ):
    
    # get lower edge of bin
    bin_low = h_AfterCut.GetXaxis().GetBinLowEdge( my_bin )
    
    # set the negatively weighted values to 0.
    bin_val = h_AfterCut.GetBinContent( my_bin )
    if bin_val < 0:
      print( 'WARNING: Bin {0} of sample {1} has negative entry, setting central value to 0.'.format(my_bin, hname) )
      h_AfterCut.SetBinContent(my_bin, 0.)
    
  nRaw = h_AfterCut.GetEntries()
  #print( 'hist.IntegralAndError() : sample {0} has integral {1:.3f} +/- {2:.3f}'.format( hname, nYield, nYieldErr ) )
  # =========================================================
  
  return [h_AfterCut, nYield, nYieldErr, nRaw]


#____________________________________________________________________________
def plot_selections(var, h_bkg, d_hsig, h_mcErr, leg, l_bkg_leg, d_bkg_leg, lumi, save_name, pc_sys, analysis, sig_reg, cut_sel, nTotBkg, l_sig, cutsAfter, annotate_text, variable_bin, l_cuts, print_lumi, IsLogY=True, UnitNorm = False):
  '''
  plots the variable var given input THStack h_bkg, one signal histogram and legend built
  makes a dat / bkg panel in lower part of figure
  '''
  print('Proceeding to plot')
  
  # gPad left/right margins
  gpLeft = 0.15
  if legend_outside_plot:
    gpRight = 0.37
    can  = TCanvas('','',1200,800)
  else:
    gpRight = 0.05
    can  = TCanvas('','',1000,800)
  gpTop = 0.05
  gpBot = 0.18
  #can  = TCanvas('','',1000,1000)
    
  d_vars = configure_vars(cut_sel)
  
  #==========================================================
  # Build canvas
  customise_gPad() 
  pad1 = TPad('pad1', '', 0.0, 0.0, 1.0, 1.0)
  #pad1 = TPad('pad1', '', 0.0, 0.40, 1.0, 1.0)
  #pad2 = TPad('pad2', '', 0.0, 0.00, 1.0, 0.4)
  pad1.Draw()
  pad1.cd()
  
  customise_gPad(top=gpTop, bot=gpBot, left=gpLeft, right=gpRight)
  if IsLogY: pad1.SetLogy()
  
  #==========================================================
  # calculate bin width 
  hNbins = d_vars[var]['hXNbins']
  hXmin  = d_vars[var]['hXmin']
  hXmax  = d_vars[var]['hXmax']
  if not variable_bin: binWidth = (hXmax - hXmin) / float(hNbins)
  
  # label axes of top pad
  varTeX = 'tlatex'
  
  Xunits = d_vars[var]['units']
  if Xunits == '':
    #xtitle = '{0}'.format( d_vars[var]['tlatex'])
    xtitle = '{0}'.format( d_vars[var][varTeX])
  else:
    xtitle = '{0} [{1}]'.format( d_vars[var][varTeX], Xunits ) 

  binUnits = d_vars[var]['units']
  if variable_bin:
    ytitle = 'Events / bin'
  elif 0.1 < binWidth < 1:
    ytitle = 'Events / {0:.2f} {1}'.format(binWidth, binUnits)
  elif binWidth <= 0.1:
    ytitle = 'Events / {0:.2f} {1}'.format(binWidth, binUnits)
  elif binWidth >= 1:
    ytitle = 'Events / {0:.0f} {1}'.format(binWidth, binUnits)
  enlargeYaxis = True
  if 'nnscore' in var:
    enlargeYaxisEvenMore = True

  #=============================================================
  # draw and decorate
  # draw elements
  if nTotBkg > 0.:
    if UnitNorm and h_bkg.Integral() > 0.:
      h_bkg.Scale(1.0/h_bkg.Integral()) 
    h_bkg.Draw('hist')
    customise_axes(h_bkg, xtitle, ytitle, 1.5, IsLogY, enlargeYaxis, enlargeYaxisEvenMore)

  # draw signal samples
  for samp in d_hsig:
    print('Drawing {0}'.format(samp))
    #d_hsig[samp].Scale(1/100)
    #for i in range(1,d_hsig[samp].GetNbinsX() + 1):
    #  val = 0
    #  n=d_hsig[samp].GetBinContent(i)
    #  w=d_hsig[samp].GetBinWidth(i)
    #  if (w > 0):
    #    val = n*100./w
    #    d_hsig[samp].SetBinContent(i,val)

    if UnitNorm and d_hsig[samp].Integral() > 0.:
      d_hsig[samp].Scale(1.0/d_hsig[samp].Integral())
    d_hsig[samp].Draw('hist same') #e2 = error coloured band
    customise_axes(d_hsig[samp], xtitle, ytitle, 1.5, IsLogY, enlargeYaxis, enlargeYaxisEvenMore)

  # Clone the total background histogram to draw the line if bkg samples not empty
  if nTotBkg > 0.:
    h_mcErr_clone = h_mcErr.Clone()
    h_mcErr_clone.SetFillColorAlpha(kWhite, 0)
    h_mcErr_clone.SetFillStyle(0)
    if UnitNorm:
      h_mcErr.Scale(1.0/h_mcErr.Integral())
      h_mcErr_clone.Scale(1.0/h_mcErr_clone.Integral())
    h_mcErr.Draw('same e2')
    h_mcErr_clone.Draw('same hist')
  
  leg.Draw('same')
  if nTotBkg > 0.:
    for bkg_leg in l_bkg_leg:
      d_bkg_leg[bkg_leg].Draw('same')
  
  # Add text e.g. ATLAS Label, sqrt{s}, lumi to plot
  add_text_to_plot(analysis, sig_reg, cut_sel, lumi, l_cuts, annotate_text, print_lumi)

  gPad.RedrawAxis() 

  #==========================================================
  # save everything
  can.cd()
  can.SaveAs(save_name + '.pdf')
  #can.SaveAs(save_name + '.png')
  can.Close()
  
#____________________________________________________________________________
def add_text_to_plot(analysis, sig_reg, cut_sel, lumi, l_cuts, annotate_text, print_lumi):
  
  print('Adding sqrt{s}, lumi, region, ntuple version to plot')
  
  #---------------------------------------------------------------
  #
  # Text for energy, lumi, region, ntuple status
  
  if legend_outside_plot:
    myText(0.7, 0.92, 'Sample (Weighted, Fraction, Raw) ', 0.03)
  else:
    if show_yields_in_leg:
      myText(0.6, 0.83, 'Sample (Weighted, Fraction, Raw) ', 0.03)
    else: pass
  #myText(0.22, 0.93, 'MadGraph5 2.6.2 + Pythia 8.230 + Delphes 3.4.1 (LO xsec, NLOPDF, xqcut 30 GeV), ' + NTUP_status, text_size*0.6, kGray+1)
  #myText(0.22, 0.93, 'MadGraph5 2.6.2 + Pythia 8.230 + Delphes 3.4.1 (LO xsec, NLOPDF), ' + NTUP_status, text_size*0.6, kGray+1)
  #myText(0.22, 0.93, 'MadGraph5 2.6.2 + Pythia 8.230 + Delphes 3.4.1', text_size*0.6, kGray+1)
  myText(0.42, 0.84, GROUP_status, text_size*0.8, kBlack)
  myText(0.20, 0.87, '#sqrt{s}' + ' = {0}, {1:.0f}'.format(ENERGY_status, lumi) + ' fb^{#minus1}', text_size, kBlack)
  
  analysis = analysis.title()
  if 'res' in cut_sel:
    cut_txt = cut_sel.replace('-res', ' Resolved')
  if 'int' in cut_sel:
    cut_txt = cut_sel.replace('-int', ' Intermediate')
  if 'bst' in cut_sel or 'boosted' in cut_sel:
    cut_txt = cut_sel.replace('-bst', ' Boosted')

  print(cut_txt) 
  if 'preselection' in sig_reg:
    myText(0.20, 0.82, cut_txt, text_size, kBlack) 
  
  # Additional annotations
  if not annotate_text == '':
    if do_BTagWeight:
      annotate_text += ', N(b-tag) = 4'
    myText(0.42, 0.82, annotate_text, text_size*0.8, kGray+2) 
  #
  #---------------------------------------------------------------
  
#____________________________________________________________________________
def mk_mcErr(hStack, pc_sys, Nbins=100, xmin=0, xmax=100, variable_bin=False, hXarray=0):
  '''
  Make the hatched error histogram for SM prediction
  '''
  if variable_bin:
    h_mcErr = TH1D('', "", Nbins, array('d', hXarray) )
  else:
    h_mcErr = TH1D('', "", Nbins, xmin, xmax)
  
  print( 'Making MC err' )
  for my_bin in range( hStack.GetStack().Last().GetSize() ):
    yval = hStack.GetStack().Last().GetBinContent(my_bin)
    
    if yval == 0:
      yval = 0.001
    # Handle pathologies where bin yield is negative
    if yval < 0:
      yval = 0.001
      print( '\nWARNING: negative histogram value {0} in bin {1}, setting to 0.001'.format(yval, my_bin) )
  
    # get statistical variance as sum of weights squared
    yval_GetErr   = hStack.GetStack().Last().GetBinError(my_bin)
    # add stat and sys err in quadrature
    yval_err = sqrt( yval_GetErr ** 2 + ( 0.01 * pc_sys * yval ) ** 2 )
    h_mcErr.SetBinContent( my_bin, yval )
    h_mcErr.SetBinError(   my_bin, yval_err ) 
  
  return h_mcErr

#____________________________________________________________________________
def mk_leg(xmin, ymin, xmax, ymax, cut_sel, l_samp, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.05, Ncols=1) :
  '''
  @l_samp : Constructs legend based on list of samples 
  @nTotBkg : Total background events
  @d_hists : The dictionary of histograms 
  @d_samp : May from samples to legend text
  @d_yields : The dictionary of yields 
  @d_yieldErr : Dictionary of errors on the yields
  @d_raw : Dictionary of raw yields
  @sampSet_type : The type of samples in the set of samples in the list 
  '''  

  # ---------------------------------------------------- 
  # Legend: construct and format
  # ---------------------------------------------------- 
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetBorderSize(0)
  leg.SetTextSize(txt_size)
  leg.SetNColumns(Ncols)
  leg.SetTextFont(132)

  # legend markers 
  d_legMk = {
    'bkg'  : 'f',
    'sig'  : 'l',
    }

  # Entries not to show 
  l_leg_do_not_show = [
   'loose_ptj1_200_to_500_2b2j'    ,
   'loose_ptj1_500_to_1000_2b2j'   ,
   'loose_ptj1_1000_to_infty_2b2j' ,
   'loose_ptj1_200_to_500_4b'    ,
   'loose_ptj1_500_to_1000_4b'   ,
   'loose_ptj1_1000_to_infty_4b' ,
   'loose_noGenFilt_ttbb',
   'loose_noGenFilt_bbh',
   'loose_noGenFilt_wh'
  ] 

  # Need to reverse background order so legend is filled as histogram is stacked
  if sampSet_type == 'bkg':
    l_samp = [x for x in reversed(l_samp)]
  for samp in l_samp: 
    #print( 'Processing legend {0}'.format(samp) )
    # obtain sample attributes 
    hist        = d_hists[samp][0]
    sample_type = d_samp[samp]['type']
    leg_entry   = d_samp[samp]['leg']
    legMk       = d_legMk[sample_type]
    print('{0}, {1}, {2:.3f} +/- {3:.3f}, {4:.0f}'.format(cut_sel, samp, d_yield[samp], d_yieldErr[samp], d_raw[samp]) )
    
    if samp not in l_leg_do_not_show:   

      # calculate the % of each background component and put in legend
      pc_yield   = 0
      if sample_type == 'bkg':
        pc_yield = 0.
        if nTotBkg >0.:
          pc_yield = 100 * ( d_yield[samp] / float(nTotBkg) )
        if show_yields_in_leg:
          leg_txt = '{0} ({1:.2g}, {2:.1f}%, {3:.0f})'.format( leg_entry, d_yield[samp], pc_yield, d_raw[samp] )
        else:
          leg_txt = '{0}'.format( leg_entry )
      if sample_type == 'sig':
        if show_yields_in_leg:
          leg_txt = '{0} ({1:.2g}, {2:.0f})'.format(leg_entry, d_yield[samp], d_raw[samp])
        else:
          leg_txt = '{0}'.format( leg_entry )

      leg.AddEntry(hist, leg_txt, legMk)
      #print('{0}, {1}, {2:.3f}, {3:.3f}%'.format(sig_reg, samp, d_yield[samp], pc_yield) )
 
  return leg
    
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
