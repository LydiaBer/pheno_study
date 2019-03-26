#!/usr/bin/env python
'''

# Getting started
Run after running say a batch submission to generate plots

Run this script as

./dump_plots_to_beamer.py

This produces a LaTeX file frames.tex

Then in your beamer template, import this TeX file by

\input{frames}

to insert into the main beamer template e.g. in slides.tex.

# Things one can configure

Define signal regions to include in TeX in list sig_regs = []
Define variables to include in TeX in list my_vars = []
Map the variable name to LaTeX in make_latex() wherein lies a dictionary

mk_frame() is where we configure the LaTeX template for each frame

'''

import os

#____________________________________________________________________________
def main():

  #---------------------------------------------------
  # Cut selections to consider
  #---------------------------------------------------
  cut_sels = [
    'preselection',
    #'commonSR',
    'finalSR',
   ]

  #---------------------------------------------------
  # Variables to consider
  #---------------------------------------------------
  my_vars = [
   'n_small_tag',
   'n_small_jets',
   'n_large_tag',
   'n_large_jets',
   'n_track_tag',
   'n_track_jets',
   'n_jets_in_higgs1',
   'n_jets_in_higgs2',
   'n_bjets_in_higgs1',
   'n_bjets_in_higgs2',
   'nElec',
   'nMuon',

   'm_hh',
   'pT_hh',
   'dR_hh',
   'dEta_hh',
   'dPhi_hh',

   'h1_M',
   'h1_Pt',
   'h1_Eta',
   'h1_Phi',
   'h1_j1_M',
   'h1_j1_Pt',
   'h1_j1_Eta',
   'h1_j1_Phi',
   'h1_j1_BTagWeight',
   'h1_j2_M',
   'h1_j2_Pt',
   'h1_j2_Eta',
   'h1_j2_Phi',
   'h1_j2_BTagWeight',
   'h1_j1_dR',
   'h1_j2_dR',
   'h1_j1_j2_dR',

   'h2_M',
   'h2_Pt',
   'h2_Eta',
   'h2_Phi',
   'h2_j1_M',
   'h2_j1_Pt',
   'h2_j1_Eta',
   'h2_j1_Phi',
   'h2_j1_BTagWeight',
   'h2_j2_M',
   'h2_j2_Pt',
   'h2_j2_Eta',
   'h2_j2_Phi',
   'h2_j2_BTagWeight',
   'h2_j1_dR',
   'h2_j2_dR',
   'h2_j1_j2_dR',

   'elec1_Pt',
   'elec1_Eta',
   'elec1_Phi',
   'muon1_Pt',
   'muon1_Eta',
   'muon1_Phi',

   'met_Et',
   'met_Phi',
    ]


  frame_tex = ''
  #----------------------------------------------------
  # Make beamer frames, loop over (regions, variables)
  #----------------------------------------------------
  for reg in cut_sels:
    print('Making title frame for {0}'.format(reg))
    frame_tex += mk_reg_frame(reg)
    for var in my_vars:
      print('Making frame for {0}, {1}'.format(reg, var))
      frame_tex += mk_frame(reg, var)

  output_name = 'frames.tex'

  # Output file
  with open(output_name, 'w') as f_frame:
    f_frame.write(frame_tex)

  print('Saving to {0}'.format(output_name))

#____________________________________________________________________________
def make_latex(var):

  # Mapping variable to LaTeX
  d_var_latex = {
   'n_small_tag'          : r'$N(j_\text{small})$ b-tagged',
   'n_small_jets'         : r'$N(j_\text{small})$',
   'n_large_tag'          : r'$N(j_\text{large})$ b-tagged',
   'n_large_jets'         : r'$N(j_\text{large})$',
   'n_track_tag'          : r'$N(j_\text{track})$ b-tagged',
   'n_track_jets'         : r'$N(j_\text{track})$',
   'n_jets_in_higgs1'     : r'$N_j \in h_1^\text{cand}$', 
   'n_jets_in_higgs2'     : r'$N_j \in h_2^\text{cand}$',
   'n_bjets_in_higgs1'    : r'$N_\text{b-jets} \in h_1^\text{cand}$',
   'n_bjets_in_higgs2'    : r'$N_\text{b-jets} \in h_2^\text{cand}$',
   'nElec'                : r'$N_e$',
   'nMuon'                : r'$N_\mu$',

   'm_hh'                 : r'$m_{hh}$',
   'pT_hh'                : r'$p_\text{T}(hh)$',
   'dR_hh'                : r'$\Delta R(h_1, h_2)$',
   'dEta_hh'              : r'$|\Delta \eta(h_1, h_2)|$',
   'dPhi_hh'              : r'$|\Delta \phi(h_1, h_2)|$',

   'h1_M'                 : r'$m(h_1^\text{cand})$',
   'h1_Pt'                : r'$p_\text{T}(h_1^\text{cand})$',
   'h1_Eta'               : r'$\eta(h_1^\text{cand})$',
   'h1_Phi'               : r'$\phi(h_1^\text{cand})$',
   'h1_j1_M'              : r'$m(j_1 \in h_1^\text{cand})$',
   'h1_j1_Pt'             : r'$p_\text{T}(j_1 \in h_1^\text{cand})$',
   'h1_j1_Eta'            : r'$\eta(j_1 \in h_1^\text{cand})$',
   'h1_j1_Phi'            : r'$\phi(j_1 \in h_1^\text{cand})$',
   'h1_j1_BTagWeight'     : r'b-tag efficiency of $j_1 \in h_1^\text{cand}$',
   'h1_j2_M'              : r'$m(j_2 \in h_1^\text{cand})$',
   'h1_j2_Pt'             : r'$p_\text{T}(j_2 \in h_1^\text{cand})$',
   'h1_j2_Eta'            : r'$\eta(j_2 \in h_1^\text{cand})$',
   'h1_j2_Phi'            : r'$\phi(j_2 \in h_1^\text{cand})$',
   'h1_j2_BTagWeight'     : r'b-tag efficiency of $j_2 \in h_1^\text{cand}$',
   'h1_j1_dR'             : r'$\Delta R(j_1 \in h_1^\text{cand}, h_1^\text{cand})$',
   'h1_j2_dR'             : r'$\Delta R(j_2 \in h_1^\text{cand}, h_1^\text{cand})$',
   'h1_j1_j2_dR'          : r'$\Delta R(j_1 \in h_1^\text{cand}, j_2 \in h_1^\text{cand})$',

   'h2_M'                 : r'$m(h_2^\text{cand})$',
   'h2_Pt'                : r'$p_\text{T}(h_2^\text{cand})$',
   'h2_Eta'               : r'$\eta(h_2^\text{cand})$',
   'h2_Phi'               : r'$\phi(h_2^\text{cand})$',
   'h2_j1_M'              : r'$m(j_1 \in h_2^\text{cand})$',
   'h2_j1_Pt'             : r'$p_\text{T}(j_1 \in h_2^\text{cand})$',
   'h2_j1_Eta'            : r'$\eta(j_1 \in h_2^\text{cand})$',
   'h2_j1_Phi'            : r'$\phi(j_1 \in h_2^\text{cand})$',
   'h2_j1_BTagWeight'     : r'b-tag efficiency of $j_1 \in h_2^\text{cand}$',
   'h2_j2_M'              : r'$m(j_2 \in h_2^\text{cand})$',
   'h2_j2_Pt'             : r'$p_\text{T}(j_2 \in h_2^\text{cand})$',
   'h2_j2_Eta'            : r'$\eta(j_2 \in h_2^\text{cand})$',
   'h2_j2_Phi'            : r'$\phi(j_2 \in h_2^\text{cand})$',
   'h2_j2_BTagWeight'     : r'b-tag efficiency of $j_2 \in h_2^\text{cand}$',
   'h2_j1_dR'             : r'$\Delta R(j_1 \in h_2^\text{cand}, h_2^\text{cand})$',
   'h2_j2_dR'             : r'$\Delta R(j_2 \in h_2^\text{cand}, h_2^\text{cand})$',
   'h2_j1_j2_dR'          : r'$\Delta R(j_1 \in h_2^\text{cand}, j_2 \in h_2^\text{cand})$',

   'elec1_Pt'             : r'$p_\text{T}(e_1)$',
   'elec1_Eta'            : r'$\eta(e_1)$',
   'elec1_Phi'            : r'$\phi(e_1)$',
   'muon1_Pt'             : r'$p_\text{T}(\mu_1)$', 
   'muon1_Eta'            : r'$\eta(\mu_1)$',
   'muon1_Phi'            : r'$\phi(\mu_1)$',

   'met_Et'               : r'$E_\text{T}^\text{miss}$',
   'met_Phi'              : r'$\phi(\text{p}_\text{T}^\text{miss})$',
  }

  return d_var_latex[var]

#____________________________________________________________________________
def mk_reg_frame(reg):

  frame = r'''
%--------------------------------------
\begin{frame}
\centering
'''

  frame += r'''{\huge \mdseries '''
  frame += reg
  
  frame += r'''}
\end{frame}
%--------------------------------------

'''
  return frame

#____________________________________________________________________________
def mk_frame(reg, var):
  '''
  Return a beamer frame for the region and variable specified
  '''

  fig_1 = r'\includegraphics[width=1.1\textwidth]{../figs/loose_preselection_' + var + '_resolved-' + reg + '_LogY}'
  fig_2 = r'\includegraphics[width=1.1\textwidth]{../figs/loose_preselection_' + var + '_intermediate-' + reg + '_LogY}'
  fig_3 = r'\includegraphics[width=1.1\textwidth]{../figs/loose_preselection_' + var + '_boosted-' + reg + '_LogY}'

  col1_head = r'''
%--------------------------------------
\begin{frame}{'''
	
  col1_head += make_latex(var) + ' | ' + reg

  col1_head += r'''}
\centering
\begin{columns}
%
\begin{column}{0.32\textwidth}  
\centering
\begin{figure}
	'''

  col1_tail = r'''
\end{figure} 
\textbf{Resolved}
\end{column}
	'''

  col2_head = r'''
\begin{column}{0.32\textwidth}
\centering
\begin{figure}
	'''

  col2_tail = r'''
\end{figure} 
\textbf{Intermediate}
\end{column}
'''

  col3_head = r'''
\begin{column}{0.32\textwidth}
\centering
\begin{figure}
    '''

  col3_tail = r'''
\end{figure}
\textbf{Boosted}
\end{column}
\end{columns}
\end{frame}
%--------------------------------------

	'''


  frame_tex = col1_head + fig_1 + col1_tail + col2_head + fig_2 + col2_tail + col3_head + fig_3 + col3_tail

  return frame_tex


#_______________________________
if __name__ == "__main__":
  main()
