import ROOT
import numpy as np
import root_numpy
from root_numpy import root2array

# This converts a flat ntuple into a numpy array file, which is the input
# format used by keras in our setup. Creates one .npz file per analysis in the
# directory where you run it.

# Location of the lists of ntuples you want to convert to numpy format.
# I've assumed that the file lists are named following my convention.
# e.g. "signalFiles_resolved.txt"
fileListLocation = "../datasets_to_train/"
#fileListLocation = "../datasets_to_validate/"

# Name of the tree we want to use
treeName = "preselection"

# Prefix for the name of the output .npz files
outputPrefix = "trainingData_all_jets_noTags_"
#outputPrefix = "validationData_"

for analysis in ["resolved", "intermediate", "boosted"]:
    inFile_sig   = fileListLocation + "/signalFiles_" + analysis + ".txt"
    inFile_4b    = fileListLocation + "/4bFiles_" + analysis + ".txt"
    inFile_2b2j  = fileListLocation + "/2b2jFiles_" + analysis + ".txt"
    inFile_ttbar = fileListLocation + "/ttbarFiles_" + analysis + ".txt"

    branchList = ["pT_hh",
                  "nMuon", "nElec",
                  "h1_M", "h1_Pt", "h1_Eta", "h1_Phi", "h1_j1_j2_dR",
                  "h2_M", "h2_Pt", "h2_Eta", "h2_Phi", "h2_j1_j2_dR",
                  "h1_j1_M", "h1_j1_Pt", "h1_j1_Eta", "h1_j1_Phi", 
                  "h1_j2_M", "h1_j2_Pt", "h1_j2_Eta", "h1_j2_Phi", 
                  "h2_j1_M", "h2_j1_Pt", "h2_j1_Eta", "h2_j1_Phi", 
                  "h2_j2_M", "h2_j2_Pt", "h2_j2_Eta", "h2_j2_Phi", 
                  "muon1_M", "muon1_Pt", "muon1_Eta", "muon1_Phi", 
                  "elec1_M", "elec1_Pt", "elec1_Eta", "elec1_Phi", 
                  "met_Et", "met_Phi", 
                  "mc_sf"]

    filepaths_sig   = []
    filepaths_4b    = []
    filepaths_2b2j  = []
    filepaths_ttbar = []

    f = open(inFile_sig,"r")
    for line in f:
        filepaths_sig.append(line.rstrip())
    f.close()

    f = open(inFile_4b,"r")
    for line in f:
        filepaths_4b.append(line.rstrip())
    f.close()

    f = open(inFile_2b2j,"r")
    for line in f:
        filepaths_2b2j.append(line.rstrip())
    f.close()

    f = open(inFile_ttbar,"r")
    for line in f:
        filepaths_ttbar.append(line.rstrip())
    f.close()

    dat_sig   = root2array(filepaths_sig,   branches=branchList, treename=treeName)
    dat_4b    = root2array(filepaths_4b,    branches=branchList, treename=treeName)
    dat_2b2j  = root2array(filepaths_2b2j,  branches=branchList, treename=treeName)
    dat_ttbar = root2array(filepaths_ttbar, branches=branchList, treename=treeName)

    np.savez(outputPrefix + analysis + ".npz", sig=dat_sig, bkg_4b=dat_4b, bkg_2b2j=dat_2b2j, bkg_ttbar=dat_ttbar)
