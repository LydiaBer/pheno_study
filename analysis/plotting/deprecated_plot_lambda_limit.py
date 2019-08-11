#!/usr/bin/python

import os,math,csv
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('PDF')
##################################################################

#dir = 'jesse_linked_delphes/varied_couplings' # directory input files to plot are in
dir = '280119/varied_couplings' # directory input files to plot are in
outdir = "./figs/{0}/lambda_limits/".format(dir)

regimes = ['resolved_SlfCoup']#, 'intermediate','boosted']
cut_sel = 'ntag4' # corresponds to set of cuts in cuts.py 

if not os.path.exists(outdir):
  os.makedirs(outdir)

lumi = 3000.0
sysErr = 0.0 # 10%

def txt_to_lists(txt_file):
  '''
  converts txt to dictionary of lists containing columns
  the dictionary keys is the header
  '''
  with open(txt_file) as input_file:
      reader = csv.reader(input_file)
      col_names = next(reader)
      data = {name: [] for name in col_names}
      for line in reader:
        for pos, name in enumerate(col_names):
          data[name].append(line[pos])

  return data
######################### Read in cutflows #########################

for regime in regimes:
  filename = './figs/{0}/YIELD_{1}_signal_{2}.txt'.format(dir, regime, cut_sel)
  print "Opening: ",filename
  d_csv = txt_to_lists(filename)
  print d_csv

  ######################### Make plots #########################

  colours = ['r', 'b', 'g', 'm', 'c', 'y', 'k']
  fig, ax = plt.subplots()
  ax.set_ylabel("$\sigma_{HH}$")
  ax.set_xlabel("$\lambda$")
  ax.set_yscale('log')
  ax.xaxis.grid(True)
  ax.yaxis.grid(True)
	
  icol=0
  #axes.set_xlim([xmin,xmax])
  fig.suptitle(regime + " topology (14TeV)")
  ax.set_ylim([1E-2,1E3])
  lvalues = []
  xsecs = []

  for count, ( x_val, y_val) in enumerate( zip( d_csv['sample'], d_csv['yield']) ) :
    lvalues.append(float(x_val.split('SlfCoup_')[1].replace('m','-')))
    xsecs.append(float(y_val)/lumi)

  sorted_lvalues, sorted_xsecs = (list(t) for t in zip(*sorted(zip(lvalues, xsecs))))

  ax.plot(sorted_lvalues, sorted_xsecs, color=colours[icol], label=cut_sel)
  icol = icol + 1
  legend = ax.legend(loc='best', shadow=True)
  fig.savefig(outdir+regime+'_xSec_14TeV.pdf')

  # Now chi2
  chi2vals = []
  index_SigSM = sorted_lvalues.index(1)
  SigSM = sorted_xsecs[index_SigSM]

  print "SIGSM: ",SigSM
  for i, lvalue in enumerate(sorted_lvalues):
    SigLam = sorted_xsecs[i] # Cross-section at lambda
    err = math.sqrt(SigLam/lumi)
    chi2 = pow(SigSM-SigLam,2)/(pow(err,2)+ pow(sysErr*SigSM,2))
    chi2vals.append(chi2)

  # Prepare chi2 plots
  fig, ax = plt.subplots()
  ax.set_ylabel("$\chi^2$")
  ax.set_xlabel("$\lambda$")
  ax.set_ylim([0,3])
  ax.set_xlim([0.9,1.1])
  #ax.set_ylim([0,1000])
  fig.suptitle("$\chi^2$ profile for all topologies $\sqrt{s}=14$ TeV L="+str(lumi)+"fb$^{-1}$. SysErr="+str(sysErr*100) + "%")
 
  # Print out final values
  ax.plot(sorted_lvalues, chi2vals, label="resolved")
  # Now add the legend with some customizations.
  legend = ax.legend(loc='best', shadow=True)
  fig.savefig(outdir+regime+'chi2_14TeV_sys'+str(sysErr).replace(".","_")+'.pdf')

