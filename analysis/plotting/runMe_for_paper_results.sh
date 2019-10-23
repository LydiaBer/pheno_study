#!/bin/bash
#----------------------------------------------------------
#
# Welcome to runMe_for_paper_results.sh
#
# Run this script to execute the sequence of python scripts
# to make (most of) the paper plots
# This also simply documents the order to run scripts
#
#----------------------------------------------------------

# Run plotting of the baseline and DNN analyses to get plots & yields
./plot.py

# Run over all signals, compare with bkg yields from plot.py to make chiSq, S/B etc
./ntuples_to_chiSq.py

# Combine the chiSq 
./combine_chiSq.py

# Make chiSq_ij vs lambda_i vs lambda_j info
./chiSq_2dlambda_discrPowerMatrix.py

# Make the 1d chiSq plots
./auto_chiSq_to_1Dlimit.py

# Make the 2d contour plots of chiSq
./chiSq_to_contour.py

# Make an overlay of the 68% CL contours in 2D for summary plot
./contours_to_summary.py

# Make the 1D 68% CL summary plot (need to hard code the limits in this script)
./summary_1dlimits.py

echo Finished.
