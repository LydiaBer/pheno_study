#!/usr/bin/env python
'''
Welcome. This script:
  - submits make_cutflow.py with various variables and regions to pplxint batch system
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
  configure batch script name to send to batch
  '''

  print 'making batch scripts...'

  submit = True

  cut_sels = ['resolved-finalSR', 'intermediate-finalSR' ,'boosted-finalSR', 'resolved-preselection', 'intermediate-preselection' ,'boosted-preselection'] 

  samp_sets = ['all','smallbkgs','mainbkgs','signals']
  
  script_name = 'torque_make_cutflow.sh'

  if doCondor:
    print('Writing submission arguments to a file for condor')
    with open('sig_reg_samp.txt', 'w') as f_sr_samp:
      for samp in samp_sets:
        for cut_sel in cut_sels:
          f_sr_samp.write( '{0} {1} {2}\n'.format(cut_sel, samp) )

    if submit:
      cmd = 'condor_submit condor_plot.sub'
      os.system(cmd)

  if doTorque:
    for samp in samp_sets:
      for cut_sel in cut_sels:    
        print('cut_sel: {0}, samp: {1}'.format(cut_sel, samp) )
        cmd   = "qsub -l walltime=01:59:00 -l cput=01:59:00 -v CUTSEL='{0}',ONESAMPLE='{1}' {2}".format(cut_sel, samp, script_name)
        if submit:
          print cmd
          os.system(cmd)
#_______________________________
if __name__ == "__main__":
  main()


