# Phenomenology Study

This code consists of the following directories:

__delphes__ to perform event reconstruction and detector smearing & efficiencies

__analysis__ folder containing code for the __resolved__, __intermediate__ and __boosted__ analyses 

__tagger__ folder containing code for the advanced B-tagger for the boosted channel -> *To be integrated to the main boosted code*

__utilities__ folder containing other code e.g. C++ code which can be used to make histograms of the final results, ```python_hepmc_new.py``` which can be used to split large hepmc files in smaller sized files -> *In process of switching to new python based plotting framework*

## Download code
```git clone https://github.com/LydiaBer/pheno_study.git```

```cd pheno_study```

## Setup environment (to be done each time the code is used!)
```source setup.sh```

## Compiling and running code
The ```README``` file in each of the directories provides further information about compiling and running the code in that directory.

**Code based on previous Oxford hh -> 4b code** The original code is available [HERE](https://github.com/beojan/oxford-hh4b-pheno-code)
