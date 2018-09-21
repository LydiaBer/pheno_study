#!/bin/sh 
#PBS -l nodes=1:ppn=8
#PBS -l cput=11:59:59
#PBS -l walltime=11:59:59
#PBS -l mem=16gb

# Setup stuff
echo "Setting up"
cd $CODEDIR
source ../../setup.sh
# source /cvmfs/sft.cern.ch/lcg/views/dev4/latest/x86_64-slc6-gcc7-opt/setup.sh

# Run
echo "Running: "
echo $CMD
$CMD

                                                                                                                                                       
           




