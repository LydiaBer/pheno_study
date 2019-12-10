'''

Welcome to variables.py

Here we configure how the variables are 
binned and labelled in the ROOT plots
using a dictionary d_vars = {}

'''

#____________________________________________________________________________
def configure_vars(cut_sel):
  
   
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
  #      }
  #
  # To do variable bin widths, place 'var' as value of 'hXNbins' 
  # and specify lower bin edges as 'binsLowE':[0,4,5,11,15,20,40,60]
  # e.g. 
  # 'lep2Pt':{'tlatex':'p_{T}(#font[12]{l}_{2})','units':'GeV','hXNbins':'var','hXmin':0,'hXmax':60,'binsLowE':[0,4,5,11,15,20,40,60]}
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
    #'m_hh' :{'tlatex':'m_hh','units':'GeV','hXNbins':100,'hXmin':200, 'hXmax':800},
    #'m_hh':{'tlatex':'m_hh','units':'GeV','hXNbins':'var','hXmin':150,'hXmax':2076,'binsLowE':[150, 250, 262, 275, 288, 302, 317, 332, 348, 365, 383, 402, 422, 443, 465, 488, 512, 537, 563, 591, 620, 651, 683, 717, 752, 789, 828, 869, 912, 957, 1004, 1054, 1106, 1161, 1219, 1279, 1342, 1409, 1479, 1552, 1629, 1710, 1795, 1884, 1978, 2076]},
    #'m_hh':{'tlatex':'m_hh','units':'GeV','hXNbins':'var','hXmin':150,'hXmax':2076,'binsLowE':[262, 275, 288, 302, 317, 332, 348, 365, 383, 402, 422, 443, 465, 488, 512, 537, 563, 591, 620, 651, 683, 717, 752, 789, 828, 869, 912, 957, 1004, 1054, 1106, 1161, 1219, 1279, 1342, 1409, 1479, 1552, 1629, 1710, 1795, 1884, 1978, 2076]},
    #'m_hh' :{'tlatex':'m_hh','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1000},

    'm_h1' :{'tlatex':'m_h1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':300},
    'm_h2' :{'tlatex':'m_h2','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':300},
    
    'pT_h1' :{'tlatex':'pT_h1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1000},
    'pT_h2' :{'tlatex':'pT_h2','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1000},

    'eta_h1' :{'tlatex':'#eta_h1','units':'GeV','hXNbins':100,'hXmin':-5, 'hXmax':5},
    'eta_h2' :{'tlatex':'#eta_h2','units':'GeV','hXNbins':100,'hXmin':-5,  'hXmax':5},

    'phi_h1' :{'tlatex':'#phi_h1','units':'GeV','hXNbins':100,'hXmin':-5, 'hXmax':5},
    'phi_h2' :{'tlatex':'#phi_h2','units':'GeV','hXNbins':100,'hXmin':-5,  'hXmax':5},
  
    'pT_hh' :{'tlatex':'pT_hh','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1000},
    'dR_hh' :{'tlatex':'dR_hh','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':5},
    'deta_hh' :{'tlatex':'d#eta_hh','units':'GeV','hXNbins':100,'hXmin':-5, 'hXmax':5},
    'dphi_hh' :{'tlatex':'d#phi_hh','units':'GeV','hXNbins':100,'hXmin':-5, 'hXmax':5},

    'pT_h1_j1' :{'tlatex':'pT_h1_j1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':500},
    'pT_h1_j2' :{'tlatex':'pT_h1_j2','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1000},
    'pT_h2_j1' :{'tlatex':'pT_h2_j1','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1000},
    'pT_h2_j2' :{'tlatex':'pT_h2_j2','units':'GeV','hXNbins':100,'hXmin':0, 'hXmax':1000},

    # For unified ntuples
    'n_small_tag'       : {'tlatex':'N(R=0.4 b-tagged jets)'            ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_small_jets'      : {'tlatex':'N(R=0.4 jets)'                     ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_large_tag'       : {'tlatex':'N(R=1.0 b-tagged jets)'            ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_large_jets'      : {'tlatex':'N(R=1.0 jets)'                     ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_track_tag'       : {'tlatex':'N(R=0.2 b-taggedjets)'             ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_track_jets'      : {'tlatex':'N(R=0.2 jets)'                     ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_jets_in_higgs1'  : {'tlatex':'N(jets #in h_{1}^{cand})'          ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_jets_in_higgs2'  : {'tlatex':'N(jets #in h_{2}^{cand})'          ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_bjets_in_higgs1' : {'tlatex':'N(b-tagged jets #in h_{1}^{cand})' ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'n_bjets_in_higgs2' : {'tlatex':'N(b-tagged jets #in h_{2}^{cand})' ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    
    'nElec' : {'tlatex':'N(electrons)' ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},
    'nMuon' : {'tlatex':'N(muons)'     ,'units':'','hXNbins':6,'hXmin':-0.5,'hXmax':5.5},

    'pT_hh'   : {'tlatex':'#it{p}_{T}(hh)'            ,'units':'GeV','hXNbins':40,'hXmin':0,'hXmax':1000},
    'dR_hh'   : {'tlatex':'#DeltaR(h_{1}, h_{2})'     ,'units':''   ,'hXNbins':20, 'hXmin':0,'hXmax':5},
    'dEta_hh' : {'tlatex':'|#Delta#eta(h_{1}, h_{2})|','units':''   ,'hXNbins':20, 'hXmin':0,'hXmax':5},
    'dPhi_hh' : {'tlatex':'|#Delta#phi(h_{1}, h_{2})|','units':''   ,'hXNbins':35, 'hXmin':0,'hXmax':3.5},
    'X_hh'    : {'tlatex':'X_{hh}                    ','units':'GeV','hXNbins':100,'hXmin':0,'hXmax':50},

    'h1_M'   : {'tlatex':'#it{m}(h_{1}^{cand})'             ,'units':'GeV','hXNbins':50,'hXmin':0   ,'hXmax':500},
    'h1_Eta' : {'tlatex':'#eta(h_{1}^{cand})'               ,'units':''   ,'hXNbins':50 ,'hXmin':-5  ,'hXmax':5},
    'h1_Phi' : {'tlatex':'#phi(h_{1}^{cand})'               ,'units':''   ,'hXNbins':70 ,'hXmin':-3.5,'hXmax':3.5},

    'h1_j1_M'   : {'tlatex':'m(j_{1} #in h_{1}^{cand})'     ,'units':'GeV','hXNbins':100,'hXmin':0   ,'hXmax':200},
    'h1_j1_Pt'  : {'tlatex':'p_{T}(j_{1} #in h_{1}^{cand})' ,'units':'GeV','hXNbins':100,'hXmin':0   ,'hXmax':1000},
    'h1_j1_Eta' : {'tlatex':'#eta(j_{1} #in h_{1}^{cand})'  ,'units':''   ,'hXNbins':50 ,'hXmin':-5  ,'hXmax':5},
    'h1_j1_Phi' : {'tlatex':'#phi(j_{1} #in h_{1}^{cand})'  ,'units':''   ,'hXNbins':70 ,'hXmin':-3.5,'hXmax':3.5},

    'h1_j2_M'   : {'tlatex':'m(j_{2} #in h_{1}^{cand})'     ,'units':'GeV','hXNbins':100,'hXmin':0   ,'hXmax':200},
    'h1_j2_Pt'  : {'tlatex':'p_{T}(j_{2} #in h_{1}^{cand})' ,'units':'GeV','hXNbins':100,'hXmin':0   ,'hXmax':1000},
    'h1_j2_Eta' : {'tlatex':'#eta(j_{2} #in h_{1}^{cand})'  ,'units':''   ,'hXNbins':50 ,'hXmin':-5  ,'hXmax':5},
    'h1_j2_Phi' : {'tlatex':'#phi(j_{2} #in h_{1}^{cand})'  ,'units':''   ,'hXNbins':70 ,'hXmin':-3.5,'hXmax':3.5},

    'h1_j1_dR'    : {'tlatex':'#DeltaR(j_{1} #in h_{1}^{cand}, h_{1}^{cand})'           ,'units':'','hXNbins':20,'hXmin':0,'hXmax':5},
    'h1_j2_dR'    : {'tlatex':'#DeltaR(j_{2} #in h_{1}^{cand}, h_{1}^{cand})'           ,'units':'','hXNbins':20,'hXmin':0,'hXmax':5},
    'h1_j1_j2_dR' : {'tlatex':'#DeltaR(j_{1} #in h_{1}^{cand}, j_{2} #in h_{1}^{cand})' ,'units':'','hXNbins':20,'hXmin':0,'hXmax':5},

    'h2_M'   : {'tlatex':'#it{m}(h_{2}^{cand})'             ,'units':'GeV','hXNbins':50,'hXmin':0,   'hXmax':500},
    'h2_Eta' : {'tlatex':'#eta(h_{2}^{cand})'               ,'units':''   ,'hXNbins':50 ,'hXmin':-5,  'hXmax':5},
    'h2_Phi' : {'tlatex':'#phi(h_{2}^{cand})'               ,'units':''   ,'hXNbins':70 ,'hXmin':-3.5,'hXmax':3.5},

    'h2_j1_M'   : {'tlatex':'m(j_{1} #in h_{2}^{cand})'     ,'units':'GeV','hXNbins':100,'hXmin':0   ,'hXmax':200},
    'h2_j1_Pt'  : {'tlatex':'p_{T}(j_{1} #in h_{2}^{cand})' ,'units':'GeV','hXNbins':100,'hXmin':0   ,'hXmax':1000},
    'h2_j1_Eta' : {'tlatex':'#eta(j_{1} #in h_{2}^{cand})'  ,'units':''   ,'hXNbins':50 ,'hXmin':-5  ,'hXmax':5},
    'h2_j1_Phi' : {'tlatex':'#phi(j_{1} #in h_{2}^{cand})'  ,'units':''   ,'hXNbins':70 ,'hXmin':-3.5,'hXmax':3.5},

    'h2_j2_M'   : {'tlatex':'m(j_{2} #in h_{2}^{cand})'     ,'units':'GeV','hXNbins':100,'hXmin':0   ,'hXmax':200},
    'h2_j2_Pt'  : {'tlatex':'p_{T}(j_{2} #in h_{2}^{cand})' ,'units':'GeV','hXNbins':100,'hXmin':0   ,'hXmax':1000},
    'h2_j2_Eta' : {'tlatex':'#eta(j_{2} #in h_{2}^{cand})'  ,'units':''   ,'hXNbins':50 ,'hXmin':-5  ,'hXmax':5},
    'h2_j2_Phi' : {'tlatex':'#phi(j_{2} #in h_{2}^{cand})'  ,'units':''   ,'hXNbins':70 ,'hXmin':-3.5,'hXmax':3.5},

    'h2_j1_dR'    : {'tlatex':'#DeltaR(j_{1} #in h_{2}^{cand}, h_{2}^{cand})'           ,'units':'','hXNbins':20,'hXmin':0,'hXmax':5},
    'h2_j2_dR'    : {'tlatex':'#DeltaR(j_{2} #in h_{2}^{cand}, h_{2}^{cand})'           ,'units':'','hXNbins':20,'hXmin':0,'hXmax':5},
    'h2_j1_j2_dR' : {'tlatex':'#DeltaR(j_{1} #in h_{2}^{cand}, j_{2} #in h_{2}^{cand})' ,'units':'','hXNbins':20,'hXmin':0,'hXmax':5},
    
    'h1_j1_BTagWeight' : {'tlatex':'b-tag efficiency of j_{1} #in h_{1}^{cand}','units':'','hXNbins':100 ,'hXmin':0,'hXmax':1.0},
    'h1_j2_BTagWeight' : {'tlatex':'b-tag efficiency of j_{2} #in h_{1}^{cand}','units':'','hXNbins':100 ,'hXmin':0,'hXmax':1.0},
    'h2_j1_BTagWeight' : {'tlatex':'b-tag efficiency of j_{1} #in h_{2}^{cand}','units':'','hXNbins':100 ,'hXmin':0,'hXmax':1.0},
    'h2_j2_BTagWeight' : {'tlatex':'b-tag efficiency of j_{2} #in h_{2}^{cand}','units':'','hXNbins':100 ,'hXmin':0,'hXmax':1.0},

    'elec1_M'   : {'tlatex':'m_{e}'     ,'units':'GeV','hXNbins':20,'hXmin':0.0 ,'hXmax':1},
    'elec1_Pt'  : {'tlatex':'p_{T}(e)'  ,'units':'GeV','hXNbins':20,'hXmin':0.0 ,'hXmax':100},
    'elec1_Eta' : {'tlatex':'#eta(e)'   ,'units':''   ,'hXNbins':50,'hXmin':-5.0,'hXmax':5.0},
    'elec1_Phi' : {'tlatex':'#phi(e)'   ,'units':''   ,'hXNbins':70,'hXmin':-3.5,'hXmax':3.5},

    'muon1_M'   : {'tlatex':'m_#mu'      ,'units':'GeV','hXNbins':20,'hXmin':0   ,'hXmax':1},
    'muon1_Pt'  : {'tlatex':'p_{T}(#mu)' ,'units':'GeV','hXNbins':20,'hXmin':0   ,'hXmax':100},
    'muon1_Eta' : {'tlatex':'#eta(#mu)'  ,'units':''   ,'hXNbins':50,'hXmin':-5.0,'hXmax':5.0},
    'muon1_Phi' : {'tlatex':'#phi(#mu)'  ,'units':''   ,'hXNbins':70,'hXmin':-3.5,'hXmax':3.5},

    'met_Et'  : {'tlatex':'E_{T}^{miss}'            ,'units':'GeV','hXNbins':80,'hXmin':0   ,'hXmax':400},
    'met_Phi' : {'tlatex':'#phi(#bf{p}_{T}^{miss})' ,'units':''   ,'hXNbins':20,'hXmin':-3.5,'hXmax':3.5}, 
    
    'nnscore_SlfCoup_1.0_sig'       : {'tlatex':'NN signal score trained on #kappa(#lambda_{hhh}) = 1','units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_1.0_top'       : {'tlatex':'NN top score trained on #kappa(#lambda_{hhh}) = 1','units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_1.0_qcd'       : {'tlatex':'NN QCD score trained on #kappa(#lambda_{hhh}) = 1','units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    
    'nnscore_SlfCoup_m20.0_sig'   : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = #minus20',  'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_m10.0_sig'   : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = #minus10',  'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_m7.0_sig'    : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = #minus7',   'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_m5.0_sig'    : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = #minus5',   'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_m2.0_sig'    : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = #minus2',   'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_m1.0_sig'    : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = #minus1',   'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_m0.5_sig'    : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = #minus0.5', 'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_0.5_sig'     : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = 0.5',       'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_1.0_sig'     : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = 1',         'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_2.0_sig'     : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = 2',         'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_3.0_sig'     : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = 3',         'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_5.0_sig'     : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = 5',         'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_7.0_sig'     : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = 7',         'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_10.0_sig'    : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = 10',        'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    'nnscore_SlfCoup_20.0_sig'    : {'tlatex':'NN signal score #kappa(#lambda_{hhh}) = 20',        'units':'','hXNbins':28,'hXmin':0.0,'hXmax':1.4},
    # -------------------//------------------------

  } # end of d_vars = {} dictionary

  # analysis specific binning and ranges 
  if 'res' in cut_sel:
    d_vars['m_hh']   = {'tlatex':'#it{m}_{hh}'               ,'units':'GeV','hXNbins':50,'hXmin':100,'hXmax':1100}
    d_vars['h1_Pt']  = {'tlatex':'#it{p}_{T}(h_{1}^{cand})'  ,'units':'GeV','hXNbins':25,'hXmin':0, 'hXmax' :500}
    d_vars['h2_Pt']  = {'tlatex':'#it{p}_{T}(h_{2}^{cand})'  ,'units':'GeV','hXNbins':25,'hXmin':0, 'hXmax' :500}
  if 'int' in cut_sel:
    d_vars['m_hh']    = {'tlatex':'#it{m}_{hh}'              ,'units':'GeV','hXNbins':40,'hXmin':200,'hXmax':1800}
    d_vars['h1_Pt']   = {'tlatex':'#it{p}_{T}(h_{1}^{cand})' ,'units':'GeV','hXNbins':20,'hXmin':200,'hXmax':1000}
    d_vars['h2_Pt']   = {'tlatex':'#it{p}_{T}(h_{2}^{cand})' ,'units':'GeV','hXNbins':20,'hXmin':0,  'hXmax':800}
  if 'bst' in cut_sel or 'boosted' in cut_sel:
    d_vars['m_hh']    = {'tlatex':'#it{m}_{hh}'              ,'units':'GeV','hXNbins':50,'hXmin':200,'hXmax':2700}
    d_vars['h1_Pt']   = {'tlatex':'#it{p}_{T}(h_{1}^{cand})' ,'units':'GeV','hXNbins':30,'hXmin':200,'hXmax':1700}
    d_vars['h2_Pt']   = {'tlatex':'#it{p}_{T}(h_{2}^{cand})' ,'units':'GeV','hXNbins':30,'hXmin':200,'hXmax':1700}

  return d_vars

