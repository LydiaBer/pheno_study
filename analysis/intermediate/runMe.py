''' 
Script for running loose analysis on the batch
Expects input filelist of files to run on 
One output file produced per input file to chosen output dir
If run on the batch 1 job per file submitted
''' 

import os,sys

### User inputs

TAG = "150719"
FILE_LISTS = ["../filelists/signal_{0}.txt".format(TAG),"../filelists/signal_4b_highstats_{0}.txt".format(TAG),"../filelists/background_{0}.txt".format(TAG)]
OUT_DIR = os.getcwd().split("/intermediate")[0]+"/outputs/"+TAG

USE_BATCH = True

### End of user inputs

# Make output directory 
if not os.path.exists(OUT_DIR):
  os.makedirs(OUT_DIR)
  os.makedirs(OUT_DIR+"/logs")

# open filelist and read line by line
for FILE_LIST in FILE_LISTS:
  with open(FILE_LIST, 'r') as filehandle:  
    filecontents = filehandle.readlines()

    for file_path in filecontents:
      # skip if commented out with hash
      if '#' in file_path: continue
      # skip if empty line
      if len(file_path.strip()) == 0: continue
      # remove spaces at the end of the line
      file_path = file_path.strip()

      output_dir = OUT_DIR
      output_filename = ""
      
      # append loose to front of filename
      if file_path.count("TopYuk") == 1:
        TopYukSlfCoup = file_path.split("TopYuk_")[1].replace("/","_").replace("Events_pp_","sample-").replace("tag_1_delphes_events_","")
        output_filename = "loose_noGenFilt_signal_hh_"+"TopYuk_"+TopYukSlfCoup
      elif file_path.count("TopYuk") == 2:
        TopYukSlfCoup = file_path.split("TopYuk_")[2].replace("/","_").replace("Events_pp_","sample-").replace("tag_1_delphes_events_","")
        output_filename = "loose_noGenFilt_4b_highstats_signal_hh_"+"TopYuk_"+TopYukSlfCoup
      else:
        Process = file_path.split("Dlph3_")[1].replace("/","_").replace("Events_pp_","sample-").replace("tag_1_delphes_events_","")
        output_filename = "loose_"+Process

      command =  "./build/intermediate-recon {0} {1} {2}".format(file_path, output_dir, output_filename)
      print file_path
      print output_filename

      if USE_BATCH:
        batch_script = os.getcwd()+"/tools/batchTemplate.sh"
        logfile = OUT_DIR+"/logs/"+output_filename.split(".root")[0]
        batch_command  = "qsub -N {0} -o {1} -e {2} -v CODEDIR='{3}',CMD='{4}' {5}".format(output_filename.split(".root")[0],logfile+".out",logfile+".err",os.getcwd(), command, batch_script)
        #print
        print(batch_command)
        os.system(batch_command)
      else: 
        print
        print(command)
        os.system(command)

