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

sampleName = 'SM hh signal'

doBlind = not(args.noBlind)

def main():
  myFile  = ROOT.TFile.Open("/home/paredes/pheno/testSoftware/pheno_study/analysis/outputs/boostTest/boosted_xptj200_4j.root")
  dRjj_h1 = myFile.Get("deltaRjj_h1")
  dRjj_h2 = myFile.Get("deltaRjj_h2")
  MakeSingleHist(dRjj_h1,"deltaRjj_h1","dRjj_leadH","",False,"dRjj_leadH.png")
  MakeSingleHist(dRjj_h2,"deltaRjj_h1","dRjj_sublH","",False,"dRjj_sublH.png")
  

def MakeSingleHist(h1, legh1, xaxisname, yaxisname, doLogY, pdftitle):
  
  #
  # Make TCanvas
  #
  canv = ROOT.TCanvas("canv","canv", 600, 600)
  canv.SetFillStyle( 4000 )
  #
  # Make
  #
  the_low_margin = 0.3
 
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
  
  #
  # Clone histogram
  #
  h1C = h1.Clone()
  h1C.SetLineWidth(2)
  h1C.SetLineColor(1)
  h1C.SetFillColor(ROOT.kYellow)
  
  leg.AddEntry(h1C, legh1, "f")
  
  h1C.Draw("hist") 

  latex.SetTextSize( 0.04 )
  latex.DrawLatex( 0.48, 0.87, ' #bf{%s}' % (sampleName))
  
  latex.SetTextSize( 0.035 )
  latex.SetTextColor( ROOT.kBlack )
  #NData = h1C.Integral(0,h1C.GetNbinsX()+1)
  #latex.DrawLatex( 0.16, 0.97, 'N.Entries = %d' % (NData))
  # latex.DrawLatex( 0.60, 0.97, '%s' % info)
  
  if yaxisname == "":
    yaxisname = h1.GetYaxis().GetTitle()
    h1C.GetYaxis().SetTitle(yaxisname)
  else:
    h1C.GetYaxis().SetTitle(yaxisname)
    
  if xaxisname == "":
    xaxisname = h1.GetXaxis().GetTitle()
    h1C.GetXaxis().SetTitle(xaxisname)
  else:
    h1C.GetXaxis().SetTitle(xaxisname)
    
  canv.Print(pdftitle)
  if doLogY:
    pad1.SetLogy()
    canv.Print(pdftitle)



if __name__ == '__main__':
  main()
  #main("VR_WP70")
  #main("VR_WP77")
