# Boosted analysis code 

This code takes as input the ROOT files produced by delphes and slims them by applying the boosted analysis selection and reconstructing the Higgs candidates for the boosted analysis. 

The three main files are as follows: 
1) ```boosted-recon.cpp``` : the file where the actual analysis take place.
2) ```utils.h``` : the file where classes and utility functions used in the "boosted-recon.cpp" are defined and specified.
3) ```Cutflow.cpp```: the file where the structure for the cutflow is defined.

## Compiling and running the code

In the ```pheno_study``` directory the ```setup.sh``` script should first be sourced before proceeding:
```source setup.sh``` 

The boosted analysis code can then be compiled by running:
```cd analysis/boosted```
```source compileMe.sh```

The code is run using commands such as ```./build/boosted-recon  input_file_path output_dir output_filename```. In practice the running of the code can be performed using the ```runMe.py``` script as follows: 

```python runMe.py```

In this script the user defines the file list containing the input files to be run over, the output directory to store the boosted analysis ROOT ntuples in and whether to run locally or on the Oxford batch system. One output boosted ROOT ntuple is produced for every input delphes ROOT file and is stored in the output directory defined by the user.  

To plot your results please read the ```README``` file in the ```plotting``` directory one level up in the ```analysis``` directory. 
