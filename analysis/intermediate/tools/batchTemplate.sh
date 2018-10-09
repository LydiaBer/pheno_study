#!/bin/sh 
#PBS -l nodes=1:ppn=8
#PBS -l cput=59:59:59
#PBS -l walltime=59:59:59
#PBS -l mem=16gb

# Setup stuff
echo "Setting up"
cd $CODEDIR
source ../../setup.sh

# Run
echo "Running: "
echo $CMD
$CMD

                                                                                                                                                       
           




