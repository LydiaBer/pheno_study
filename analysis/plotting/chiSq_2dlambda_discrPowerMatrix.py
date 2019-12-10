#!/usr/bin/env python
'''

Welcome to chiSq_2dlambda_discrPowerMatrix.py
This is a simple script to plot the output of ntuples_to_chiSq.py

This creates a triangular 2D matrix with heat map
of chiSq(i,j) vs lambda_i vs lambda_j

'''

import matplotlib as mplt
mplt.use('Agg') # So we can use without X forwarding

import numpy as np
import math
import matplotlib.pyplot as plt
import csv, os
import matplotlib.colors as colors

# So we can produce PDFs
from matplotlib.backends.backend_pdf import PdfPages

#___________________________________________________
def show_values(pc, fmt="%.2f", **kw):
    '''
    Heatmap with text in each cell with matplotlib's pyplot
    Source: http://stackoverflow.com/a/25074150/395857 
    By HYRY
    '''
    #from itertools import izip
    pc.update_scalarmappable()
    ax = pc.get_axes()
    #for p, color, value in izip(pc.get_paths(), pc.get_facecolors(), pc.get_array()):
    for p, color, value in zip(pc.get_paths(), pc.get_facecolors(), pc.get_array()):
      x, y = p.vertices[:-2, :].mean(0)
      if np.all(color[:3] > 0.5):
        color = (0.0, 0.0, 0.0)
      else:
        color = (1.0, 1.0, 1.0)
      ax.text(x, y, fmt % value, ha="center", va="center", color=color, **kw)
    
#___________________________________________________
def heatmap(AUC, title, xlabel, ylabel, xticklabels, yticklabels, zlabel, my_file):
    '''
    From http://stackoverflow.com/questions/25071968/heatmap-with-text-in-each-cell-with-matplotlibs-pyplot
    Inspired by:
    - http://stackoverflow.com/a/16124677/395857 
    - http://stackoverflow.com/a/25074150/395857
    '''

    #----------------------------------------------
    # Plot it out
    #----------------------------------------------
    fig, ax = plt.subplots() 
    fig.set_size_inches(12, 8)
    my_cmap = mplt.cm.get_cmap('inferno_r')
    my_cmap.set_under('#ffffd9')
    
    #if 'lam10' in my_file:
    c = ax.pcolor(AUC, edgecolors='#FFFFFF', linestyle= 'solid', linewidths=1, cmap=my_cmap, norm=colors.LogNorm(vmin=0.001, vmax=1e3))
    #else:
    #c = ax.pcolor(AUC, edgecolors='#FFFFFF', linestyle= 'solid', linewidths=1, cmap=my_cmap, vmin=0.0, vmax=70.0)
     
    #----------------------------------------------
    # put the major ticks at the middle of each cell
    #----------------------------------------------
    ax.set_yticks(np.arange(AUC.shape[0]) + 0.5, minor=False)
    ax.set_xticks(np.arange(AUC.shape[1]) + 0.5, minor=False)
    # set tick labels
    #ax.set_xticklabels(np.arange(1,AUC.shape[1]+1), minor=False)
    ax.set_xticklabels(xticklabels, minor=False, rotation=0)
    ax.set_yticklabels(yticklabels, minor=False)
    
    # set title and x/y labels
    plt.title(title)
    plt.xlabel(xlabel, labelpad=20, size=30)
    plt.ylabel(ylabel, labelpad=20, size=30)

    # Remove last blank column
    plt.xlim( (0, AUC.shape[1]) )

    # Turn off all the ticks
    ax = plt.gca()    
    for t in ax.xaxis.get_major_ticks():
      t.tick1On = False
      t.tick2On = False
    for t in ax.yaxis.get_major_ticks():
      t.tick1On = False
      t.tick2On = False

    # Add color bar
    cb = plt.colorbar(c)
    cb.outline.set_linewidth(0)
    cb.set_label(label=zlabel, size=30, labelpad=10)
    
    #----------------------------------------------
    # Add text in each cell 
    #----------------------------------------------
    Nparam = len(yticklabels)
    for y in range(Nparam):
      for x in range(Nparam):
        
        cell_val = float(AUC[y, x])
        if abs(cell_val) > 0.1:
          cell_color = '#EFEFEF'
        if abs(cell_val) < 0.1:
          cell_color = '#232323'
        if x > y:
          if cell_val > 1000.:
            cell_text = r'$>10^3$'.format(cell_val)
          elif cell_val > 100.:
            cell_text = r'${0:.0f}$'.format(cell_val)
          elif cell_val > 0.01:
            cell_text = r'${0:.2g}$'.format(cell_val)
          else:
            cell_text = r'$< 0.01$'
        else:
          cell_text = ''
            
        plt.text(x + 0.5, y + 0.5, cell_text,
                 horizontalalignment='center',
                 verticalalignment='center',
                 color = cell_color,
                 size = 14
                 )
  
    #----------------------------------------------
    # Labelling text on plot
    #----------------------------------------------
    fig.text(0.17, 0.89, r'$\sqrt{s}=14~\textrm{TeV}, 3000~\textrm{fb}^{-1}$', color='Black', size=25)
    
    if 'SRNN' in my_file:
      fig.text(0.17, 0.83, r'$hh \to 4b~\textrm{Neural network analysis}$', color='Black', size=25)
    else:
      fig.text(0.17, 0.83, r'$hh \to 4b~\textrm{Baseline analysis}$', color='Black', size=25)
    fig.text(0.17, 0.765, r'$0.3\%~\textrm{systematics}$', color='Black', size=25)
   
    if 'combined' in my_file:
      fig.text(0.17, 0.71, r'$\textrm{Combined categories}$', color='Black', size=25) 
    elif 'resolved' in my_file:
      fig.text(0.17, 0.71, r'$\textrm{Resolved~category}$', color='Black', size=25)
    elif 'intermediate' in my_file:
      fig.text(0.17, 0.71, r'$\textrm{Intermediate~category}$', color='Black', size=25)
    else:
      fig.text(0.17, 0.71, r'$\textrm{Boosted~category}$', color='Black', size=25)
    
    if 'SRNN' in my_file:
      if 'lam10' in my_file:
        fig.text(0.17, 0.65, r'$\textrm{DNN trained on}~\kappa(\lambda_{hhh}) = 10$', color='Black', size=25)
      elif 'lam5' in my_file:
        fig.text(0.17, 0.65, r'$\textrm{DNN trained on}~\kappa(\lambda_{hhh}) = 5$', color='Black', size=25)
      else:
        fig.text(0.17, 0.65, r'$\textrm{DNN trained on}~\kappa(\lambda_{hhh}) = 1$', color='Black', size=25)
    
    plt.tight_layout(pad=0.5)

    #----------------------------------------------
    # Save as PDF  
    #----------------------------------------------
    mkdir('figs')
    save_name = 'figs/' + my_file.replace('.csv', '_Sys1pc.pdf') 
    plt.savefig(save_name, format='pdf', dpi=150)

#_______________________________________
def main():
  
  #----------------------------------------------
  # Lambda values to plot
  #----------------------------------------------
  l_lambda = [-20, -15, -10, -7, -5, -2, -1, 1, 2, 3, 5, 7, 10, 15, 20]
  N_dimensions = len(l_lambda)

  #----------------------------------------------
  # Data files to plot
  #----------------------------------------------
  l_files = [
    'CHISQ_2Dlambda_loose_preselection_SR_res_multibin_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SR_int_multibin_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SR_bst_multibin_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SR_all_multibin_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SRNN_res_multibin_lam1_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SRNN_int_multibin_lam1_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SRNN_bst_multibin_lam1_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SRNN_all_multibin_lam1_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SRNN_res_multibin_lam5_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SRNN_int_multibin_lam5_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SRNN_bst_multibin_lam5_combined_chiSq_ij_Sys0p3pc.csv',
    'CHISQ_2Dlambda_loose_preselection_SRNN_all_multibin_lam5_combined_chiSq_ij_Sys0p3pc.csv',
  ]

  for my_file in l_files:

    correlation_matrix = []
    correlation = []
    
    l_varX = []
    l_varY = []
    
    file_loc = 'data/' + my_file
    print('Processing {0}'.format(file_loc))
    
    #----------------------------------------------
    # Open file and sort data into lists
    #----------------------------------------------
    with open( file_loc ) as csvfile:
      myreader = csv.reader(csvfile, delimiter=',')
      previous_lambda = l_lambda[0]
      for rownum, row in enumerate(myreader):
        if 'lambda_i' in row: continue
        if float( row[0] ) not in l_lambda: continue
        if float( row[1] ) not in l_lambda: continue
        #print row
        
        # Fill each set of lambda values in a new list
        if not float( row[0] ) == previous_lambda:
          correlation_matrix.append(correlation)
          correlation = []
        if float(row[0]) > float(row[1]):
          correlation.append(-1.)
        else:
          correlation.append(float(row[3]))
        if row[0] not in l_varX:
          l_varX.append(float(row[0]))
        if row[1] not in l_varY:
          l_varY.append(float(row[1]))

        previous_lambda = float(row[0])
      # add the last correlations to the matrix
      correlation_matrix.append(correlation)
        
    #----------------------------------------------
    # Convert nested lists into numpy array
    #----------------------------------------------
    data = np.array(correlation_matrix)
    #print(data)
    
    #----------------------------------------------
    # Axis labels
    #----------------------------------------------
    xlabel = r'$\kappa(\lambda_{hhh}^i)$'
    ylabel = r'$\kappa(\lambda_{hhh}^j)$'
    zlabel = r'$\textrm{Discrimination power}~\chi^2_{ij}$'
    title  = ''
    xticklabels = []
    yticklabels = []
    
    # convert tick labels to latex
    for x in l_lambda:
      #x_latex = d_latex[x.strip()]
      x_latex = r'${0:.0f}$'.format(x)
      xticklabels.append(x_latex)
      #y_latex = d_latex[y.strip()]
      y_latex = r'${0:.0f}$'.format(x)
      yticklabels.append(y_latex)
    
    plt.rcParams.update({'font.size': 18})
    plt.rcParams['text.usetex'] = True 
    
    #----------------------------------------------
    # Make the heat map
    #----------------------------------------------
    heatmap(data, title, xlabel, ylabel, xticklabels, yticklabels, zlabel, my_file)

#_________________________________________________________________________
def mkdir(dirPath):
  # Makes new directory @dirPath
  try:
    os.makedirs(dirPath)
    print 'Successfully made new directory ' + dirPath
  except OSError:
    pass

if __name__ == "__main__":
    main()
