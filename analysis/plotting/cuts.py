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
def configure_cuts(var, sig_reg, print_cuts=True):

  ''' 
  Can define multiple lists and combine them
  e.g. to create different analysis regions CR, VR, SR
  '''

  l_masscut = [
    'm_hh>0.'
  ]  
  
  # =============================================
  d_cuts = {
    'masscut'     : l_masscut
  }
  # From cut lists
  l_cuts = d_cuts[sig_reg]
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
