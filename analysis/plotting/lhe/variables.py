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
  #
  # Jets & MET
  #  - MET variables
  # ---------------------------------------------

  d_vars = {
    
    # -------------------//------------------------
    

    'Higgs1Pt' :{'ntup_var':'Higgs1Pt','tlatex':'#it{p}_{T}(h)',\
                'units':'GeV','hXNbins':100,'hXmin':0.0,'hXmax':500.,'cut_pos':0,'cut_dir':'right'},
    'Higgs1Eta' :{'ntup_var':'Higgs1Eta','tlatex':'#eta(h_{1})',\
                'units':'','hXNbins':50,'hXmin':-5.0,'hXmax':5.,'cut_pos':0,'cut_dir':'right'},
    'Higgs1Phi' :{'ntup_var':'Higgs1Phi','tlatex':'#phi(h_{1})',\
                'units':'','hXNbins':40,'hXmin':-4.0,'hXmax':4.,'cut_pos':0,'cut_dir':'right'},

    'Higgs2Pt' :{'ntup_var':'Higgs2Pt','tlatex':'#it{p}_{T}(h_{2})',\
                'units':'GeV','hXNbins':100,'hXmin':0.0,'hXmax':500.,'cut_pos':0,'cut_dir':'right'},
    'Higgs2Eta' :{'ntup_var':'Higgs2Eta','tlatex':'#eta(h_{2})',\
                'units':'','hXNbins':50,'hXmin':-5.0,'hXmax':5.,'cut_pos':0,'cut_dir':'right'},
    'Higgs2Phi' :{'ntup_var':'Higgs2Phi','tlatex':'#phi(h_{2})',\
                'units':'','hXNbins':40,'hXmin':-4.0,'hXmax':4.,'cut_pos':0,'cut_dir':'right'},

    'DiHiggsM' :{'ntup_var':'DiHiggsM','tlatex':'#font[12]{m}_{hh}',\
                'units':'GeV','hXNbins':120,'hXmin':200.0,'hXmax':800.,'cut_pos':0,'cut_dir':'right'},
    'DiHiggsDeltaEta' :{'ntup_var':'fabs(DiHiggsDeltaEta)','tlatex':'|#Delta#eta(h_{1}, h_{2})|',\
                'units':'','hXNbins':20,'hXmin':0.0,'hXmax':4.0,'cut_pos':0,'cut_dir':'right'},
    
    'h1_Pt' :{'ntup_var':'h1_Pt','tlatex':'#it{p}_{T}(h)',\
                'units':'GeV','hXNbins':100,'hXmin':0.0,'hXmax':500.,'cut_pos':0,'cut_dir':'right'},
    'm_hh' :{'ntup_var':'m_hh','tlatex':'#font[12]{m}_{hh}',\
                'units':'GeV','hXNbins':120,'hXmin':200.0,'hXmax':800.,'cut_pos':0,'cut_dir':'right'},
    

  } # end of d_vars = {} dictionary

  return d_vars

