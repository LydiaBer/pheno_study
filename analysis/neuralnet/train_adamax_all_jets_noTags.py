import statistics
import collections
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
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

# This program trains a neural network based on input numpy array files.
# Output is one trained NN file (nn_*.h5) and one scaler file (scaler_*.sav)
# per analysis. Optionally also makes plots of the output distributions for the
# training sample.

### NOTE this program uses 0.2 of the data as a validation set

def main(argv):

    # Path of the directory containing .npz files to train on.
    # Standard naming convention is assumed (e.g. "trainingData_resolved.npz")
    trainingDataPath = "."

    # Training parameters
    numEpochs = 15
    batchSize = 100
    dropoutFraction = 0.3
    # initial learning rate for adamax
    INIT_LR = 5e-3

    # store parameters of the network in a string
    #param_string = "_w_OPadamaxEP"+str(numEpochs)+"BS"+str(batchSize)+"DO"+str(dropoutFraction).replace(".","")
    param_string = "EP15_LR"+str(INIT_LR).replace("0.","0p")
    print ("paramters string "+param_string)
    # Plot score distributions for the training sample?
    makePlots = True
    
    target_nevents = 100000

    signal_weight = MyDict()
    ttbar_weight = MyDict()
    qcd_weight = MyDict()
    for analysis in ["resolved", "intermediate", "boosted"]:

        print("Starting training for " + analysis)
        # Load the input file and grab the data from it.
        # Label each type of background
        # Calculate weight for each 'target' sample
        inFile = np.load(trainingDataPath + "/trainingData_all_jets_noTags_" + analysis + ".npz")

        signalData = pandas.DataFrame(inFile["sig"])
        signalData["target"] = 0
        signal_weight[analysis] = target_nevents/len(signalData)
        print(len(signalData),"(",signal_weight[analysis],") signal (weight) events found")

        backgroundData = pandas.DataFrame(inFile["bkg_4b"])
        backgroundData["target"] = 1
        print(len(backgroundData), "4b background events found")

        background_2b2j = pandas.DataFrame(inFile["bkg_2b2j"])
        background_2b2j["target"] = 1
        print(len(background_2b2j), "2b2j background events found")
        backgroundData = backgroundData.append(background_2b2j)

        qcd_weight[analysis] = target_nevents/len(backgroundData)
        print(len(backgroundData),"(",qcd_weight[analysis], ") qcd (weight) background events found")

        background_ttbar = pandas.DataFrame(inFile["bkg_ttbar"])
        background_ttbar["target"] = 2
        ttbar_weight[analysis] = target_nevents/len(background_ttbar)
        print(len(background_ttbar),"(",ttbar_weight[analysis], ") ttbar (weight) background events found")
        backgroundData = backgroundData.append(background_ttbar)

        allData = signalData.append(backgroundData, ignore_index = True)

        # Set all event weights to 1 by default
        allData.loc[:, 'mc_sf'] = 1.
        # Apply manual event weighting: numbers that give "reasonable behavior"
        allData.loc[allData.target == 0, 'mc_sf'] = signal_weight[analysis] # signal
        allData.loc[allData.target == 1, 'mc_sf'] = qcd_weight[analysis]    # QCD
        allData.loc[allData.target == 2, 'mc_sf'] = ttbar_weight[analysis]  # ttbar

        # shuffle data to get representative validation set
        allData = shuffle(allData)

        xTrainData = allData
        procType = xTrainData.pop("target")


        X_train, X_test, yTypeTrain, yTypeTest = train_test_split(xTrainData, procType, test_size=0.2, random_state=123)

        # These aren't input features, separate them out.
        evtWeightsTrain = X_train.pop("mc_sf")
        evtWeightsVal = X_test.pop("mc_sf")

        # Convert pandas dataframes into numpy arrays
        X_test = X_test.values
        X_train = X_train.values
        evtWeightsTrain = evtWeightsTrain.values
        evtWeightsVal = evtWeightsVal.values
        y_test = keras.utils.to_categorical(yTypeTest, num_classes=3)
        y_train = keras.utils.to_categorical(yTypeTrain, num_classes=3)
        yTypeTest = yTypeTest.values
        yTypeTrain = yTypeTrain.values


        # Convert this into the right format for keras

        # Scale input features to mean=0, stddev=1
        classStd1 = StandardScaler().fit(X_train)
        X_train = classStd1.fit_transform(X_train)
        other_classStd1 = StandardScaler().fit(X_test)
        X_test = classStd1.fit_transform(X_test)
        joblib.dump(classStd1, "scaler_" + analysis + param_string +".sav")

        # Construct the NN architecture
        model = Sequential()
        model.add(Dense(200, activation="relu", input_dim=39))#input_dim should be as long as the branchList given to the NN
        model.add(Dropout(dropoutFraction))
        model.add(Dense(200, activation="relu"))
        model.add(Dense(3, activation="softmax")) # output nodes

        model.compile(
                loss='categorical_crossentropy',  # we train 10-way classification
                optimizer=keras.optimizers.adamax(lr=INIT_LR),  # for SGD
                metrics=['acc']  # report accuracy during training
                )

        # Train the NN
        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=numEpochs, batch_size=batchSize, sample_weight=evtWeightsTrain,verbose=2)
        model.save("nn_all_jets_noTags_" + analysis + param_string +".h5")

        # plot accuracy and loss 
        plt.figure(figsize=(16, 8))
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title(analysis + ', model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig("training/acc_" + analysis +"_"+ param_string +".png")

        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title(analysis + ', model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.figure(figsize=(16, 8))
        plt.plot(history.history['loss'])
        plt.savefig("training/loss_" + analysis +"_"+ param_string +".png")

        # Optionally, plot the output distributions for the training sample.
        if makePlots:
            # Run training sample back through the NN
            probTrain = model.predict(X_train)
            probTest = model.predict(X_test)

            # Construct discriminant
            scores_train = np.log(probTrain[:,0]/(probTrain[:,1]+probTrain[:,2]))
            scores_test = np.log(probTest[:,0]/(probTest[:,1]+probTest[:,2]))

            # Format data for convenience
            trainData = pandas.DataFrame(X_train)
            trainData['sig_score'] = pandas.Series(probTrain[:,0], index=trainData.index)
            trainData['qcd_score'] = pandas.Series(probTrain[:,1], index=trainData.index)
            trainData['top_score'] = pandas.Series(probTrain[:,2], index=trainData.index)
            trainData['disc'] = pandas.Series(scores_train, index=trainData.index)
            trainData['weight'] = pandas.Series(evtWeightsTrain, index=trainData.index)
            trainData['process'] = pandas.Series(yTypeTrain, index=trainData.index)

            print("signal mean = ", statistics.mean(trainData[trainData.process == 0]['sig_score']))
            print("   QCD mean = ", statistics.mean(trainData[trainData.process == 1]['sig_score']))
            print(" ttbar mean = ", statistics.mean(trainData[trainData.process == 2]['sig_score']))

            testData = pandas.DataFrame(X_test)
            testData['sig_score'] = pandas.Series(probTest[:,0], index=testData.index)
            testData['qcd_score'] = pandas.Series(probTest[:,1], index=testData.index)
            testData['top_score'] = pandas.Series(probTest[:,2], index=testData.index)
            testData['disc'] = pandas.Series(scores_test, index=testData.index)
            testData['weight'] = pandas.Series(evtWeightsVal, index=testData.index)
            testData['process'] = pandas.Series(yTypeTest, index=testData.index)

            # Plot distributions of signal score on validation data
            hist_params = {'density': True, 'bins': 50, 'linewidth': 2}
            min_value = 0
            max_value = 1
            plt.figure(figsize=(12,6))
            plt.hist(trainData[trainData.process == 0]['sig_score'], color=["r"], weights=trainData[trainData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal', **hist_params)
            plt.hist(trainData[trainData.process == 1]['sig_score'], color=["b"], weights=trainData[trainData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD', **hist_params)
            plt.hist(trainData[trainData.process == 2]['sig_score'], color=["g"], weights=trainData[trainData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar', **hist_params)
            plt.hist(testData[testData.process == 0]['sig_score'], color=["r"], linestyle = "dotted", weights=testData[testData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal(Val)', **hist_params)
            plt.hist(testData[testData.process == 1]['sig_score'], color=["b"], linestyle = "dotted", weights=testData[testData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD(Val)', **hist_params)
            plt.hist(testData[testData.process == 2]['sig_score'], color=["g"], linestyle = "dotted", weights=testData[testData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar(Val)', **hist_params)
            plt.legend(loc='best')
            plt.xlabel("signal score",fontsize=20)
            plt.ylabel("1/N dN/d(NN Score)",fontsize=20)
            #plt.yscale('log')
            plt.title(analysis + ", (training sample)")
            plt.savefig("sig_scores_" + analysis + param_string +".png")
            plt.figure(figsize=(12,6))
            plt.hist(trainData[trainData.process == 0]['qcd_score'], color=["r"], weights=trainData[trainData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal', **hist_params)
            plt.hist(trainData[trainData.process == 1]['qcd_score'], color=["b"], weights=trainData[trainData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD', **hist_params)
            plt.hist(trainData[trainData.process == 2]['qcd_score'], color=["g"], weights=trainData[trainData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar', **hist_params)
            plt.hist(testData[testData.process == 0]['qcd_score'], color=["r"], linestyle = "dotted", weights=testData[testData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal(Val)', **hist_params)
            plt.hist(testData[testData.process == 1]['qcd_score'], color=["b"], linestyle = "dotted", weights=testData[testData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD(Val)', **hist_params)
            plt.hist(testData[testData.process == 2]['qcd_score'], color=["g"], linestyle = "dotted", weights=testData[testData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar(Val)', **hist_params)
            plt.legend(loc='best')
            plt.xlabel("qcd score",fontsize=20)
            plt.ylabel("1/N dN/d(NN Score)",fontsize=20)
            #plt.yscale('log')
            plt.title(analysis +  ", (training sample)")
            plt.savefig("qcd_scores_" + analysis + param_string +".png")
            plt.figure(figsize=(12,6))
            plt.hist(trainData[trainData.process == 0]['top_score'], color=["r"], weights=trainData[trainData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal', **hist_params)
            plt.hist(trainData[trainData.process == 1]['top_score'], color=["b"], weights=trainData[trainData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD', **hist_params)
            plt.hist(trainData[trainData.process == 2]['top_score'], color=["g"], weights=trainData[trainData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar', **hist_params)
            plt.hist(testData[testData.process == 0]['top_score'], color=["r"], linestyle = "dotted", weights=testData[testData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal(Val)', **hist_params)
            plt.hist(testData[testData.process == 1]['top_score'], color=["b"], linestyle = "dotted", weights=testData[testData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD(val)', **hist_params)
            plt.hist(testData[testData.process == 2]['top_score'], color=["g"], linestyle = "dotted", weights=testData[testData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar(val)', **hist_params)
            plt.legend(loc='best')
            plt.xlabel("ttbar score",fontsize=20)
            plt.ylabel("1/N dN/d(NN Score)",fontsize=20)
            #plt.yscale('log')
            plt.title(analysis + ", (training sample)")
            plt.savefig("top_scores_" + analysis + param_string +".png")

            # Plot distributions of composite discriminant on training data
            plt.figure(figsize=(8, 4))
            plt.hist(trainData[trainData.process == 0]['disc'], color=["r"], weights=trainData[trainData.process == 0]['weight'], range=(min_value, max_value), histtype='step', label='Signal', **hist_params)
            plt.hist(trainData[trainData.process == 1]['disc'], color=["b"], weights=trainData[trainData.process == 1]['weight'], range=(min_value, max_value), histtype='step', label='QCD', **hist_params)
            plt.hist(trainData[trainData.process == 2]['disc'], color=["g"], weights=trainData[trainData.process == 2]['weight'], range=(min_value, max_value), histtype='step', label='ttbar', **hist_params)
            plt.legend(loc='best')
            plt.xlabel("Discriminant",fontsize=20)
            plt.ylabel("1/N dN/d(Discriminant)",fontsize=20)
            #plt.yscale('log')
            plt.title(analysis + ", Discriminant (training sample)")
            plt.savefig("discs_" + analysis + param_string +".png")

class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val


if __name__ == "__main__":
    main(sys.argv[1:])
