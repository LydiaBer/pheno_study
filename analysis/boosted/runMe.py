''' 
Script for running boosted analysis on the batch
Expects input filelist of files to run on 
One output file produced per input file to chosen output dir
If run on the batch 1 job per file submitted
''' 

import os

### User inputs

FILE_LIST = "./run/sliced_trackJetBtagged_samples_boosted.txt" #2018sep13_all_merged_delphes.txt"
OUT_DIR = os.getcwd().split("/boosted")[0]+"/outputs/./sliced_trackJetBtagged_samples"#2018sep13"
USE_BATCH = True

### End of user inputs

# Make output directory 
if not os.path.exists(OUT_DIR):
  os.makedirs(OUT_DIR)
  os.makedirs(OUT_DIR+"/logs")

# open filelist and read line by line
with open(FILE_LIST, 'r') as filehandle:  
  filecontents = filehandle.readlines()

  for line in filecontents:
      # remove linebreak which is the last character of the string
      file_dir = line[:-1]
      # skip if commented out with hash
      if '#' in line: continue
      # skip if empty line
      if len(line.strip()) == 0: continue

      output_dir = OUT_DIR
      # Get list of files in directory specified in file list
      files = os.listdir(file_dir)
   
      # Loop over files in directory specified in FILE_LIST
      for file in files: 

        # make file path from file dir and file
        file_path = file_dir+"/"+file

        # make short output filename of form boosted_genfiltercut_sample.root
        if "hh_loop_sm" in file_path:
          output_filename = "boosted_loop_hh_"+file   
 
        elif "signal/varied_coupling" in file_path:
          TopYuk = file_path.split("TopYuk_")[1].split("/SlfCoup")[0]
          output_filename = "boosted_hh_"+"TopYuk_"+TopYuk+"_"+file  

        elif "4b" in file_path:
          if "20_to_200" in file_path:
            filter = "20_to_200_4b"
          if "200_to_500" in file_path:
            filter = "200_to_500_4b"
          if "500_to_1000" in file_path:
            filter = "500_to_1000_2b2j"
          if "1000_to_infty" in file_path:
            filter = "1000_to_infty_4b"
          output_filename = "boosted_{0}_{1}_{2}".format(filter, file_path.split("/")[-2],file)

        elif "2b2j" in file_path:
          if "20_to_200" in file_path:
            filter = "20_to_200_2b2j"
          if "200_to_500" in file_path:
            filter = "200_to_500_2b2j"
          if "500_to_1000" in file_path:
            filter = "500_to_1000_2b2j"
          if "1000_to_infty" in file_path:
            filter = "1000_to_infty_2b2j"
          output_filename = "boosted_{0}_{1}_{2}".format(filter, file_path.split("/")[-2],file)

        command =  "./build/boosted-recon {0} {1} {2}".format(file_path, output_dir, output_filename)
        if USE_BATCH:
          batch_script = os.getcwd()+"/tools/batchTemplate.sh"
          logfile = OUT_DIR+"/logs/"+output_filename.split(".root")[0]
          batch_command  = "qsub -N {0} -o {1} -e {2} -v CODEDIR='{3}',CMD='{4}' {5}".format(output_filename.split(".root")[0],logfile+".out",logfile+".err",os.getcwd(), command, batch_script)
          print(batch_command)
          os.system(batch_command)
        else: 
          print(command)
          os.system(command)
           
