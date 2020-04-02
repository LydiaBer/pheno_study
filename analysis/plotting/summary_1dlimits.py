#!/usr/bin/env python
#-----------------------------------------------------------------------
#
# Lydia Beresford and Jesse Liu 2019
#
# Script to make summary plot of 1D lambda limits
# Everything is rather ad hoc hard coded manually implemented for now
#
#-----------------------------------------------------------------------

import os, json, math, csv, argparse, datetime
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import matplotlib.lines as mlines

# Plot for kappa(lambda) = 5
klam5 = False

plt.rcParams.update({'font.size': 25})
#  plt.tight_layout(pad=1.8)
# ATLAS requires Helvetica typeface
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = [
   r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
   r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
   #r'\usepackage{helvet}',    # set the normal font here
   #r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
   #r'\sansmath',              # <- tricky! -- gotta actually tell tex to use!
   r'\usepackage[utf8]{inputenc}',
   r'\DeclareUnicodeCharacter{2212}{$-$}',
]  
#-------------------------------------
# Figures
#-------------------------------------
fig, ax = plt.subplots()
fig.set_size_inches(11, 8)

#-------------------------------------
# Define colours
#-------------------------------------
myLightBlue  = '#6baed6'
myMediumBlue = '#2171b5'
myDarkBlue   = '#08306b'
myDarkOrange = '#ec7014'
myGrey       = '#a8a8a8'

# SM
plt.plot([1., 1.], [-1, 18.5], ls='-',lw=2.,color=myGrey)
ax.text(0.2, 18.8,r'$\mathrm{SM}$', size='20')

bstColor = myLightBlue
bstWidth = 2.3
intColor = myMediumBlue
intWidth = 2.6
resColor = myDarkBlue
resWidth = 2.9
comColor = myDarkOrange
comWidth = 3.3
print('plot first')
  
# Dummy lines for legend
plt.plot([-25.,-25.],[-5,-5],'|',ms=0,mew=0,mec=bstColor,ls='-',lw=bstWidth,color=bstColor,label='$\mathrm{Boosted}$')
plt.plot([-25.,-25], [-5,-5],'|',ms=0,mew=0,mec=intColor,ls='-',lw=intWidth,color=intColor,label='$\mathrm{Intermediate}$')
plt.plot([-25,-25.], [-5,-5],'|',ms=0,mew=0,mec=resColor,ls='-',lw=resWidth,color=resColor,label='$\mathrm{Resolved}$')
plt.plot([-25.,-25.],[-5,-5],'|',ms=0,mew=0,mec=comColor,ls='-',lw=comWidth,color=comColor,label='$\mathrm{Combined}$')

if klam5:

  # 5% systematic
  plt.plot([-25.,25.],  [18.,18.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-8.2,15.8], [17.7,17.7],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-5.5,11.9], [17.4,17.4],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved
  plt.plot([-4.7,11.6], [17.1,17.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined
  ax.text(-23,17.5,r'$5.0\%$', size='20')

  # 2% syst
  plt.plot([-12.4,25.], [16.,16.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-4.2,14.4], [15.7,15.7], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-2.6,9.7],  [15.4,15.4], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-2.5,9.4],  [15.1,15.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,15.5,r'$2.0\%$', size='20')

  # 1.5% syst
  plt.plot([-11.0,25.],[14.,14.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-3.8,12.6],[13.7,13.7], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-2.4,8.9], [13.4,13.4], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-2.2,8.8],  [13.1,13.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,13.5,r'$1.5\%$', size='20')

  # 1% syst
  plt.plot([-10.1,17.6],[12.,12.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-3.4,11.4], [11.7,11.7],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-2.0,8.2],  [11.4,11.4],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-1.9,8.1],  [11.1,11.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,11.5,r'$1.0\%$', size='20')

  # 0.3% syst
  plt.plot([-8.2,13.9], [10.,10.], '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-3.1,10.5], [9.7,9.7], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-0.97,6.7], [9.4,9.4], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-0.8,6.6],  [9.1,9.1], '|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,9.5,r'$0.3\%$', size='20')

  # 0% syst
  plt.plot([-8.0,13.2], [8.,8.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-3.0,10.4], [7.7,7.7],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-0.8,6.4],  [7.4,7.4],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-0.7,6.3],  [7.1,7.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,7.5,r'$0.0\%$', size='20')

  ax.text(2.5,3.2,r'$\mathrm{DNN~trained~on~} \kappa_\lambda = 5$', size='20')
else:
  # 5% systematic
  plt.plot([-25.,25.],  [18.,18.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-8.9,16.3], [17.7,17.7],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-7.2,13.9], [17.4,17.4],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved
  plt.plot([-5.3,12.8], [17.1,17.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined
  ax.text(-23,17.5,r'$5.0\%$', size='20')

  # 2% syst
  plt.plot([-11.8,25.], [16.,16.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-4.4,12.3], [15.7,15.7], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-3.8,10.0],  [15.4,15.4], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-3.2,9.8],  [15.1,15.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,15.5,r'$2.0\%$', size='20')

  # 1.5% syst
  plt.plot([-10.6,25.],[14.,14.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-4.2,11.1],[13.7,13.7], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-3.0,9.5], [13.4,13.4], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-2.5,9.3],  [13.1,13.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,13.5,r'$1.5\%$', size='20')

  # 1% syst
  plt.plot([-9.2,17.6],[12.,12.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-3.8,10.4], [11.7,11.7],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-2.2,8.9],  [11.4,11.4],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-1.9,8.2],  [11.1,11.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,11.5,r'$1.0\%$', size='20')

  # 0.3% syst
  plt.plot([-7.9,14.5], [10.,10.], '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-3.0,9.7], [9.7,9.7], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-1.1,7.3], [9.4,9.4], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-0.85,7.3],  [9.1,9.1], '|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,9.5,r'$0.3\%$', size='20')

  # 0% syst
  plt.plot([-5.5,13.3], [8.,8.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
  plt.plot([-2.7,9.6], [7.7,7.7],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
  plt.plot([-0.68,7.1],  [7.4,7.4],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
  plt.plot([-0.53,7.0],  [7.1,7.1],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
  ax.text(-23,7.5,r'$0.0\%$', size='20')
  ax.text(2.5,3.2,r'$\mathrm{DNN~trained~on~} \kappa_\lambda = 1$', size='20')

ax.text(2.5,4.5,  r'$\sqrt{s} = 14~\mathrm{TeV},~3000~\mathrm{fb}^{-1}$', size='20')
ax.text(2.5,2,  r'$hh\rightarrow 4b,~68\%~\mathrm{CL~intervals}$', size='20')
ax.legend(frameon=False,scatterpoints=1,numpoints=1,prop={'size':18})
#-------------------------------------
# y-axis labels for each measurement
#-------------------------------------
#ax.set_yticklabels(labels)

print('axes')
#-------------------------------------
# Axis ticks
#-------------------------------------
ax.minorticks_on()
ax.tick_params('x', length=12, width=1, which='major', labelsize='20', pad=10)
ax.tick_params('x', length=6, width=1, which='minor') 
ax.tick_params('y', length=0, width=0, which='major', labelsize='0', pad=-1)
ax.tick_params('y', length=0, width=0, which='minor', labelsize='0') 
ax.yaxis.set_major_formatter(plt.NullFormatter())
print('axes size')
#-------------------------------------
# Axes size
#-------------------------------------
plt.xlabel(r'$\kappa_\lambda$', size='30', labelpad=15 )
plt.ylabel(r'$\mathrm{Background~systematic}$', size='30', labelpad=60 )
plt.xlim(-20.,20.)
plt.ylim(1., 20.)

#-------------------------------------
# Additional annotations
#-------------------------------------
plt.tight_layout(pad=0.3)
plt.subplots_adjust(left=0.15)
print('saving to file')
# Save to file
if klam5:
  save_name = 'figs/summary_1dlimits_DNNklam5.pdf'
else:
  save_name = 'figs/summary_1dlimits_DNNklam1.pdf'

plt.savefig(save_name, format='pdf', dpi=200)
