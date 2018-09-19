# Intermediate analysis code 

This code takes as input the ROOT files produced by delphes and slims them by applying the intermediate analysis selection and reconstructing the Higgs candidates for the intermediate analysis. 

The three main files are as follows: 
1) ```inter-recon.cpp``` : the file where the actual analysis take place.
2) ```utils.h``` : the file where classes and utility functions used in the "inter-recon.cpp" are defined and specified.
3) ```Cutflow.cpp```: the file where the structure for the cutflow is defined.

## Compiling and running the code

In the ```pheno_study``` directory the ```setup.sh``` script should first be sourced before proceeding:
```source setup.sh``` 

The intermediate analysis code can then be compiled by running:
```cd analysis/intermediate```
```source compileMe.sh```

The code is run using commands such as ```./build/inter-recon  input_file_path output_dir output_filename```. In practice the running of the code can be performed using the ```runMe.py``` script as follows: 

```python runMe.py```

In this script the user defines the file list containing the input files to be run over, the output directory to store the intermediate analysis ROOT ntuples in and whether to run locally or on the Oxford batch system. One output intermediate ROOT ntuple is produced for every input delphes ROOT file and is stored in the output directory defined by the user.  
