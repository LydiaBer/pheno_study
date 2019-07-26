#!/usr/bin/env python
'''
Welcome. This script:
  - submits plot.py with various variables and regions to pplxint batch system
'''

import sys, os, time, argparse

#____________________________________________________________________________
def main():

  doTorque = False
  doCondor = False

  # Parse in arguments
  parser = argparse.ArgumentParser(description='Submit plots to batch system.')
  #parser.add_argument('-f', '--fitType',  type=str, nargs='?', help='Fit type. Choose from (bkg, excl, disc, simp)', default='bkg')
  parser.add_argument('--doTorque', action='store_true', help='Submit to torque batch system.')
  parser.add_argument('--doCondor', action='store_true', help='Submit to condor batch system.')

  args = parser.parse_args()
  if args.doTorque:
    print('Submitting to torque batch system...')
    doTorque = True
  if args.doCondor:
    print('Submitting to condor batch system...')
    doCondor = True

  if (not doTorque) and (not doCondor):
    print('Not submitting any jobs as no batch system was specified.')
    print('Please use flag --doTorque or --doCondor to select batch system to submit to.')
    sys.exit()

  mk_batch_scripts(doTorque, doCondor)

#_________________________________________________________________________
def mk_batch_scripts(doTorque=False, doCondor=False):
  '''
  configure f_in, f_out, selector and batch script name to send to batch
  '''

  print 'making batch scripts...'

  submit = True

  cut_sels = [
  'resolved-preselection',
  'intermediate-preselection',
  'boosted-preselection',
  #'resolved-commonSR',
  #'intermediate-commonSR',
  #'boosted-commonSR',
  #'resolved-finalSR',
  #'intermediate-finalSR',
  #'boosted-finalSR',
  ]

  my_vars = [
   'n_small_tag',
   'n_small_jets',
   'n_large_tag',
   'n_large_jets',
   'n_track_tag',
   'n_track_jets',
   'n_jets_in_higgs1',
   'n_jets_in_higgs2',
   'n_bjets_in_higgs1',
   'n_bjets_in_higgs2',
   'nElec',
   'nMuon',

   'm_hh',
   'pT_hh',
   'dR_hh',
   'dEta_hh',
   'dPhi_hh',

   'h1_M',
   'h1_Pt',
   'h1_Eta',
   'h1_Phi',
   'h1_j1_M',
   'h1_j1_Pt',
   'h1_j1_Eta',
   'h1_j1_Phi',
   'h1_j1_BTagWeight',
   'h1_j2_M',
   'h1_j2_Pt',
   'h1_j2_Eta',
   'h1_j2_Phi',
   'h1_j2_BTagWeight',
   'h1_j1_dR',
   'h1_j2_dR',
   'h1_j1_j2_dR',

   'h2_M',
   'h2_Pt',
   'h2_Eta',
   'h2_Phi',
   'h2_j1_M',
   'h2_j1_Pt',
   'h2_j1_Eta',
   'h2_j1_Phi',
   'h2_j1_BTagWeight',
   'h2_j2_M',
   'h2_j2_Pt',
   'h2_j2_Eta',
   'h2_j2_Phi',
   'h2_j2_BTagWeight',
   'h2_j1_dR',
   'h2_j2_dR',
   'h2_j1_j2_dR',

   'elec1_Pt',
   'elec1_Eta',
   'elec1_Phi',
   'muon1_Pt',
   'muon1_Eta',
   'muon1_Phi',

   'met_Et',
   'met_Phi',
    ]

  my_vars = [
   'm_hh',
   'h1_M',
   'h2_M',
   'h1_Pt',
   'h2_Pt',
    ]
  
  script_name = 'torque_plot.sh'
  
  if doCondor:
    print('Writing submission arguments to a file for condor')
    with open('sig_reg_var.txt', 'w') as f_sr_var:
      for var in my_vars:
        for sigReg in sig_regs:
          f_sr_var.write( '{0} {1}\n'.format(cut_sel, var) )

    if submit:
      cmd = 'condor_submit condor_plot.sub'
      os.system(cmd)

  if doTorque:
    for var in my_vars:
      for cut_sel in cut_sels:    
        print('cut_sel: {0}, var: {1}'.format(cut_sel, var) )
        cmd   = "qsub -l walltime=01:59:00 -l cput=01:59:00 -v VARIABLE='{0}',CUTSEL='{1}' {2}".format(var, cut_sel, script_name)
        #cmd   = "qsub -l walltime=15:59:00 -l cput=15:59:00 -v var='{0}',sig_reg='{1}' {2}".format(var, sigReg, script_name)
        if submit:
          os.system(cmd)

#_______________________________
if __name__ == "__main__":
  main()


