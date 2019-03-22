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
  #TOPPATH = '/data/atlas/atlasdata/DiHiggsPheno/ntuples'
  #TOPPATH = '/data/atlas/atlasdata/beresford/jrf/hh4b_pheno/pheno_study/lydia-dev/pheno_study/analysis/outputs' 
  TOPPATH = '/home/jesseliu/pheno/fcc/data/samples/14TeV/2019mar18/all_merged_delphes/ntuples_2019mar22'

  # Path to ntuples 
  bkg_path  = TOPPATH + '/' + dir
  sig_path  = TOPPATH + '/' + dir
  sig_path  = TOPPATH + '/merged_signals' + dir
  
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
  
  #------------------------------------
  # Loose analysis
  # Resolved:     n_large_jets  = 0
  # Intermediate: n_large_jets >= 1
  # Boosted:      n_large_jets >= 2
  #------------------------------------

  if analysis is 'loose':
    l_samp_bkg = [
                  #'loose_noGenFilt_bkg_wh_trackJetBTag',
                  #'loose_noGenFilt_bkg_zh_trackJetBTag',
                  #'loose_noGenFilt_bkg_zz_trackJetBTag',
                  #'loose_noGenFilt_bkg_bbh_trackJetBTag',
                  #'loose_noGenFilt_bkg_tth_trackJetBTag',
                  #'loose_noGenFilt_bkg_ttbb_trackJetBTag',
                  'loose_noGenFilt_bkg_ttbar_trackJetBTag',
                  'loose_ptj1_20_to_200_bkg_2b2j',
                  'loose_ptj1_200_to_500_bkg_2b2j',
                  'loose_ptj1_500_to_1000_bkg_2b2j',
                  'loose_ptj1_1000_to_infty_bkg_2b2j',
                  'loose_ptj1_20_to_200_bkg_4b',
                  'loose_ptj1_200_to_500_bkg_4b',
                  'loose_ptj1_500_to_1000_bkg_4b',
                  'loose_ptj1_1000_to_infty_bkg_4b',
                 ]

    l_samp_sig = [
                 #'loose_noGenFilt_4b',
                 #'loose_ptj1_20_to_200_bkg_4b',
                 #'loose_noGenFilt_signal_hh_loop_sm_trackJetBTag',
                 'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                 'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0', 
                 'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0', 
    ]


  # Samples for kappa lambda coupling plot
  if analysis is 'loose_kl':
    l_samp_bkg = []

    l_samp_sig = [
                 'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                 'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0', 
                 'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0', 
    ]

  # Samples for kappa top coupling plot
  if analysis is 'loose_kt':
    l_samp_bkg = []

    l_samp_sig = [
                 'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_1.0', 
                 'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                 'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_1.0', 
    ]




  #------------------------------------
  # Resolved analysis
  #------------------------------------

  if analysis is 'resolved':
    l_samp_bkg = [#'resolved_noGenFilt_bkg_ttbar_trackJetBTag',
                  #'resolved_ptj1_20_to_200_bkg_2b2j',
                  #'resolved_ptj1_200_to_500_bkg_2b2j',
                  #'resolved_ptj1_500_to_1000_bkg_2b2j',
                  #'resolved_ptj1_1000_to_infty_bkg_2b2j',
                  'resolved_ptj1_20_to_200_bkg_4b',
                  'resolved_ptj1_200_to_500_bkg_4b',
                  'resolved_ptj1_500_to_1000_bkg_4b',
                  'resolved_ptj1_1000_to_infty_bkg_4b',
                 ]

    l_samp_sig = [
                 #'resolved_noGenFilt_4b',
                 #'resolved_ptj1_20_to_200_bkg_4b',
                 'resolved_noGenFilt_signal_hh_loop_sm_trackJetBTag',
    ]

  # Samples for kappa lambda coupling plot
  if analysis is 'resolved_kl':
    l_samp_bkg = []

    l_samp_sig = [
                 'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                 'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0', 
                 'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0', 
    ]

  # Samples for kappa top coupling plot
  if analysis is 'resolved_kt':
    l_samp_bkg = []

    l_samp_sig = [
                 'resolved_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_1.0', 
                 'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                 'resolved_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_1.0', 
    ]

  #------------------------------------
  # Boosted analysis
  #------------------------------------

  if analysis is 'boosted':
    l_samp_bkg = ['boosted_noGenFilt_bkg_ttbar_trackJetBTag',
                  'boosted_ptj1_20_to_200_bkg_2b2j',
                  'boosted_ptj1_200_to_500_bkg_2b2j',
                  'boosted_ptj1_500_to_1000_bkg_2b2j',
                  'boosted_ptj1_1000_to_infty_bkg_2b2j',
                  'boosted_ptj1_20_to_200_bkg_4b',
                  'boosted_ptj1_200_to_500_bkg_4b',
                  'boosted_ptj1_500_to_1000_bkg_4b',
                  'boosted_ptj1_1000_to_infty_bkg_4b',
                 ]

    l_samp_sig = [
                 'boosted_noGenFilt_signal_hh_loop_sm_trackJetBTag',
    ]

  # Samples for kappa lambda coupling plot
  if analysis is 'boosted_kl':
    l_samp_bkg = []

    l_samp_sig = [
                 'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                 'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0', 
                 'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0', 
    ]

  # Samples for kappa top coupling plot
  if analysis is 'boosted_kt':
    l_samp_bkg = []

    l_samp_sig = [
                 'boosted_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_1.0', 
                 'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0', 
                 'boosted_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_1.0', 
    ]

  # Old samples 
  # Samples with no generator pT filter

  #if analysis is 'resolved_noGenFilt':
  #  l_samp_bkg = [
  #               'resolved_noGenFilt_2b2j',
  #               'resolved_noGenFilt_4b',
  #               'resolved_noGenFilt_4j',
  #               'resolved_noGenFilt_ttbar'
  #    ]

  #  l_samp_sig = [
  #               'resolved_loop_hh'
  #  ]

  ## Samples with generator pT filter

  #if analysis is 'resolved':
  #  l_samp_bkg = [
  #               'resolved_xpt200_2b2j',  
  #               'resolved_xpt200_4b',    
  #               'resolved_xpt200_4j',
  #               'resolved_noGenFilt_ttbar'
  #    ]

  #  l_samp_sig = [
  #               'resolved_loop_hh'
  #  ]

  # Samples with no generator pT filter

  #if analysis is 'boosted_noGenFilt':
  #  l_samp_bkg = [
  #               'boosted_noGenFilt_2b2j',  
  #               'boosted_noGenFilt_4b',    
  #               'boosted_noGenFilt_4j',
  #               'boosted_noGenFilt_ttbar'
  #    ]

  #  l_samp_sig = [
  #               'boosted_loop_hh'
  #  ]

  ## Samples with generator pT filter

  #if analysis is 'boosted':
  #  l_samp_bkg = [
  #               'boosted_xpt200_2b2j',  
  #               'boosted_xpt200_4b',    
  #               'boosted_xpt200_4j',
  #               'boosted_noGenFilt_ttbar'
  #    ]

  #  l_samp_sig = [
  #               'boosted_loop_hh'
  #  ]

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
    

    #------------------------------------
    # Loose analysis
    #------------------------------------
    
    'loose_noGenFilt_signal_hh_loop_sm_trackJetBTag':{'type':'sig','leg':'HH','l_color':kRed+3 },

    'loose_noGenFilt_bkg_tth_trackJetBTag'  :{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'loose_noGenFilt_bkg_zz_trackJetBTag'   :{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'loose_noGenFilt_bkg_ttbb_trackJetBTag' :{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'loose_noGenFilt_bkg_ttbar_trackJetBTag':{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'loose_ptj1_20_to_200_bkg_2b2j'         :{'type':'bkg', 'leg':'2b2j 20-200', 'f_color':myLightBlue},
    'loose_ptj1_200_to_500_bkg_2b2j'        :{'type':'bkg', 'leg':'2b2j 200-500', 'f_color':myLightGreen},
    'loose_ptj1_500_to_1000_bkg_2b2j'       :{'type':'bkg', 'leg':'2b2j 500-1000', 'f_color':myLightOrange},
    'loose_ptj1_1000_to_infty_bkg_2b2j'     :{'type':'bkg', 'leg':'2b2j 1000-infty', 'f_color':myLightPurple},
    'loose_ptj1_20_to_200_bkg_4b'           :{'type':'bkg', 'leg':'4b 20-200', 'f_color':myMediumBlue},
    'loose_ptj1_200_to_500_bkg_4b'          :{'type':'bkg', 'leg':'4b 200-500', 'f_color':myMediumGreen},
    'loose_ptj1_500_to_1000_bkg_4b'         :{'type':'bkg', 'leg':'4b 500-1000', 'f_color':myMediumOrange},
    'loose_ptj1_1000_to_infty_bkg_4b'       :{'type':'bkg', 'leg':'4b 1000-infty', 'f_color':myMediumPurple},

    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_0.5':{'type':'sig','leg':'HH kl = 0','l_color':kBlue },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0':{'type':'sig','leg':'HH kl = 1','l_color':kRed },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0':{'type':'sig','leg':'HH kl = 2','l_color':myLighterOrange},
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_3.0':{'type':'sig','leg':'HH kl = 3','l_color':myLightBlue },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0':{'type':'sig','leg':'HH kl = 5','l_color':myLightGreen },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_7.0':{'type':'sig','leg':'HH kl = 7','l_color':myLightPink },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0':{'type':'sig','leg':'HH kl = 10','l_color':kBlue},
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m1.0':{'type':'sig','leg':'HH kl = -1','l_color':myMediumBlue },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m2.0':{'type':'sig','leg':'HH kl = -2','l_color':myMediumGreen },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m3.0':{'type':'sig','leg':'HH kl = -3','l_color':myMediumOrange },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0':{'type':'sig','leg':'HH kl = -5','l_color':kGreen },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m7.0':{'type':'sig','leg':'HH kl = -7','l_color':myMediumPurple },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m10.0':{'type':'sig','leg':'HH kl = -10','l_color':myDarkBlue },

    'loose_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_1.0':{'type':'sig','leg':'HH kt = 0.8','l_color':kBlue },
    'loose_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0':{'type':'sig','leg':'HH kt = 1','l_color':kRed }, 
    'loose_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_1.0':{'type':'sig','leg':'HH kt = 1.2','l_color':myLightGreen }, 
    
    #------------------------------------
    # Resolved analysis
    #------------------------------------
    
    'resolved_noGenFilt_signal_hh_loop_sm_trackJetBTag':{'type':'sig','leg':'HH','l_color':kRed+3 },

    'resolved_noGenFilt_bkg_ttbar_trackJetBTag':{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'resolved_ptj1_20_to_200_bkg_2b2j':{'type':'bkg', 'leg':'2b2j 20-200', 'f_color':myLightBlue},
    'resolved_ptj1_200_to_500_bkg_2b2j':{'type':'bkg', 'leg':'2b2j 200-500', 'f_color':myLightGreen},
    'resolved_ptj1_500_to_1000_bkg_2b2j':{'type':'bkg', 'leg':'2b2j 500-1000', 'f_color':myLightOrange},
    'resolved_ptj1_1000_to_infty_bkg_2b2j':{'type':'bkg', 'leg':'2b2j 1000-infty', 'f_color':myLightPurple},
    'resolved_ptj1_20_to_200_bkg_4b':{'type':'bkg', 'leg':'4b 20-200', 'f_color':myMediumBlue},
    'resolved_ptj1_200_to_500_bkg_4b':{'type':'bkg', 'leg':'4b 200-500', 'f_color':myMediumGreen},
    'resolved_ptj1_500_to_1000_bkg_4b':{'type':'bkg', 'leg':'4b 500-1000', 'f_color':myMediumOrange},
    'resolved_ptj1_1000_to_infty_bkg_4b':{'type':'bkg', 'leg':'4b 1000-infty', 'f_color':myMediumPurple},

    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_0.5':{'type':'sig','leg':'HH kl = 0','l_color':kBlue },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0':{'type':'sig','leg':'HH kl = 1','l_color':kRed },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0':{'type':'sig','leg':'HH kl = 2','l_color':myLighterOrange},
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_3.0':{'type':'sig','leg':'HH kl = 3','l_color':myLightBlue },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0':{'type':'sig','leg':'HH kl = 5','l_color':myLightGreen },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_7.0':{'type':'sig','leg':'HH kl = 7','l_color':myLightPink },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0':{'type':'sig','leg':'HH kl = 10','l_color':kBlue},
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m1.0':{'type':'sig','leg':'HH kl = -1','l_color':myMediumBlue },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m2.0':{'type':'sig','leg':'HH kl = -2','l_color':myMediumGreen },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m3.0':{'type':'sig','leg':'HH kl = -3','l_color':myMediumOrange },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0':{'type':'sig','leg':'HH kl = -5','l_color':kGreen },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m7.0':{'type':'sig','leg':'HH kl = -7','l_color':myMediumPurple },
    'resolved_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m10.0':{'type':'sig','leg':'HH kl = -10','l_color':myDarkBlue },

    'resolved_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_1.0':{'type':'sig','leg':'HH kt = 0.8','l_color':kBlue },
    'resolved_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_1.0':{'type':'sig','leg':'HH kt = 1.2','l_color':myLightGreen }, 

    #------------------------------------
    # Boosted analysis
    #------------------------------------
    
    'boosted_noGenFilt_signal_hh_loop_sm_trackJetBTag':{'type':'sig','leg':'HH','l_color':kRed+3 },

    'boosted_noGenFilt_bkg_ttbar_trackJetBTag':{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    'boosted_ptj1_20_to_200_bkg_2b2j':{'type':'bkg', 'leg':'2b2j 20-200', 'f_color':myLightBlue},
    'boosted_ptj1_200_to_500_bkg_2b2j':{'type':'bkg', 'leg':'2b2j 200-500', 'f_color':myLightGreen},
    'boosted_ptj1_500_to_1000_bkg_2b2j':{'type':'bkg', 'leg':'2b2j 500-1000', 'f_color':myLightOrange},
    'boosted_ptj1_1000_to_infty_bkg_2b2j':{'type':'bkg', 'leg':'2b2j 1000-infty', 'f_color':myLightPurple},
    'boosted_ptj1_20_to_200_bkg_4b':{'type':'bkg', 'leg':'4b 20-200', 'f_color':myMediumBlue},
    'boosted_ptj1_200_to_500_bkg_4b':{'type':'bkg', 'leg':'4b 200-500', 'f_color':myMediumGreen},
    'boosted_ptj1_500_to_1000_bkg_4b':{'type':'bkg', 'leg':'4b 500-1000', 'f_color':myMediumOrange},
    'boosted_ptj1_1000_to_infty_bkg_4b':{'type':'bkg', 'leg':'4b 1000-infty', 'f_color':myMediumPurple},

    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_0.5':{'type':'sig','leg':'HH kl = 0','l_color':kBlue },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_1.0':{'type':'sig','leg':'HH kl = kt = 1','l_color':kRed },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_2.0':{'type':'sig','leg':'HH kl = 2','l_color':myLighterOrange},
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_3.0':{'type':'sig','leg':'HH kl = 3','l_color':myLightBlue },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_5.0':{'type':'sig','leg':'HH kl = 5','l_color':myLightGreen },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_7.0':{'type':'sig','leg':'HH kl = 7','l_color':myLightPink },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_10.0':{'type':'sig','leg':'HH kl = 10','l_color':kBlue},
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m1.0':{'type':'sig','leg':'HH kl = -1','l_color':myMediumBlue },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m2.0':{'type':'sig','leg':'HH kl = -2','l_color':myMediumGreen },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m3.0':{'type':'sig','leg':'HH kl = -3','l_color':myMediumOrange },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m5.0':{'type':'sig','leg':'HH kl = -5','l_color':kGreen },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m7.0':{'type':'sig','leg':'HH kl = -7','l_color':myMediumPurple },
    'boosted_noGenFilt_signal_hh_TopYuk_1.0_SlfCoup_m10.0':{'type':'sig','leg':'HH kl = -10','l_color':myDarkBlue },

    'boosted_noGenFilt_signal_hh_TopYuk_0.8_SlfCoup_1.0':{'type':'sig','leg':'HH kt = 0.8','l_color':kBlue },
    'boosted_noGenFilt_signal_hh_TopYuk_1.2_SlfCoup_1.0':{'type':'sig','leg':'HH kt = 1.2','l_color':myLightGreen }, 
    
    }
    # Old sample names below for making comparison plots

    #'resolved_loop_hh':{'type':'sig','leg':'HH','l_color':kRed+3 },
    #'resolved_hh_TopYuk_1.0_SlfCoup_0.5':{'type':'sig','leg':'HH kl = 0','l_color':kBlue },
    #'resolved_hh_TopYuk_1.0_SlfCoup_1.0':{'type':'sig','leg':'HH kl = 1','l_color':kRed },
    #'resolved_hh_TopYuk_1.0_SlfCoup_2.0':{'type':'sig','leg':'HH kl = 2','l_color':myLighterOrange},
    #'resolved_hh_TopYuk_1.0_SlfCoup_3.0':{'type':'sig','leg':'HH kl = 3','l_color':myLightBlue },
    #'resolved_hh_TopYuk_1.0_SlfCoup_5.0':{'type':'sig','leg':'HH kl = 5','l_color':myLightGreen },
    #'resolved_hh_TopYuk_1.0_SlfCoup_7.0':{'type':'sig','leg':'HH kl = 7','l_color':myLightPink },
    #'resolved_hh_TopYuk_1.0_SlfCoup_10.0':{'type':'sig','leg':'HH kl = 10','l_color':kBlue},
    #'resolved_hh_TopYuk_1.0_SlfCoup_m1.0':{'type':'sig','leg':'HH kl = -1','l_color':myMediumBlue },
    #'resolved_hh_TopYuk_1.0_SlfCoup_m2.0':{'type':'sig','leg':'HH kl = -2','l_color':myMediumGreen },
    #'resolved_hh_TopYuk_1.0_SlfCoup_m3.0':{'type':'sig','leg':'HH kl = -3','l_color':myMediumOrange },
    #'resolved_hh_TopYuk_1.0_SlfCoup_m5.0':{'type':'sig','leg':'HH kl = -5','l_color':kGreen },
    #'resolved_hh_TopYuk_1.0_SlfCoup_m7.0':{'type':'sig','leg':'HH kl = -7','l_color':myMediumPurple },
    #'resolved_hh_TopYuk_1.0_SlfCoup_m10.0':{'type':'sig','leg':'HH kl = -10','l_color':myDarkBlue },
    #
    #'resolved_hh_TopYuk_0.5_SlfCoup_1.0':{'type':'sig','leg':'HH kt = 0.5','l_color':myDarkOrange },

    #'resolved_noGenFilt_4b':{'type':'sig', 'leg':'4b', 'l_color':myLightBlue},    
    #'resolved_noGenFilt_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    #'resolved_noGenFilt_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    
    #'resolved_noGenFilt_ttbar':{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    #'resolved_xpt200_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    #'resolved_xpt200_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    #'resolved_xpt200_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    

    ##------------------------------------
    ## Boosted analysis
    ##------------------------------------
    #
    #'boosted_loop_hh':{'type':'sig','leg':'HH','l_color':kRed+3 },

    #'boosted_noGenFilt_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    #'boosted_noGenFilt_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    #'boosted_noGenFilt_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    
    #'boosted_noGenFilt_ttbar':{'type':'bkg', 'leg':'ttbar', 'f_color':myLightPink},    
    #'boosted_xpt200_4b':{'type':'bkg', 'leg':'4b', 'f_color':myLightBlue},    
    #'boosted_xpt200_2b2j':{'type':'bkg', 'leg':'2b2j', 'f_color':myLightGreen},
    #'boosted_xpt200_4j':{'type':'bkg', 'leg':'4j', 'f_color':myLightOrange},    
    #}

  return d_samp


