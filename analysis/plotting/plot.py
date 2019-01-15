#!/usr/bin/env python
'''

Welcome to plot.py

Plotting script from Jesse Liu modified for HH4b pheno

From: /data/atlas/atlasdata/jesseliu/atlas/susy/compressed_ew/atlas-susy-ew/various_higgsinofitter/r21/v2_3/HiggsinoFitter/plotting
and /home/jesseliu/pheno/fcc/PhenoSim/analyse/conventional/hh4b/plotting

* This is a script to efficiently make 1-dimensional plots from ntuples 
* Configure various aspects in other files
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
from samples    import *
from cuts       import *
from variables  import *
from beautify   import *

#--------------------------------------------------
#
# TODO matching dictionary temporary until we make new ntuples with low pT filter instead of matching
# TODO implement auto cross-check of number of events for slicing dictionary to ensure this is kept up to date EXIT on mis-match!
# TODO Could add back in cutflow part incl add_cut or needed in previous stage as have cuts affecting many jets, cut arrow, N-1
# TODO Could add back in significance scan

# Global settings

# Labels
GROUP_status = '#bf{#it{Pheno4b}} Internal'
NTUP_status = "Samples: 13 Sep 2018"
ENERGY_status = '14 TeV'

# text size as percentage
text_size = 0.035

#
#--------------------------------------------------

#____________________________________________________________________________
def main():
  
  t0 = time.time()
  
  #================================================
  # user set values
  dir = 'jesse_linked_delphes/varied_couplings' # directory input files to plot are in

  l_vars     = ['m_hh']#,'m_h1']#,'m_h2','pT_h1','pT_h2','eta_h1','eta_h2','phi_h1','phi_h2','pT_hh','dR_hh','deta_hh','dphi_hh']
  l_analyses = ['resolved_TopYuk']#, 'resolved_noGenFilt']#, 'intermediate', 'intermediate_noGenFilt', 'boosted', 'boosted_noGenFilt'] # corresponds to sets of files in samples.py 
  l_sig_regs = ['signal']#,'pre-selection'] # gets specific region from input ROOT file

  cut_sel = 'ntag4' # corresponds to set of cuts in cuts.py 
  lumi    =  3000.0 
  savedir = 'figs'+"/"+dir
  yield_var = "m_hh" # Will plot multiple variables but only want to save yield file for a single variable

  IsLogY   = False
  annotate_text = 'MC Pileup 0, No k-factors'

  # Slicing weight (weight down by number of slices run over)
  # Don't include resolved, intermediate, boosted etc. in key as depends on MC sample not analysis selection!  
  d_slicing_weight = {
               'loop_hh' : 100000./50000.,
               'noGenFilt_4b' : 1200000./50000.,
               'noGenFilt_2b2j' : 1200000./50000.,
               'noGenFilt_4j' :  1200000./50000.,
               'noGenFilt_ttbar' : 1200000./50000.,
               'xpt200_4b' : 1200000./50000.,
               'xpt200_2b2j' : 1200000./50000.,
               'xpt200_4j' : 1200000./50000.,
               'hh_TopYuk_1.0_SlfCoup_0.5' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_1.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_2.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_3.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_5.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_7.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_10.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_m1.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_m2.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_m3.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_m5.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_m7.0' : 100000./50000., 
               'hh_TopYuk_1.0_SlfCoup_m10.0' : 100000./50000., 
               'hh_TopYuk_0.5_SlfCoup_1.0' : 100000./50000.,
  }

  # Matching weight (Delphes saves unmatched xsec not matched xsec which is lower)
  # For now weight down 4j and 2b2j by ratio of matched xsec/non matched xsec (using xsec from single 50k slice as proxy for all slices)
  # In future can reproduce samples with explicit pT filter cut (increase stats) and xqcut removed then this step will not be necessary
  # Set to 1 for all other samples 

  # xsecs for ratios taken from: 
  # /data/atlas/atlasdata/jesseliu/pheno/fcc/samples/14TeV/2018sep13/pp2jjjj/01/Events/pp_1/pp_1_tag_1_banner.txt
  # /data/atlas/atlasdata/jesseliu/pheno/fcc/samples/14TeV/2018sep13/pp2bbjj/01/Events/pp_1/pp_1_tag_1_banner.txt

  d_matching_weight = {
               'noGenFilt_4j' : 106811.992819/887124.3069,
               'noGenFilt_2b2j' : 38165.8048156/116266.19204,
               'xpt200_4j' :13515.2473531/71702.662768,
               'xpt200_2b2j' :655.237254906/1799.7624417,
               'noGenFilt_ttbar' : 1.,
               'noGenFilt_4b' : 1.,
               'xpt200_4b' : 1.,
               'loop_hh' : 1.,
               'hh_TopYuk_1.0_SlfCoup_0.5' : 1., 
               'hh_TopYuk_1.0_SlfCoup_1.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_2.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_3.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_5.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_7.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_10.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_m1.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_m2.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_m3.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_m5.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_m7.0' : 1., 
               'hh_TopYuk_1.0_SlfCoup_m10.0' : 1., 
               'hh_TopYuk_0.5_SlfCoup_1.0' : 1.,
}

  #================================================
  
  # -------------------------------------------------------------
  # Argument parser
  parser = argparse.ArgumentParser(description='Analyse background/signal TTrees and make plots.')
  parser.add_argument('-l', '--lumi',      type=str, nargs='?', help='Float of integrated luminosity to normalise MC to.', default=lumi)
  parser.add_argument('-n', '--noLogY',  action='store_true', help='Do not draw log Y axis.')
 
  args = parser.parse_args()
  if args.lumi:
    lumi = args.lumi
  if args.noLogY:
    IsLogY = False
  
  # -------------------------------------------------------------
  # --------------
  # LOOP over list of analyses l_analyses
  # --------------
  
  for analysis in l_analyses:
  
    # --------------
    # LOOP over list of signal regions l_sig_regs:
    # --------------
    
    for sig_reg in l_sig_regs:
    
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
        print( 'Selection region: {0}'.format(cut_sel) )
        print( 'Normalising luminosity: {0}'.format(lumi) )
        print( '\n--------------------------------------------\n' )
        
        mkdir(savedir) 
  
        if cut_sel is '': 
          save_name = savedir + '/{0}_{1}_{2}'.format(analysis, sig_reg, save_var)
        else:
          save_name = savedir + '/{0}_{1}_{2}_{3}'.format(analysis, sig_reg, save_var, cut_sel)
   
        if IsLogY: save_name += '_LogY'
  
        print_lumi = lumi # [1/fb]
        print('Lumi to print: {0}'.format(print_lumi))
      
        calc_selections(var, yield_var, dir, savedir, analysis, d_slicing_weight, d_matching_weight, lumi, save_name, sig_reg, cut_sel, print_lumi, annotate_text, IsLogY)

  tfinish = time.time()
  telapse = tfinish - t0
    
  print('\n--------------------------------------------------')
  print('Finished plotting in {0:.1f}s'.format(telapse) )
  print('Have a lovely day :) ')
  print('--------------------------------------------------')

#____________________________________________________________________________
def calc_selections(var, yield_var, dir, savedir, analysis, d_slicing_weight, d_matching_weight, lumi, save_name, sig_reg, cut_sel, print_lumi, annotate_text='', IsLogY=True, l_print_cuts=[]):
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
  d_vars = configure_vars()
  
  cut_string, l_cuts = configure_cuts(var, cut_sel) 
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
  # sample sig/bkg yield yieldErr raw
  # ----------------------------------------------------------------- 

  yield_file = savedir + '/YIELD_{0}_{1}_{2}.txt'.format(analysis, sig_reg, cut_sel)
  with open(yield_file, 'w') as f_out: 
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
  
    # Choose full path of sample by its type  
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
   
    # Get sample part of name for use in d_slicing_weight and d_matching_weight
    # i.e. remove resolved_, intermediate_ or boosted_ from name
    l_samp_split = samp.split("_")[1:]
    no_ana_name_samp = '_'.join(l_samp_split)

    # hh weight so visible on plots
    my_weight = 1.
    if "hh" in samp:
      my_weight = 10000.0

    # Get TH1F histogram from the TTree in the TFile and store to dictionary entry
    d_hists[samp] = tree_get_th1f( d_files[samp], d_slicing_weight[no_ana_name_samp], d_matching_weight[no_ana_name_samp], my_weight, samp, var, sig_reg, cutsAfter, hNbins, hXmin, hXmax, lumi, variable_bin, hXarray)

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
 
    if var is yield_var:
      with open(yield_file, 'a') as f_out: 
        f_out.write('{0},{1},{2},{3},{4}\n'.format(samp,sample_type,d_yield[samp]/my_weight,d_yieldErr[samp]/my_weight,d_raw[samp]))
        #print '{0},{1},{2},{3},{4}\n'.format(samp,sample_type,d_yield[samp],d_yieldErr[samp],d_raw[samp])

  f_out.close()
 
  errStatBkg = sqrt( nVarBkg ) # treat total statistical error as sum in quadrature of sample stat errors
  errTotBkg  = sqrt( errStatBkg**2 + (0.2 * nTotBkg) ** 2 )
  
  print('errStatBkg: {0:.3f}, sqrtB: {1:.3f}, errTotBkg: {2:.3f}'.format(errStatBkg, sqrt(nTotBkg), errTotBkg))

  print('==============================================')
  print('----------------------------------------------')
  print('{0}, Total bkg, {1:.3f}, {2:.3f}'.format(cut_sel, nTotBkg, errTotBkg))
  print('----------------------------------------------')
 
  # ----------------------------------------------------------------- 
  # legend for bkg, signals and total bkg yield
  # ----------------------------------------------------------------- 
  leg = mk_leg(0.47, 0.6, 0.88, 0.78, cut_sel, l_sampOther, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.03)
  # legend with breakdown of background by sample
  d_bkg_leg = {}
  l_bkg_leg = ['samp1']
  d_bkg_leg['samp1'] = mk_leg(0.57, 0.68, 0.88, 0.83, cut_sel, l_samp_bkg, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.03)

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
    leg.AddEntry(h_mcErr, 'Bkg Total ({0:.3g})'.format(nTotBkg), 'lf')
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
, annotate_text ,variable_bin, l_cuts, print_lumi, IsLogY)
  # ----------------------------------------------------------------- 
  
  return nTotBkg


#_______________________________________________________
def tree_get_th1f(f, slicing_weight, matching_weight, my_weight, hname, var, sig_reg, cutsAfter='', Nbins=100, xmin=0, xmax=100, lumifb=0, variable_bin=False, hXarray=0):
  '''
  from a TTree, project a leaf 'var' and return a TH1F
  '''
  if variable_bin:
    h_AfterCut   = TH1D(hname + '_hist', "", Nbins, array('d', hXarray) )
  else:
    h_AfterCut   = TH1D(hname + '_hist', "", Nbins, xmin, xmax)
 
  h_AfterCut.Sumw2()
  
  lumi     = lumifb * 1000 # convert to [pb^{-1}]

  mc_weight = "mc_sf"
  if cutsAfter is '':
    cut_after = '(({0}) * ({1}) * ({2}) * ({3}) / ({4}))'.format(mc_weight, lumi, my_weight, matching_weight, slicing_weight) 
  else:
    cut_after = '(({0}) * ({1}) * ({2}) * ({3}) * ({4}) / ({5}))'.format(cutsAfter, mc_weight, lumi, my_weight, matching_weight, slicing_weight) 
  
  print('---------------------------------')
  print('Final weighted cut string: ')
  print(cut_after)
  print('---------------------------------')

  # ========================================================= 
  t = f.Get(sig_reg)
  t.Project(hname + '_hist', var, cut_after )
  #t.Project(hname + '_hist',sig_reg,cut_after )

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
  print( 'hist.IntegralAndError() : sample {0} has integral {1:.3f} +/- {2:.3f}'.format( hname, nYield, nYieldErr ) )
  # =========================================================
  
  return [h_AfterCut, nYield, nYieldErr, nRaw]


#____________________________________________________________________________
def plot_selections(var, h_bkg, d_hsig, h_mcErr, leg, l_bkg_leg, d_bkg_leg, lumi, save_name, pc_sys, analysis, sig_reg, cut_sel, nTotBkg, l_sig, cutsAfter, annotate_text, variable_bin, l_cuts, print_lumi, IsLogY=True):
  '''
  plots the variable var given input THStack h_bkg, one signal histogram and legend built
  makes a dat / bkg panel in lower part of figure
  '''
  print('Proceeding to plot')
  
  # gPad left/right margins
  gpLeft = 0.15
  gpRight = 0.05
  gpTop = 0.08
  gpBot = 0.15
  #can  = TCanvas('','',1000,1000)
  can  = TCanvas('','',1000,800)
    
  d_vars = configure_vars()
  
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

  #=============================================================
  # draw and decorate
  # draw elements
  if nTotBkg > 0.:
    h_bkg.Draw('hist')
    customise_axes(h_bkg, xtitle, ytitle, 1.5, IsLogY, enlargeYaxis)

  # draw signal samples
  for samp in d_hsig:
    print('Drawing {0}'.format(samp))
    d_hsig[samp].Draw('hist same') #e2 = error coloured band
    customise_axes(d_hsig[samp], xtitle, ytitle, 1.5, IsLogY, enlargeYaxis)

  # Clone the total background histogram to draw the line if bkg samples not empty
  if nTotBkg > 0.:
    h_mcErr_clone = h_mcErr.Clone()
    h_mcErr_clone.SetFillColorAlpha(kWhite, 0)
    h_mcErr_clone.SetFillStyle(0)
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
  
  myText(0.6, 0.83, 'Sample (Weighted, Fraction, Raw) ', 0.03)
  myText(0.22, 0.93, 'MadGraph5 2.6.2 + Pythia 8.230 + Delphes 3.4.1 (LO xsec, NLOPDF, xqcut 30 GeV), ' + NTUP_status, text_size*0.6, kGray+1)
  myText(0.18, 0.82, GROUP_status, text_size, kBlack)
  myText(0.18, 0.77, '#sqrt{s}' + ' = {0}, {1}'.format(ENERGY_status, lumi) + ' fb^{#minus1}', text_size, kBlack)
  if 'signal' in sig_reg:
    myText(0.18, 0.73, "SR "+analysis+" "+cut_sel, text_size, kBlack) 
  if 'control' in sig_reg:
    myText(0.18, 0.73, "CR "+analysis+" "+cut_sel, text_size, kBlack) 
  if 'sideband' in sig_reg:
    myText(0.18, 0.73, "SB "+analysis+" "+cut_sel, text_size, kBlack) 
  
  # Additional annotations
  if not annotate_text == '':
    myText(0.18, 0.69, annotate_text, text_size*0.8, kGray+2) 
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
def mk_leg(xmin, ymin, xmax, ymax, cut_sel, l_samp, d_samp, nTotBkg, d_hists, d_yield, d_yieldErr, d_raw, sampSet_type='bkg', txt_size=0.05) :
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
  leg.SetNColumns(1)

  # legend markers 
  d_legMk = {
    'bkg'  : 'f',
    'sig'  : 'l',
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
    if "HH" in leg_entry:
      leg_entry = leg_entry+" x10000"
    legMk       = d_legMk[sample_type]
  
    #print('samp: {0}, type: {1}, legMk: {2}'.format(samp, sample_type, legMk) ) 
    # calculate the % of each background component and put in legend
    pc_yield   = 0
    if sample_type == 'bkg':
      pc_yield = 0.
      if nTotBkg >0.:
        pc_yield = 100 * ( d_yield[samp] / float(nTotBkg) )
      leg_txt = '{0} ({1:.2g}, {2:.1f}%, {3:.0f})'.format( leg_entry, d_yield[samp], pc_yield, d_raw[samp] )
    if sample_type == 'sig':
      leg_txt = '{0} ({1:.2g}, {2:.0f})'.format(leg_entry, d_yield[samp], d_raw[samp])

    leg.AddEntry(hist, leg_txt, legMk)
    #print('{0}, {1}, {2:.3f}, {3:.3f}%'.format(sig_reg, samp, d_yield[samp], pc_yield) )
    print('{0}, {1}, {2:.3f} +/- {3:.3f}, {4:.0f}'.format(cut_sel, samp, d_yield[samp], d_yieldErr[samp], d_raw[samp]) )
 
  
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

