''' 
Script for running boosted analysis on the batch
Expects input filelist of files to run on 
One output file produced per input file to chosen output dir
If run on the batch 1 job per file submitted
''' 

import os

### User inputs

FILE_LIST = "../filelists/2018sep13_all_merged_delphes.txt"
OUT_DIR = os.getcwd().split("/resolved")[0]+"/outputs/2018sep13_all_merged_delphes"
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
        file_path = line[:-1]
        # skip if commented out with hash
        if '#' in line: continue
        # skip if empty line
        if len(line.strip()) == 0: continue
        output_dir = OUT_DIR
        output_filename = "boosted_"+file_path.split("/")[-1] # output name = boosted_inputname 
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
           
