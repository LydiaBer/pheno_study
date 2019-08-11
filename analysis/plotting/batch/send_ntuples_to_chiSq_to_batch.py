#!/usr/bin/env python
'''
Welcome. This script:
  - submits ntuples_to_chiSq.py with various regions to pplxint batch system
'''

import sys, os, time, argparse

#____________________________________________________________________________
def main():

  doTorque = True
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

  #---------------------------------------------------
  # Cut selections to consider
  #---------------------------------------------------

  l_cut_sels = ['resolved-preselection', 'intermediate-preselection' ,'boosted-preselection',
                #'resolved-commonSR',     'intermediate-commonSR',     'boosted-commonSR',
                'resolved-finalSR',      'intermediate-finalSR',      'boosted-finalSR' ] 
  
  script_name = 'torque_ntuples_to_chiSq.sh'
  
  if doCondor:
    print('Writing submission arguments to a file for condor')
    with open('sig_reg_var.txt', 'w') as f_sr:
      for reg in l_cut_sels:
        f_sr.write( '{0} {1}\n'.format(reg) )

    if submit:
      cmd = 'condor_submit condor_ntuples_to_chiSq.sub'
      os.system(cmd)

  if doTorque:
    for reg in l_cut_sels:
      print('cut_sel: {0}'.format(reg) )
      cmd   = "qsub -l walltime=11:59:00 -l cput=11:59:00 -v CUTSEL='{0}' {1}".format(reg, script_name)
      if submit:
        os.system(cmd)

#_______________________________
if __name__ == "__main__":
  main()


