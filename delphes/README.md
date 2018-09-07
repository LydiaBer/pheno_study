This is a complete Delphes Installation. Download the content of this folder.

First source the following file :
```
$ source /cvmfs/sft.cern.ch/lcg/views/dev4/latest/x86_64-slc6-gcc7-opt/setup.sh
```

To recompile, type:

```
$ make -j 4
``` 

(CMAKE needs to be already installed)

A new module called ```BTaggingFat``` has been introduced in this version. It can be used to B-tag Large R Jets in Delphes.
This new addition displays the Error : 
```Error in <TList::Clear>: A list is accessing an object (0x2467bd0) already deleted (list name = TList)```

which has been reported to the authors in the following [ticket](https://cp3.irmp.ucl.ac.be/projects/delphes/ticket/1320#ticket).

To run the detector simulation using an ```hepmc``` file use teh following command from the shell :

```$./DelphesHepMC cards/delphes_card_ATLAS_E.tcl output_filename.root input_filename.hepmc ```

