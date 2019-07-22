import statistics
import collections
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
    #fileListLocation = "/home/balunas/pheno/neuralnet/filelists/toAppend"
    fileListLocation = "../datasets_to_append/"
    # Path of the directory containing your trained NN and scaler files.
    # I've assumed they have the standard auto-generated names.
    nnLocation = "/home/paredes/pheno/testnn/pheno_study/analysis/neuralnet/train_all_jets"


    inFileList = ""
    nnFile = ""
    inTreeName = "preselection"
    # parameter strings of the two networks that were trained
    networks = ["all_jets_LR0p005"]
    
    for analysis in ["boosted"]:
    #for analysis in ["boosted", "intermediate", "resolved"]:
      #inFileList = fileListLocation + "/" + analysis + ".txt"
      inFileList = "test_append.txt"
      # List of variables the NN uses (must exactly match the one used to build the NN)
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
                    "h1_j1_BTag","h1_j2_BTag","h2_j1_BTag","h2_j2_BTag"]
      # Read in the list of ntuple files we want to append and loop over them.
      f = open(inFileList,"r")
      for line in f:
        # create a dictionary to store scores for all networks and event types
        scoreBranch = MyDict()
        for net in networks:
          nnFilepath = nnLocation + "/nn_all_jets_noTags_" + analysis + net + ".h5"
            
          scalerFilepath = nnLocation + "/scaler_" + analysis + net + ".sav"
          if analysis == "boosted":
            nnFilepath = nnLocation + "/nn_all_jets_noTags_boostedall_jets_LR5e-05.h5"
            scalerFilepath = nnLocation + "/scaler_boostedall_jets_LR5e-05.sav"

          inFilepath = line.rstrip()

          # Load the input file and grab the data from it.
          inArray = root2array(inFilepath, branches=branchList, treename=inTreeName)
          inFile = ROOT.TFile.Open(inFilepath)
          inTree = inFile.Get(inTreeName)
          print("Processing", inFilepath,"with", nnFilepath,"and",scalerFilepath, len(inArray), "events found")

          # Silly hack to remove stuctured dtype
          inDF = pandas.DataFrame(inArray)
          inArray = inDF.values

          # Scale input features to mean=0, stddev=1
          scaler = joblib.load(scalerFilepath)
          inArray = scaler.fit_transform(inArray)

          # Load the NN from file
          model = keras.models.load_model(nnFilepath)

          # Run validation sample through the NN
          scores = model.predict(inArray,batch_size=None)
          # Convert to 1D basic python arrays
          # 0 == signal; 1 == qcd; 2 == ttbar
          scores_sig = scores[:,0].tolist()
          scores_qcd = scores[:,1].tolist()
          scores_top = scores[:,2].tolist()
          print("mean sig score = ", statistics.mean(scores_sig))
          print("mean qcd score = ", statistics.mean(scores_qcd))
          print("mean top score = ", statistics.mean(scores_top))
          # Give it the correct numpy array structure for a branch
          scoreBranch[net]["sig"] = np.array(scores_sig, dtype=[('nnscore_'+net+'_sig', np.float32)])
          scoreBranch[net]["qcd"] = np.array(scores_qcd, dtype=[('nnscore_'+net+'_qcd', np.float32)])
          scoreBranch[net]["top"] = np.array(scores_top, dtype=[('nnscore_'+net+'_top', np.float32)])

        # Create output file
        outFilepath = inFilepath.replace(".root", "_withNNs.root").split('/')[-1]
        #print("Writing output to", outFilepath)
        outFile = ROOT.TFile(outFilepath, 'recreate')
        # Make a copy of the input tree
        outTree = inTree.CloneTree()
        # Add our NN score branch to the copy
        for net in networks:
          array2tree(scoreBranch[net]["sig"], tree=outTree)
          array2tree(scoreBranch[net]["qcd"], tree=outTree)
          array2tree(scoreBranch[net]["top"], tree=outTree)
        # Write the augmented tree to output file
        outTree.Write()

        inFile.Close()
        outFile.Close()

      f.close()

class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val

if __name__ == "__main__":
    main(sys.argv[1:])
