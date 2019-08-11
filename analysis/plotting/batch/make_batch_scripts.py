#!/usr/bin/env python
'''
Welcome to make_batch_scripts.py
  - This is called on the first setup to make the torque and condor batch submission scripts
  - These are made to live in torque/ and condor/ directories
  - If they are unsatisfactory, modify the content of this script and rerun it to regenerate those batch scripts
  - A helpful guide for condor batch submission is http://batchdocs.web.cern.ch/batchdocs/local/submit.html
'''

import sys, os, time, argparse


#____________________________________________________________________________
def main():

  mk_batch_script( 'torque', 'plot' )
  mk_batch_script( 'torque', 'make_cutflow', True )
  mk_batch_script( 'torque', 'ntuples_to_chiSq', False, True)
  #mk_batch_script( 'condor', 'plot' )


#_________________________________________________________________________
def mk_batch_script( batch_type, plotscript, cutflow = False, chi2 = False):
  '''
  Make the batch script program that the cluster computer core runs
  '''

  # Get current working directory
  cwd = os.getcwd()

  # Name batch submission script
  script_name = '{0}/{1}_{2}.sh'.format( cwd, batch_type, plotscript )
  print( 'Present working directory is {0}'.format(cwd) )
  print( 'Making script {0}'.format(script_name) )

  # Write the following lines to the batch submission script
  with open(script_name, 'w') as f_script:
    f_script.write( '#!/bin/bash\n' )

    if 'torque' in batch_type:
      f_script.write('#PBS -m n\n#PBS -N "plot_physics"\n' )

    f_script.write( '# Batch script for {0} submission created by plotting/batch/make_batch_scripts.py\n'.format(batch_type) )
    f_script.write( 'cd {0} ; cd ../../.. \n'.format(cwd) )
    f_script.write( 'source setup.sh ; cd analysis/plotting\n' )


    if cutflow:
      if 'torque' in batch_type:
        f_script.write( './'+plotscript+'.py -s $CUTSEL -o $ONESAMPLE\n' )
      if 'condor' in batch_type:
        f_script.write( './'+plotscript+'.py -s $1 -o $2\n' )
    elif chi2:
      if 'torque' in batch_type:
        f_script.write( './'+plotscript+'.py -s $CUTSEL\n' )
      if 'condor' in batch_type:
        f_script.write( './'+plotscript+'.py -s $1\n' )
    else:
      if 'torque' in batch_type:
        f_script.write( './'+plotscript+'.py -s $CUTSEL -v $VARIABLE\n' )
      if 'condor' in batch_type:
        f_script.write( './'+plotscript+'.py -s $1 -v $2\n' )

#_______________________________
if __name__ == "__main__":
  main()
