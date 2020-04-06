## Automated ntuples to paper plots in 3 easy steps

1. Clone the repository:
```git clone https://github.com/LydiaBer/pheno_study.git```

2. Go into the plotting directory:
```cd pheno_study/analysis/plotting```

3. Run the automated script and wait for plots to appear in ```figs``` directory:
```./runMe_for_paper_results.sh```

Enjoy.

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

and run:
```python haddme_ktkl.py DIRNAME```

## Using existing ntuples

If instead of using the ntuples you have produced which are stored in your outputs directory you can instead plot centrally produced ntuples by changing ```TOPPATH = ''``` in ```samples.py``` to point to the existing ntuples. Centrally stored ntuples can be found here: /data/atlas/atlasdata/DiHiggsPheno/ntuples

## Running the plotting code

In the ```pheno_study``` directory the ```setup.sh``` script should first be sourced before proceeding:
```source setup.sh``` 

We then go to the ```plotting``` directory: 
```cd analysis/plotting```

The code is then run as follows: 

```python plot.py```

Or on the batch:

```cd batch ; python make_batch_scripts.py ; python send_plotting_to_batch.py --doTorque```

The output pdf files (and YIELD files for mhh) are stored in the ```figs``` directory.  

## Cutflows

The code is run as follows:

```python make_cutflow.py```

Or on the batch:

```cd batch ; python send_cutflows_to_batch.py --doTorque```

The output cutflow files are stored in the ```cutflows``` directory.  

## 1D plot for Self-coupling limits and 2D plots for Top Yukawa vs Self-coupling
First the ```plot.py``` must be run (as described above) in order to produce YIELD files for the constraint code. 

Next the `ntuples_to_chiSq.py` script loops through signal samples processed through ntupler and produces a CSV containing S/B, acceptance, chi-squares etc. Currently only works with intermediate; needs work to make this more configurable and extend to other channels. This uses the YIELD files produced by plot.py. Open this and configure luminosities etc, then run as
```python ntuples_to_chiSq.py```. Or on the batch:
```cd batch ; python send_ntuples_to_chiSq_to_batch.py --doTorque```

The `chiSq_to_1Dlimit.py` allows plotting the CSV file into a 1D contour plot from the output CSV of `ntuples_to_chiSq.py`. Run as
```python chiSq_to_1Dlimit.py``` 
The output 1D limit plots are stored in the ```figs``` directory.

The `chiSq_to_contour.py` allows plotting the CSV file into a 2D contour plot from the output CSV of `ntuples_to_chiSq.py`. Run as
```python chiSq_to_contour.py```
The output 1D limit plots are stored in the ```contours``` directory.

## How to make plots in paper

Here we list the figures in the paper and the scripts used to make them. 

* **Figure 2:** 2D cross-section vs kapt vs klam. Run the script `hh4b_extract_xsec.py` (ROOT). This takes as input the cross-section values stored in the file `xsec_14TeV_hh.txt`.
* **Figure 3:** Parton-level (LHE) mhh and pT(H) distributions vs klam. Run `plot_lhe.py` script (ROOT) in the `lhe` directory to make the plots. Ntuples are made by running over the MadGraph LHE files using `lhe_to_ntuples.py`, which can be assisted by using `run_diHiggs.sh`. Once these ntuples are made, .
* **Figure 4:** m(hh) resolution plots truth to reco. See `m_hh_resolution` directory.
* **Figure 5:** Unit normalised signal distributions at reco level. Run the `plot_signal_only.py` script (ROOT). 
* **Figure 6:** Acceptance x efficiency plots. Run the `chiSq_to_1Dlimit.py` script (ROOT) uncommenting the designated parts of the code to plot acceptance. This takes as input the output files produced by the `ntuples_to_chiSq.py`, which runs over the signal and background ntuples.
* **Figures 7-9:** Luminosity normalised signal vs background SR distributions. Made using `plot.py` (ROOT), running over the signal and background ntuples.
* **Figure 10:** SHAP value plots.
* **Figure 11:** 1D chi-square vs klam plots. Run the `chiSq_to_1Dlimit.py` script (ROOT). This takes as input the output files produced by the `ntuples_to_chiSq.py`, which runs over the signal and background ntuples. 
* **Figure 12:** 1D 68% CL limits vs background systematics. Run the `summary_1dlimits.py` script (matplotlib). As the input is hard-coded in this script, it should run out of the box once you've sourced right matplotlib/latex dependencies.
* **Figure 13:** Chi-square(ij) vs klam(i) vs klam(j) discrimination power matrix. Run the `chiSq_2dlambda_discrPowerMatrix.py` script (ROOT).
* **Figure 14:** Heat map 2D chi-quare vs kapt vs klam plots. Run the `chiSq_to_contour.py` script (ROOT). This takes as input the output files produced by the `ntuples_to_chiSq.py`, which runs over the signal and background ntuples. 
* **Figure 15:** 2D contour limits overlay summary plot. Run the `contours_to_summary.py` script (ROOT). The input contour files are stored in the `contours/` directory.
* **Figure 18:** ROC curves for DNN cut. Run `plot_roc_curves.py` script (python).
* **Figures 21-24:** m(h) and m(hh) vs DNN score correlation plots. Run the `plot_score_vs_mass.py` script (ROOT).

