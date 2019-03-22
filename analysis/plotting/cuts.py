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
def configure_cuts(var, cut_sel, print_cuts=True):

  ''' 
  Can define multiple lists and combine them
  e.g. to create different analysis regions CR, VR, SR
  '''

  l_ntag4 = [
    '(ntag>3)',
  ]  

  l_SR_resolved = ['n_large_jets == 0',
                   'n_small_jets >= 4',
                   #'n_bjets_in_higgs1 >= 2',
                   #'n_bjets_in_higgs2 >= 2',
  ]

  l_SR_intermediate = ['n_large_jets == 1',
                       #'n_bjets_in_higgs1 >= 2',
                       #'n_bjets_in_higgs2 >= 2',
  ]

  l_SR_boosted = ['n_large_jets == 2',
                  #'n_bjets_in_higgs1 >= 2',
                  #'n_bjets_in_higgs2 >= 2',
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
    'resolved'     : l_SR_resolved,
    'intermediate' : l_SR_intermediate,
    'boosted'      : l_SR_boosted,
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
