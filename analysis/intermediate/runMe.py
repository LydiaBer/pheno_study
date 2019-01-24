''' 
Script for running intermediate analysis on the batch
Expects input filelist of files to run on 
One output file produced per input file to chosen output dir
If run on the batch 1 job per file submitted
''' 

import os

### User inputs

FILE_LIST = "../filelists/signal_240119.txt"
OUT_DIR = os.getcwd().split("/intermediate")[0]+"/outputs/signal_240119"
USE_BATCH = False

### End of user inputs

# Make output directory 
if not os.path.exists(OUT_DIR):
  os.makedirs(OUT_DIR)
  os.makedirs(OUT_DIR+"/logs")

# open filelist and read line by line
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

      # make short output filename of form intermediate_sample.root
      if "signal/nominal" in file_path:
        output_filename = 'intermediate_'+file_path.split('nominal/')[1]  

      elif "signal/varied_coupling" in file_path:
        TopYuk = file_path.split("TopYuk_")[1].split("/SlfCoup")[0]
        SlfCoup = file_path.split("SlfCoup_")[1].split("_sample")[0]
        output_filename = "intermediate_hh_"+"TopYuk_"+TopYuk+"_"+"SlfCoup_"+SlfCoup+"trackJetBTag.root"  

      #elif "bkg" in file_path:
      #  if "unfiltered" in file_path:
      #    filter = "noGenFilt"
      #  if "pt200" in file_path:
      #    filter = "xpt200"
      #  output_filename = "intermediate_{0}_{1}_{2}".format(filter, file_path.split("/")[-2],file)

      command =  "./build/intermediate-recon {0} {1} {2}".format(file_path, output_dir, output_filename)
      if USE_BATCH:
        batch_script = os.getcwd()+"/tools/batchTemplate.sh"
        logfile = OUT_DIR+"/logs/"+output_filename.split(".root")[0]
        batch_command  = "qsub -N {0} -o {1} -e {2} -v CODEDIR='{3}',CMD='{4}' {5}".format(output_filename.split(".root")[0],logfile+".out",logfile+".err",os.getcwd(), command, batch_script)
        print
        print(batch_command)
        #os.system(batch_command)
      else: 
        print(command)
        os.system(command)

