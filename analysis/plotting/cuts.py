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
