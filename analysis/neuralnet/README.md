# Neural Network Selection 

This code provides the basics necessary to train and use neural networks for all 3 analyses. First off, you'll need to make sure you have an LCG release set up so you have access to the necessary software. This can be done with: ```source /cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-slc6-gcc8-opt/setup.sh```

This is set up as a 3-step procedure:

1) Convert the training data into the necessary format. This is done with ```root_npz_conversion.py```. Note that this can just as easily be used to convert test data into the same format if you need to for any reason.
2) Train the networks. This is done with ```trainNNs.py```. Note that this will produce two output files per analysis, you need both!
3) Apply your trained networks back to the test data (that is, the portion you didn't train on). This is done with ```appendNtuple.py```. This produces copies of your ntuples with a new additional branch containing the NN score.

In all cases, no command-line arguments are required, but you'll need to set the hard-coded filepaths for the inputs at the top of each program.
