# Neural Network Selection 

This code provides the basics necessary to train and use neural networks for all 3 analyses. First off, you'll need to make sure you have an LCG release set up so you have access to the necessary software. This can be done with: ```source /cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-slc6-gcc8-opt/setup.sh```

This is set up as a 2-step procedure:

1) Train the networks. This is done with ```train_lambdai_vs_bkg/train_lambdai_vs_bkg.py``` for all three analyses and for a given lambda variation, various lambda trainings can be done with ``` train_lambdai_vs_bkg/train_all_lambdas_batches.sh```. Note that this will produce two output files per analysis and per lambda variation, you need both!
2) Apply your trained networks back to the test data (that is, the portion you didn't train on). This is done with  the three scripts ```appendNtuple_<analysis>_ObO.py```, which will run a set of NNs defined within this file and append their scores to the given sample. This is automated in the scripts ```run_append_<analysis>.sh```. This produces copies of your ntuples with a new additional branch containing the NN score.

Both steps are computationally demanding, so it is best to run them on a batch system.

# Random Search Hyper-Parameter Optimization

```random_search_lambdai.py``` and ```random_search.py``` re-train the NNs with random choises of batch size, initial learning rate, and drop-out rate, and compare the performance of each based on the area under the ROC curve of each. It will print out each time a better combinaiton is found.

# NN Validation and Feature Importance Tests

Correlation plots made to validate the NNs training and performance are in `correlation_plots/`.
The plots are made with ```plot_score_vs_mass.py```, and the jupyter notebooks in the directory explore some of the features observed in these correlation plots. 

The feature importance plots which use the SHAP framework are done in the jupyter notebooks in `shap_values/`, named ```shap_plots-<analysis>-lambda<variation>.ipynb```.
To run these, the shap package must be installed (```pip install shap --user```).
