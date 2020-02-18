#!/usr/bin/env python
'''
plot_signalOnly.py is the main script to do the plotting
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

import os, sys, time, argparse, time
from math import sqrt
from random import gauss
from array import array

from samples import *
from cuts import *
from variables import *

SIGPATH = '/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/merged_nn_score_ntuples'

doBTagWeight = True

normalise_unity = True

# text size as percentage
text_size = 0.05

#____________________________________________________________________________
def main():
  
  t0 = time.time()
  
  #================================================
  # default values
  sig_reg = 'SR-preselect'
  var     = 'Jet[0].PT'

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
  parser.add_argument('-n', '--noLogY',  action='store_true', help='Do not draw log Y axis.')
 
  args = parser.parse_args()
  if args.variable:
    var      = args.variable
  if args.sigReg:
    sig_reg = args.sigReg
  if args.noLogY:
    IsLogY = False

  print( '=========================================' )
  print( 'Plotting variable: {0}'.format(var) )
  print( 'Selection region: {0}'.format(sig_reg) )
  print( 'Normalising luminosity: {0}'.format(lumi) )
  print( '=========================================\n' )
  
  #================================================
  # make (relative) save directory if needed 
  savedir = 'figs/2019mar18'
  mkdir(savedir)

  l_SRs = [
    'all-preselection'
    ]
  l_vars = [
  # 'n_large_jets',
   'm_hh'
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

  l_samp = [
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0',
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m2.0',
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m1.0',
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0',
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0',
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_3.0',
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0',
    #'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0',
  ]

  # obtain cut to apply (string)
  normCutsAfter, l_cuts = configure_cuts(sig_reg) 
  
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
  d_hsig  = {}
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
  myLightBlue     = TColor.GetColor('#9ecae1')
  myMediumBlue    = TColor.GetColor('#0868ac')
  myDarkBlue      = TColor.GetColor('#08306b')
  
  myMediumOrange  = TColor.GetColor('#feb24c')
  myDarkOrange    = TColor.GetColor('#ec7014')
  myDarkerOrange  = TColor.GetColor('#cc4c02')
  
  l_styles = [1, 1, 1, 2, 1, 1, 1]
  l_colors = [myDarkBlue, myMediumBlue, myLightBlue, kGray+1, myMediumOrange, myDarkOrange, myDarkerOrange]
  Nsignal_count = 0
  for count, samp in enumerate(l_samp):
    print('Processing sample: {0}'.format(samp))
    full_path = SIGPATH + '/' + samp + '.root'
    
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
    d_hsig[samp]     = hist
    d_nRaw[samp]     = nRaw
    d_yieldErr[samp] = nYieldErr
    # add background to stacked histograms
    format_hist(hist, 3, l_colors[count], l_styles[count], f_color=0)
    Nsignal_count += 1
    l_sig.append(samp) 
  leg = mk_leg(0.72, 0.45, 0.92, 0.85, sig_reg, l_samp, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_nRaw, sampSet_type='bkg', txt_size=0.05)
   
  #============================================================
  # proceed to plot
  plot_selections(var, d_hsig, leg, save_name, sig_reg, nTotBkg, l_sig, cutsAfter, l_cuts, annotate_text, variable_bin, IsLogY)
  
  return nTotBkg

#____________________________________________________________________________
def plot_selections(var, d_hsig, leg, save_name, sig_reg, nTotBkg, l_sig, cutsAfter, l_cuts, annotate_text, variable_bin, IsLogY=True):
  '''
  plots the variable var given input THStack h_bkg, one signal histogram and legend built
  makes a dat / bkg panel in lower part of figure
  to-do: should be able to read in a list of signals
  '''
  print('Proceeding to plot')
  
  # gPad left/right margins
  gpLeft = 0.14
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
  
  customise_axes(d_hsig[l_sig[0]], xtitle, ytitle, 1.6, IsLogY, enlargeYaxis)
  
  myText(0.19, 0.84, 'pp #rightarrow hh, #kappa_{#it{t}} = 1, #sqrt{s} = 14 TeV', text_size, kBlack) 
  myText(0.19, 0.77, 'Reconstructed level, preselection', text_size, kBlack) 
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

  gPad.RedrawAxis() 

  #==========================================================
  # save everything
  can.cd()
  can.SaveAs(save_name + '.pdf')
  #can.SaveAs(save_name + '.eps')
  #can.SaveAs(save_name + '.png')
  can.Close()
  
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
  Ngen = f.loose_cutflow.GetBinContent(1)
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
  xax.SetLabelSize(text_size)
  xax.SetLabelOffset(0.03)
  xax.SetTitleOffset(1.5)
  xax.SetTickSize(0.04)

  #xax.SetRangeUser(0,2000) 
  #xax.SetNdivisions(5) 
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
        hist.SetMaximum(ymax*scaleFactor)
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


