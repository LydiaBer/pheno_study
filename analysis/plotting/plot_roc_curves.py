import statistics
import collections
import getopt, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from numpy import linspace
import pandas
import math
from sklearn.preprocessing import StandardScaler
import root_numpy
from ROOT import gSystem
from root_numpy import root2array
import time
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import plot_model
from math import sqrt
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
from scipy import interp
from itertools import cycle
import argparse



# This program trains a neural network based on input numpy array files.
# Output is one trained NN file (nn_*.h5) and one scaler file (scaler_*.sav)
# per analysis. Optionally also makes plots of the output distributions for the
# training sample.

### NOTE this program uses 0.2 of the data as a validation set

def main(argv):
  nnLocation = "/home/paredes/pheno/testnn/pheno_study/analysis/neuralnet/train_all_jets"

  nnPathVarlambda = "/home/paredes/pheno/testnn/pheno_study/analysis/neuralnet/train_lambdai_vs_bkg"
  nnPathAlllambda = "/home/paredes/pheno/testnn/pheno_study/analysis/neuralnet/train_alllambda_vs_bkg"
  lambdaVarList = [
    "1.0",
    "5.0"
    #"all",
  ]
  # Path of the directory containing .npz files to train on.
  # Standard naming convention is assumed (e.g. "trainingData_resolved.npz")
  trainingDataPath = "."

  # Training parameters
  numEpochs = 20
  batchSize = 100
  dropoutFraction = 0.3
  # initial learning rate for adamax
  init_lr = MyDict()
  init_lr["boosted"] = 5e-5
  init_lr["intermediate"] = 5e-3
  init_lr["resolved"] = 5e-3

  # store parameters of the network in a string
  #param_string = "_w_OPadamaxEP"+str(numEpochs)+"BS"+str(batchSize)+"DO"+str(dropoutFraction).replace(".","")
  # Plot score distributions for the training sample?
  makePlots = True
  
  target_nevents = 100000

  signal_weight = MyDict()
  ttbar_weight = MyDict()
  qcd_weight = MyDict()

  fileListLocation = "../datasets_to_validate/new_split_ntuples"

  # Name of the tree we want to use
  inTreeName = "preselection"
  
  # Prefix for the name of the output .npz files
  outputPrefix = "trainingData_all_jets_"
  #outputPrefix = "validationData_"
  
  fpr = MyDict()
  tpr = MyDict()
  roc_auc = MyDict()
  for net in lambdaVarList:
    for analysis in ["resolved", "intermediate","boosted"]:
    #for analysis in ["resolved","intermediate"]:
      nnFilePaths = MyDict()
      scalerPaths = MyDict()
      if net == "all":
        nnFilePaths["all"] = nnPathAlllambda + "/nn_all_jets_" + analysis + "_allLambdas.h5" 
        scalerPaths["all"] = nnPathAlllambda + "/scaler_" + analysis + "_allLambdas.sav" 
      else:
        nnFilePaths[net] = nnPathVarlambda + "/nn_all_jets_" + analysis + "_SlfCoup_" + net + ".h5" 
        scalerPaths[net] = nnPathVarlambda + "/scaler_" + analysis + "_SlfCoup_" + net + ".sav" 
      param_string = "_SlfCoup_"+net
      print ("paramters string "+param_string)

      print("Calculating ROC curves for " + analysis)
      # Load the input file and grab the data from it.
      # Label each type of background
      # Calculate weight for each 'target' sample

      inFile_sig   = fileListLocation + "/signalFiles_" + analysis + "_SlfCoup_"+net+".txt"
      inFile_4b    = fileListLocation + "/4bFiles_" + analysis + ".txt"
      inFile_2b2j  = fileListLocation + "/2b2jFiles_" + analysis + ".txt"
      inFile_ttbar = fileListLocation + "/ttbarFiles_" + analysis + ".txt"

      
      branchList = ["pT_hh","m_hh",
                    "nMuon", "nElec",
                    "h1_M", "h1_Pt", "h1_Eta", "h1_Phi", "h1_j1_j2_dR",
                    "h2_M", "h2_Pt", "h2_Eta", "h2_Phi", "h2_j1_j2_dR",
                    "met_Et", "met_Phi", 
                    "h1_j1_BTag","h1_j2_BTag","h2_j1_BTag","h2_j2_BTag",
                    "mc_sf"]
      
      nFeatures = len(branchList)-1
      
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
      
      dat_sig   = root2array(filepaths_sig,   branches=branchList, treename=inTreeName)
      dat_4b    = root2array(filepaths_4b,    branches=branchList, treename=inTreeName)
      dat_2b2j  = root2array(filepaths_2b2j,  branches=branchList, treename=inTreeName)
      dat_ttbar = root2array(filepaths_ttbar, branches=branchList, treename=inTreeName)
      
      #np.savez(outputPrefix + analysis + ".npz", sig=dat_sig, bkg_4b=dat_4b, bkg_2b2j=dat_2b2j, bkg_ttbar=dat_ttbar)


      signalData = pandas.DataFrame(dat_sig)
      signalData["target"] = 0
      signal_weight[analysis] = target_nevents/len(signalData)
      #print(len(signalData),"(",signal_weight[analysis],") signal (weight) events found")
      n_sig = len(signalData)

      backgroundData = pandas.DataFrame(dat_4b)
      backgroundData["target"] = 1
      #print(len(backgroundData), "4b background events found")

      background_2b2j = pandas.DataFrame(dat_2b2j)
      background_2b2j["target"] = 1
      #print(len(background_2b2j), "2b2j background events found")
      backgroundData = backgroundData.append(background_2b2j)
      #print("appended 2b2j to 4b")

      qcd_weight[analysis] = target_nevents/len(backgroundData)
      #print(len(backgroundData),"(",qcd_weight[analysis], ") qcd (weight) background events found")
      n_qcd = len(backgroundData)

      background_ttbar = pandas.DataFrame(dat_ttbar)
      background_ttbar["target"] = 2
      ttbar_weight[analysis] = target_nevents/len(background_ttbar)
      #print(len(background_ttbar),"(",ttbar_weight[analysis], ") ttbar (weight) background events found")
      backgroundData = backgroundData.append(background_ttbar)
      n_ttbar = len(background_ttbar)

      allData = signalData.append(backgroundData, ignore_index = True)

      sigW = 1 - n_sig/(n_ttbar+n_qcd+n_sig)
      qcdW = 1 - n_qcd/(n_ttbar+n_qcd+n_sig)
      sigW = 1 - n_ttbar/(n_ttbar+n_qcd+n_sig)
      #classWeight = [0:,1:,2:]

      # Set all event weights to 1 by default
      allData.loc[:, 'mc_sf'] = 1.
      # Apply manual event weighting: numbers that give "reasonable behavior"
      allData.loc[allData.target == 0, 'mc_sf'] = signal_weight[analysis] # signal
      allData.loc[allData.target == 1, 'mc_sf'] = qcd_weight[analysis]    # QCD
      allData.loc[allData.target == 2, 'mc_sf'] = ttbar_weight[analysis]  # ttbar

      # shuffle data to get representative validation set
      #allData = shuffle(allData)

      X_train = allData
      yTypeTrain = X_train.pop("target")

      # These aren't input features, separate them out.
      evtWeightsTrain = X_train.pop("mc_sf")

      # Convert pandas dataframes into numpy arrays
      X_train = X_train.values
      evtWeightsTrain = evtWeightsTrain.values
      y_train = keras.utils.to_categorical(yTypeTrain, num_classes=3)
      yTypeTrain = yTypeTrain.values


      # Convert this into the right format for keras

      # Scale input features to mean=0, stddev=1
      scaler = joblib.load(scalerPaths[net])
      X_train = scaler.transform(X_train)

      # Load the NN architecture
      model = keras.models.load_model(nnFilePaths[net])
      # Optionally, plot the output distributions for the training sample.

      # Run training sample back through the NN
      probTrain = model.predict(X_train)

      # Compute ROC curve and ROC area for each class
      for i in range(0,3):
        fpr[net][analysis][i], tpr[net][analysis][i], _ = roc_curve(y_train[:, i], probTrain[:, i])
        roc_auc[net][analysis][i] = auc(fpr[net][analysis][i], tpr[net][analysis][i])

    # Plot all ROC curves
    plt.figure(figsize=(8,8))
    plt.rcParams["font.size"] = "18"
    lw = 3
    colors = cycle(['red', 'blue', 'green'])
    types = ['-', '--', ':']
    for analysis,typ in zip(["resolved", "intermediate","boosted"],types):
      plt.plot(fpr[net][analysis][0], tpr[net][analysis][0], color='firebrick', lw=lw,linestyle=typ, label=analysis+' (AUC = {0:0.2f})'.format(roc_auc[net][analysis][0]))
    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    #custom_lines = [Line2D([0], [0], color='black', lw=3,linestyle = '-'),
    #                Line2D([0], [0], color='black', lw=3,linestyle = '--'),
    #                Line2D([0], [0], color='black', lw=3,linestyle = ':'),
    #                Line2D([0], [0], color='midnightblue', lw=3),
    #                Line2D([0], [0], color='seagreen', lw=3),
    #                Line2D([0], [0], color='firebrick', lw=3)]

    title_net =  net;
    if net.find('m') >= 0:
      title_net = title_net.replace('m','-')
    plt.title(' Signal Score ROC Curves, $\kappa_{\lambda}$ = '+title_net)
    #plt.legend(custom_lines,['resolved','intermediate','boosted','qcd score','ttbar score','signal score'],loc="lower right", frameon=False)

    plt.savefig("/home/paredes/public_html/pheno/nn_lambdai_vs_bkg/paper_roc/ROCs_sigOnly"+ param_string +"_val_set.png")
    plt.savefig("/home/paredes/public_html/pheno/nn_lambdai_vs_bkg/paper_roc/ROCs_sigOnly"+ param_string +"_val_set.pdf")


class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val


if __name__ == "__main__":
    main(sys.argv[1:])
