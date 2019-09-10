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
import gc
import argparse

parser = argparse.ArgumentParser(description='Normalize low-Tag and ttbar backgrounds to data for boosted hh to 4b.')
parser.add_argument('-i','--inputFile',type=str, default='./myNtuple.root', help='Name of the input ntuple.')
args = parser.parse_args()


# This program applies a trained NN to a set of ntuples, adding a new branches
# for the signal NN score. It will produce appended copies of the original
# ntuples in the directory you run it from.

inFilepath = args.inputFile

def main():
  # Path of the directory containing your filelists.
  # I've assumed they're named "resolved.txt", "intermediate.txt", and "boosted.txt"
  #fileListLocation = "/home/balunas/pheno/neuralnet/filelists/toAppend"
  fileListLocation = "./datasets_to_append/new_split_ntuples"
  # Path of the directory containing your trained NN and scaler files.
  # I've assumed they have the standard auto-generated names.

  nnLocation = "/home/paredes/pheno/testnn/pheno_study/analysis/neuralnet/train_all_jets"

  nnPathVarlambda = "/home/paredes/pheno/testnn/pheno_study/analysis/neuralnet/train_lambdai_vs_bkg"
  nnPathAlllambda = "/home/paredes/pheno/testnn/pheno_study/analysis/neuralnet/train_alllambda_vs_bkg"
  lambdaVarList = [
    "20.0", 
    "10.0",
    "7.0",
    "5.0",
    "3.0",
    "2.0",
    "1.0",
    "0.5",
    "m0.5",
    "m1.0",
    "m2.0",
    "m5.0",
    "m7.0",
    "m10.0",
    "m20.0"
  ]

  nnFile = ""
  inTreeName = "preselection"
  
  # List of variables the NN uses (must exactly match the one used to build the NN)
  branchList = ["pT_hh","m_hh",
                "nMuon", "nElec",
                "h1_M", "h1_Pt", "h1_Eta", "h1_Phi", "h1_j1_j2_dR",
                "h2_M", "h2_Pt", "h2_Eta", "h2_Phi", "h2_j1_j2_dR",
                "met_Et", "met_Phi",
                "h1_j1_BTag","h1_j2_BTag","h2_j1_BTag","h2_j2_BTag"
                ]
  #for analysis in ["boosted"]:
  for analysis in ["resolved"]:
    
    # dictionary to store all nn names
    nnFilePaths = MyDict()
    scalerPaths = MyDict()
    nnFilePaths["all"] = nnPathAlllambda + "/nn_all_jets_" + analysis + "_allLambdas.h5" 
    scalerPaths["all"] = nnPathAlllambda + "/scaler_" + analysis + "_allLambdas.sav" 
    for var in lambdaVarList:
      nnFilePaths[var] = nnPathVarlambda + "/nn_all_jets_" + analysis + "_SlfCoup_" + var + ".h5" 
      scalerPaths[var] = nnPathVarlambda + "/scaler_" + analysis + "_SlfCoup_" + var + ".sav" 

    nnList = lambdaVarList.copy()
    nnList.append("all")

    # Read in the list of ntuple files we want to append and loop over them.
    # create a dictionary to store scores for all networks and event types
    scoreBranch = MyDict()

    # Load the input file and grab the data from it.
    inArray = root2array(inFilepath, branches=branchList, treename=inTreeName)
    inFile = ROOT.TFile.Open(inFilepath)
    inTree = inFile.Get(inTreeName)

    # Silly hack to remove stuctured dtype
    inDF = pandas.DataFrame(inArray)
    inArray = inDF.values
    print("Processing", inFilepath)


    for net in nnList:

      # Scale input features to mean=0, stddev=1
      scaler = joblib.load(scalerPaths[net])
      inArray = scaler.transform(inArray)

      # Load the NN from file
      model = keras.models.load_model(nnFilePaths[net])

      # Run validation sample through the NN
      scores = model.predict(inArray,batch_size=None)
      # Convert to 1D basic python arrays
      # 0 == signal; 1 == qcd; 2 == ttbar
      scores_sig = scores[:,0].tolist()
      scores_qcd = scores[:,1].tolist()
      scores_top = scores[:,2].tolist()
      #print("mean sig score = ", statistics.mean(scores_sig))
      #print("mean qcd score = ", statistics.mean(scores_qcd))
      #print("mean top score = ", statistics.mean(scores_top))
      # Give it the correct numpy array structure for a branch
      namePrefix = 'nnscore_SlfCoup_'+net
      if net == "all":
        namePrefix = 'nnscore_all'
      scoreBranch[net]["sig"] = np.array(scores_sig, dtype=[(namePrefix+'_sig', np.float32)])
      scoreBranch[net]["qcd"] = np.array(scores_qcd, dtype=[(namePrefix+'_qcd', np.float32)])
      scoreBranch[net]["top"] = np.array(scores_top, dtype=[(namePrefix+'_top', np.float32)])
      del scores
      gc.collect()
      inArray = scaler.inverse_transform(inArray)

    # Create output file
    nameSuffix =  "_background_withNNs.root"
    if inFilepath.find("signal") > 0:
      nameSuffix =  "_withNNs.root"
    outFilepath = inFilepath.replace(".root", nameSuffix).split('/')[-1]
    #print("Writing output to", outFilepath)
    outFile = ROOT.TFile("out_all_nns/"+outFilepath, 'recreate')
    # Make a copy of the input tree
    outTree = inTree.CloneTree()
    # Add our NN score branch to the copy
    for net in nnList:
      array2tree(scoreBranch[net]["sig"], tree=outTree)
      array2tree(scoreBranch[net]["qcd"], tree=outTree)
      array2tree(scoreBranch[net]["top"], tree=outTree)
    # Write the augmented tree to output file
    outTree.Write()

    inFile.Close()
    outFile.Close()
    gc.collect()

class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val

if __name__ == "__main__":
  main()

