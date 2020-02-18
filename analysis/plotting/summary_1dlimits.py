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
myLightOrange  = '#fec49f'
myMediumOrange = '#fe9929'
myDarkOrange   = '#ec7014'
myMediumPink   = '#fcc5c0'
myDarkPink     = '#ae017e'
myLightPurple  = '#dadaeb'
myMediumPurple = '#9e9ac8'
myDarkPurple   = '#6a51a3'
myGreen  = '#41ab5d'
myPurple = '#9e9ac8'
myGrey   = '#a8a8a8'

# SM
plt.plot([1., 1.], [-1, 18.5], ls='-',lw=2.,color=myGrey)
ax.text(0.2, 18.8,r'$\mathrm{SM}$', size='20')

bstColor = myLightBlue
bstWidth = 2.3
intColor = myMediumBlue
intWidth = 2.6
resColor = myDarkBlue
resWidth = 2.9
comColor = myDarkPink
comWidth = 3.3
print('plot first')
# Dummy lines for legend
plt.plot([-25.,-25.],[-5,-5],'|',ms=0,mew=0,mec=bstColor,ls='-',lw=bstWidth,color=bstColor,label='$\mathrm{Boosted}$')
plt.plot([-25.,-25], [-5,-5],'|',ms=0,mew=0,mec=intColor,ls='-',lw=intWidth,color=intColor,label='$\mathrm{Intermediate}$')
plt.plot([-25,-25.], [-5,-5],'|',ms=0,mew=0,mec=resColor,ls='-',lw=resWidth,color=resColor,label='$\mathrm{Resolved}$')
plt.plot([-25.,-25.],[-5,-5],'|',ms=0,mew=0,mec=comColor,ls='-',lw=comWidth,color=comColor,label='$\mathrm{Combined}$')

% 5% systematic
plt.plot([-25.,25.],  [18.,18.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-8.2,15.8], [17.8,17.8],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-5.5,11.9],[17.6,17.6],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved
plt.plot([-4.7,11.6], [17.4,17.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined
ax.text(-38,17.8,r'5\% syst', size='20')

# 2% syst
plt.plot([-12.4,25.],  [16.,16.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-4.2,14.4], [15.8,15.8], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-2.6,9.7], [15.6,15.6], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-2.5,9.4],   [15.4,15.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'2\% syst', size='20')

# 1.5% syst
plt.plot([-11.0,25.],[14.,14.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-3.8,12.6],[13.8,13.8], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-2.4,8.9], [13.6,13.6], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-2.2,8.8],  [13.4,13.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'1.5\% syst', size='20')

# 1% syst
plt.plot([-10.1,17.6],[12.,12.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-3.4,11.4], [11.8,11.8],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-2.0,8.2],  [11.6,11.6], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-1.9,8.1],  [11.4,11.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'1\% syst', size='20')

# 0.3% syst
plt.plot([-8.2,13.9],[12.,12.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-3.1,10.5],[11.8,11.8], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-0.97,6.7],[11.6,11.6], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-0.8,6.6],  [11.4,11.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'0.3% syst', size='20')

# 0% syst
plt.plot([-8.0,13.2], [12.,12.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-3.0,10.4], [11.8,11.8],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-0.8,6.4],  [11.6,11.6],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-0.7,6.3],  [11.4,11.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'0\% syst', size='20')% 5% systematic
plt.plot([-25.,25.],  [18.,18.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-8.2,15.8], [17.8,17.8],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-5.5,11.9],[17.6,17.6],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved
plt.plot([-4.7,11.6], [17.4,17.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined
ax.text(-38,17.8,r'5\% syst', size='20')

# 2% syst
plt.plot([-12.4,25.],  [16.,16.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-4.2,14.4], [15.8,15.8], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-2.6,9.7], [15.6,15.6], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-2.5,9.4],   [15.4,15.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'2\% syst', size='20')

# 1.5% syst
plt.plot([-11.0,25.],[14.,14.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-3.8,12.6],[13.8,13.8], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-2.4,8.9], [13.6,13.6], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-2.2,8.8],  [13.4,13.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'1.5\% syst', size='20')

# 1% syst
plt.plot([-10.1,17.6],[12.,12.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-3.4,11.4], [11.8,11.8],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-2.0,8.2],  [11.6,11.6], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-1.9,8.1],  [11.4,11.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'1\% syst', size='20')

# 0.3% syst
plt.plot([-8.2,13.9],[12.,12.],   '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-3.1,10.5],[11.8,11.8], '|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-0.97,6.7],[11.6,11.6], '|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-0.8,6.6],  [11.4,11.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'0.3% syst', size='20')

# 0% syst
plt.plot([-8.0,13.2], [12.,12.],  '|',ms=10,mew=3,mec=bstColor,ls='-',lw=bstWidth,color=bstColor) # Boosted
plt.plot([-3.0,10.4], [11.8,11.8],'|',ms=10,mew=3,mec=intColor,ls='-',lw=intWidth,color=intColor) # Intermediate
plt.plot([-0.8,6.4],  [11.6,11.6],'|',ms=10,mew=3,mec=resColor,ls='-',lw=resWidth,color=resColor) # Resolved 
plt.plot([-0.7,6.3],  [11.4,11.4],'|',ms=10,mew=3,mec=comColor,ls='-',lw=comWidth,color=comColor) # Combined  
ax.text(-38,15.8,r'0\% syst', size='20')
# Label the range of SMEFT line
#ax.text(-0.055, 0.25,r'$\Lambda = 140~\mathrm{GeV}$', size='20')
ax.text(2.5,1.3,r'$\sqrt{s} = 14~\mathrm{TeV},~3000~\mathrm{fb}^{-1}$', size='20')
ax.text(2.5,0,  r'$hh\rightarrow 4b,~68\%~\mathrm{CL~intervals}$', size='20')
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
plt.xlabel(r'$\kappa(\lambda_{hhh})$', size='30', labelpad=15 )
plt.xlim(-20.,20.)
plt.ylim(-1., 20.)
'''
#-------------------------------------
# Legend
#-------------------------------------
print('legend handles')
# Construct legend handles and labels
leg_handles = []
leg_labels  = []
leg_handles.append( mlines.Line2D([], [], color=myBlue, linewidth=4, linestyle='-'))
leg_labels.append(r'$\mathrm{}$')
leg_handles.append( mlines.Line2D([], [], color=myOrange, linewidth=4, linestyle='-'))
leg_labels.append(r'$\mathrm{Theoretical~prediction}$')
leg_handles.append( mlines.Line2D([], [], color=myGreen, linewidth=4, linestyle='-'))
leg_labels.append(r'$\mathrm{PbPb} \to \mathrm{Pb}(\gamma\gamma\to\tau\tau)\mathrm{Pb}~\mathrm{(this~work)}$')
leg_handles.append( mlines.Line2D([], [], color=myGreen, linewidth=0, linestyle='-'))
leg_labels.append(r'$\mathrm{LHC}~\sqrt{s_\mathrm{NN}} = 5.02~\mathrm{TeV}$')

# Define the legend
print('legend')
leg = plt.legend(leg_handles,
                 leg_labels,
                 frameon=False,
                 #loc='upper left',
                 bbox_to_anchor=(0.81,1.0),
                 prop={'size':18},
                 borderpad=1.9,
                 labelspacing=0.2,
                 handlelength=0.8,
                 handleheight=1.5,
                 scatterpoints=1,
                 numpoints=1)

print('1 & 2 signal legend')
# Construct 1 and 2 sigma legend manually
plt.plot([-0.049, -0.029],   [8.0, 8.0], ls='-', lw=1.5, color='#555555')
plt.plot([-0.042, -0.042],   [7.9, 8.1], ls='-', lw=2,   color='#555555')
plt.plot([-0.036, -0.036],   [7.9, 8.1], ls='-', lw=2,   color='#555555')
plt.plot([-0.0416, -0.0364], [8.0, 8.0], ls='-', lw=4,   color='#555555')
print('1 & 2 sigma legend text')
ax.text(-0.037, 7.6,r'$1\sigma$', size='12')
ax.text(-0.030, 7.6,r'$2\sigma$', size='12')
'''
#-------------------------------------
# Additional annotations
#-------------------------------------
plt.tight_layout(pad=0.3)
plt.subplots_adjust(left=0.31)
print('saving to file')
# Save to file
plt.savefig('figs/summary_1dlimits.pdf', format='pdf', dpi=200)
