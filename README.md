# Phenomenology Study
**Based on previous Oxford hh->4b Code**

The original code is available [HERE](https://github.com/beojan/oxford-hh4b-pheno-code)

Before running any code, from your command line source the setup script: 

```source setup.sh```

The __analysis__ folder contains the analysis code for the __resolved__, __intermediate__ and __boosted__ regime.

The __tagger__ folder contains the code for the advanced B-tagger for the boosted channel.

The __utilities__ folder contains C++ code which can be used to make histograms of the final results. It also contains the ```python_hepmc_new.py``` which can be used to split large hepmc files in smaller sized files.

The __delphes__ folder contains the full installation of Delphes. Inside ```delphes/cards``` you can find the ```delphes_cards_ATLAS_E.tcl``` which is a card, based on ```delphes_cards_ATLAS.tcl```, that allows for FatJet BTagging, Track-Jets identification and Flavour association for the TrackJets. 

Specific information on each analysis code can be found in the README file inside the corresponding analysis folder.

To make the Delphes installation running, please open the README file inside the ___delphes___ folder.

For further information about the tagger, please open the README file inside the ___tagger___ folder. 
