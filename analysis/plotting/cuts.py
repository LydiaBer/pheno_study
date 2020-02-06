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
                   'h2_M > 90 && h2_M < 140',
                  ]

  l_intermediate = [
                       'n_large_jets == 1',
                       'n_small_jets >= 2',
                       #'n_bjets_in_higgs1 >= 2',
                       #'n_bjets_in_higgs2 >= 2',
  ]
  
  l_intermediate_SR = [
                   'h1_M > 90 && h1_M < 140',
                   'h2_M > 90 && h2_M < 140',
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
              'n_jets_in_higgs1 >= 2 && n_jets_in_higgs2 >= 2',
              ]

  # Binning for resolved
  l_200mHH250  = ['m_hh > 200 && m_hh < 250']
  l_250mHH300  = ['m_hh > 250 && m_hh < 300']
  l_300mHH350  = ['m_hh > 300 && m_hh < 350']
  l_350mHH400  = ['m_hh > 350 && m_hh < 400']
  l_400mHH500  = ['m_hh > 400 && m_hh < 500']
  l_500mHH     = ['m_hh > 500']
  
  # Binning for intermediate
  l_200mHH500  = ['m_hh > 200 && m_hh < 500']
  l_500mHH600  = ['m_hh > 500 && m_hh < 600']
  l_600mHH     = ['m_hh > 600']
  
  # Binning for boosted
  l_500mHH800  = ['m_hh > 500 && m_hh < 800']
  l_800mHH     = ['m_hh > 800']

  # Single cuts on DNN score
  l_NNlamM20  = ['nnscore_SlfCoup_m20.0_sig > 0.75']
  l_NNlamM10  = ['nnscore_SlfCoup_m10.0_sig > 0.75']
  l_NNlamM7   = ['nnscore_SlfCoup_m7.0_sig  > 0.75']
  l_NNlamM5   = ['nnscore_SlfCoup_m5.0_sig  > 0.75']
  l_NNlamM2   = ['nnscore_SlfCoup_m2.0_sig  > 0.75']
  l_NNlamM1   = ['nnscore_SlfCoup_m1.0_sig  > 0.75']
  l_NNlamM0p5 = ['nnscore_SlfCoup_m0.5_sig  > 0.75']

  l_NNlam0p5  = ['nnscore_SlfCoup_0.5_sig   > 0.75']
  l_NNlam1    = ['nnscore_SlfCoup_1.0_sig  > 0.75']
  l_NNlam2    = ['nnscore_SlfCoup_2.0_sig  > 0.75']
  l_NNlam3    = ['nnscore_SlfCoup_3.0_sig  > 0.75']
  l_NNlam5    = ['nnscore_SlfCoup_5.0_sig  > 0.75']
  l_NNlam7    = ['nnscore_SlfCoup_7.0_sig  > 0.75']
  l_NNlam10   = ['nnscore_SlfCoup_10.0_sig > 0.75']
  l_NNlam20   = ['nnscore_SlfCoup_20.0_sig > 0.75']

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

    #------------------------------------------------
    # Inclusive SRs (no multibin)
    #------------------------------------------------

    'SR-res-nolargerveto' : l_common + l_resolved_SR + ['n_small_jets >= 4'],

    # No DNN
    'SR-res' : l_SR_res,
    'SR-int' : l_SR_int,
    'SR-bst' : l_SR_bst,

    # DNN trained on k(lambda) = 1
    'SRNN-res-lam1' : l_SR_res + l_NNlam1,
    'SRNN-int-lam1' : l_SR_int + l_NNlam1,
    'SRNN-bst-lam1' : l_SR_bst + l_NNlam1,

    # DNN trained on k(lambda) = 5
    'SRNN-res-lam5' : l_SR_res + l_NNlam5,
    'SRNN-int-lam5' : l_SR_int + l_NNlam5,
    'SRNN-bst-lam5' : l_SR_bst + l_NNlam5,
    
    # DNN trained on k(lambda) = 7
    'SRNN-res-lam7' : l_SR_res + l_NNlam7,
    'SRNN-int-lam7' : l_SR_int + l_NNlam7,
    'SRNN-bst-lam7' : l_SR_bst + l_NNlam7,
    
    # DNN trained on k(lambda) = 10
    'SRNN-res-lam10' : l_SR_res + l_NNlam10,
    'SRNN-int-lam10' : l_SR_int + l_NNlam10,
    'SRNN-bst-lam10' : l_SR_bst + l_NNlam10,

    # DNN trained on k(lambda) = -1
    'SRNN-res-lamM1' : l_SR_res + l_NNlamM1,
    'SRNN-int-lamM1' : l_SR_int + l_NNlamM1,
    'SRNN-bst-lamM1' : l_SR_bst + l_NNlamM1,

    # DNN trained on k(lambda) = -7
    'SRNN-res-lamM2' : l_SR_res + l_NNlamM2,
    'SRNN-int-lamM2' : l_SR_int + l_NNlamM2,
    'SRNN-bst-lamM2' : l_SR_bst + l_NNlamM2,

    # DNN trained on k(lambda) = -5
    'SRNN-res-lamM5' : l_SR_res + l_NNlamM5,
    'SRNN-int-lamM5' : l_SR_int + l_NNlamM5,
    'SRNN-bst-lamM5' : l_SR_bst + l_NNlamM5,
    
    #------------------------------------------------
    # Multibin SRs 
    #------------------------------------------------

    #------------------------------------------------
    # No DNN

    # Resolved multibin
    'SR-res-200mHH250' : l_SR_res + l_200mHH250,
    'SR-res-250mHH300' : l_SR_res + l_250mHH300,
    'SR-res-300mHH350' : l_SR_res + l_300mHH350,
    'SR-res-350mHH400' : l_SR_res + l_350mHH400,
    'SR-res-400mHH500' : l_SR_res + l_400mHH500,
    'SR-res-500mHH'    : l_SR_res + l_500mHH,

    # Intermediate multibin
    'SR-int-200mHH500' : l_SR_int + l_200mHH500,
    'SR-int-500mHH600' : l_SR_int + l_500mHH600,
    'SR-int-600mHH'    : l_SR_int + l_600mHH,

    # Boosted multibin 
    'SR-bst-500mHH800' : l_SR_bst + l_500mHH800,
    'SR-bst-800mHH'    : l_SR_bst + l_800mHH,

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
    'SRNN-int-200mHH500-lam1' : l_SR_int + l_200mHH500 + l_NNlam1,
    'SRNN-int-500mHH600-lam1' : l_SR_int + l_500mHH600 + l_NNlam1,
    'SRNN-int-600mHH-lam1'    : l_SR_int + l_600mHH    + l_NNlam1,

    # Boosted multibin DNN
    'SRNN-bst-500mHH800-lam1' : l_SR_bst + l_500mHH800 + l_NNlam1,
    'SRNN-bst-800mHH-lam1'    : l_SR_bst + l_800mHH    + l_NNlam1,

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
    'SRNN-int-200mHH500-lam5' : l_SR_int + l_200mHH500 + l_NNlam5,
    'SRNN-int-500mHH600-lam5' : l_SR_int + l_500mHH600 + l_NNlam5,
    'SRNN-int-600mHH-lam5'    : l_SR_int + l_600mHH    + l_NNlam5,

    # Boosted multibin DNN lam5
    'SRNN-bst-500mHH800-lam5' : l_SR_bst + l_500mHH800 + l_NNlam5,
    'SRNN-bst-800mHH-lam5'    : l_SR_bst + l_800mHH    + l_NNlam5,

    #------------------------------------------------
    # DNN trained on k(lambda) = 7

    # Resolved multibin DNN lam7
    'SRNN-res-200mHH250-lam7' : l_SR_res + l_200mHH250 + l_NNlam7,
    'SRNN-res-250mHH300-lam7' : l_SR_res + l_250mHH300 + l_NNlam7,
    'SRNN-res-300mHH350-lam7' : l_SR_res + l_300mHH350 + l_NNlam7,
    'SRNN-res-350mHH400-lam7' : l_SR_res + l_350mHH400 + l_NNlam7,
    'SRNN-res-400mHH500-lam7' : l_SR_res + l_400mHH500 + l_NNlam7,
    'SRNN-res-500mHH-lam7'    : l_SR_res + l_500mHH    + l_NNlam7,

    # Intermediate multibin DNN lam7
    'SRNN-int-200mHH500-lam7' : l_SR_int + l_200mHH500 + l_NNlam7,
    'SRNN-int-500mHH600-lam7' : l_SR_int + l_500mHH600 + l_NNlam7,
    'SRNN-int-600mHH-lam7'    : l_SR_int + l_600mHH    + l_NNlam7,

    # Boosted multibin DNN lam7
    'SRNN-bst-500mHH800-lam7' : l_SR_bst + l_500mHH800 + l_NNlam7,
    'SRNN-bst-800mHH-lam7'    : l_SR_bst + l_800mHH    + l_NNlam7,


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
    'SRNN-int-200mHH500-lam10' : l_SR_int + l_200mHH500 + l_NNlam10,
    'SRNN-int-500mHH600-lam10' : l_SR_int + l_500mHH600 + l_NNlam10,
    'SRNN-int-600mHH-lam10'    : l_SR_int + l_600mHH    + l_NNlam10,

    # Boosted multibin DNN lam10
    'SRNN-bst-500mHH800-lam10' : l_SR_bst + l_500mHH800 + l_NNlam10,
    'SRNN-bst-800mHH-lam10'    : l_SR_bst + l_800mHH    + l_NNlam10,

    #------------------------------------------------
    # DNN trained on k(lambda) = -1

    # Resolved multibin DNN lamM1
    'SRNN-res-200mHH250-lamM1' : l_SR_res + l_200mHH250 + l_NNlamM1,
    'SRNN-res-250mHH300-lamM1' : l_SR_res + l_250mHH300 + l_NNlamM1,
    'SRNN-res-300mHH350-lamM1' : l_SR_res + l_300mHH350 + l_NNlamM1,
    'SRNN-res-350mHH400-lamM1' : l_SR_res + l_350mHH400 + l_NNlamM1,
    'SRNN-res-400mHH500-lamM1' : l_SR_res + l_400mHH500 + l_NNlamM1,
    'SRNN-res-500mHH-lamM1'    : l_SR_res + l_500mHH    + l_NNlamM1,

    # Intermediate multibin DNN lamM1
    'SRNN-int-200mHH500-lamM1' : l_SR_int + l_200mHH500 + l_NNlamM1,
    'SRNN-int-500mHH600-lamM1' : l_SR_int + l_500mHH600 + l_NNlamM1,
    'SRNN-int-600mHH-lamM1'    : l_SR_int + l_600mHH    + l_NNlamM1,

    # Boosted multibin DNN lamM1
    'SRNN-bst-500mHH800-lamM1' : l_SR_bst + l_500mHH800 + l_NNlamM1,
    'SRNN-bst-800mHH-lamM1'    : l_SR_bst + l_800mHH    + l_NNlamM1,

    #------------------------------------------------
    # DNN trained on k(lambda) = -2

    # Resolved multibin DNN lamM2
    'SRNN-res-200mHH250-lamM2' : l_SR_res + l_200mHH250 + l_NNlamM2,
    'SRNN-res-250mHH300-lamM2' : l_SR_res + l_250mHH300 + l_NNlamM2,
    'SRNN-res-300mHH350-lamM2' : l_SR_res + l_300mHH350 + l_NNlamM2,
    'SRNN-res-350mHH400-lamM2' : l_SR_res + l_350mHH400 + l_NNlamM2,
    'SRNN-res-400mHH500-lamM2' : l_SR_res + l_400mHH500 + l_NNlamM2,
    'SRNN-res-500mHH-lamM2'    : l_SR_res + l_500mHH    + l_NNlamM2,

    # Intermediate multibin DNN lamM2
    'SRNN-int-200mHH500-lamM2' : l_SR_int + l_200mHH500 + l_NNlamM2,
    'SRNN-int-500mHH600-lamM2' : l_SR_int + l_500mHH600 + l_NNlamM2,
    'SRNN-int-600mHH-lamM2'    : l_SR_int + l_600mHH    + l_NNlamM2,

    # Boosted multibin DNN lamM2
    'SRNN-bst-500mHH800-lamM2' : l_SR_bst + l_500mHH800 + l_NNlamM2,
    'SRNN-bst-800mHH-lamM2'    : l_SR_bst + l_800mHH    + l_NNlamM2,

    #------------------------------------------------
    # DNN trained on k(lambda) = -5

    # Resolved multibin DNN lamM5
    'SRNN-res-200mHH250-lamM5' : l_SR_res + l_200mHH250 + l_NNlamM5,
    'SRNN-res-250mHH300-lamM5' : l_SR_res + l_250mHH300 + l_NNlamM5,
    'SRNN-res-300mHH350-lamM5' : l_SR_res + l_300mHH350 + l_NNlamM5,
    'SRNN-res-350mHH400-lamM5' : l_SR_res + l_350mHH400 + l_NNlamM5,
    'SRNN-res-400mHH500-lamM5' : l_SR_res + l_400mHH500 + l_NNlamM5,
    'SRNN-res-500mHH-lamM5'    : l_SR_res + l_500mHH    + l_NNlamM5,

    # Intermediate multibin DNN lamM5
    'SRNN-int-200mHH500-lamM5' : l_SR_int + l_200mHH500 + l_NNlamM5,
    'SRNN-int-500mHH600-lamM5' : l_SR_int + l_500mHH600 + l_NNlamM5,
    'SRNN-int-600mHH-lamM5'    : l_SR_int + l_600mHH    + l_NNlamM5,

    # Boosted multibin DNN lamM5
    'SRNN-bst-500mHH800-lamM5' : l_SR_bst + l_500mHH800 + l_NNlamM5,
    'SRNN-bst-800mHH-lamM5'    : l_SR_bst + l_800mHH    + l_NNlamM5,
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
