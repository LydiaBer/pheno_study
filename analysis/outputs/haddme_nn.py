import os, sys

if len(sys.argv) < 3:
  print " Usage: python hadd_nn.py input_dir input_cutflow_dir"
  sys.exit(1)

indir = sys.argv[1]
incutdir = sys.argv[2] 

# make directories
os.system("mkdir {0}/separate".format(indir))  

# merge testing samples into single files containing resolved, intermediate and boosted, keep separate files in separate directory
files = os.listdir(indir)
for file in files:
  # extract basename
  if "withNNs" in file and "intermediate_2_" in file: # use intermediate to extract basename as no 1000-infty QCD slice for resolved 
    print 
    print file
    basename = indir+'/'+file.split(".intermediate_2_")[0]
    outname = basename.replace('.ro','.root') # due to .ro typo in current names
    
    # do hadding of files and cutflows, hadd cutflow twice if hadding 0-3 slices (i.e. signals and single H) as cutflow is for half stats case
    if any(name in outname for name in ('TopYuk', '_wh','_zh','_zz','_bbh','_tth','_ttbb')):
      print "hadd {0} {1}*.root {2}.cutflow.root {2}.cutflow.root".format(outname,basename,basename.replace(indir,incutdir))
      os.system("hadd {0} {1}*.root {2}.cutflow.root {2}.cutflow.root".format(outname,basename,basename.replace(indir,incutdir)))
    else:
      print "hadd {0} {1}*.root {2}.cutflow.root".format(outname,basename,basename.replace(indir,incutdir))
      os.system("hadd {0} {1}*.root {2}.cutflow.root".format(outname,basename,basename.replace(indir,incutdir)))
    
    # move separate files to directory
    print "mv {0}*_0_*.root {1}/separate".format(basename,indir)
    os.system("mv {0}*_0_*.root {1}/separate".format(basename,indir))  
    print "mv {0}*_1_*.root {1}/separate".format(basename,indir)
    os.system("mv {0}*_1_*.root {1}/separate".format(basename,indir))  
    print "mv {0}*_2_*.root {1}/separate".format(basename,indir)
    os.system("mv {0}*_2_*.root {1}/separate".format(basename,indir))  
    print "mv {0}*_3_*.root {1}/separate".format(basename,indir)
    os.system("mv {0}*_3_*.root {1}/separate".format(basename,indir))  
