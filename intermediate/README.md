# HH → 4b Resolved Regime Reconstruction

## NTuples
This software works with ntuples produced using
[XhhCommon](https://gitlab.cern.ch/hh4b/XhhCommon/).
Suitable NTuples are available on the grid:

- `user.saparede.HH4B.2018-04-29T1237Z.data17-rel21` **BEWARE -- NOT BLINDED. DO
  NOT LOOK AT SIGNAL REGION.**
- `user.bstanisl.HH4B.2018-04-30T0908Z.data16-rel21`
- `user.bstanisl.HH4B.2018-04-30T0908Z.data15-rel21`

However, the 2015 and 2016 NTuples contain a few corrupt files, so the
reconstruction needs to be run one file at a time.

## Running the Reconstruction
The reconstruction software requires ROOT 6.12, and the kinematic reweighting
and plotting scripts also require Python 3.6. The easiest way to get these on
LXPLUS or a Tier 3 is to use the LCG 93python3 release with:

``` console
$ source /cvmfs/sft.cern.ch/lcg/views/LCG_93python3/x86_64-slc6-gcc7-opt/setup.sh
```

The code can then be built with CMake:

``` console
$ mkdir build
$ cd build
$ cmake ..
$ make
```

The executable will then be found at `build/resolved-recon`. The help text is:

``` console
$ ./resolved-recon --help
Reconstruct and filter events in the HH->4b resolved channel
Usage:
  resolved-recon [OPTION...] input files

 main options:
  -f, arg              Untagged to tagged normalization (default: 0.22)
  -m, --mc_config arg  Config file if MC
      --tree arg       Tree name (default: XhhMiniNtuple)
      --top_veto       Top Veto (default: false)
      --grl arg        GRL
  -o, --output arg     Output file (default: reconstructed.root)
  -h, --help           Help

```

It can be run on data with a command like:

```console
$ ~/hh4b/recon/build/resolved-recon -f 0.16 --top_veto --grl ~/hh4b/GRLs/data16_13TeV.periodAllYear_DetStatus-v89-pro21-01_DQDefects-00-02-04_PHYS_StandardGRL_All_Good_25ns_BjetHLT.xml -o data16.root /data/atlas/atlasdata/hh4b-ntuples/**/*.root
```

In particular, notice the `--grl` option which takes the GRL xml file, and the
`--top_veto` option to enable the top veto. You should correct the paths to the
executable, GRL, and input NTuples to match your setup.

As you can see, the reconstruction can be run on many input files at once.
However, if some of these files are corrupt, they can cause a segfault (this is
fixed in the upcoming [ROOT
6.14](https://root-forum.cern.ch/t/tdataframe-segfault-on-error-reading-file/29081),
and this reconstruction software will be updated for this ROOT version once it
is in an LCG release). As a result, on data it's best to run the reconstruction
on one or a few files at a time. `find` and `xargs` can be helpful for this.

### Running on MC
When running on MC, the reconstruction must be run on all files at once, to
correctly calculate the event weights. In addition, the `--grl` option should
not be given, but instead the `--mc_config` option should be used, with its
argument being a JSON file describing the Monte-Carlo configuration. An example
configuration file is in `ttbar.nonallhad.json`. The `lumi` variable in this
file is the total integrated luminosity the MC should be normalized to (3.1 for
2015 data only).

## Kinematic Reweighting and Plotting
The code for kinematic reweighting and plotting can be found in the `tools`
directory. In addition to the LCG release, these require the
[root_pandas](https://github.com/scikit-hep/root_pandas) and
[atlas_mpl_style](https://github.com/beojan/atlas-mpl) Python modules, both of
which can be installed from PIP:

``` console
$ pip install --user root_pandas
$ pip install --user atlas-mpl-style
```

Having done this, copy `kinematic-reweighting.py` and `plot.py` into the same
directory as the output from the reweighting software. Then, update the
`input_file` in `kinematic-reweighting.py` and run

``` console
$ ./kinematic-reweighting.py
```

This will produce `Iterations.pdf` which shows the outcome of each iteration of
the reweighting, and `reweight.pickle` which contains the reweighting
information in a format the plotting tool can understand. It will also print an
optimized normalization and n-jets factor, which should be passed to `plot.py`.
The plotting tool is then run with a command like

``` console
$ ./plot.py --norm 0.10031 -f 0.18747 signal m_hh data16.root
```

The help text for this is:

``` console
$ ./plot.py --help
usage: plot.py [-h] [--no-kinematic-reweighting] [--mc MC_label MC_file]
               [--norm NORM] [-f F]
               {signal,control,sideband}
               {m_hh,m_h1,pT_h1,eta_h1,m_h2,pT_h2,eta_h2,njets,pT_4,pT_2,eta_i,dRjj_1,dRjj_2}
               data_file

Plot data and background (QCD and MC)

positional arguments:
  {signal,control,sideband}
                        HH mass region
  {m_hh,m_h1,pT_h1,eta_h1,m_h2,pT_h2,eta_h2,njets,pT_4,pT_2,eta_i,dRjj_1,dRjj_2}
                        Variable to plot
  data_file             Data ROOT file

optional arguments:
  -h, --help            show this help message and exit
  --no-kinematic-reweighting
  --mc MC_label MC_file
                        MC backgrounds
  --norm NORM           QCD normalization
  -f F                  n-jets factor
```
