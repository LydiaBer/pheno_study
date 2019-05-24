import statistics
import getopt, sys
import matplotlib.pyplot as plt
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

# This program trains a neural network based on input numpy array files.
# Output is one trained NN file (nn_*.h5) and one scaler file (scaler_*.sav)
# per analysis. Optionally also makes plots of the output distributions for the
# training sample.

def main(argv):

    # Path of the directory containing .npz files to train on.
    # Standard naming convention is assumed (e.g. "trainingData_resolved.npz")
    trainingDataPath = "."

    # Training parameters
    #numEpochs = 30
    #batchSize = 100
    #dropoutFraction = 0.5
    numEpochs = 40
    batchSize = 32
    dropoutFraction = 0.3
    INIT_LR = 5e-3

    param_string = "OPadamaxEP"+str(numEpochs)+"BS"+str(batchSize)+"DO"+str(0.3).replace(".","")
    print ("paramters string "+param_string)
    # Plot score distributions for the training sample?
    makePlots = True

    for analysis in ["resolved", "intermediate", "boosted"]:

        print("Starting training for " + analysis)
        # Load the input file and grab the data from it.
        # Label each type of background.
        inFile = np.load(trainingDataPath + "/trainingData_" + analysis + ".npz")

        signalData = pandas.DataFrame(inFile["sig"])
        signalData["target"] = 0
        print(len(signalData), "signal events found")

        backgroundData = pandas.DataFrame(inFile["bkg_4b"])
        backgroundData["target"] = 1
        print(len(backgroundData), "4b background events found")

        background_2b2j = pandas.DataFrame(inFile["bkg_2b2j"])
        background_2b2j["target"] = 1
        print(len(background_2b2j), "2b2j background events found")
        backgroundData = backgroundData.append(background_2b2j)

        background_ttbar = pandas.DataFrame(inFile["bkg_ttbar"])
        background_ttbar["target"] = 2
        print(len(background_ttbar), "ttbar background events found")
        backgroundData = backgroundData.append(background_ttbar)

        allData = signalData.append(backgroundData, ignore_index = True)

        # Set all event weights to 1 by default
        allData.loc[:, 'mc_sf'] = 1.
        # Apply manual event weighting: numbers that give "reasonable behavior"
        if analysis is "resolved":
            allData.loc[allData.target == 0, 'mc_sf'] = 12.  # signal
            allData.loc[allData.target == 1, 'mc_sf'] = 0.2  # QCD
            allData.loc[allData.target == 2, 'mc_sf'] = 0.2 # ttbar
        if analysis is "intermediate":
            allData.loc[allData.target == 0, 'mc_sf'] = 20.  # signal
            allData.loc[allData.target == 1, 'mc_sf'] = 0.3  # QCD
            allData.loc[allData.target == 2, 'mc_sf'] = 1. # ttbar
        if analysis is "boosted":
            allData.loc[allData.target == 0, 'mc_sf'] = 20.  # signal
            allData.loc[allData.target == 1, 'mc_sf'] = 0.03  # QCD
            allData.loc[allData.target == 2, 'mc_sf'] = 2. # ttbar

        xTrainData = allData

        # These aren't input features, separate them out.
        evtWeightsTrain = xTrainData.pop("mc_sf")
        procTypeTrain = xTrainData.pop("target")

        # Convert pandas dataframes into numpy arrays
        xTrainData = xTrainData.values
        evtWeightsTrain = evtWeightsTrain.values
        procTypeTrain = procTypeTrain.values

        # Convert this into the right format for keras
        yTrainCategories = keras.utils.to_categorical(procTypeTrain, num_classes=3)

        # Scale input features to mean=0, stddev=1
        classStd1 = StandardScaler().fit(xTrainData)
        xTrainData = classStd1.fit_transform(xTrainData)
        # Record the scaler parameters, we'll need them later
        joblib.dump(classStd1, "scaler_" + analysis + param_string +".sav")

        # Construct the NN architecture
        model = Sequential()
        model.add(Dense(100, activation="relu", input_dim=10))
        model.add(Dropout(dropoutFraction))
        model.add(Dense(100, activation="relu"))
        model.add(Dense(3, activation="softmax")) # output nodes

        model.compile(
                #optimizer='sgd',
                loss='categorical_crossentropy',  # we train 10-way classification
                optimizer=keras.optimizers.adamax(lr=INIT_LR),  # for SGD
                metrics=['accuracy']  # report accuracy during training
                )

        # Train the NN
        model.fit(xTrainData, yTrainCategories, epochs=numEpochs, batch_size=batchSize, sample_weight=evtWeightsTrain,verbose=2)
        model.save("nn_" + analysis + param_string +".h5")

        # Optionally, plot the output distributions for the training sample.
        if makePlots:
            # Run training sample back through the NN
            probVal = model.predict(xTrainData)

            # Construct discriminant
            scores = np.log(probVal[:,0]/(probVal[:,1]+probVal[:,2]))

            # Format data for convenience
            trainData = pandas.DataFrame(xTrainData)
            trainData['MVA'] = pandas.Series(probVal[:,0], index=trainData.index)
            trainData['disc'] = pandas.Series(scores, index=trainData.index)
            trainData['weight'] = pandas.Series(evtWeightsTrain, index=trainData.index)
            trainData['process'] = pandas.Series(procTypeTrain, index=trainData.index)

            print("signal mean = ", statistics.mean(trainData[trainData.process == 0]['MVA']))
            print("   QCD mean = ", statistics.mean(trainData[trainData.process == 1]['MVA']))
            print(" ttbar mean = ", statistics.mean(trainData[trainData.process == 2]['MVA']))

            # Plot distributions of signal score on validation data
            hist_params = {'density': True, 'bins': 50, 'linewidth': 2}
            min_value = 0
            max_value = 1
            plt.figure(figsize=(16, 8))
            plt.hist(trainData[trainData.process == 0]['MVA'], color=["r"], weights=trainData[trainData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal', **hist_params)
            plt.hist(trainData[trainData.process == 1]['MVA'], color=["b"], weights=trainData[trainData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD', **hist_params)
            plt.hist(trainData[trainData.process == 2]['MVA'], color=["g"], weights=trainData[trainData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar', **hist_params)
            plt.legend(loc='best')
            plt.xlabel("NN Score",fontsize=20)
            plt.ylabel("1/N dN/d(NN Score)",fontsize=20)
            plt.yscale('log')
            plt.title("NN Score (training sample)")
            plt.savefig("scores_" + analysis + param_string +".png")

            # Plot distributions of composite discriminant on training data
            plt.figure(figsize=(16, 8))
            plt.hist(trainData[trainData.process == 0]['disc'], color=["r"], weights=trainData[trainData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal', **hist_params)
            plt.hist(trainData[trainData.process == 1]['disc'], color=["b"], weights=trainData[trainData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD', **hist_params)
            plt.hist(trainData[trainData.process == 2]['disc'], color=["g"], weights=trainData[trainData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar', **hist_params)
            plt.legend(loc='best')
            plt.xlabel("Discriminant",fontsize=20)
            plt.ylabel("1/N dN/d(Discriminant)",fontsize=20)
            plt.yscale('log')
            plt.title("Discriminant (training sample)")
            plt.savefig("discs_" + analysis + param_string +".png")

if __name__ == "__main__":
    main(sys.argv[1:])
