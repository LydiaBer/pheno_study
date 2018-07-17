This folder contains the file needed to implement the BTagging for the FatJets in Delphes.

In order to introduce this new feature in your delphes installation copy the file as follows.

In your ``` modules``` folder:
1) Replace the ```ModulesLinkDef.h``` with the one in this folder.
2) Copy the ```BTaggingFat.h``` and ```BTaggingFat.cc``` files in the ```module``` folder.

In your ```cards``` folder replace the ```delphes_card_CMS.tcl``` file with the one in this folder.

Then in the main delphes dir 

```
./configure
make
```

This new addition displays the Error : 
```Error in <TList::Clear>: A list is accessing an object (0x2467bd0) already deleted (list name = TList)```

which has been reported to the authors in the following [ticket](https://cp3.irmp.ucl.ac.be/projects/delphes/ticket/1320#ticket).

To run the detector simulation using an ```hepmc``` file use teh following command from the shell :

```$./DelphesHepMC cards/delphes_card_CMS.tcl output_filename.root input_filename.hepmc ```

