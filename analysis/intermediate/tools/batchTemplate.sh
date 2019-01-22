#!/bin/sh 
#PBS -l cput=11:59:59
#PBS -l walltime=11:59:59

# Setup stuff
echo "Setting up"
cd $CODEDIR
source ../../setup.sh

# Run
echo "Running: "
echo $CMD
$CMD

                                                                                                                                                       
           




