#!/usr/bin/env python
'''
Welcome to HiggsinoFitter make_batch_scripts.py
  - This is called on the first setup to make the torque and condor batch submission scripts
  - These are made to live in torque/ and condor/ directories
  - If they are unsatisfactory, modify the content of this script and rerun it to regenerate those batch scripts
  - A helpful guide for condor batch submission is http://batchdocs.web.cern.ch/batchdocs/local/submit.html
'''

import sys, os, time, argparse

TOP_dir = '/data/atlas/atlasdata/jesseliu/pheno/fcc/hh4b/analysis_code/github/2019mar21/pheno_study'

#____________________________________________________________________________
def main():

  mk_batch_script( 'torque' )
  mk_batch_script( 'condor' )


#_________________________________________________________________________
def mk_batch_script( batch_type ):
  '''
  Make the batch script program that the cluster computer core runs
  '''


  # Name batch submission script
  script_name = '{0}/analysis/plotting/batch/{1}_plot.sh'.format( TOP_dir, batch_type )
  # Write the following lines to the batch submission script
  with open(script_name, 'w') as f_script:
    f_script.write( '#!/bin/bash\n' )

    if 'torque' in batch_type:
      f_script.write('#PBS -m n\n#PBS -N "plot_physics"\n' )

    f_script.write( '# Batch script for {0} submission created by plotting/batch/make_batch_scripts.py\n'.format(batch_type) )
    f_script.write( 'cd {0}\n'.format(TOP_dir) )
    f_script.write( 'source setup.sh ; cd analysis/plotting\n' )
    
    if 'torque' in batch_type:
      f_script.write( './plot.py -s $SIGREG -v $VARIABLE\n' )
    if 'condor' in batch_type:
      f_script.write( './plot.py -s $1 -v $2\n' )


#_______________________________
if __name__ == "__main__":
  main()
