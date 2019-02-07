import os, sys

if len(sys.argv) < 2:
  print " Usage: python hadd_ktkl.py input_dir"
  sys.exit(1)

indir = sys.argv[1] 
os.system("mkdir {0}/separate".format(indir))  

files = os.listdir(indir)
for file in files:
  if "TopYuk" in file and "sample-0_" in file:
    #print 
    #print file
    basename = indir+'/'+file.split("_sample")[0]
    print "hadd {0} {1}*sample*.root".format(basename+".root", basename)
    os.system("hadd {0} {1}*sample*.root".format(basename+".root", basename))
    print "mv {0}*sample*.root {1}/separate".format(basename,indir)
    os.system("mv {0}*sample*.root {1}/separate".format(basename,indir))  
