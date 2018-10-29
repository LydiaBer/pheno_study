# Plotting code

This code takes as input the ROOT files produced by the resolved, intermediate and boosted analysis codes. 
Weighting is applied to normalise each sample to the correct cross-section. Additional cuts can also be applied.
The background histograms are then stacked and plotted with the signal histogram overlaid. 

The main files are as follows: 
1) ```plot.py``` : the master file where the plotting takes place.
2) ```samples.py```: defines which set of input ROOT files should be run over, specified depending on the ```dir``` and ```analysis``` specified in ```plot.py```. ```
3) ```variables.py``` : defines binning and labelling for variables we want to make histograms for.
4) ```cuts.py```: defines additional cut selections to be applied by specifying ```cut_sel``` in ```plot.py```.
5) ```beautify.py```: contains additional plotting functions to change plot formatting. 

## Hadding input ROOT files

Before plotting your results, the output NTuples from the analysis steps should be 'hadded' together to form single files for each signal sample, or each bkg with or without a pT filter applied. In order to do this scripts are provided in the outputs directory. The scripts can be used as follows:

In the ```pheno_study``` directory the ```setup.sh``` script should first be sourced before proceeding:
```source setup.sh``` 

```cd analysis/outputs```

You then move the scripts to the directory containing your ntuples e.g. TO BE UPDATED: should modify scripts to run on directory of choice rather than manually as explained below

```mv haddme_ktkl.py jesse_linked_delphes```
```mv haddme.sh jesse_linked_delphes```

and run in the following order:
```python haddme_ktkl.py```
```source haddme.sh```

## Using existing ntuples

If instead of using the ntuples you have produced which are stored in your outputs directory you can instead plot centrally produced ntuples by changing ```TOPPATH = '../outputs'``` in ```samples.py``` to point to the existing ntuples. Centrally stored ntuples can be found here: /data/atlas/atlasdata/DiHiggsPheno/ntuples

## Running the code

In the ```pheno_study``` directory the ```setup.sh``` script should first be sourced before proceeding:
```source setup.sh``` 

We then go to the ```plotting``` directory: 
```cd analysis/plotting```

The code is then run as follows: 

```python plot.py```

The output pdf files are stored in the ```figs``` directory.  
