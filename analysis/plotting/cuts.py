'''

Welcome to cuts.py

Here we have configure_cuts()
This a cut string added_cuts
and a list of cuts applied l_cuts_nMinus1

Configure the regions in dictionary d_cuts = {}
that is keyed by the region name,
whose value is the nominal list of cuts 
to be applied to this region.

'''

#____________________________________________________________________________
def configure_cuts(cut_sel, print_cuts=True):

  ''' 
  Can define multiple lists and combine them
  e.g. to create different analysis regions CR, VR, SR
  '''

  l_ntag4 = [
    '(ntag>3)',
  ]  
  
  l_resolved = ['n_large_jets == 0',
                   'n_small_jets >= 4',
                   #'n_bjets_in_higgs1 >= 2',
                   #'n_bjets_in_higgs2 >= 2',
  ]
  
  l_resolved_SR = [
                   'h1_M > 90 && h1_M < 140',
                   'h2_M > 80 && h2_M < 130',
                  ]

  l_intermediate = [
                       'n_large_jets == 1',
                       'n_small_jets >= 2',
                       #'n_bjets_in_higgs1 >= 2',
                       #'n_bjets_in_higgs2 >= 2',
  ]
  
  l_intermediate_SR = [
                   'h1_M > 90 && h1_M < 140',
                   'h2_M > 80 && h2_M < 130',
                  ]

  l_boosted = ['n_large_jets == 2',
                  #'n_bjets_in_higgs1 >= 2',
                  #'n_bjets_in_higgs2 >= 2',
  ]
  
  l_boosted_SR = [
                   'h1_M > 90 && h1_M < 140',
                   'h2_M > 90 && h2_M < 140',
                  ]

  l_common = [ 
              'met_Et < 150',
              'nElec == 0',
              'nMuon == 0',
              'dEta_hh < 1.5',
              'h1_M > 50',
              'h2_M > 50',
              ]

  # Binning for resolved
  l_200mHH250  = ['m_hh > 200 && m_hh < 250']
  l_250mHH300  = ['m_hh > 250 && m_hh < 300']
  l_300mHH350  = ['m_hh > 300 && m_hh < 350']
  l_350mHH400  = ['m_hh > 350 && m_hh < 400']
  l_400mHH500  = ['m_hh > 400 && m_hh < 500']
  l_500mHH     = ['m_hh > 500']
  
  # Binning for intermediate
  l_200mHH400  = ['m_hh > 200 && m_hh < 400']
  l_400mHH600  = ['m_hh > 400 && m_hh < 600']
  l_600mHH     = ['m_hh > 600']
  
  # Binning for boosted
  l_500mHH700  = ['m_hh > 500 && m_hh < 700']
  l_700mHH900  = ['m_hh > 700 && m_hh < 900']
  l_900mHH     = ['m_hh > 900']

  # Single cuts on DNN score
  l_NNlamM20  = ['nnscore_SlfCoup_m20.0_sig > 0.85']
  l_NNlamM10  = ['nnscore_SlfCoup_m10.0_sig > 0.85']
  l_NNlamM7   = ['nnscore_SlfCoup_m7.0_sig  > 0.85']
  l_NNlamM5   = ['nnscore_SlfCoup_m5.0_sig  > 0.85']
  l_NNlamM2   = ['nnscore_SlfCoup_m2.0_sig  > 0.85']
  l_NNlamM1   = ['nnscore_SlfCoup_m1.0_sig  > 0.85']
  l_NNlamM0p5 = ['nnscore_SlfCoup_m0.5_sig  > 0.85']

  l_NNlam0p5  = ['nnscore_SlfCoup_0.5_sig   > 0.85']
  l_NNlam1    = ['nnscore_SlfCoup_1.0_sig  > 0.85']
  l_NNlam2    = ['nnscore_SlfCoup_2.0_sig  > 0.85']
  l_NNlam3    = ['nnscore_SlfCoup_3.0_sig  > 0.85']
  l_NNlam5    = ['nnscore_SlfCoup_5.0_sig  > 0.85']
  l_NNlam7    = ['nnscore_SlfCoup_7.0_sig  > 0.85']
  l_NNlam10   = ['nnscore_SlfCoup_10.0_sig > 0.85']
  l_NNlam20   = ['nnscore_SlfCoup_20.0_sig > 0.85']

  # Define final inclusive SRs for 3 channels
  l_SR_res = l_common + l_resolved     + l_resolved_SR 
  l_SR_int = l_common + l_intermediate + l_intermediate_SR 
  l_SR_bst = l_common + l_boosted      + l_boosted_SR 


  # =============================================
  d_cuts = {
    'ntag4'        : l_ntag4,
    'all-preselection'          : ['n_large_jets >= 0'],

    'resolved-preselection'     : l_resolved,
    'intermediate-preselection' : l_intermediate,
    'boosted-preselection'      : l_boosted,

    'resolved-commonSR'         : l_common + l_resolved,
    'intermediate-commonSR'     : l_common + l_intermediate,
    'boosted-commonSR'          : l_common + l_boosted,

    # Inclusive SRs (no multibin)
    'SR-res' : l_SR_res,
    'SR-int' : l_SR_int,
    'SR-bst' : l_SR_bst,
    # DNN trained on k(lambda) = 1
    'SRNN-res' : l_SR_res + l_NNlam1,
    'SRNN-int' : l_SR_int + l_NNlam1,
    'SRNN-bst' : l_SR_bst + l_NNlam1,
    
    #------------------------------------------------
    # Baseline analysis
    # Resolved multibin baseline
    'SR-res-200mHH250' : l_SR_res + l_200mHH250,
    'SR-res-250mHH300' : l_SR_res + l_250mHH300,
    'SR-res-300mHH350' : l_SR_res + l_300mHH350,
    'SR-res-350mHH400' : l_SR_res + l_350mHH400,
    'SR-res-400mHH500' : l_SR_res + l_400mHH500,
    'SR-res-500mHH'    : l_SR_res + l_500mHH,

    # Intermediate multibin baseline
    'SR-int-200mHH400' : l_SR_int + l_200mHH400,
    'SR-int-400mHH600' : l_SR_int + l_400mHH600,
    'SR-int-600mHH'    : l_SR_int + l_600mHH,

    # Boosted multibin baseline
    'SR-bst-500mHH700' : l_SR_bst + l_500mHH700,
    'SR-bst-700mHH900' : l_SR_bst + l_700mHH900,
    'SR-bst-900mHH'    : l_SR_bst + l_900mHH,

    #------------------------------------------------
    # DNN trained on k(lambda) = 1
    # Resolved multibin DNN
    'SRNN-res-200mHH250-lam1' : l_SR_res + l_200mHH250 + l_NNlam1,
    'SRNN-res-250mHH300-lam1' : l_SR_res + l_250mHH300 + l_NNlam1,
    'SRNN-res-300mHH350-lam1' : l_SR_res + l_300mHH350 + l_NNlam1,
    'SRNN-res-350mHH400-lam1' : l_SR_res + l_350mHH400 + l_NNlam1,
    'SRNN-res-400mHH500-lam1' : l_SR_res + l_400mHH500 + l_NNlam1,
    'SRNN-res-500mHH-lam1'    : l_SR_res + l_500mHH    + l_NNlam1,

    # Intermediate multibin DNN
    'SRNN-int-200mHH400-lam1' : l_SR_int + l_200mHH400 + l_NNlam1,
    'SRNN-int-400mHH600-lam1' : l_SR_int + l_400mHH600 + l_NNlam1,
    'SRNN-int-600mHH-lam1'    : l_SR_int + l_600mHH    + l_NNlam1,

    # Boosted multibin DNN
    'SRNN-bst-500mHH700-lam1' : l_SR_bst + l_500mHH700 + l_NNlam1,
    'SRNN-bst-700mHH900-lam1' : l_SR_bst + l_700mHH900 + l_NNlam1,
    'SRNN-bst-900mHH-lam1'    : l_SR_bst + l_900mHH    + l_NNlam1,

    #------------------------------------------------
    # DNN trained on k(lambda) = 5
    # Resolved multibin DNN lam5
    'SRNN-res-200mHH250-lam5' : l_SR_res + l_200mHH250 + l_NNlam5,
    'SRNN-res-250mHH300-lam5' : l_SR_res + l_250mHH300 + l_NNlam5,
    'SRNN-res-300mHH350-lam5' : l_SR_res + l_300mHH350 + l_NNlam5,
    'SRNN-res-350mHH400-lam5' : l_SR_res + l_350mHH400 + l_NNlam5,
    'SRNN-res-400mHH500-lam5' : l_SR_res + l_400mHH500 + l_NNlam5,
    'SRNN-res-500mHH-lam5'    : l_SR_res + l_500mHH    + l_NNlam5,

    # Intermediate multibin DNN lam5
    'SRNN-int-200mHH400-lam5' : l_SR_int + l_200mHH400 + l_NNlam5,
    'SRNN-int-400mHH600-lam5' : l_SR_int + l_400mHH600 + l_NNlam5,
    'SRNN-int-600mHH-lam5'    : l_SR_int + l_600mHH    + l_NNlam5,

    # Boosted multibin DNN lam5
    'SRNN-bst-500mHH700-lam5' : l_SR_bst + l_500mHH700 + l_NNlam5,
    'SRNN-bst-700mHH900-lam5' : l_SR_bst + l_700mHH900 + l_NNlam5,
    'SRNN-bst-900mHH-lam5'    : l_SR_bst + l_900mHH    + l_NNlam5,

    #------------------------------------------------
    # DNN trained on k(lambda) = 10
    # Resolved multibin DNN lam10
    'SRNN-res-200mHH250-lam10' : l_SR_res + l_200mHH250 + l_NNlam10,
    'SRNN-res-250mHH300-lam10' : l_SR_res + l_250mHH300 + l_NNlam10,
    'SRNN-res-300mHH350-lam10' : l_SR_res + l_300mHH350 + l_NNlam10,
    'SRNN-res-350mHH400-lam10' : l_SR_res + l_350mHH400 + l_NNlam10,
    'SRNN-res-400mHH500-lam10' : l_SR_res + l_400mHH500 + l_NNlam10,
    'SRNN-res-500mHH-lam10'    : l_SR_res + l_500mHH    + l_NNlam10,

    # Intermediate multibin DNN lam10
    'SRNN-int-200mHH400-lam10' : l_SR_int + l_200mHH400 + l_NNlam10,
    'SRNN-int-400mHH600-lam10' : l_SR_int + l_400mHH600 + l_NNlam10,
    'SRNN-int-600mHH-lam10'    : l_SR_int + l_600mHH    + l_NNlam10,

    # Boosted multibin DNN lam10
    'SRNN-bst-500mHH700-lam10' : l_SR_bst + l_500mHH700 + l_NNlam10,
    'SRNN-bst-700mHH900-lam10' : l_SR_bst + l_700mHH900 + l_NNlam10,
    'SRNN-bst-900mHH-lam10'    : l_SR_bst + l_900mHH    + l_NNlam10,

  } 
  
  l_cuts = [''] 
  added_cuts = ''
  if cut_sel is not '':
    # From cut lists
    l_cuts = d_cuts[cut_sel]
    # join cuts with && (AND) operator
    added_cuts = ' && '.join(l_cuts)

  if print_cuts:
    print('===============================================')
    print('Cuts applied:')
    for x in l_cuts:
      print x
    print('-----------------------------------------------')
    print 'Unweighted final cut-string:', added_cuts
    print('===============================================')
 
  return added_cuts, l_cuts
