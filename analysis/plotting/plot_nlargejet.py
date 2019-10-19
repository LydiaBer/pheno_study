#!/usr/bin/env python
'''
plot.py is the main script to do the plotting
This reads the ntuples produced by SusySkimHiggsino
Makes plots of data vs MC in various variables
Configure various aspects in
  - cuts.py
  - samples.py
  - variables.py
One specifies the samples to be plotted at the top of calc_selections() function
'''
# So Root ignores command line inputs so we can use argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(1)
from ROOT import *
import time 
from math import sqrt
from random import gauss
import os, sys, time, argparse
from array import array

from samples import *
from cuts import *
from variables import *


# Labels
#GROUP_status = '#bf{#it{Pheno4b}} Internal'
#NTUP_status = "Samples: 11 Aug 2018 '4 #times 1.5m campaign' "
#ENERGY_status = '14 TeV'

GROUP_status = '#bf{#it{Pheno4b}}'
NTUP_status = "19 Mar 2019"
ENERGY_status = '14 TeV'

# Jesse's configuration
#TOPPATH = '/home/jesseliu/pheno/fcc/data/samples/14TeV/2018aug11'
#TOPPATH = '/home/jesseliu/pheno/fcc/PhenoSim/data/samples/14TeV/2018sep13/all_merged_delphes'
#TOPPATH = '/home/jesseliu/pheno/fcc/PhenoSim/data/samples/14TeV/2018nov26/all_merged_delphes/ntuples'
TOPPATH = '/home/jesseliu/pheno/fcc/PhenoSim/data/samples/14TeV/2019mar18/all_merged_delphes/ntuples'
#TOPPATH = '/home/jesseliu/pheno/fcc/PhenoSim/data/hh4b/analysis_code/pheno_study/analysis/intermediate/output'
#/data/atlas/atlasdata/jesseliu/pheno/packages/fcc/madanalysis5/ntupMkr/Build'
BKGPATH = TOPPATH
SIGPATH = TOPPATH + '/merged_signals'

use_mc_fakes = False 
useLooseNominal = False
# When lots of samples, put leg outside plot so less crowded
legend_outside_plot = False

doBTagWeight = False

normalise_unity = True
# text size as percentage
text_size = 0.045

#____________________________________________________________________________
def main():
  
  t0 = time.time()
  
  #================================================
  # default values
  var     = 'Jet[0].PT'
  sig_reg = 'SR-preselect'
  var     = 'm_h2'
  sig_reg = 'SR-1ibsmall-2ibtrk-Mass'

  lumi    = 1.0 # [1/fb]
  
  #lumi    = 80.0 # [1/fb]
  ttbarSamp='ttbar'
  unblind = False
  cutArrow = False
  IsLogY = False
  # check user has inputted variables or not
  parser = argparse.ArgumentParser(description='Analyse background/signal TTrees and make plots.')
  parser.add_argument('-v', '--variable',  type=str, nargs='?', help='String name for the variable (as appearing in the TTree) to make N-1 in.', default=var)
  parser.add_argument('-s', '--sigReg',    type=str, nargs='?', help='String name of selection (signal/control) region to perform N-1 selection.', default=sig_reg)
  parser.add_argument('-l', '--lumi',      type=str, nargs='?', help='Float of integrated luminosity to normalise MC to.', default=lumi)
  parser.add_argument('-t', '--ttbarSamp', type=str, nargs='?', help='ttbar sample to use.', default=ttbarSamp)
  parser.add_argument('-u', '--unblind',   type=str, nargs='?', help='Should the SRs be unblinded?')
  parser.add_argument('-a', '--cutArrow',  action='store_true', help='Draw arrows where cuts are placed for N-1 plots.')
  parser.add_argument('-n', '--noLogY',  action='store_true', help='Do not draw log Y axis.')
 
  args = parser.parse_args()
  if args.variable:
    var      = args.variable
  if args.sigReg:
    sig_reg = args.sigReg
  if args.lumi:
    lumi = args.lumi
  if args.ttbarSamp:
    ttbarSamp = args.ttbarSamp

  # I know we could just use a bool argument here, but maybe safer to 
  # require the string, so it's harder to unblind by mistake!
  if args.unblind == 'True':
    unblind = True
  if args.cutArrow:
    cutArrow = True
  if args.noLogY:
    IsLogY = False

  print( '=========================================' )
  print( 'Plotting variable: {0}'.format(var) )
  print( 'Selection region: {0}'.format(sig_reg) )
  print( 'Normalising luminosity: {0}'.format(lumi) )
  print( 'ttbar Sample: {0}'.format(ttbarSamp) )
  print( '=========================================\n' )
  
  #================================================
  # make (relative) save directory if needed 
  savedir = 'figs/2019mar18'
  mkdir(savedir)

  l_SRs = [
    'SR-preselect',
    'SR-h1Pt200',
    'SR-1trkj-0ib',
    'SR-2trkj-0ib',
    'SR-2trkj-1ib',
    'SR-2trkj-2ib',
    'SR-2smallj-1ib',
    'SR-2smallj-2ib',
    'SR-2ibsmall-1ibtrk',
    'SR-1ibsmall-2ibtrk',
    'SR-2ibsmall-2ibtrk',
  ]

  l_vars = [
   'm_h1_large_jet', 
   'pT_h1_large_jet',
   'm_h2',
   'pT_h2', 
   'dR_trkJet1_large_jet', 
   'dR_trkJet2_large_jet',
   'dR_trkJet1_trkJet2', 
   'm_hh',
    ]
  l_SRs = [
  'SR-0LJ-preselect',
  #'SR-0LJ-2b',
  #'SR-0LJ-4b',
  ]
  l_vars = [
   'n_large_jets',
   'n_bjets_in_higgs1+n_bjets_in_higgs2', 
  ]
  
  for var in l_vars:
    for sig_reg in l_SRs:
      save_var = var
      # convert maths characters are legit file names
      if '/' in var:
        save_var = var.replace('/', 'Over', 1)
      if '(' in var:
        save_var = save_var.replace('(', '', 1)
      if ')' in var:
        save_var = save_var.replace(')', '', 1)
      if IsLogY:
        save_name = savedir + '/hist1d_{0}_{1}'.format(save_var, sig_reg)
      if not IsLogY:
        save_name = savedir + '/hist1d_{0}_{1}_noLogY'.format(save_var, sig_reg)

      add_cut = 'm_hh > 0'
      annotate_text = ''

      #==========================================================
      # List samples to analyse 
      #==========================================================
      if use_mc_fakes:
        ttbarSamp = 'alt_ttbar_nonallhad'
      else: 
        ttbarSamp = 'ttbar' 

      calc_selections(var, add_cut, lumi, save_name, sig_reg, annotate_text, ttbarSamp, unblind, cutArrow, IsLogY)

  tfinish = time.time()
  telapse = tfinish - t0
  print( '{0:.3f}s'.format(telapse))

#____________________________________________________________________________
def calc_selections(var, add_cuts, lumi, save_name, sig_reg, annotate_text='', ttbarSamp='ttbar', unblind=False, cutArrow=False, IsLogY=True):
  '''
  Extract trees given a relevant variable
  '''
  #==========================================================
  # Prepare information and objects for analysis and plots
  #==========================================================

  # Multibosons
  l_samp1 = [
    #'bbh',
    #'tth',
    #'zh',
    #'4b_1000_to_infty',
    #'4b_500_to_1000',
    #'4b_200_to_500',
    #'4b_20_to_200',
    #'ttbar',
    #'2b2j_1000_to_infty',
    #'2b2j_500_to_1000',
    #'2b2j_200_to_500',
    #'2b2j_20_to_200',
    ]

  l_sampOther = [
    #'pp2hh_loop_sm',
    'pp2hh_TopYuk_1.0_SlfCoup_5.0',
    'pp2hh_TopYuk_1.0_SlfCoup_3.0',
    'pp2hh_TopYuk_1.0_SlfCoup_2.0',
    'pp2hh_TopYuk_1.0_SlfCoup_1.0',
    'pp2hh_TopYuk_1.0_SlfCoup_m1.0',
    'pp2hh_TopYuk_1.0_SlfCoup_m2.0',
    'pp2hh_TopYuk_1.0_SlfCoup_m5.0',
  ]

  # blind the SRs
  if 'SR' not in sig_reg or unblind :
    l_sampOther = ['data'] + l_sampOther

  #l_samp = l_sampOther
  l_samp = l_samp1 + l_sampOther
  if use_mc_fakes:
    l_samp += l_samp4

  # obtain cut to apply (string)
  normCutsAfter, l_cuts = configure_cuts(var, add_cuts, sig_reg) 
  
  # get dictionary defining sample properties
  d_samp = configure_samples()
  
  # get dictionary of histogram configurations
  d_vars = configure_vars()
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

  # declare stacked background  
  hs = THStack('','')
  hs_intgl_low = THStack('','') # lower cut integral (for significance cut)
  hs_intgl_upp = THStack('','') # upper cut integral (for significance cut)
 
  # initialise objects to fill in loop 
  d_files = {}
  d_hists = {}
  d_yield = {}
  d_nRaw = {}
  d_yieldErr = {}
  nTotBkg = 0 # yield of background
  nRawBkg = 0 # yield of background
  nVarBkg = 0 # variance of background
 
  l_bkg = []
  l_sig = []
  
  h_dat = 0
  N_dat = 0

  #==========================================================
  # loop through samples, fill histograms
  #==========================================================
  l_styles = [1, 1, 1, 2, 1, 1, 1, 1, 1]
  Nsignal_count = 0
  for samp in l_samp:
    if 'SR' in sig_reg and 'data' in samp and not unblind:
      continue
    #print( 'Processing {0}'.format(samp) )
    # obtain sample attributes 
    sample_type = d_samp[samp]['type']
    path        = d_samp[samp]['path']
  
    # Choose full path of sample by its type  
    full_path = ''
    if sample_type == 'sig':
      l_color     = d_samp[samp]['l_color']
      full_path = SIGPATH + '/' + path
      l_sig.append(samp)
    if sample_type == 'bkg':
      f_color     = d_samp[samp]['f_color']
      full_path = BKGPATH + '/' + path 
      l_bkg.append(samp)
    if sample_type == 'data':
      full_path = BKGPATH + '/' + path
    
    cutsAfter = normCutsAfter 

    # assign TFile to a dictionary entry
    d_files[samp] = TFile(full_path)

    weighted_lumi = str(lumi)
    if doBTagWeight:
      if '2b' in sig_reg:
        weighted_lumi = '{0} * h1_j1_BTagWeight * h1_j2_BTagWeight'.format(lumi)
      if '4b' in sig_reg:
        weighted_lumi = '{0} * h1_j1_BTagWeight * h1_j2_BTagWeight * h2_j1_BTagWeight * h2_j2_BTagWeight'.format(lumi)

    # obtain histogram from file and store to dictionary entry
    d_hists[samp] = tree_get_th1f( d_files[samp], samp, var, cutsAfter, hNbins, hXmin, hXmax, weighted_lumi, variable_bin, hXarray)

    # ---------------------------------------------------- 
    # Stacked histogram: construct and format
    # ---------------------------------------------------- 
    # extract key outputs of histogram 
    hist        = d_hists[samp][0]
    nYield      = d_hists[samp][1]
    h_intgl_low = d_hists[samp][2]
    h_intgl_upp = d_hists[samp][3]
    nYieldErr   = d_hists[samp][4]
    nRaw        = d_hists[samp][5]
    
    # samp : nYield number of events for each sample
    d_yield[samp]    = nYield
    d_nRaw[samp]     = nRaw
    d_yieldErr[samp] = nYieldErr
    # add background to stacked histograms
    if sample_type == 'bkg':
      hs.Add(hist)
      hs_intgl_low.Add(h_intgl_low)
      hs_intgl_upp.Add(h_intgl_upp)
      
      format_hist(hist, 1, 0, 1, f_color, 1001, 0)
      nTotBkg  += nYield
      nRawBkg  += nRaw
      nVarBkg  += nYieldErr ** 2
    
    if sample_type == 'sig':
      #format_hist(hist, 2, l_color, 2, f_color)
      format_hist(hist, 3, l_color, l_styles[Nsignal_count], f_color=0)
      Nsignal_count += 1
    
    if sample_type == 'data':
      h_dat = hist
      format_hist(h_dat,  1, kBlack, 1)
      N_dat = nYield

  errStatBkg = sqrt( nVarBkg ) # treat total statistical error as sum in quadrature of sample stat errors
  errTotBkg  = sqrt( errStatBkg**2 + (0.2 * nTotBkg) ** 2 )
  
  print('errStatBkg: {0:.3f}, sqrtB: {1:.3f}, errTotBkg: {2:.3f}'.format(errStatBkg, sqrt(nTotBkg), errTotBkg))

  print('==============================================')
  print('{0}, Data, {1}'.format(sig_reg, N_dat))
  print('----------------------------------------------')
  #print('{0}, Total bkg, {1:.3f} +/- {2:.3f}'.format(sig_reg, nTotBkg, errTotBkg))
  print('{0}, Total bkg, {1:.3f}, {2:.3f}'.format(sig_reg, nTotBkg, errTotBkg))
  print('----------------------------------------------')

  # legend for signals, data and total bkg yield
  #leg = mk_leg(0.42, 0.66, 0.63, 0.89, sig_reg, l_sampOther, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_nRaw, sampSet_type='bkg', txt_size=0.033)
  if legend_outside_plot:
    leg = mk_leg(0.64, 0.01, 0.88, 0.24, sig_reg, l_sampOther, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_nRaw, sampSet_type='bkg', txt_size=0.04)
  else:
    leg = mk_leg(0.65, 0.45, 0.92, 0.77, sig_reg, l_sampOther, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_nRaw, sampSet_type='bkg', txt_size=0.043)
  # legend with breakdown of background by sample
  d_bkg_leg = {}
  #l_bkg_leg = ['samp1', 'samp2', 'samp3']
  l_bkg_leg = ['samp1']
  if use_mc_fakes:
    l_bkg_leg.append('samp4')
  
  if legend_outside_plot:
    d_bkg_leg['samp1'] = mk_leg(0.64, 0.25, 0.88, 0.85, sig_reg, l_samp1, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_nRaw, sampSet_type='bkg', txt_size=0.04)
  else:
    d_bkg_leg['samp1'] = mk_leg(0.55, 0.73, 0.88, 0.85, sig_reg, l_samp1, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_nRaw, sampSet_type='bkg', txt_size=0.043)
  #d_bkg_leg['samp1'] = mk_leg(0.46, 0.70, 0.58, 0.93, sig_reg, l_samp1, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, sampSet_type='bkg', txt_size=0.030)
  #d_bkg_leg['samp2'] = mk_leg(0.59, 0.70, 0.71, 0.93, sig_reg, l_samp2, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, sampSet_type='bkg', txt_size=0.030)
  #d_bkg_leg['samp2'] = mk_leg(0.77, 0.68, 0.89, 0.93, sig_reg, l_samp2, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, sampSet_type='bkg', txt_size=0.029)
  #d_bkg_leg['samp3'] = mk_leg(0.78, 0.70, 0.88, 0.93, sig_reg, l_samp3, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, sampSet_type='bkg', txt_size=0.030)
  if use_mc_fakes:
    d_bkg_leg['samp4'] = mk_leg(0.86, 0.70, 0.90, 0.93, sig_reg, l_samp4, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_nRaw, sampSet_type='bkg', txt_size=0.030)
   
  print('==============================================')
 
  #============================================================
  # Now all background histogram and signals obtained
  # Proceed to make significance scan
  #============================================================
  # first evaluate the the signal to background ratio
  #pc_sigOverBkg = 100 * ( d_yield[signal_samp] / float( nTotBkg ) )
  #leg.AddEntry(0, 'Sig / Bkg = {0:.1f}%'.format(pc_sigOverBkg), '')
 
  # dicitonary for histograms and its significance plots
  # in format {samp_name : histogram}
  d_hsig = {}
  d_hsigZ20 = {}
  d_hsigZ05 = {}
  
  # obtain direction of cut  
  cut_dir = d_vars[var]['cut_dir'] 
  for samp in l_samp:
    sample_type = d_samp[samp]['type']
    if sample_type == 'sig':
      d_hsig[samp] = d_hists[samp][0]
 
  #============================================================
  # proceed to plot
  plot_selections(var, hs, d_hsig, h_dat, d_hsigZ05, d_hsigZ20, leg, l_bkg_leg, d_bkg_leg, lumi, save_name, sig_reg, nTotBkg, l_sig, cutsAfter, l_cuts, annotate_text, variable_bin, unblind, cutArrow, IsLogY)
  
  return nTotBkg

#____________________________________________________________________________
def plot_selections(var, h_bkg, d_hsig, h_dat, d_hsigZ05, d_hsigZ20, leg, l_bkg_leg, d_bkg_leg, lumi, save_name, sig_reg, nTotBkg, l_sig, cutsAfter, l_cuts, annotate_text, variable_bin, unblind=False, cutArrow=False, IsLogY=True):
  '''
  plots the variable var given input THStack h_bkg, one signal histogram and legend built
  makes a dat / bkg panel in lower part of figure
  to-do: should be able to read in a list of signals
  '''
  print('Proceeding to plot')
  
  # gPad left/right margins
  gpLeft = 0.14
  if legend_outside_plot:
    gpRight = 0.37
  else:
    gpRight = 0.05
  
  
  d_vars = configure_vars()
  
  #==========================================================
  # build canvas
  can  = TCanvas('','',1300,1000)
  customise_gPad()
  
  pad1 = TPad('pad1', '', 0.0, 0.0, 1.0, 1.0)
  #pad2 = TPad('pad2', '', 0.0, 0.00, 1.0, 0.4)
  pad1.Draw()
  pad1.cd()
  
  if IsLogY:
    pad1.SetLogy()
  customise_gPad(top=0.07, bot=0.22, left=gpLeft, right=gpRight)
  #customise_gPad(top=0.03, bot=0.20, left=gpLeft, right=gpRight)
  #=============================================================
  # draw and decorate
  # draw elements
  #h_bkg.Draw('hist')
  # draw signal samples
  print('--------------------------------------')
  print('Drawing histograms')
  print(d_hsig)
  for samp in l_sig:
    print('Drawing {0}'.format(samp))
    d_hsig[samp].Draw('hist same') #e2 = error coloured band
  # clone the total background histogram to draw the line
  
  leg.Draw('same')
  #==========================================================
  # calculate bin width 
  hNbins = d_vars[var]['hXNbins']
  hXmin  = d_vars[var]['hXmin']
  hXmax  = d_vars[var]['hXmax']
  if not variable_bin:
    binWidth = (hXmax - hXmin) / float(hNbins)
  
  # label axes of top pad
  xtitle = ''
  binUnits = d_vars[var]['units']
  if variable_bin:
    ytitle = 'Events / bin'
  elif 0.1 < binWidth < 1:
    ytitle = 'Events / {0:.2f} {1}'.format(binWidth, binUnits)
  elif binWidth <= 0.1:
    ytitle = 'Events / {0:.2f} {1}'.format(binWidth, binUnits)
  elif binWidth >= 1:
    if normalise_unity:
      #ytitle = 'Fraction of Events / {0:.0f} {1}'.format(binWidth, binUnits)
      ytitle = 'Fraction of Events'.format(binWidth, binUnits)
    else:
      ytitle = 'Events / {0:.0f} {1}'.format(binWidth, binUnits)
  enlargeYaxis = False
  #if 'Pass' in sig_reg or 'preselect':
  if 'Pass' in sig_reg or 'preselect' in sig_reg:
    enlargeYaxis = False
  
  
  varTeX = 'tlatex'
  
  Xunits = d_vars[var]['units']
  if Xunits == '':
    #xtitle = '{0}'.format( d_vars[var]['tlatex'])
    xtitle = '{0}'.format( d_vars[var][varTeX])
  else:
    xtitle = '{0} [{1}]'.format( d_vars[var][varTeX], Xunits ) 
  
  customise_axes(d_hsig[l_sig[0]], xtitle, ytitle, 2.8, IsLogY, enlargeYaxis)
  
  #==========================================================
  # arrow to indicate where cut is
  # Case 2-sided cuts
  
  # set height of arrow
  ymin_Ar = gPad.GetUymin()
  ymax_Ar = h_bkg.GetMaximum()
  if IsLogY:
    ymax_Ar = 80
  if not IsLogY:
    ymax_Ar = 0.8*ymax_Ar
  # arrow width is 5% of the maximum x-axis bin 
  arr_width = hXmax * 0.06
  if 'cut_pos2' in d_vars[var].keys():
    cut_pos2 = d_vars[var]['cut_pos2']
    cut_dir2 = d_vars[var]['cut_dir2']
    cutAr2   = cut_arrow(cut_pos2, ymin_Ar, cut_pos2, ymax_Ar, cut_dir2, 0.012, arr_width)
    if cutArrow:
      cutAr2[0].Draw()
      cutAr2[1].Draw()
  # otherwise 1-sided cut 
  cut_pos = d_vars[var]['cut_pos']
  cut_dir = d_vars[var]['cut_dir']
  cutAr = cut_arrow(cut_pos, ymin_Ar, cut_pos, ymax_Ar, cut_dir, 0.012, arr_width)
  if cutArrow:
    cutAr[0].Draw()
    cutAr[1].Draw()

  # replace -mm with mu mu
  if '-ee' in sig_reg:
    sig_reg = sig_reg.replace('-ee', ' ee', 1)
  if '-mm' in sig_reg:
    sig_reg = sig_reg.replace('-mm', ' #mu#mu', 1)
  if '-em' in sig_reg:
    sig_reg = sig_reg.replace('-em', ' e#mu', 1)
  if '-me' in sig_reg:
    sig_reg = sig_reg.replace('-me', ' #mue', 1)
  if '-ee-me' in sig_reg:
    sig_reg = sig_reg.replace('-ee-me', ' ee+#mue', 1)
  if '-mm-em' in sig_reg:
    sig_reg = sig_reg.replace('-mm-em', ' #mu#mu+e#mu', 1)

  if '-SF' in sig_reg:
    sig_reg = sig_reg.replace('-SF', ' ee+#mu#mu', 1)
  if '-DF' in sig_reg:
    sig_reg = sig_reg.replace('-DF', ' e#mu+#mue', 1)
  if '-AF' in sig_reg:
    sig_reg = sig_reg.replace('-AF', ' ee+#mu#mu+e#mu+#mue', 1)
  
  #==========================================================
  # Text for ATLAS, energy, lumi, region, ntuple status
  if legend_outside_plot:
    myText(0.70, 0.86, 'Sample (Weighted, Fraction, Raw) ', 0.043)
  else:
    pass
    #myText(0.54, 0.86, 'Sample (Weighted, Fraction, Raw) ', 0.043)
  
  #myText(0.17, 0.95, 'MadGraph5 2.6.2 + Pythia 8.230 + Delphes 3.4.1 (LO xsec, NLOPDF), ' + NTUP_status, text_size*0.6, kGray+1)
  #myText(0.21, 0.85, GROUP_status, text_size, kBlack)
  #myText(0.29, 0.85, '{0}, {1}'.format(ENERGY_status, lumi) + ' fb^{#minus1}', text_size, kBlack) 
  myText(0.39, 0.85, 'pp #rightarrow hh, #kappa(#it{y}_{top}) = 1, #sqrt{s} = ' + '{0}'.format(ENERGY_status), text_size, kBlack) 
  myText(0.39, 0.79, 'Reconstructed level, preselection', text_size, kBlack) 
  #myText(0.21, 0.80, sig_reg, text_size, kBlack) 
  #myText(0.22, 0.75, 'Pileup 0 ', text_size*0.7, kGray+1) 

  if doBTagWeight:
    if '2b' in sig_reg:
      l_2b = ['h1_j1_BTagWeight',
              'h1_j2_BTagWeight' ]
      l_cuts += l_2b
   
    if '4b' in sig_reg: 
      l_4b = ['h1_j1_BTagWeight',
              'h1_j2_BTagWeight',
              'h2_j1_BTagWeight',
              'h2_j2_BTagWeight' ]
      l_cuts += l_4b

  '''
  # print cuts for reference
  for it, cut in enumerate( l_cuts ):
    myText(0.43, 0.85-float(it)/35, cut, text_size*0.8, kBlack)

  if not annotate_text == '':
    myText(0.22, 0.69, annotate_text, text_size*0.6, kGray+1) 
  '''

  gPad.RedrawAxis() 


  #==========================================================
  # save everything
  can.cd()
  can.SaveAs(save_name + '.pdf')
  #can.SaveAs(save_name + '.eps')
  #can.SaveAs(save_name + '.png')
  can.Close()

  
#____________________________________________________________________________
def draw_sig_scan(l_signals, d_hsigZ, cut_dir, xtitle, hXmin, hXmax):
  '''
  Draw significance scan 
  for signals in list l_signals
  using significance histograms d_hsigZ
  labelled by cut_dir, xtitle
  in range hXmin, hXmax
  '''
  print('Making significance scan plot in lower panel')
  #----------------------------------------------------
  # draw significances
  d_samp = configure_samples()
  ytitle = 'Significance Z'
  ytitle = 'S/#sqrt{B+(5%B)^{2}}'
  for i, samp in enumerate(l_signals):
    hsigZ = d_hsigZ[samp]
    hsigZ.Draw('hist same')
    if i < 1:
      customise_axes(hsigZ, xtitle, ytitle, 1.2)
    l_color     = d_samp[samp]['l_color'] 
    format_hist(hsigZ, 2, l_color, 1, 0)
  
  # draw line for the ratio = 1
  l = draw_line(hXmin, 1.97, hXmax, 1.97, color=kAzure+1, style=7) 
  l.Draw()
  if 'left' in cut_dir:
    myText(0.67, 0.83, 'Select left',  0.07, kBlack)
  if 'right' in cut_dir:
    myText(0.67, 0.83, 'Select right', 0.07, kBlack)

#____________________________________________________________________________
def mk_sigZ_plot(h_intgl_sig, h_intgl_bkg, pc_syst, Nbins=100, xmin=0, xmax=100):
  '''
  Takes background & signal one-sided integral histograms
  and input percentage systematic
  Returns the signal significance Z histogram
  '''
  print('Making significance plot')
  h_pcsyst = TH1D('', "", Nbins, xmin, xmax)
  h_05syst = TH1D('', "", Nbins, xmin, xmax)
  h_20syst = TH1D('', "", Nbins, xmin, xmax)
  for my_bin in range( h_intgl_bkg.GetStack().Last().GetSize() ): 
    sExp     = h_intgl_sig.GetBinContent(my_bin)
    bExp     = h_intgl_bkg.GetStack().Last().GetBinContent(my_bin)  
    bin_low  = h_intgl_bkg.GetStack().Last().GetBinLowEdge( my_bin )
   
    # Case pathology 
    # Set significance is 0 if bExp or sExp is below 0
    if bExp <= 0:
      RS_sigZ = 0
    if sExp <= 0:
      RS_sigZ = 0
    if bExp > 0 and sExp > 0:
      
      # add statistical and systematic uncertainties in quadrature
      BUnc   = sqrt ( abs( bExp + ( ( pc_syst / float(100) ) * bExp ) ** 2 ) )
      sigZ   = sExp / float(BUnc)
      h_pcsyst.Fill(bin_low, sigZ)
      #RS_sigZ = RooStats.NumberCountingUtils.BinomialExpZ( sExp, bExp, BUnc/float(bExp) )
      #h_pcsyst.Fill(bin_low, RS_sigZ)
      
      #print('{0}, {1}, {2}, {3}, {4}, {5}'.format(my_bin, bin_low, bExp, sExp, my_sigZ, RS_sigZ) )
      #BUnc05 = sqrt ( abs( bExp + ( 0.05 * bExp ) ** 2 ) )
      #BUnc20 = sqrt ( abs( bExp + ( 0.20 * bExp ) ** 2 ) )
      # calculate my significance
      #my_sigZ = sExp / float( BUnc )
   
  return h_pcsyst
    
#____________________________________________________________________________
def mk_mcErr(hStack, pc_sys, Nbins=100, xmin=0, xmax=100, variable_bin=False, hXarray=0):
  '''
  smear stacked MC histogram with 'Gaussian' sqrt(N) to emulate stats 
  also add a pc systematic
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
    # ============================================================ 
    # SERIOUS ISSUE: NEED TO INVESTIGATE!
    # why are there negative histogram values? something flawed going on
    # for now, take mean of adjacent bin y-values to disguise anomaly
    if yval < 0:
      yval = 0.001
      print( '\nSERIOUS WARNING: negative histogram value {0} in bin {1}'.format(yval, my_bin) )
      print( 'Please investigate. For now setting value to mean of neighbouring bins.\n' )
      #yMinus1 = hStack.GetStack().Last().GetBinContent(my_bin - 1)
      #yPlus1  = hStack.GetStack().Last().GetBinContent(my_bin + 1)
      #yval = (yPlus1 + yMinus1) / float(2)
    # ============================================================ 
  
    # get statistical variance as sum of weights squared
    yval_GetErr   = hStack.GetStack().Last().GetBinError(my_bin)
    # add stat and sys err in quadrature
    yval_err = sqrt( yval_GetErr ** 2 + ( 0.01 * pc_sys * yval ) ** 2 )
    h_mcErr.SetBinContent( my_bin, yval )
    h_mcErr.SetBinError(   my_bin, yval_err ) 
  
  return h_mcErr
   
#_______________________________________________________
def tree_get_th1f(f, hname, var, cutsAfter='', Nbins=100, xmin=0, xmax=100, lumifb=35, variable_bin=False, hXarray=0):
  '''
  from a TTree, project a leaf 'var' and return a TH1F
  '''
  print(hname)
  if variable_bin:
    h_AfterCut   = TH1D(hname + '_hist', "", Nbins, array('d', hXarray) )
  else:
    h_AfterCut   = TH1D(hname + '_hist', "", Nbins, xmin, xmax)
 
  #h_AfterCut.Sumw2()
 
  # MadGraph LO cross-sections in pb
  d_xsec = {
    'pp2hh_loop_sm' : 1.60835E-02,
    'pp2hh_TopYuk_1.0_SlfCoup_1.0' : 1.60835E-02,
    'pp2hh_TopYuk_1.0_SlfCoup_2.0' : 3.68395E-02,
    'pp2hh_TopYuk_1.0_SlfCoup_5.0' : 3.68395E-02,
    'pp2hh_TopYuk_1.0_SlfCoup_m5.0' : 2.58555E-01,
    'bbh'        : 7.6E-02,
    'tth'        : 4.35E-01,
    'zh'         : 7.19E-01,
    'wh'         : 1.36,
    'pp2ttbar'   : 597.,
    'ttbar'      : 597.,
    'pp2bbbb'    : 8.9e+05,
    'pp2bbjj'    : 7.2e+06,
    'pp2jjjj'    : 1.8e+07,
    '4b_20_to_200'       : 63.2,
    '4b_200_to_500'      : 2.82,
    '4b_500_to_1000'     : 4.08E-02,
    '4b_1000_to_infty'   : 5.50E-04,
    '2b2j_20_to_200'     : 2.26E+04,
    '2b2j_200_to_500'    : 1.54E+03,
    '2b2j_500_to_1000'   : 35.26,
    '2b2j_1000_to_infty' : 0.706,
  }
  
  lumi     = '({0}) * (10 ** 3)'.format(lumifb) # convert to [pb^{-1}]
  xsec = 1.
  #xsec = d_xsec[hname]
  if 'pp2hh' in hname:
    my_weight = 1000.
  else:
    my_weight = 1.
  
  t = f.Get( 'preselection') 
  Ngen = f.intermediate_cutflow.GetBinContent(1)
  print('Ngen: {0}'.format(Ngen))
   
  cut_after = '({0}) * ({1}) * ({2}) * ({3}) / ({4})'.format(cutsAfter, xsec, lumi, my_weight, float(Ngen)) 
  #cut_after = '( ({0}) * ({1}) ) * Event.Weight * {2}'.format(cutsAfter, lumi, my_weight) 
  # ========================================================= 
  t.Project( hname + '_hist', var, cut_after )
  # =========================================================
  # perform integrals to find 
  # total yield, one-sided lower and upper cumulative histos
  nYieldErr = ROOT.Double(0)
  nYield    = h_AfterCut.IntegralAndError(0, Nbins+1, nYieldErr)
  nRaw      = h_AfterCut.GetEntries()
  h_intgl_lower = TH1D(hname + '_intgl_lower', "", Nbins, xmin, xmax)
  h_intgl_upper = TH1D(hname + '_intgl_upper', "", Nbins, xmin, xmax)
 
  if normalise_unity:
    h_AfterCut.Scale(1./nYield)
  
  print('---------------------------------------------')
  print('N generated events: {0}'.format(Ngen) )
  print('N raw events after cuts: {0}'.format(nRaw) )
  print('Weighted cutstring: {0}'.format(cut_after) )
  print('---------------------------------------------')
  
  for my_bin in range( h_AfterCut.GetXaxis().GetNbins() + 1 ):
    
    # get lower edge of bin
    bin_low = h_AfterCut.GetXaxis().GetBinLowEdge( my_bin )
    
    # set the negatively weighted values to 0.
    bin_val = h_AfterCut.GetBinContent( my_bin )
    if bin_val < 0:
      print( 'WARNING: Bin {0} of sample {1} has negative entry, setting central value to 0.'.format(my_bin, hname) )
      h_AfterCut.SetBinContent(my_bin, 0.)
    
    # do one-sided integral either side of bin
    intgl_lower = h_AfterCut.Integral( 0, my_bin ) 
    intgl_upper = h_AfterCut.Integral( my_bin, Nbins+1 ) 
    
    h_intgl_lower.Fill( bin_low, intgl_lower )
    h_intgl_upper.Fill( bin_low, intgl_upper )
  print( 'Sample {0} has integral {1:.3f} +/- {2:.3f} (raw {3})'.format( hname, nYield, nYieldErr, nRaw ) )

  # =========================================================
  
  return [h_AfterCut, nYield, h_intgl_lower, h_intgl_upper, nYieldErr, nRaw]

#____________________________________________________________________________
def format_hist(hist, l_width=2, l_color=kBlue+2, l_style=1, f_color=0, f_style=1001, l_alpha=1.0):
  
  # lines
  hist.SetLineColorAlpha(l_color, l_alpha)
  hist.SetLineStyle(l_style)
  hist.SetLineWidth(l_width)
  
  # fills
  hist.SetFillColor(f_color)
  hist.SetFillStyle(f_style)
  # markers
  hist.SetMarkerColor(l_color)
  hist.SetMarkerSize(1.1)
  hist.SetMarkerStyle(20)

#____________________________________________________________________________
def customise_gPad(top=0.03, bot=0.15, left=0.17, right=0.08):
  gPad.Update()
  gStyle.SetTitleFontSize(0.0)
  
  # gPad margins
  gPad.SetTopMargin(top)
  gPad.SetBottomMargin(bot)
  gPad.SetLeftMargin(left)
  gPad.SetRightMargin(right)
  
  gStyle.SetOptStat(0) # hide usual stats box 
  
  gPad.Update()
  
#____________________________________________________________________________
def customise_axes(hist, xtitle, ytitle, scaleFactor=1.1, IsLogY=False, enlargeYaxis=False):
  # set a universal text size
  #text_size = 0.055
  text_size = 55
  TGaxis.SetMaxDigits(4) 
  ##################################
  # X axis
  xax = hist.GetXaxis()
  xax.CenterTitle() 
  
  # precision 3 Helvetica (specify label size in pixels)
  xax.SetLabelFont(133)
  xax.SetTitleFont(133)
  #xax.SetTitleFont(13) # times
 
  print('xtitle: ' + xtitle) 
  xax.SetTitle(xtitle)
  xax.SetTitleSize(text_size*1.2)
  # top panel
  '''
  #if xtitle == '':
  if 'Events' in ytitle:
  #if False:
    xax.SetLabelSize(0)
    xax.SetLabelOffset(0.02)
    xax.SetTitleOffset(2.0)
    xax.SetTickSize(0.04)  
  # bottom panel
  else:
  '''
  xax.SetLabelSize(text_size)
  xax.SetLabelOffset(0.03)
  xax.SetTitleOffset(1.5)
  xax.SetTickSize(0.04)

  #xax.SetRangeUser(0,2000) 
  xax.SetNdivisions(4) 
  gPad.SetTickx() 
  
  ##################################
  # Y axis
  yax = hist.GetYaxis()
  # precision 3 Helvetica (specify label size in pixels)
  yax.SetLabelFont(133)
  yax.SetTitleFont(133)
  yax.CenterTitle() 
 
  
  yax.SetTitle(ytitle)
  yax.SetTitleSize(text_size*1.2)
  yax.SetTitleOffset(1.0)    
  
  yax.SetLabelOffset(0.015)
  yax.SetLabelSize(text_size - 7)
 
  ymax = hist.GetMaximum()
  ymin = hist.GetMinimum()
  
  # top events panel
  #if xtitle == '':
  if 'Events' in ytitle:
    yax.SetNdivisions(505) 
    if IsLogY:
      if enlargeYaxis:
        ymax = 2 * 10 ** 10
        ymin = 20
      else:
        ymax = 3 * 10 ** 8
        ymin = 0.05
        #ymax = 3 * 10 ** 3
        #ymin = 0.0005
      hist.SetMaximum(ymax)
      hist.SetMinimum(ymin)
    else:
      if normalise_unity:
        hist.SetMaximum(ymax*1.1)
      else:
        hist.SetMaximum(ymax*scaleFactor)
      #hist.SetMaximum(100)
      #hist.SetMaximum(30)
      #hist.SetMaximum(60)
      hist.SetMinimum(0.0)
  # bottom data/pred panel 
  elif 'Significance' in ytitle or 'sqrt' in ytitle:
    hist.SetMinimum(0.0)
    hist.SetMaximum(4.5) 
    yax.SetNdivisions(205)
  elif 'Data' in ytitle:
    hist.SetMinimum(0.0)
    hist.SetMaximum(2.0) 
    yax.SetNdivisions(205)
   
  gPad.SetTicky()
  gPad.Update()


#____________________________________________________________________________
def myText(x, y, text, tsize=0.05, color=kBlack, angle=0) :
  
  l = TLatex()
  l.SetTextSize(tsize)
  l.SetTextFont(132)
  l.SetNDC()
  l.SetTextColor(color)
  l.SetTextAngle(angle)
  l.DrawLatex(x,y, text)

#____________________________________________________________________________
def cut_arrow(x1, y1, x2, y2, direction='right', ar_size=1.0, ar_width=10, color=kGray+3, style=1) :
  
  l = TLine(x1, y1, x2, y2)
  if direction == 'right':
    ar = TArrow(x1-0.02, y2, x1+ar_width, y2, ar_size, '|>')
  if direction == 'left':
    ar = TArrow(x1-ar_width+0.02, y2, x1, y2, ar_size, '<|')
  if direction == 'up':
    ar = TArrow(x1, y1, x1, y2, ar_size, '|>')
  if direction == 'down':
    ar = TArrow(x1, y1, x1, y2, ar_size, '<|')
  l.SetLineWidth(4)
  l.SetLineStyle(style)
  l.SetLineColor(color) 
  ar.SetLineWidth(4)
  ar.SetLineStyle(style)
  ar.SetLineColor(color) 
  ar.SetFillColor(color)  
  return [l, ar]

#____________________________________________________________________________
def mk_leg(xmin, ymin, xmax, ymax, sig_reg, l_samp, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_nRaw, sampSet_type='bkg', txt_size=0.05) :
  '''
  @l_samp : Constructs legend based on list of samples 
  @nTotBkg : Total background events
  @d_hists : The dictionary of histograms 
  @d_samp : May from samples to legend text
  @d_yields : The dictionary of yields 
  @d_yieldErr : Dictionary of errors on the yields
  @sampSet_type : The type of samples in the set of samples in the list 
  '''  

  # ---------------------------------------------------- 
  # Legend: construct and format
  # ---------------------------------------------------- 
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetBorderSize(0)
  leg.SetTextSize(txt_size)
  leg.SetTextFont(132)
  leg.SetNColumns(1)

  # legend markers 
  d_legMk = {
    'bkg'  : 'f',
    'sig'  : 'l',
    'data' : 'ep'
    }

  # Need to reverse background order so legend is filled as histogram is stacked
  if sampSet_type == 'bkg':
    l_samp = [x for x in reversed(l_samp)]
  for samp in l_samp: 
    #print( 'Processing {0}'.format(samp) )
    # obtain sample attributes 
    hist        = d_hists[samp][0]
    sample_type = d_samp[samp]['type']
    leg_entry   = d_samp[samp]['leg']
    legMk       = d_legMk[sample_type]
   
    #print('samp: {0}, type: {1}, legMk: {2}'.format(samp, sample_type, legMk) ) 
    # calculate the % of each background component and put in legend
    pc_yield   = 0
    if sample_type == 'bkg':
      pc_yield = 100 * ( d_yield[samp] / float(nTotBkg) )
      leg_txt = '{0} ({1:.3g}, {2:.1f}%, {3:.0f})'.format( leg_entry, d_yield[samp], pc_yield, d_nRaw[samp] )
    if sample_type == 'sig':
      #leg_txt = '{0} ({1:.3g}, {2:.0f})'.format(leg_entry, d_yield[samp], d_nRaw[samp])
      leg_txt = leg_entry#, d_yield[samp], d_nRaw[samp])

    if sample_type == 'data':
      leg_txt = '{0} ({1:.0f} Events)'.format(leg_entry, d_yield['data'])  
    leg.AddEntry(hist, leg_txt, legMk)
    #print('{0}, {1}, {2:.3f}, {3:.3f}%'.format(sig_reg, samp, d_yield[samp], pc_yield) )
    print('{0}, {1}, {2:.3f} +/- {3:.3f}, {4:.0f}'.format(sig_reg, samp, d_yield[samp], d_yieldErr[samp], d_nRaw[samp]) )
  
  return leg

#____________________________________________________________________________
def draw_line(xmin, ymin, xmax, ymax, color=kGray+1, style=2) :
  
  # draw line of kinematically forbidden region
  line = TLine(xmin , ymin , xmax, ymax)
  line.SetLineWidth(2)
  line.SetLineStyle(style)
  line.SetLineColor(color) # 12 = gray
  return line
 
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


