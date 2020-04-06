#!/usr/bin/env python
'''
Welcome to plot_lhe.py
This makes Fig 3 of the paper. 

Plots a signal for multiple selections and signals
Choice between displaying histograms normalised to cross-section or unnormalised

'''

# So Root ignores command line inputs so we can use argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os, datetime
from ROOT import *
from variables import *
from math      import sqrt

TOPPATH = '/home/jesseliu/pheno/fcc/PhenoSim/analyse/conventional/hh4b/lhe_analyse/ntuples'

normalise_unity = True
fix_TOPYUK = True
fix_SLFCOUP = False

# Blues
myLighterBlue   = TColor.GetColor('#deebf7')
myLightBlue     = TColor.GetColor('#9ecae1')
myMediumBlue    = TColor.GetColor('#4292c6')
myDarkBlue      = TColor.GetColor('#08519c')
myDarkerBlue    = TColor.GetColor('#08306b')

# Greens
myLightGreen    = TColor.GetColor('#c7e9c0')
myMediumGreen   = TColor.GetColor('#41ab5d')
myDarkGreen     = TColor.GetColor('#006d2c')

# Oranges
myLighterOrange = TColor.GetColor('#ffeda0')
myLightOrange   = TColor.GetColor('#fec49f')
myMediumOrange  = TColor.GetColor('#fe9929')
myDarkOrange    = TColor.GetColor('#ec7014')
myDarkerOrange  = TColor.GetColor('#cc4c02')

# Greys
myLightestGrey  = TColor.GetColor('#f0f0f0')
myLighterGrey   = TColor.GetColor('#e3e3e3')
myLightGrey     = TColor.GetColor('#969696')

# Pinks
myLightPink     = TColor.GetColor('#fde0dd')
myMediumPink    = TColor.GetColor('#fcc5c0')
myDarkPink      = TColor.GetColor('#dd3497')

# Purples
myLightPurple   = TColor.GetColor('#dadaeb')
myMediumPurple  = TColor.GetColor('#9e9ac8')
myDarkPurple    = TColor.GetColor('#6a51a3')

#____________________________________________________________________________
def main():

  mkdir('plots')

  # --------------
  # User inputs
  # --------------

  l_vars = [
    'h1_Pt',
    #'Higgs2Pt',
    #'DiHiggsDeltaEta',
    'm_hh',
    ]

  # Category 1: Low mass splitting optimised for splitting of 0 - 60 GeV
  unweighted_cuts = '(m_hh > 0.)'
  pc_sys = 0.2 # percentage systematic 

  normalise = True # normalise to cross-section or plot unnormalised events
  lumi      = 100.0 # inverse fb
  weights   = 1.0 # Not including photon or lepton efficiencies, optimising using 'best case scenario'
  raw_bkg   = 50000 # raw background events
  raw_sig   = 100000 # raw signal events

  filename_bkg = 'aa2WW_lvlv'
 
  if fix_TOPYUK:
 
    l_filename_sigs = [
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_m5.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_m2.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_m0.5',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_5.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_7.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_10.0',
    ] 
    
    l_filename_sigs = [
      #'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_0.5',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_1.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_2.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_2.5',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_3.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_4.0',
    ] 
  elif fix_SLFCOUP: 
    l_filename_sigs = [
    
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_0.5_SlfCoup_1.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_0.8_SlfCoup_1.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_1.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.2_SlfCoup_1.0',
      'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.5_SlfCoup_1.0',
    
      #'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_0.5_SlfCoup_m1.0',
      #'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_m1.0',
      #'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.5_SlfCoup_m1.0',
    ]

  # sample colors - Only small selection of representative samples listed here, add more if needed 
  d_sampcolor = {
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_0.5_SlfCoup_m1.0' : myDarkBlue, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_m1.0' : myMediumOrange, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.5_SlfCoup_m1.0' : myLightBlue, 
    
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_0.5_SlfCoup_1.0' : myDarkerOrange, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_0.8_SlfCoup_1.0' : myMediumOrange, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_1.0' : myLightBlue, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.2_SlfCoup_1.0' : myMediumBlue, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.5_SlfCoup_1.0' : myDarkerBlue, 
    
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_m5.0' : myDarkPurple, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_m2.0' : myDarkerOrange, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_m0.5' : myMediumOrange, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_5.0'  : myLightBlue, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_7.0'  : myMediumBlue, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_10.0' : myDarkerBlue, 
    
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_0.5'  : myDarkPurple, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_1.0'  : myDarkerOrange, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_2.0'  : myMediumOrange, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_2.5'  : myLightBlue, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_3.0'  : myMediumBlue, 
    'MG5_LHEonly_14TeV_pp2hh_HeavyHiggsTHDM_TopYuk_1.0_SlfCoup_4.0'  : myDarkerBlue, 
    
   }

  # --------------
  # Get background & signal files and make histograms 
  # --------------

  # Initialise objects to fill in loop 
  d_hists    = {} # Dictionary of histograms 
  d_hists_sb = {} # Dictionary of SoverSqrtBSyst histograms
  d_files = {}

  # --------------
  # LOOP over list of variables l_var
  # --------------

  for var in l_vars:
    # Get dictionary of histogram configurations from variables.py
    d_vars  = configure_vars()
  
    hXNbins = d_vars[var]['hXNbins']
    hXmin   = d_vars[var]['hXmin']
    hXmax   = d_vars[var]['hXmax']
    cut_dir = d_vars[var]['cut_dir'] 
  
    # SIGNALS # 
    for samp in l_filename_sigs: 
      # Get bkg TFile and cross-section from dictionary
      sig_path = TOPPATH + '/' + samp + '.root'
      sig_file = TFile(sig_path)

      xsec_sig = 1.0

      # assign TFile to a dictionary entry
      d_files[samp] = TFile(sig_path)
 
      # Get TH1F histogram from the TTree in the TFile and store to dictionary entry
      d_hists[samp] = tree_get_th1f(d_files[samp], samp, var, unweighted_cuts, hXNbins, hXmin, hXmax, lumi, weights, normalise, xsec_sig, raw_sig  )
   
    # --------------
    # Plot
    # --------------
    if normalise:
      if fix_TOPYUK:
        save_name = './plots/Norm_'+var+'_varySlfCoup'
      elif fix_SLFCOUP:
        save_name = './plots/Norm_'+var+'_varyTopYuk'
      else:
        save_name = './plots/Norm_'+var

    else:
      save_name = './plots/NonNorm_'+var
    plot_selections(var, d_hists, l_filename_sigs, d_sampcolor, lumi, save_name, pc_sys)

#-------------------------------------------------------
# Functions
#-------------------------------------------------------

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

#____________________________________________________________________________
def draw_line(xmin, ymin, xmax, ymax, color=kGray+1, style=2) :

  # Function to draws lines given locations @xmin, ymin, xmax, ymax

  line = TLine(xmin , ymin , xmax, ymax)
  line.SetLineWidth(2)
  line.SetLineStyle(style)
  line.SetLineColor(color) # 12 = gray
  return line
 
#____________________________________________________________________________
def plot_selections(var, d_hists, l_filename_sigs, d_sampcolor, lumi, save_name, pc_sys, IsLogY=False):
  '''
  plots the variable var given input dictionary containing bkg and signal histograms
  makes a S/sqrt(B) with sytematic panel in lower part of figure from dictionary containing SoverSqrtBSyst histograms
  '''
  print('Proceeding to plot')
  
  # gPad left/right margins
  gpLeft = 0.21
  gpRight = 0.05
  can  = TCanvas('','',1000,800)
  
  #==========================================================
  # Build canvas   
  
  customise_gPad(top=0.06, bot=0.19, left=gpLeft, right=gpRight)
  if IsLogY: pad1.SetLogy()
  
  #=============================================================
  # draw and decorate

  # construct legend
  xl1, yl1 = 0.45, 0.48
  xl2, yl2 = xl1+0.25, yl1+0.28
  leg = TLegend(xl1,yl1,xl2,yl2)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0) # transparent
  leg.SetTextSize(0.055)
  leg.SetTextFont(132)

  # calculate bin width 
  d_vars = configure_vars()

  hNbins = d_vars[var]['hXNbins']
  hXmin  = d_vars[var]['hXmin']
  hXmax  = d_vars[var]['hXmax']
  binWidth = (hXmax - hXmin) / float(hNbins)
  
  # label axes of top pad
  varTeX = 'tlatex'
  
  Xunits = d_vars[var]['units']
  if Xunits == '':
    #xtitle = '{0}'.format( d_vars[var]['tlatex'])
    xtitle = '{0}'.format( d_vars[var][varTeX])
  else:
    xtitle = '{0} [{1}]'.format( d_vars[var][varTeX], Xunits ) 
  
  binUnits = d_vars[var]['units']
  if 0.1 < binWidth < 1:
    ytitle = 'Fraction of Events / {0:.2f} {1}'.format(binWidth, binUnits)
  elif binWidth <= 0.1:
    ytitle = 'Fraction of Events / {0:.2f} {1}'.format(binWidth, binUnits)
  elif binWidth >= 1:
    ytitle = 'Fraction of Events / {0:.0f} {1}'.format(binWidth, binUnits)
  enlargeYaxis = False
  
  #h_sig = d_hists[l_filename_sigs[0]][0]
  #h_sig.Draw('hist')

  # loop over and draw signal samples 
  for i, samp in enumerate(l_filename_sigs):
    print('Drawing {0}'.format(samp))
    h_sig = d_hists[samp][0]
    #print d_hists
    h_sig.Draw('hist same') 
    if i==0: 
      customise_axes(h_sig, xtitle, ytitle, 2.8, IsLogY, enlargeYaxis)

    info = samp.split('_') # parse signal file name
    TOPYUK  = '{0:.1f}'.format( float(info[6]) )
    
    SlfCoup = info[8]
    if 'm' in SlfCoup:
      SlfCoup = SlfCoup.split('m')[1]
      SLFCOUP = '#minus{0:.1f}'.format( float(SlfCoup) )
    else:
      SLFCOUP = '{0:.1f}'.format( float(SlfCoup) )

    print( 'TopYuk: {0}, SlfCoup: {1}'.format(TOPYUK, SLFCOUP) )

    if fix_TOPYUK:
      leg_txt = '#kappa_{#lambda} = ' + SLFCOUP
    elif fix_SLFCOUP:
      leg_txt = '#kappa_{#it{t}} = ' + TOPYUK
    else:
      leg_txt = '#kappa_{#it{t}} = ' + TOPYUK + ', #kappa_{#lambda} = ' + SLFCOUP

    leg.AddEntry(h_sig, leg_txt, 'l') 

    color = d_sampcolor[samp]
    h_sig.SetLineColor(color) 
    h_sig.SetLineWidth(3)
  
  leg.Draw('same')
  process_txt = 'p p #rightarrow h h, Parton level'
  if fix_TOPYUK:
    process_txt += ', #kappa_{#it{t}} = 1.0'
  elif fix_SLFCOUP:
    process_txt += ', #kappa_{#lambda} = 1.0'
  
  # annotating text
  #myText(0.24, 0.87, '#bf{#it{Pheno4b}}' + ' {0} {1}'.format(datetime.date.today().strftime('%B %d, %Y'), ADD_TXT), 0.037, kBlack)  
  myText(0.26, 0.85, 'MadGraph5 2.6.2 #sqrt{s} = 14 TeV', 0.055, kBlack) 
  myText(0.26, 0.79, process_txt, 0.055, kBlack) 

  gPad.RedrawAxis() 
  
  #==========================================================
  # save everything
  can.cd()
  can.SaveAs(save_name + '.pdf')
  can.Close()


#_______________________________________________________
def tree_get_th1f(f, hname, var, unweighted_cuts='', Nbins=100, xmin=0, xmax=100, lumifb=100, weights=1.0, normalise=False, xsec=0, raw_bkg=0):
  '''
  from a TTree, project a leaf 'var' and return a TH1F
  '''
  h_AfterCut   = TH1D(hname + '_hist', "", Nbins, xmin, xmax)
 
  #h_AfterCut.Sumw2()
  lumi         = lumifb * 10 ** 3 # convert to [pb^{-1}]
  cuts_after   = unweighted_cuts

  # normalise to cross-section if normalise set to True
  if normalise:
    cuts_after = '(({0} * {1} * {2} * {3}) / {4})'.format(unweighted_cuts, lumi, weights, xsec, raw_bkg)

  # Get tree    
  t = f.Get('tree')

  # Use ntup_var in projection as this is the actual command rather than the variable nickname
  d_vars   = configure_vars()
  ntup_var = d_vars[var]['ntup_var']

  # Project into histogram
  t.Project( hname + '_hist', ntup_var, cuts_after )

  # perform integrals to find 
  # total yield, one-sided lower and upper cumulative histos
  nYieldErr = ROOT.Double(0)
  nYield    = h_AfterCut.IntegralAndError(1, Nbins, nYieldErr) # Lydia modified to use Nbins not Nbins+1 
  
  if normalise_unity:
    h_AfterCut.Scale( 1. / h_AfterCut.Integral() )

  h_intgl_lower = TH1D(hname + '_intgl_lower', "", Nbins, xmin, xmax)
  h_intgl_upper = TH1D(hname + '_intgl_upper', "", Nbins, xmin, xmax)
  
  for my_bin in range(1, h_AfterCut.GetXaxis().GetNbins() + 1 ):
    
    # get lower edge of bin
    bin_center = h_AfterCut.GetXaxis().GetBinCenter(my_bin)
    
    # set the negatively weighted values to 0.
    bin_val = h_AfterCut.GetBinContent( my_bin )
    if bin_val < 0:
      print( 'WARNING: Bin {0} of sample {1} has negative entry, setting central value to 0.'.format(my_bin, hname) )
      h_AfterCut.SetBinContent(my_bin, 0.)
    
    # do one-sided integral either side of bin
    intgl_lower = h_AfterCut.Integral( 1, my_bin ) 
    intgl_upper = h_AfterCut.Integral( my_bin, Nbins ) # Lydia modified to use Nbins not Nbins+1 
    
    h_intgl_lower.Fill( bin_center, intgl_lower )
    h_intgl_upper.Fill( bin_center, intgl_upper )
  
  nRaw = h_AfterCut.GetEntries()

  print('---------------------------------')
  print(hname)
  print('Normalising luminosity: {0} /fb'.format(lumifb) )
  print('Cross-section: {0} '.format(xsec) )
  print('Unweighted cuts: {0}'.format(unweighted_cuts) )
  print('Normalising to cross-section: {0}'.format(normalise) )
  print('Final weighted cut string: {0}'.format(cuts_after) )
  print('Integral: {0:.3f} +/- {1:.3f}'.format(nYield, nYieldErr) )
  print('nRaw: {0}'.format(nRaw) )
  print('---------------------------------')

  return [h_AfterCut, nYield, h_intgl_lower, h_intgl_upper, nYieldErr, nRaw]


#____________________________________________________________________________
def customise_axes(hist, xtitle, ytitle, scaleFactor=1.1, IsLogY=False, enlargeYaxis=False):

  # set a universal text size
  text_size = 0.06

  #text_size = 35

  TGaxis.SetMaxDigits(4) 
  ##################################
  # X axis
  xax = hist.GetXaxis()
  xax.CenterTitle() 
  # precision 3 Helvetica (specify label size in pixels)
  xax.SetLabelFont(132)
  xax.SetTitleFont(132)
 
  xax.SetTitle(xtitle)
  xax.SetTitleSize(text_size*1.2)
  # top panel
  xax.SetLabelSize(text_size)

  xax.SetLabelOffset(0.02)
  xax.SetTitleOffset(1.2)
  xax.SetTickSize(0.05)
 
  #xax.SetRangeUser(0,2000) 
  #xax.SetNdivisions(-505) 
  gPad.SetTickx() 
  
  ##################################
  # Y axis
  yax = hist.GetYaxis()
  yax.CenterTitle()
  # precision 3 Helvetica (specify label size in pixels)
  yax.SetLabelFont(132)
  yax.SetTitleFont(132)
 
  
  yax.SetTitle(ytitle)
  yax.SetTitleSize(text_size*1.2)
  yax.SetTitleOffset(1.5) 
  
  yax.SetLabelOffset(0.015)
  yax.SetLabelSize(text_size)
 
  ymax = hist.GetMaximum()
  ymin = hist.GetMinimum()
 
 
  scaleFactor = 3.5
  scaleFactor = 3.2
  # top events panel
  #if xtitle == '':
  if 'Events' in ytitle:
    yax.SetNdivisions(505) 
    if IsLogY:
      if enlargeYaxis:
        ymax = 2 * 10 ** 12
        ymin = 2
      else:
        ymax = 5 * 10 ** 6
        ymin = 0.5
      hist.SetMaximum(ymax)
      hist.SetMinimum(ymin)
    if not IsLogY:
      hist.SetMaximum(700)
      hist.SetMaximum(ymax*scaleFactor)
      hist.SetMinimum(0.0)

  # bottom data/pred panel 
  #elif 'S/sqrt(B)' in ytitle:
  #  hist.SetMinimum(0.0)
  #  hist.SetMaximum(50) 
  #  yax.SetNdivisions(205)
  elif 'None' in ytitle:
    hist.SetMinimum(0.0)
    hist.SetMaximum(1.1) 
    yax.SetNdivisions(205)
   
  gPad.SetTicky()

  gPad.Update()

#____________________________________________________________________________
def customise_gPad(top=0.06, bot=0.17, left=0.17, right=0.08):

  gPad.Update()
  gStyle.SetTitleFontSize(0.0)
  
  # gPad margins
  gPad.SetTopMargin(top)
  gPad.SetBottomMargin(bot)
  gPad.SetLeftMargin(left)
  gPad.SetRightMargin(right)
  
  gStyle.SetOptStat(0) # hide usual stats box 
  gStyle.SetTextFont(132) 
  gPad.Update()

#____________________________________________________________________________
def myText(x, y, text, tsize=0.05, color=kBlack, angle=0) :
  
  l = TLatex()
  l.SetTextSize(tsize)
  l.SetNDC()
  l.SetTextFont(132)
  l.SetTextColor(color)
  l.SetTextAngle(angle)
  l.DrawLatex(x,y, text)


#-------------------------------------------------------
# Main
#-------------------------------------------------------
if __name__ == "__main__":
  main()
