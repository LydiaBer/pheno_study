import ROOT as R

import numpy as np
from array import array

from copy import deepcopy

def ComputeBasicMuQCD(data_ntag, ttbar_ntag, data_0tag, ttbar_0tag):
  
  #
  # 4/3/2-tag
  #
  # Data
  N_ntag_data = data_ntag.Integral(0, data_ntag.GetNbinsX()+1)
  E_ntag_data = N_ntag_data**(0.5)
  #
  # ttbar
  E_ntag_top = R.Double(0)
  N_ntag_top = ttbar_ntag.IntegralAndError(0, ttbar_ntag.GetNbinsX()+1, E_ntag_top)
  #
  # Data - ttbar
  N_ntag_qcd = N_ntag_data - N_ntag_top
  E_ntag_qcd = ( E_ntag_data**2 + E_ntag_top**2 )**(0.5)
  
  #
  # 0-tag
  #
  # Data
  N_0tag_data = data_0tag.Integral(0, data_0tag.GetNbinsX()+1)
  E_0tag_data = N_0tag_data**(0.5)
  #
  # ttbar
  E_0tag_top = R.Double(0)
  N_0tag_top = ttbar_0tag.IntegralAndError(0, ttbar_0tag.GetNbinsX()+1, E_0tag_top)
  #
  # Data - ttbar
  N_0tag_qcd = N_0tag_data - N_0tag_top
  E_0tag_qcd = ( E_0tag_data**2 + E_0tag_top**2 )**(0.5)

  ####
  mu_qcd = N_ntag_qcd / N_0tag_qcd
  mu_qcd_err = mu_qcd * ( (E_ntag_qcd/N_ntag_qcd)**2 + (E_0tag_qcd/N_0tag_qcd) )**(0.5)

  print "No Fit: mu_qcd = ", mu_qcd, "+/-", mu_qcd_err
  print "No Fit: Ndata_s=", N_ntag_data, "+/-", E_ntag_data
  print "No Fit: Ndata_c=", N_0tag_data, "+/-", E_0tag_data
  print "No Fit: Ntop_s=", N_ntag_top, "+/-", E_ntag_top
  print "No Fit: Ntop_c=", N_0tag_top, "+/-", E_0tag_top
  print "No Fit: Nqcd_s=", N_ntag_qcd, "+/-", E_ntag_qcd
  print "No Fit: Nqcd_c=", N_0tag_qcd, "+/-", E_0tag_qcd

  return [mu_qcd, mu_qcd_err]

class BackgroundFitter:
    
  def __init__(self,name="Fitter"):
    print "Creating BackgroundFitter : ", name
    self.name = name
    self.h_qcd = None
    self.h_top = None
    self.h_top_in_bkg_model = None
    self.h_data = None
    self.minuit = None

    out = {}
  
  def NegLogL(self, npar, gin, f, par, ifag):
    L = 0.0

    self.muqcd = par[0];
    self.topscale = par[1];

    Nbins = self.h_data.GetNbinsX()

    for ibin in range(1,Nbins+1):
      expected_i = self.muqcd * self.h_qcd.GetBinContent(ibin) + self.topscale * self.h_top.GetBinContent(ibin)
      
      if expected_i > 0:
        L += expected_i - (self.h_data.GetBinContent(ibin)) * np.log( expected_i );

    f[0] = L
    return

  def Initialize(self, data_ntag, ttbar_ntag,data_bkd_model,ttbar_bkd_model):
    #
    # Get Histograms
    #
    self.h_data = data_ntag.Clone("data")
    self.h_top  = ttbar_ntag.Clone("top")
    self.h_qcd  = data_bkd_model.Clone("qcd")
    normFactorLowerTag = ttbar_ntag.Integral()/data_bkd_model.Integral()
    self.h_top_in_bkg_model = ttbar_ntag.Clone("top_in_bkg_model")
    self.h_top_in_bkg_model.Scale(normFactorLowerTag)
    self.h_data.Add(self.h_top, 1.5)
    #
    # Setup Minuit
    #
    self.minuit = R.TMinuit(2) # 2 parameter fit
    self.minuit.SetPrintLevel(1)
    self.minuit.SetErrorDef(0.5)
    self.minuit.SetFCN(self.NegLogL)

  def RunFit(self,dataLabel,outDir):
    results = self.__Fit()
    print "********************************"
    print "Fit Results for : ", self.name
    print " "
    print "mu_qcd = ", results["muqcd"], "+/-", results["muqcd_e"]
    print "top_scale = ", results["topscale"], "+/-", results["topscale_e"]
    print "correlation=", results["corr_muqcd_topscale"]
    print "********************************"
    
    text_file = open(outDir + "/DataDrivenNorm_"+self.name+".txt", "w")
    text_file.write("%s \n" %(self.name))
    text_file.write("mu_qcd = %f +/- %f \n" %(results["muqcd"], results["muqcd_e"]))
    text_file.write("top_scale = %f +/- %f \n" %(results["topscale"], results["topscale_e"]))
    text_file.write("correlation = %f \n" %(results["corr_muqcd_topscale"]))
    text_file.close()
    
    self.MakePlot( results["muqcd"], results["topscale"],dataLabel,outDir)
    
    return results
    
  def __Fit(self):
    self.__ClearMinuit()
    self.minuit.Migrad()
    self.minuit.Command("MINOS")

    eparab = R.Double(0) #dummy
    gcc = R.Double(0)    #dummy

    muqcd         = R.Double(0)
    muqcd_e       = R.Double(0)
    muqcd_e_up    = R.Double(0)
    muqcd_e_dw    = R.Double(0)
    topscale      = R.Double(0)
    topscale_e    = R.Double(0)
    topscale_e_up = R.Double(0)
    topscale_e_dw = R.Double(0)
    
    self.minuit.GetParameter( 0, muqcd, muqcd_e )
    self.minuit.mnerrs( 0, muqcd_e_up, muqcd_e_dw, eparab, gcc )

    self.minuit.GetParameter( 1, topscale, topscale_e );
    self.minuit.mnerrs( 1, topscale_e_up, topscale_e_dw, eparab, gcc );

    cov= array('d', [0,0,0,0])
    self.minuit.mnemat(cov,2) # stored as if [ cov[0,0], cov[1,0], cov[0,1], cov[1,1] ]
    corr_muqcd_topscale = cov[1]  / ( cov[0] * cov[3] )**(0.5)

    out = { "muqcd" : muqcd,
            "muqcd_e" : muqcd_e,
            "muqcd_e_up" : muqcd_e_up,
            "muqcd_e_dw" : muqcd_e_dw,
            "topscale" : topscale,
            "topscale_e" : topscale_e,
            "topscale_e_up" : topscale_e_up,
            "topscale_e_dw" : topscale_e_dw,
            "corr_muqcd_topscale": corr_muqcd_topscale }
    return out
    
  def __ClearMinuit(self):
    print self.minuit
    self.minuit.Command("CLEAR");
    self.minuit.DefineParameter(0,"muqcd", 0.01, 0.01, 0.00001, 100);
    self.minuit.DefineParameter(1,"topscale",1.5, 0.1, 0.00001, 400);
    return
    
  def MakePlot(self, muqcd, topscale,dataLabel,outDir):
    c=R.TCanvas("c_"+self.name,"c",600,600)
    c.SetFillStyle( 4000 )
    #
    # Make
    #
    the_low_margin = 0.3
    pad1 = R.TPad("pad1","pad1",0.0, the_low_margin, 1.0, 1.0)
    pad1.SetTopMargin( 0.06 )
    pad1.SetBottomMargin( 0.0 )
    pad1.SetFillStyle( 4000 )
    pad1.SetFillColor( 0 )
    pad1.SetFrameFillStyle( 4000 )
    pad1.SetFrameFillColor( 0 )
    pad1.Draw()
    #
    
    pad2 = R.TPad("pad2","pad2",0.0, 0.0, 1.0, the_low_margin)
    pad2.SetTopMargin( 0.10 )
    pad2.SetBottomMargin( 0.325 )
    pad2.SetFillStyle( 4000 )
    pad2.SetFillColor( 0 )
    pad2.SetFrameFillStyle( 4000 )
    pad2.SetFrameFillColor( 0 )
    pad2.Draw()
    pad1.cd()
    #
    latex = R.TLatex()
    latex.SetNDC()
    latex.SetTextFont( 42 )
    latex.SetTextSize( 0.035 )
    latex.SetTextColor( 1 )
    latex.SetTextAlign( 12 )
    h_data2 = self.h_data.Clone("data2")
    info = self.name
    print "cuy   ****"+info
    h_data2.SetFillColor(0)
    h_data2.SetLineColor(R.kBlack)
    h_data2.SetLineWidth(2)
    self.SetDataStyle(h_data2)
    #h_data2.Rebin(nrebin)
        
    h_top2 = self.h_top.Clone("top2")
    h_top2.Scale( topscale )
    h_top2.SetFillColor(R.kGreen)
    h_top2.SetLineColor(R.kBlack)
    h_top2.SetLineWidth(1)
    #h_top2.Rebin(nrebin)

    h_qcd2 = self.h_qcd.Clone("qcd2")
    h_qcd2.Scale( muqcd )
    h_qcd2.SetLineColor(R.kRed)
    h_qcd2.SetFillColor(0)
    h_qcd2.SetLineWidth(1)
    #h_qcd2.Rebin(nrebin)

    h_pred = h_top2.Clone("pred")
    h_pred.Add( h_qcd2, 1.0)
    h_pred.SetLineColor(R.kBlue)
    h_pred.SetFillColor(0)
    h_pred.SetLineWidth(1)

    h_data2.SetStats(False)
    h_top2.SetStats(False)
    h_qcd2.SetStats(False)
    h_pred.SetStats(False)
    
    h_data2.Draw("E")
    h_top2.Draw("sameHIST")
    h_qcd2.Draw("sameHIST")
    h_pred.Draw("sameHIST")
    h_data2.Draw("sameE")
    
    maximum = h_data2.GetMaximum()
    h_data2.SetMaximum(1.35*maximum)
    pad1.Update()
    
    leg = R.TLegend(0.55,0.7,0.92,0.91)
    leg.SetNColumns( 1 )
    leg.SetFillStyle( 0 )
    leg.SetBorderSize( 0 )
    leg.SetTextFont( 43 )
    leg.SetTextSize( 18 )
    leg.AddEntry(h_data2,dataLabel+" + ttbar","PL")
    leg.AddEntry(h_top2,"ttbar ","F")
    leg.AddEntry(h_qcd2,"QCD model ","L")
    leg.AddEntry(h_pred,"ttbar + QCD","L")
    leg.SetFillColor(0)
    leg.Draw()

    btagregion = 'Sideband, 4b+3b+2b-split'
    ##if '4tag' in info:
    ##  btagregion = '4-Tag'
    ##elif '3tag' in info:
    ##  btagregion = '3-Tag'
    ##elif '2tagSplit' in info:
    ##  btagregion = '2-Tag-Split'
    latex.DrawLatex( 0.18, 0.87, ' #bf{%s}' % (btagregion))
    
    pad2.cd()
    pad2.SetGridy()
    
    ratio = h_data2.Clone("ratio")
    ratio.Divide(h_pred)
    ratio.SetMaximum( 1.75 )
    ratio.SetMinimum( 0.25 )
    
    ratio.SetLineStyle( 1 )
    ratio.SetLineColor( R.kBlack )
    ratio.SetMarkerSize( 0.8 )
    ratio.GetYaxis().SetNdivisions( 5, 3, 0 )
    ratio.SetMaximum( 1.75 )
    ratio.SetMinimum( 0.25 )
    
    ratio.GetYaxis().SetTitle( "#frac{Data}{Pred}" )
    ratio.GetYaxis().CenterTitle( True )
    self.SetDataStyle(ratio)
    ratio.Draw()
    pad2.Update()
    
    #
    # Draw line
    #
    line = R.TLine( pad2.GetUxmin(), 1, pad2.GetUxmax(), 1 )
    line.SetLineColor( R.kRed + 1 )
    line.SetLineWidth( 3 )
    line.Draw()
    #
    # Draw ratio again
    #
    ratio.Draw('same')  

    #raw_input()
    # print "Final Numbers after fit:"
    # print "Ndata = ", h_data2.Integral()
    # print "Npred = ", h_pred.Integral()
    # print "Nqcd = ", h_qcd2.Integral()
    # print "Ntop = ", h_top2.Integral()
    
    c.SaveAs(outDir + "/DataDrivenFit_"+self.name+".pdf")

    return c
    
  def SetDataStyle(self, h ):
   
    x = h.GetXaxis()
    x.SetLabelFont( 43 )
    x.SetTitleFont( 43 )
    x.SetLabelSize( 20 )
    x.SetTitleSize( 20 )
   
    y = h.GetYaxis()
    y.SetLabelFont( 43 )
    y.SetTitleFont( 43 )
    y.SetLabelSize( 20 )
    y.SetTitleSize( 20 )
   
    h.SetMarkerStyle( 20 )
    h.SetMarkerSize( 0.8 )
    h.SetLineColor( 1 )
   
    h.SetTitleOffset( 1.9, 'Y' )
    h.SetTitleOffset( 3.2, 'X' )
    
