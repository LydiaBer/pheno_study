'''

Welcome to samples.py

This has a few functions to
- Define the paths to the ntuples in get_sample_paths()
- Specify which background and signal samples to plot in get_samples_to_plot()
- Configure sample type, legend entry and colours in configure_samples() 

'''

import os
from ROOT import TColor
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange

#____________________________________________________________________________
def get_sample_paths(dir = ''):

  # -------------------------------------
  #
  # Set paths to ntuples
  #
  # -------------------------------------
  
  # Paths to ntuples # 
  TOPPATH = '../outputs'
  
  # Path to ntuples 
  bkg_path  = TOPPATH + '/' + dir
  sig_path  = TOPPATH + '/' + dir
  
  # Suffix of the sample file names
  bkg_suffix   = '.root'
  sig_suffix   = '.root'
  
  return bkg_path, sig_path, bkg_suffix, sig_suffix


#____________________________________________________________________________
def get_samples_to_plot(analysis = ''):
  '''
  List of background and signal samples to analyse in plot.py 
  '''

  #------------------------------------
  # Background and signal samples
  #------------------------------------

  l_samp_bkg = []
  l_samp_sig = []

  # Samples with no generator pT filter

  if analysis is 'intermediate_noGenFilt':
    l_samp_bkg = [
                 'intermediate_noGenFilt_2b2j',  
                 'intermediate_noGenFilt_4b',    
                 'intermediate_noGenFilt_4j',
                 'intermediate_noGenFilt_ttbar'
      ]

    l_samp_sig = [
                 'intermediate_loop_hh'
    ]

  if analysis is 'boosted_noGenFilt':
    l_samp_bkg = [
                 'boosted_noGenFilt_2b2j',  
                 'boosted_noGenFilt_4b',    
                 'boosted_noGenFilt_4j'
                 'boosted_noGenFilt_ttbar'
      ]

    l_samp_sig = [
                 'boosted_loop_hh'
    ]
  if analysis is 'resolved_noGenFilt':
    l_samp_bkg = [
                 'resolved_noGenFilt_2b2j',
                 'resolved_noGenFilt_4b',
                 'resolved_noGenFilt_4j',
                 'resolved_noGenFilt_ttbar'
      ]

    l_samp_sig = [
                 'resolved_loop_hh'
    ]

  # Samples with generator pT filter

  if analysis is 'resolved':
    l_samp_bkg = [
                 'resolved_xptb200_2b2j',  
                 'resolved_xptb200_4b',    
                 'resolved_xptj200_4j',
                 'resolved_noGenFilt_ttbar'
      ]

    l_samp_sig = [
                 'resolved_loop_hh'
    ]

  if analysis is 'intermediate':
    l_samp_bkg = [
                 'intermediate_xptb200_2b2j',
                 'intermediate_xptb200_4b',
                 'intermediate_xptj200_4j',
                 'intermediate_noGenFilt_ttbar'
      ]

    l_samp_sig = [
                 'intermediate_loop_hh',
    ]

  if analysis is 'boosted':
    l_samp_bkg = [
                 'boosted_xptb200_2b2j',  
                 'boosted_xptb200_4b',    
                 'boosted_xptj200_4j',
                 'boosted_noGenFilt_ttbar'
      ]

    l_samp_sig = [
                 'boosted_loop_hh'
    ]


  return l_samp_bkg, l_samp_sig

#____________________________________________________________________________
def configure_samples():
  
  # -------------------------------------
  #
  # Custom colours (in hexadecimal RGB)
  # Taken from http://colorbrewer2.org/
  #
  # -------------------------------------

  # Blues
  myLighterBlue   = TColor.GetColor('#deebf7')
  myLightBlue     = TColor.GetColor('#9ecae1')
  myMediumBlue    = TColor.GetColor('#0868ac')
  myDarkBlue      = TColor.GetColor('#08306b')

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

  # -------------------------------------
  #
  # Samples dictionary
  #
  # 'TTree name for sample' : 
  #                 { 'type'    : set as data, background or signal
  #                   'leg'     : label that appears in the plot legend
  #                   'f_color' : fill colour of background sample
  #                   'l_color' : line colour of signal sample 
  #                   }
  #
  # -------------------------------------
  d_samp = {
    
    # Bkg samples
    'resolved_noGenFilt_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    'resolved_noGenFilt_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    'resolved_noGenFilt_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    
    'resolved_noGenFilt_ttbar':{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'resolved_xptb200_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    'resolved_xptb200_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    'resolved_xptj200_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    

    'intermediate_noGenFilt_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    'intermediate_noGenFilt_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    'intermediate_noGenFilt_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    
    'intermediate_noGenFilt_ttbar':{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'intermediate_xptb200_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    'intermediate_xptb200_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    'intermediate_xptj200_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    

    'boosted_noGenFilt_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    'boosted_noGenFilt_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    'boosted_noGenFilt_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    
    'boosted_noGenFilt_ttbar':{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'boosted_xptb200_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    'boosted_xptb200_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    'boosted_xptj200_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    

    # Signals
    'resolved_loop_hh':{'type':'sig','leg':'HH','l_color':kRed+3 },
    'intermediate_loop_hh':{'type':'sig','leg':'HH','l_color':kRed+3 },
    'boosted_loop_hh':{'type':'sig','leg':'HH','l_color':kRed+3 }
    }

  return d_samp


