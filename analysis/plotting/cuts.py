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
  #jesse_intermediate: ['n_large_jets == 1',
  #                       'pT_h1 > 200',
  #                       'n_small_jets >= 2',
  #                       'n_assoc_track_jets >= 2',
  #                       'n_assoc_track_tag >= 2',
  #                       'n_small_tag >= 1'
  #                       ]
  l_SR_resolved     = l_common + l_resolved     + l_resolved_SR 
  l_SR_intermediate = l_common + l_intermediate + l_intermediate_SR 
  l_SR_boosted      = l_common + l_boosted      + l_boosted_SR 

  l_NN_lambda_m20 = ['nnscore_SlfCoup_m20.0_qcd < 0.2', 
                     'nnscore_SlfCoup_m20.0_top < 0.2', 
                     'nnscore_SlfCoup_m20.0_sig > 0.85']

  l_NN_lambda_m10 = ['nnscore_SlfCoup_m10.0_qcd < 0.2', 
                     'nnscore_SlfCoup_m10.0_top < 0.2', 
                     'nnscore_SlfCoup_m10.0_sig > 0.85']

  l_NN_lambda_m7 = ['nnscore_SlfCoup_m7.0_qcd < 0.2', 
                    'nnscore_SlfCoup_m7.0_top < 0.2', 
                    'nnscore_SlfCoup_m7.0_sig > 0.85']

  l_NN_lambda_m5 = ['nnscore_SlfCoup_m5.0_qcd < 0.2', 
                    'nnscore_SlfCoup_m5.0_top < 0.2', 
                    'nnscore_SlfCoup_m5.0_sig > 0.85']

  l_NN_lambda_m2 = ['nnscore_SlfCoup_m2.0_qcd < 0.2', 
                    'nnscore_SlfCoup_m2.0_top < 0.2', 
                    'nnscore_SlfCoup_m2.0_sig > 0.85']

  l_NN_lambda_m1 = ['nnscore_SlfCoup_m1.0_qcd < 0.2', 
                    'nnscore_SlfCoup_m1.0_top < 0.2', 
                    'nnscore_SlfCoup_m1.0_sig > 0.85']

  l_NN_lambda_m0p5 = ['nnscore_SlfCoup_m0.5_qcd < 0.2', 
                      'nnscore_SlfCoup_m0.5_top < 0.2', 
                      'nnscore_SlfCoup_m0.5_sig > 0.85']

  l_NN_lambda_0p5=['nnscore_SlfCoup_0.5_qcd < 0.2', 
                   'nnscore_SlfCoup_0.5_top < 0.2', 
                   'nnscore_SlfCoup_0.5_sig > 0.85']

  l_NN_lambda_1  = ['nnscore_SlfCoup_1.0_qcd < 0.2', 
                    'nnscore_SlfCoup_1.0_top < 0.2', 
                    'nnscore_SlfCoup_1.0_sig > 0.85']

  l_NN_lambda_2  = ['nnscore_SlfCoup_2.0_qcd < 0.2', 
                    'nnscore_SlfCoup_2.0_top < 0.2', 
                    'nnscore_SlfCoup_2.0_sig > 0.85']

  l_NN_lambda_3  = ['nnscore_SlfCoup_3.0_qcd < 0.2', 
                    'nnscore_SlfCoup_3.0_top < 0.2', 
                    'nnscore_SlfCoup_3.0_sig > 0.85']

  l_NN_lambda_5  = ['nnscore_SlfCoup_5.0_qcd < 0.2', 
                    'nnscore_SlfCoup_5.0_top < 0.2', 
                    'nnscore_SlfCoup_5.0_sig > 0.85']

  l_NN_lambda_7  = ['nnscore_SlfCoup_7.0_qcd < 0.2', 
                    'nnscore_SlfCoup_7.0_top < 0.2', 
                    'nnscore_SlfCoup_7.0_sig > 0.85']

  l_NN_lambda_10 = ['nnscore_SlfCoup_10.0_qcd < 0.2', 
                    'nnscore_SlfCoup_10.0_top < 0.2', 
                    'nnscore_SlfCoup_10.0_sig > 0.85']

  l_NN_lambda_20 = ['nnscore_SlfCoup_20.0_qcd < 0.2', 
                    'nnscore_SlfCoup_20.0_top < 0.2', 
                    'nnscore_SlfCoup_20.0_sig > 0.85']


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

    'resolved-finalSR'          : l_common + l_resolved     + l_resolved_SR,
    'intermediate-finalSR'      : l_common + l_intermediate + l_intermediate_SR,
    'boosted-finalSR'           : l_common + l_boosted      + l_boosted_SR,

    'resolved-finalSRNNQCD'     : l_common + l_resolved     + l_resolved_SR +     ['nnscore_SlfCoup_1.0_qcd < 0.2'],
    'intermediate-finalSRNNQCD' : l_common + l_intermediate + l_intermediate_SR + ['nnscore_SlfCoup_1.0_qcd < 0.2'],
    'boosted-finalSRNNQCD'      : l_common + l_boosted      + l_boosted_SR +      ['nnscore_SlfCoup_1.0_qcd < 0.2'],

    'resolved-finalSRNNQCDTop'     : l_common + l_resolved     + l_resolved_SR +     ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.2'],
    'intermediate-finalSRNNQCDTop' : l_common + l_intermediate + l_intermediate_SR + ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'],
    'boosted-finalSRNNQCDTop'      : l_common + l_boosted      + l_boosted_SR +      ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'],

    'resolved-finalSRNNlow'     : l_common + l_resolved +     l_resolved_SR +     ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.2'] + ['nnscore_SlfCoup_1.0_sig <= 0.85'],
    'intermediate-finalSRNNlow' : l_common + l_intermediate + l_intermediate_SR + ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_1.0_sig <= 0.85'],
    'boosted-finalSRNNlow'      : l_common + l_boosted +      l_boosted_SR +      ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_1.0_sig <= 0.85'],

    'resolved-finalSRNN'        : l_common + l_resolved +     l_resolved_SR +     ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.2'] + ['nnscore_SlfCoup_1.0_sig > 0.85'],
    'intermediate-finalSRNN'    : l_common + l_intermediate + l_intermediate_SR + ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_1.0_sig > 0.85'],
    'boosted-finalSRNN'         : l_common + l_boosted +      l_boosted_SR +      ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_1.0_sig > 0.85'],

    'resolved-finalSRNNlamm5'        : l_common + l_resolved +     l_resolved_SR +     ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.2'] + ['nnscore_SlfCoup_m5.0_sig > 0.85'],
    'intermediate-finalSRNNlamm5'    : l_common + l_intermediate + l_intermediate_SR + ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_m5.0_sig > 0.85'],
    'boosted-finalSRNNlamm5'         : l_common + l_boosted +      l_boosted_SR +      ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_m5.0_sig > 0.85'],

    'resolved-finalSRNNlam10'        : l_common + l_resolved +     l_resolved_SR +     ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.2'] + ['nnscore_SlfCoup_10.0_sig > 0.85'],
    'intermediate-finalSRNNlam10'    : l_common + l_intermediate + l_intermediate_SR + ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_10.0_sig > 0.85'],
    'boosted-finalSRNNlam10'         : l_common + l_boosted +      l_boosted_SR +      ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_10.0_sig > 0.85'],

    'resolved-finalSRNNlam10low'        : l_common + l_resolved +     l_resolved_SR +     ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.2'] + ['nnscore_SlfCoup_10.0_sig <= 0.85'],
    'intermediate-finalSRNNlam10low'    : l_common + l_intermediate + l_intermediate_SR + ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_10.0_sig <= 0.85'],
    'boosted-finalSRNNlam10low'         : l_common + l_boosted +      l_boosted_SR +      ['nnscore_SlfCoup_1.0_qcd < 0.2'] + ['nnscore_SlfCoup_1.0_top < 0.1'] + ['nnscore_SlfCoup_10.0_sig <= 0.85'],

    'resolved-finalSRNNSig'     : l_common + l_resolved     + l_resolved_SR +     ['nnscore_SlfCoup_1.0_sig > 0.6'],
    'intermediate-finalSRNNSig' : l_common + l_intermediate + l_intermediate_SR + ['nnscore_SlfCoup_1.0_sig > 0.6'],
    'boosted-finalSRNNSig'      : l_common + l_boosted      + l_boosted_SR +      ['nnscore_SlfCoup_1.0_sig > 0.6'],

    'resolved-finalSRNNlam_m20'     : l_SR_resolved     + l_NN_lambda_m20,
    'intermediate-finalSRNNlam_m20' : l_SR_intermediate + l_NN_lambda_m20,
    'boosted-finalSRNNlam_m20'      : l_SR_boosted      + l_NN_lambda_m20,

    'resolved-finalSRNNlam_m10'     : l_SR_resolved     + l_NN_lambda_m10,
    'intermediate-finalSRNNlam_m10' : l_SR_intermediate + l_NN_lambda_m10,
    'boosted-finalSRNNlam_m10'      : l_SR_boosted      + l_NN_lambda_m10,

    'resolved-finalSRNNlam_m7'     : l_SR_resolved     + l_NN_lambda_m7,
    'intermediate-finalSRNNlam_m7' : l_SR_intermediate + l_NN_lambda_m7,
    'boosted-finalSRNNlam_m7'      : l_SR_boosted      + l_NN_lambda_m7,

    'resolved-finalSRNNlam_m5'     : l_SR_resolved     + l_NN_lambda_m5,
    'intermediate-finalSRNNlam_m5' : l_SR_intermediate + l_NN_lambda_m5,
    'boosted-finalSRNNlam_m5'      : l_SR_boosted      + l_NN_lambda_m5,

    'resolved-finalSRNNlam_m2'     : l_SR_resolved     + l_NN_lambda_m2,
    'intermediate-finalSRNNlam_m2' : l_SR_intermediate + l_NN_lambda_m2,
    'boosted-finalSRNNlam_m2'      : l_SR_boosted      + l_NN_lambda_m2,

    'resolved-finalSRNNlam_m1'     : l_SR_resolved     + l_NN_lambda_m1,
    'intermediate-finalSRNNlam_m1' : l_SR_intermediate + l_NN_lambda_m1,
    'boosted-finalSRNNlam_m1'      : l_SR_boosted      + l_NN_lambda_m1,

    'resolved-finalSRNNlam_m0p5'     : l_SR_resolved     + l_NN_lambda_m0p5,
    'intermediate-finalSRNNlam_m0p5' : l_SR_intermediate + l_NN_lambda_m0p5,
    'boosted-finalSRNNlam_m0p5'      : l_SR_boosted      + l_NN_lambda_m0p5,

    'resolved-finalSRNNlam0p5'     : l_SR_resolved     + l_NN_lambda_0p5,
    'intermediate-finalSRNNlam0p5' : l_SR_intermediate + l_NN_lambda_0p5,
    'boosted-finalSRNNlam0p5'      : l_SR_boosted      + l_NN_lambda_0p5,

    'resolved-finalSRNN'          : l_SR_resolved     + l_NN_lambda_1,
    'intermediate-finalSRNN'      : l_SR_intermediate + l_NN_lambda_1,
    'boosted-finalSRNN'           : l_SR_boosted      + l_NN_lambda_1,

    'resolved-finalSRNNlam2'      : l_SR_resolved     + l_NN_lambda_2,
    'intermediate-finalSRNNlam2'  : l_SR_intermediate + l_NN_lambda_2,
    'boosted-finalSRNNlam2'       : l_SR_boosted      + l_NN_lambda_2,

    'resolved-finalSRNNlam3'      : l_SR_resolved     + l_NN_lambda_3,
    'intermediate-finalSRNNlam3'  : l_SR_intermediate + l_NN_lambda_3,
    'boosted-finalSRNNlam3'       : l_SR_boosted      + l_NN_lambda_3,

    'resolved-finalSRNNlam5'      : l_SR_resolved     + l_NN_lambda_5,
    'intermediate-finalSRNNlam5'  : l_SR_intermediate + l_NN_lambda_5,
    'boosted-finalSRNNlam5'       : l_SR_boosted      + l_NN_lambda_5,

    'resolved-finalSRNNlam7'      : l_SR_resolved     + l_NN_lambda_7,
    'intermediate-finalSRNNlam7'  : l_SR_intermediate + l_NN_lambda_7,
    'boosted-finalSRNNlam7'       : l_SR_boosted      + l_NN_lambda_7,

    'resolved-finalSRNNlam10'     : l_SR_resolved     + l_NN_lambda_10,
    'intermediate-finalSRNNlam10' : l_SR_intermediate + l_NN_lambda_10,
    'boosted-finalSRNNlam10'      : l_SR_boosted      + l_NN_lambda_10,

    'resolved-finalSRNNlam20'     : l_SR_resolved     + l_NN_lambda_20,
    'intermediate-finalSRNNlam20' : l_SR_intermediate + l_NN_lambda_20,
    'boosted-finalSRNNlam20'      : l_SR_boosted      + l_NN_lambda_20,



    #'SR-1ibsmall-2ibtrk' : l_SR_1ibsmall_2ibtrk,
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
