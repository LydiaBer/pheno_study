import os
import ROOT
import array
import collections
import math
import argparse

parser = argparse.ArgumentParser(description='Normalize low-tag and ttbar backgrounds to data for boosted hh to 4b.')
parser.add_argument('-f','--fileName',type=str, default='./hist-all.root', help='Name of the input file conaining histograms.')
parser.add_argument('-d','--dirPlots',type=str, default='./plots/', help='Directory to save histograms.')
parser.add_argument('--noBlind', action='store_true', help='Unblind signal region.')
args = parser.parse_args()

import BackgroundUtils as BkgdUtils

ROOT.gROOT.SetBatch(True)

lumi = 0.5
outDir  = args.dirPlots
signalName = 'loop_hh' 
s_4jName = 'xptj200_4j' 
s_2b2jName = 'xptb200_2b2j' 
s_4bName = 'xptb200_4b' 

signalLabel = 'signal'
s_4jLabel = 'xptj200_4j'
s_2b2jLabel = 'xptb200_2b2j'
s_4bLabel = 'xptb200_4b'

weight_4b = (3000000.0) * (1.0) * (1.0) / (24.0)
weight_4j = (3000000.0) * (1.0) * (0.120402509534) / (24.0)
weight_2b2j = (3000000.0) * (1.0) * (0.328262275954) / (24.0)

doBlind = not(args.noBlind)

def main(trackJetType = "FR"):
  
  fileDir = '../outputs/boostTest/'
  sampleList = [
    signalName,
    s_2b2jName,
    s_4jName,
    s_4bName
  ]

  variableList = [
    'hh_m',
    'hcand1_pt',
    'hcand2_pt',
    'hcand1_m',
    'hcand2_m',
    'hcand1_eta',
    'hcand2_eta',
    'hcand1_phi',
    'hcand2_phi',
    'hcand1jet1_pt', 
    'hcand1jet1_eta',
    'hcand1jet1_phi',
    'hcand1jet2_pt', 
    'hcand1jet2_eta',
    'hcand1jet2_phi',
    'hcand2jet1_pt', 
    'hcand2jet1_eta',
    'hcand2jet1_phi',
    'hcand2jet2_pt', 
    'hcand2jet2_eta',
    'hcand2jet2_phi'

    # add sub-jet mass?

    # 'hcand1jet1_nconstituents',
    # 'hcand1jet2_nconstituents',
    # 'hcand2jet1_nconstituents',
    # 'hcand2jet2_nconstituents',
    #'hcand1_hcand2_dR',
    #'hcand1_hcand2_dEta',
    #'hcand1_hcand2_dPhi',
  ]
  massregionList = [
    'SR',
    'CR',
    'SB',
    'lowTag_SR',
    'lowTag_CR',
    'lowTag_SB'
  ]
  tagRegionList = [
    '',
    'lowTag_'
    ]
 
  #trackJetType = "FR"
  #trackJetType = "VR_WP70"
  #trackJetType = "VR_WP77"

  histograms = MyDict()
  files = MyDict()

  #
  # Get all the histograms in the root file
  #
  #combining Control and SR for sample in sampleList:
  #combining Control and SR   files[sample]  = ROOT.TFile.Open(fileDir + 'boosted_' + sample + '.root')
  #combining Control and SR   for region in massregionList:
  #combining Control and SR         for variable in variableList:
  #combining Control and SR           histoName =  region + '_' + variable
  #combining Control and SR           histograms[sample][region][variable] = files[sample].Get(histoName)
  #combining Control and SR           print histograms[sample][region][variable].GetName(),' retrieved from  ', histoName 

  for sample in sampleList:
    files[sample]  = ROOT.TFile.Open(fileDir + 'boosted_' + sample + '.root')
    for region in tagRegionList:
          for variable in variableList:
            histoName =  region + 'SB_' + variable
            histograms[sample][region + 'SB'][variable] = files[sample].Get(histoName)
            print histograms[sample][region + 'SB'][variable],' retrieved from  ', histoName 
            addedHisto = files[sample].Get(region + 'CR_' + variable) + files[sample].Get(region + 'SR_' + variable)
            histograms[sample][region + 'SR'][variable] = addedHisto
  
  # data
  data_4tag_SB = weight_4b*histograms[s_4bName]['SB']['hcand1_m'] + weight_4j*histograms[s_4jName]['SB']['hcand1_m'] + weight_2b2j*histograms[s_2b2jName]['SB']['hcand1_m'] 
  print data_4tag_SB
  #data_bkd_model_for_SB = histograms[dataName]['0tag_SB']['hcand1_m']
  data_bkd_model_for_4b_SB = weight_4b*histograms[s_4bName]['lowTag_SB']['hcand1_m'] + weight_4j*histograms[s_4jName]['lowTag_SB']['hcand1_m'] + weight_2b2j*histograms[s_2b2jName]['lowTag_SB']['hcand1_m']
  print data_bkd_model_for_4b_SB

  mu_4tag = data_4tag_SB.Integral(0,data_4tag_SB.GetNbinsX()+1)/data_bkd_model_for_4b_SB.Integral(0,data_bkd_model_for_4b_SB.GetNbinsX()+1) 
  print 'norm factor    ', mu_4tag
  

  for massregion in ['SB','SR']:
      for variable in variableList:
        #
        # GetHisto
        #
        hist_lowerTag_4tag = weight_4b*histograms[s_4bName]['lowTag_' + massregion][variable] + weight_4j*histograms[s_4jName][ 'lowTag_' + massregion][variable] +weight_2b2j*histograms[s_2b2jName]['lowTag_' + massregion][variable] 
        #hist_lowerTag = histograms[dataName]['_lowerTag_'+massregion][variable] 
        #
        # 4-tag QCD
        #
        qcdName = 'qcd_Boosted_4tag_'+massregion+'_h_'+variable
        hist_lowerTagC_4tagqcd = hist_lowerTag_4tag.Clone(qcdName)
        #hist_lowerTagC_4tagqcd = hist_lowerTag.Clone(qcdName)
        hist_lowerTagC_4tagqcd.Scale(mu_4tag)
        histograms['qcd'][massregion][variable] = hist_lowerTagC_4tagqcd
    
        data_4tag = weight_4b*histograms[s_4bName][massregion][variable] + weight_4j*histograms[s_4jName][massregion][variable] +weight_2b2j*histograms[s_2b2jName][massregion][variable] 

        clone_bkg_4b   = weight_4b*histograms[s_4bName]['lowTag_' + massregion][variable].Clone('scaled_4b_lowtag')
        clone_bkg_4j   = weight_4j*histograms[s_4jName]['lowTag_' + massregion][variable].Clone('scaled_4j_lowtag')
        clone_bkg_2b2j   = weight_2b2j*histograms[s_2b2jName]['lowTag_' + massregion][variable].Clone('scaled_2b2j_lowtag')

        clone_bkg_4b.Scale(mu_4tag)  
        clone_bkg_4j.Scale(mu_4tag)  
        clone_bkg_2b2j.Scale(mu_4tag)
        
        doLogY = False
        if "hcand1_pt" in variable:
          doLogY = True
        elif "hcand2_pt" in variable:
          doLogY = True
        elif "hh_mass" in variable:
          doLogY = True
        
        #
        # Plot 4tag
        #
        MakeDataVsPredictionPlots(data_4tag, clone_bkg_4b, clone_bkg_4j, clone_bkg_2b2j,  "bkg 4b", "bkg 4j","bkg 2b2j","", "Events", False, doLogY,trackJetType+"_4tag_"+massregion,"_estimationVSbkg_"+massregion+"_"+variable)
#  9 def MakeDataVsPredictionPlots(data,     l    ttbar,           h1,           h2,             h3,   legttbar,    legh1,    legh2,      legh3, xaxisname, yaxisname, doBlind, doLogY, info, pdftitle):

          
        #else:
        #  sig_4tag = histograms[signalName][massregion][variable].Clone("sig_bkgd_4tag")
        #  
        #  sig_4tag.Scale(2)
        #  
        #  sig_4tag.Add(qcd_4tag)    
        #  
        #  sig_4tag.Add(ttbar_4tag)    
        #
        #  if doBlind:
        #    #
        #    # Plot 4tag
        #    #
        #    MakeDataVsPredictionPlots(sig_4tag, qcd_4tag, ttbar_4tag, "QCD", "t#bar{t}", "", "Events", True, doLogY,trackJetType+"_4tag_"+massregion, trackJetType+"_DatavsQCD_4tag_"+massregion+"_"+variable)
        #  else:
        #    #
        #    # Plot 4tag
        #    #
        #    MakeDataVsPredictionPlots(data_4tag, qcd_4tag, ttbar_4tag, "QCD", "t#bar{t}", "", "Events", False, doLogY,trackJetType+"_4tag_"+massregion, trackJetType+"_DatavsQCD_4tag_"+massregion+"_"+variable)
           
  regionsForYields = [
    '2tagsplit_SR',
    '2tagsplit_CR',
    '2tagsplit_SB',
    '3tag_SR',
    '3tag_CR',
    '3tag_SB',
    '4tag_SR',
    '4tag_CR',
    '4tag_SB',
  ]
  
  #for region in regionsForYields:
  #  yields_qcd   = histograms['qcd'][region]["hh_mass"].Integral(0,histograms['qcd'][region]["hh_mass"].GetNbinsX()+1)
  #  yields_ttbar = histograms['ttbar'][region]["hh_mass"].Integral(0,histograms['ttbar'][region]["hh_mass"].GetNbinsX()+1)
  #  yields_pred  = yields_qcd + yields_ttbar
  #  if 'SR' in region and doBlind:
  #    yields_data  = 'BLIND'
  #    print '%s, %s (%.1f), ratio = BLIND, qcd = %.1f, ttbar = %.1f ' %(region, yields_data, yields_pred, yields_qcd, yields_ttbar)
  #  else:
  #    yields_data  = histograms[dataName][region]["hh_mass"].Integral(0,histograms[dataName][region]["hh_mass"].GetNbinsX()+1)
  #    print '%s, %.1f (%.1f), ratio = %.2f, qcd = %.1f, ttbar = %.1f ' %(region, yields_data, yields_pred, yields_data/yields_pred, yields_qcd, yields_ttbar)

  #
  # Save mhh histogram
  #
  # for region in ["4tag_SR","3tag_SR","2tagsplit_SR"]:
  #   outfile = ROOT.TFile.Open('./rootfiles/LimitSetting_Inputs_Backgrounds_'+trackJetType+'_'+region+'.root','RECREATE')
  #   histo_qcd_mhh = histograms['qcd'][region]["hh_mass"].Clone("qcd_hh")
  #   outfile.WriteTObject(histo_qcd_mhh)
  #   histo_ttbar_mhh = histograms['ttbar'][region]["hh_mass"].Clone("ttbar_hh")
  #   outfile.WriteTObject(histo_ttbar_mhh)
  #   outfile.Close()

  #
  # Save all histograms
  #
  outfile = ROOT.TFile.Open('./rootfiles/Histos_Backgrounds_'+trackJetType+'.root','RECREATE')
  for region in ["SB","SR"]:
    for variable in variableList:
      histo_qcd = histograms['qcd'][region][variable].Clone("qcd_"+region+"_"+variable)
      outfile.WriteTObject(histo_qcd)
     
  outfile.Close()
      
class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val
    
def MakeDataVsPredictionPlots(data, h1, h2, h3, legh1, legh2, legh3, xaxisname, yaxisname, doBlind, doLogY, info, pdftitle):
  
  #
  # Make TCanvas
  #
  canv = ROOT.TCanvas("canv","canv", 600, 600)
  canv.SetFillStyle( 4000 )
  #
  # Make
  #
  the_low_margin = 0.3
  pad1 = ROOT.TPad("pad1","pad1",0.0, the_low_margin, 1.0, 1.0)
  pad1.SetTopMargin( 0.06 )
  pad1.SetBottomMargin( 0.0 )
  pad1.SetFillStyle( 4000 )
  pad1.SetFillColor( 0 )
  pad1.SetFrameFillStyle( 4000 )
  pad1.SetFrameFillColor( 0 )
  pad1.Draw()
  #
  pad2 = ROOT.TPad("pad2","pad2",0.0, 0.0, 1.0, the_low_margin)
  pad2.SetTopMargin( 0.10 )
  pad2.SetBottomMargin( 0.325 )
  pad2.SetFillStyle( 4000 )
  pad2.SetFillColor( 0 )
  pad2.SetFrameFillStyle( 4000 )
  pad2.SetFrameFillColor( 0 )
  pad2.Draw()
  pad1.cd()
 
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextFont( 42 )
  latex.SetTextSize( 0.035 )
  latex.SetTextColor( 1 )
  latex.SetTextAlign( 12 )
 
  xLat = 0.35
  yLat = 0.90
  xLeg = xLat + 0.35
  yLeg = yLat
   
  leg_h =  0.07 * 3
  leg = ROOT.TLegend( xLeg, yLeg - leg_h, xLeg + 0.35, yLeg )
  leg.SetNColumns( 1 )
  leg.SetFillStyle( 0 )
  leg.SetBorderSize( 0 )
  leg.SetTextFont( 43 )
  leg.SetTextSize( 18 )
  
  stack = ROOT.THStack("stack","stack")
  
  #
  # Clone histogram
  #
  h1C = h1.Clone()
  h1C.SetLineWidth(2)
  h1C.SetLineColor(1)
  h1C.SetFillColor(ROOT.kYellow)
  
  stack.Add(h1C)
  leg.AddEntry(h1C, legh1, "f")
  
  #
  # Clone histogram
  #
  h2C = h2.Clone()
  h2C.SetLineWidth(2)
  h2C.SetLineColor(1)
  h2C.SetFillColor(ROOT.kCyan)
  
  stack.Add(h2C)
  leg.AddEntry(h2C, legh2, "f")
  
  #
  # Clone histogram
  #
  h3C = h3.Clone()
  h3C.SetLineWidth(2)
  h3C.SetLineColor(1)
  h3C.SetFillColor(ROOT.kViolet)
  
  stack.Add(h3C)
  leg.AddEntry(h3C, legh3, "f")
  
  stack.Draw("hist") 
  
  if yaxisname == "":
    yaxisname = h1.GetYaxis().GetTitle()
    stack.GetYaxis().SetTitle(yaxisname)
  else:
    stack.GetYaxis().SetTitle(yaxisname)
    
  if xaxisname == "":
    xaxisname = h1.GetXaxis().GetTitle()
    stack.GetXaxis().SetTitle(xaxisname)
  else:
    stack.GetXaxis().SetTitle(xaxisname)
    
  pad1.Update()
  
  
  #
  # Get total background histogram
  #
  totalbkgd   = stack.GetStack().Last().Clone("totalbkgd")
  systematics = [] 
  Syst = getSystematicUncertaintyBand(totalbkgd,systematics)
  Syst.SetFillColor( ROOT.kBlack )
  Syst.SetFillStyle( 3245 )
  Syst.SetLineColor( ROOT.kWhite )
  Syst.SetMarkerStyle( 1 )
  
  # Syst.Draw( 'E2 same' )
  
  if doBlind:
    dataC = data.Clone()
    dataC.SetLineColor(ROOT.kBlue)
    dataC.SetLineStyle(2)
    dataC.SetLineWidth(2)
    # dataC.SetFillColor(ROOT.kBlue)
    leg.AddEntry(dataC, "G(1000) x 2", "l")
    dataC.Draw('HIST same')
    stack.Draw('HIST same')
    Syst.Draw( 'E2 same' )
  else:
    Syst.Draw( 'E2 same' )
    dataC = data.Clone()
    SetDataStyle(dataC)
    leg.AddEntry(dataC, "NTag", "pe")
    dataC.Draw('P same')
  
  maximum = max(dataC.GetMaximum(), totalbkgd.GetMaximum())
  stack.SetMaximum(1.45*maximum)
  pad1.Update()
  
  #
  # Legend
  #
  #pad1.Modified()
  leg.Draw()
  
  
  #
  # Draw region text
  #
  btagregion = '4b+3b+2b-split'
  hcandmassregion = 'Signal Region'
  #if '4tag' in info:
  #  btagregion = '4-Tag'
  #elif '3tag' in info:
  #  btagregion = '3-Tag'
  #elif '2tag_' in info:
  #  btagregion = '2-Tag-Split'
    
  if 'SR' in info:
    hcandmassregion = 'Signal Region'
  elif 'CR' in info:
    hcandmassregion = 'Control Region'
  elif 'SB' in info:
    hcandmassregion = 'Sideband Region'
  
  latex.SetTextSize( 0.04 )
  latex.DrawLatex( 0.18, 0.87, ' #bf{%s %s}' % (btagregion,hcandmassregion))
  
  latex.SetTextSize( 0.035 )
  latex.SetTextColor( ROOT.kBlack )
  NData = dataC.Integral(0,totalbkgd.GetNbinsX()+1)
  NBkgd = totalbkgd.Integral(0,totalbkgd.GetNbinsX()+1)
  latex.DrawLatex( 0.16, 0.97, 'Data/Pred = %d/%.1f=%.2f ' % (NData,NBkgd,NData/NBkgd))
  # latex.DrawLatex( 0.60, 0.97, '%s' % info)

  kolg, chi2, ndf = compare(dataC, totalbkgd)
  #latex.SetTextAngle( 90 )
  # latex.DrawLatex(  0.97, 0.02, "KS = %5.3f, #chi^{2}/ndf = %.1f/%i = %.3f" %(kolg, chi2, ndf, chi2/ndf))
  latex.DrawLatex(  0.55, 0.97, "KS = %5.5f,  #chi^{2}/ndf = %.1f/%i = %.3f" %(kolg, chi2, ndf, chi2/ndf))
  
  latex.SetTextAngle( 90 )
  latex.DrawLatex( 0.97, 0.50, '%s' % info)

  pad2.cd()
  pad2.SetGridy()
  Ratio, SystBand = GetRatioHistogram( dataC, totalbkgd, Syst )
  #
  # Ratio
  #
  # Ratio = dataC.Clone("Ratio")
  # Ratio.Divide(h1C)
  
  # for i in range( 0, dataC.GetNbinsX()):
  #   bin = i + 1
  #   print dataC.GetBinError( bin )

 
  Ratio.SetLineStyle( 1 )
  Ratio.SetLineColor( ROOT.kBlack )
  Ratio.SetMarkerSize( 0.8 )
  Ratio.GetYaxis().SetNdivisions( 5, 3, 0 )
  Ratio.SetMaximum( 1.75 )
  Ratio.SetMinimum( 0.25 )
  Ratio.GetXaxis().SetTitle( xaxisname )
  if(doBlind):
    Ratio.GetYaxis().SetTitle( "#frac{Pred+Sig}{Pred}" )
  else:
    Ratio.GetYaxis().SetTitle( "#frac{Data}{Pred}" )
  Ratio.GetYaxis().CenterTitle( True )
  SetDataStyle(Ratio)  
  #
  # Draw ratio plot
  # 
  Ratio.SetStats(False)
  Ratio.Draw()
  #
  # Draw systematics band
  #
  SystBand.SetFillColor( ROOT.kBlack )
  SystBand.SetFillStyle( 3245 )
  SystBand.SetLineColor( ROOT.kWhite )
  SystBand.SetMarkerStyle( 1 )
  SystBand.Draw( 'E2same' )
  pad2.Update()
 
  #
  # Draw line
  #
  line = ROOT.TLine( pad2.GetUxmin(), 1, pad2.GetUxmax(), 1 )
  line.SetLineColor( ROOT.kRed + 1 )
  line.SetLineWidth( 3 )
  line.Draw()
 
  #
  # Draw ratio again
  #
  Ratio.Draw('same')  
 
  canv.Print(outDir + pdftitle + ".pdf")
  if doLogY:
    pad1.SetLogy()
    canv.Print(outDir + pdftitle + "_LogY.pdf")

def SetDataStyle( h ):
 
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

def getSystematicUncertaintyBand(nom,systematics):
  
  from ROOT import TGraphAsymmErrors
  from math import sqrt,pow
  # 
  # This is the quadrature sum of all the systematics this sample knows about.
  # 
  n_bins_combined = nom.GetNbinsX()
  x=[]; ex_up=[]; ex_down=[]
  y=[]; ey_up=[]; ey_down=[]

  
  for i in xrange(1, n_bins_combined+1, 1):
    up = 0.0
    down = 0.0
    
    x.append(nom.GetBinCenter(i))
    bin_width = nom.GetBinWidth(i)
    # print nom.GetBinCenter(i)

    ex_down.append(bin_width/2.)
    ex_up.append(bin_width/2.)
    y.append(nom.GetBinContent(i))
    
    for sysHist in systematics:
      print sysHist.GetName()
      n_bins = sysHist.GetNbinsX()
      if not n_bins == n_bins_combined:
        raise RuntimeError('Number of bins in histograms does not agree between systematics.')
      nominal = nom.GetBinContent(i)
      this_syst = sysHist.GetBinContent(i)
      up,down = addInQuadrature(nominal, this_syst,up,down)
      
    up,down = addInStatBin(i,nom,up,down)
    
    if up > 0: 
      ey_up.append(sqrt(up))
    else: 
      ey_up.append(0)
    if down > 0: 
      ey_down.append(sqrt(down))
    else: 
      ey_down.append(0)
    
  x = array.array('d',x)
  y = array.array('d',y)
  ex_up   = array.array('d',ex_up)
  ex_down = array.array('d',ex_down)
  ey_up   = array.array('d',ey_up)
  ey_down = array.array('d',ey_down)
  
  # ratio = TGraphAsymmErrors(n_bins_combined+1,x,y,ex_down,ex_up,ey_down,ey_up)
  # print n_bins_combined
  # print len(x)
  # print len(y)
  ratio = TGraphAsymmErrors(n_bins_combined,x,y,ex_down,ex_up,ey_down,ey_up)
  return ratio

def GetRatioHistogram( Data, MonteCarlo, Syst ):
  
  Result = Data.Clone( 'RatioHistogramFor' + Data.GetName() )
  SystBand = Syst.Clone( 'RatioHistogramFor' + MonteCarlo.GetName())
  SystBandFinal = Syst.Clone( 'FinalRatioHistogramFor' + MonteCarlo.GetName())
  
  AverageRatio = 0
  NumberOfPoints = 0

  for i in range(0, Result.GetNbinsX()):
    bin = i + 1
    
    x = SystBand.GetX()[i]
    y = SystBand.GetY()[i]
    
    xtemp = SystBandFinal.GetX()[i]
    ytemp = SystBandFinal.GetY()[i]
    
    x_err_up   = SystBand.GetEXhigh()[i]
    x_err_down = SystBand.GetEXlow()[i]
    y_err_up   = SystBand.GetEYhigh()[i]
    y_err_down = SystBand.GetEYlow()[i]
    
    SystBandFinal.SetPoint(i, x, 1.)
    if y > 0:
      SystBandFinal.SetPointEYhigh(i, y_err_up / y)
      SystBandFinal.SetPointEYlow(i, y_err_down / y)
    else:
      SystBandFinal.SetPointEYhigh(i, 0)
      SystBandFinal.SetPointEYlow(i, 0)
    
    SystBandFinal.SetPointEXhigh(i, x_err_up )
    SystBandFinal.SetPointEXlow(i, x_err_down )
    
    if MonteCarlo.GetBinContent( bin ) > 0:
      Result.SetBinContent( bin, Data.GetBinContent( bin ) / MonteCarlo.GetBinContent( bin ) )
      Result.SetBinError( bin, math.sqrt( math.pow( Data.GetBinError( bin ) / MonteCarlo.GetBinContent( bin ), 2 ) + math.pow( Data.GetBinContent( bin ) * MonteCarlo.GetBinError( bin ) / math.pow( MonteCarlo.GetBinContent( bin ), 2 ), 2 ) ) )
      AverageRatio += Data.GetBinContent( bin ) / MonteCarlo.GetBinContent( bin )
      NumberOfPoints += 1.
    
  Result.SetLineStyle( 1 )
  Result.SetLineColor( ROOT.kBlack )
  Result.SetMarkerSize( 0.8 )
  Result.GetYaxis().SetNdivisions( 5, 3, 0 )
  Result.SetMaximum( 1.75 )
  Result.SetMinimum( 0.25 )
  #Result.GetYaxis().SetTitle( '#frac{Data}{Pred}' )
  Result.GetYaxis().SetTitle( 'Data/Pred.' )
  Result.GetYaxis().CenterTitle( True )
  
  return (Result,SystBandFinal)
  
def addQuad(sys, nom):
  from math import sqrt,pow
  
  sys_diff = sys - nom
  sys_diff += pow(sys_diff,2)
  
  return sys_diff

def addInQuadrature(sys, nom, up, down):
  from math import sqrt,pow
  
  sys_diff = sys - nom
  
  if sys_diff > 0:
    up += pow(sys_diff,2)
  elif sys_diff < 0:
    down += pow(sys_diff,2)
    
  return (up,down)

def addInStatBin(i,nom, up, down):
  from math import sqrt,pow
  
  mcstat = nom.GetBinError(i)
  up += pow(mcstat,2)
  down += pow(mcstat,2)
  
  return (up,down)

def compare(data, pred):
  ks   = data.KolmogorovTest(pred)
  chi2 =        data.Chi2Test(pred, "QUWP CHI2")
  ndf  = chi2 / data.Chi2Test(pred, "QUW CHI2/NDF") if chi2 else 0.0
  return ks, chi2, ndf

if __name__ == '__main__':
  main("FR")
  #main("VR_WP70")
  #main("VR_WP77")
