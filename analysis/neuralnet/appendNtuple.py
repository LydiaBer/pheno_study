import statistics
import getopt, sys
import numpy as np
from numpy import linspace
import pandas
import math
from sklearn.preprocessing import StandardScaler
import root_numpy
from ROOT import gSystem
from root_numpy import root2array, array2tree
import time
import keras
from keras.models import Sequential
from math import sqrt
from sklearn.externals import joblib
import ROOT

# This program applies a trained NN to a set of ntuples, adding a new branches
# for the signal NN score. It will produce appended copies of the original
# ntuples in the directory you run it from.

def main(argv):

    # Path of the directory containing your filelists.
    # I've assumed they're named "resolved.txt", "intermediate.txt", and "boosted.txt"
    fileListLocation = "/home/balunas/pheno/neuralnet/filelists/toAppend"
    # Path of the directory containing your trained NN and scaler files.
    # I've assumed they have the standard auto-generated names.
    nnLocation = "/home/balunas/pheno/neuralnet/training"


    inFileList = ""
    nnFile = ""
    inTreeName = "preselection"

    for analysis in ["resolved", "intermediate", "boosted"]:

        inFileList = fileListLocation + "/" + analysis + ".txt"
        nnFilepath = nnLocation + "/nn_" + analysis + ".h5"
        scalerFilepath = nnLocation + "/scaler_" + analysis + ".sav"

        # List of variables the NN uses (must exactly match the one used to build the NN)
        branchList = ["pT_hh", "dPhi_hh",
                      "h1_M", "h1_Pt", "h1_Eta", "h1_j1_j2_dR",
                      "h2_M", "h2_Pt", "h2_Eta", "h2_j1_j2_dR"]

        # Read in the list of ntuple files we want to append and loop over them.
        f = open(inFileList,"r")
        for line in f:
            inFilepath = line.rstrip()

            # Load the input file and grab the data from it.
            inArray = root2array(inFilepath, branches=branchList, treename=inTreeName)
            inFile = ROOT.TFile.Open(inFilepath)
            inTree = inFile.Get(inTreeName)
            print("Processing", inFilepath, len(inArray), "events found")

            # Silly hack to remove stuctured dtype
            inDF = pandas.DataFrame(inArray)
            inArray = inDF.values

            # Scale input features to mean=0, stddev=1
            scaler = joblib.load(scalerFilepath)
            inArray = scaler.fit_transform(inArray)

            # Load the NN from file
            model = keras.models.load_model(nnFilepath)

            # Run validation sample through the NN
            scoresRaw = model.predict(inArray)
            # Gonvert to 1D basic python array
            scores = scoresRaw[:,0].tolist()
            print("mean score = ", statistics.mean(scores))
            # Give it the correct numpy array structure for a branch
            scoreBranch = np.array(scores, dtype=[('nnscore', np.float32)])

            # Create output file
            outFilepath = inFilepath.replace(".root", "_withNN.root").split('/')[-1]
            #print("Writing output to", outFilepath)
            outFile = ROOT.TFile(outFilepath, 'recreate')
            # Make a copy of the input tree
            outTree = inTree.CloneTree()
            # Add our NN score branch to the copy
            array2tree(scoreBranch, tree=outTree)
            # Write the augmented tree to output file
            outTree.Write()

            inFile.Close()
            outFile.Close()

        f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
