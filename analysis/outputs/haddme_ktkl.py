import os, glob

os.system("mkdir separate")  

files = os.listdir(".")
for file in files:
  if "TopYuk" in file and "sample-0_" in file:
    #print 
    #print file
    basename = file.split("_sample")[0]
    print basename
    print "hadd {0} {1}*.root".format(basename+".root", basename)
    os.system("hadd {0} {1}*.root".format(basename+".root", basename))
    os.system("mv {0}*.root separate".format(basename))  
