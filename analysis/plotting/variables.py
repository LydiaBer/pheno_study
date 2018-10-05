'''

Welcome to variables.py

Here we configure how the variables are 
binned and labelled in the ROOT plots
using a dictionary d_vars = {}

'''

#____________________________________________________________________________
def configure_vars():
  
   
  # ---------------------------------------------
  #
  # Format for each variable entry
  #
  # 'variable name as in TTree ntuple of SusySkimHiggsino' 
  #    : {
  #       'tlatex'  : ROOT TLaTeX axis entry to display in plot
  #       'units'   : Units of variable to print on plot
  #       'hXNbins' : Number of bins
  #       'hXmin',  : Lower x axis edge
  #       'hXmax'   : Upper x axis edge 
  #       'cut_pos' : Arrow position (for N-1 plots)
  #       'cut_dir' : Cut direction for N-1 Zn significance scan and arrow direction
  #      }
  #
  # To do variable bin widths, place 'var' as value of 'hXNbins' 
  # and specify lower bin edges as 'binsLowE':[0,4,5,11,15,20,40,60]
  # e.g. 
  # 'lep2Pt':{'tlatex':'p_{T}(#font[12]{l}_{2})','units':'GeV','hXNbins':'var','hXmin':0,'hXmax':60,'binsLowE':[0,4,5,11,15,20,40,60],'cut_pos':200,'cut_dir':'left'}, 
  #
  # ---------------------------------------------
  
  # ---------------------------------------------
  #
  # Contents
  # TODO Fill in as add variables
  # ---------------------------------------------

  d_vars = {
   
    # -------------------//------------------------
   
    # ---------------------------------------------
    # Higgs variables
    # ---------------------------------------------
    'm_hh' :{'tlatex':'m_hh','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1800,'cut_pos':0.,'cut_dir':'right'},
    'm_h1' :{'tlatex':'m_h1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':300,'cut_pos':0.,'cut_dir':'right'},
    'pT_h1' :{'tlatex':'pT_h1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1000,'cut_pos':0.,'cut_dir':'right'},
    'm_hh/(pT_h1)' :{'tlatex':'m_hh/pT h1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':30,'cut_pos':0.,'cut_dir':'right'},
    'm_hh-(pT_h1)' :{'tlatex':'m_hh-pT h1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':300,'cut_pos':0.,'cut_dir':'right'},
    'm_hh/(eta_h1)' :{'tlatex':'m_hh/eta h1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':3000,'cut_pos':0.,'cut_dir':'right'},

    # -------------------//------------------------

  } # end of d_vars = {} dictionary

  return d_vars

