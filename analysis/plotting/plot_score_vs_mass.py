#!/usr/bin/env python
'''
Script to make the m(h) and m(hh) vs DNN score 
2D correlation plots from the ntuples in inFileList

To run, do:

source /cvmfs/sft.cern.ch/lcg/views/LCG_94/x86_64-slc6-gcc8-opt/setup.sh
./plot_score_vs_mass.py

'''

import collections
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(1)
from ROOT import gSystem,TTree,TFile,TCanvas,TPad,gPad

def main():
  inFileList = [
      #"loose_ptj1_200_to_500_2b2j.ro.boosted_2_background_withNNs.root",
      #"loose_ptj1_200_to_500_2b2j.ro.intermediate_2_background_withNNs.root",
      #"loose_ptj1_500_to_1000_2b2j.ro.intermediate_2_background_withNNs.root",
      #"loose_ptj1_1000_to_infty_2b2j.ro.intermediate_2_background_withNNs.root",
      #"loose_ptj1_500_to_1000_2b2j.ro.boosted_2_background_withNNs.root",
      #"loose_ptj1_20_to_200_4b.ro.intermediate_2_background_withNNs.root",
      #"loose_ptj1_200_to_500_4b.ro.intermediate_2_background_withNNs.root",
      #"loose_ptj1_500_to_1000_4b.ro.intermediate_2_background_withNNs.root",
      #"loose_ptj1_1000_to_infty_2b2j.ro.boosted_2_background_withNNs.root",
      #"loose_ptj1_1000_to_infty_4b.ro.intermediate_2_background_withNNs.root",
      #"loose_ptj1_20_to_200_4b.ro.boosted_2_background_withNNs.root",
      #"loose_ptj1_200_to_500_4b.ro.boosted_2_background_withNNs.root",
      "loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_1.0_merged.ro.intermediate_2_withNNs.root",
      #"loose_ptj1_500_to_1000_4b.ro.boosted_2_background_withNNs.root",
      "loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_5.0_merged.ro.intermediate_2_withNNs.root",
      #"loose_ptj1_1000_to_infty_4b.ro.boosted_2_background_withNNs.root",
      "loose_noGenFilt_ttbar.ro.intermediate_2_background_withNNs.root",
      "loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_1.0_merged.ro.boosted_2_withNNs.root",
      "loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_5.0_merged.ro.boosted_2_withNNs.root",
      "loose_noGenFilt_ttbar.ro.resolved_2_background_withNNs.root",
      #"loose_ptj1_20_to_200_2b2j.ro.resolved_2_background_withNNs.root",
      #"loose_ptj1_200_to_500_2b2j.ro.resolved_2_background_withNNs.root",
      #"loose_ptj1_500_to_1000_2b2j.ro.resolved_2_background_withNNs.root",
      #"loose_ptj1_20_to_200_4b.ro.resolved_2_background_withNNs.root",
      #"loose_ptj1_200_to_500_4b.ro.resolved_2_background_withNNs.root",
      #"loose_ptj1_500_to_1000_4b.ro.resolved_2_background_withNNs.root",
      "loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_1.0_merged.ro.resolved_2_withNNs.root",
      "loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_5.0_merged.ro.resolved_2_withNNs.root",
      "loose_noGenFilt_ttbar.ro.boosted_2_background_withNNs.root"
      ]
  #varList = ["event.h1_M","event.h2_M","event.m_hh"]
  #varList = ["event.h1_M"]
  varList = ["event.m_hh"]
  #netList = ["nnscore_w_OPsgdEP30BS100DO05","nnscore_w_OPadamaxEP30BS100DO03"]
  #already got lambda = 1
  netList = ["SlfCoup_5.0","SlfCoup_1.0"]
  #netList = ["SlfCoup_5.0"]
  filePath = "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/"

  ROOT.gStyle.SetOptStat(0)
  ROOT.gStyle.SetPalette(ROOT.kSunset)
  ROOT.TColor.InvertPalette()

  for fileName in inFileList:
    f = TFile(filePath+fileName)
    t = f.Get("preselection")
    print('filePath+fileName: {0}'.format(filePath+fileName))
    ROOT.gStyle.SetOptTitle(0)
    for var in varList:
      for net in netList:
        print('var: {0}, net: {1}'.format(var, net))
        #don't plot signal score 5 for sample 1 and vice-versa
        if net.find("_5.0")>0 and fileName.find("SlfCoup_1.0") > 0:
          continue
        if net.find("_1.0")>0 and fileName.find("SlfCoup_5.0") > 0:
          continue
        outfile=''
        if var.find("h1_M")>0:
          yaxis = 'Leading Higgs Candidate Mass [GeV]'
        elif var.find("h2_M")>0:
          yaxis = 'Subleading Higgs Candidate Mass [GeV]'
        elif var.find("m_hh")>0:
          yaxis = '#it{m}_{hh} [GeV]'
          outfile += 'mhh'

        if fileName.find("_signal_") > 0:
          text = "p p #rightarrow h h signal sample"
          outfile += 'sig'
        elif fileName.find("ttbar.ro") > 0:
          text = "t#bar{t} background sample"
          outfile += 'top'
        else:
          text = "QCD bkg sample"
          outfile += 'qcd'

        if net.find("_5")>0:
          nn = '#kappa_{#lambda} = 5'
          if fileName.find("_signal_") > 0:
            text += ', %s' % nn
          outfile += '5_'
        elif net.find("_1")>0:
          nn = '#kappa_{#lambda} = 1'
          if fileName.find("_signal_") > 0:
            text += ', %s' % nn
          outfile += '1_'

        if fileName.find(".ro.resolved") > 0:
          text_ana = "Resolved"
          outfile += 'resolved_'
        elif fileName.find(".ro.boosted") > 0:
          text_ana = "Boosted"
          outfile += 'boosted_'
        elif fileName.find(".ro.intermediate") > 0:
          text_ana = "Intermediate"
          outfile += 'intermediate_'

        c = TCanvas()
        pad1 = TPad('pad1', '', 0.0, 0.0, 1.0, 1.0)
        pad1.Draw()
        pad1.cd()
        gPad.Update()
        gPad.SetBottomMargin(0.13)
        gPad.SetTopMargin(0.03)
        gPad.SetLeftMargin(0.14)
        gPad.SetRightMargin(0.18)
        gPad.Update()
        # Draw histogram
        t.Draw(var+":nnscore_"+net+"_sig>>h","","colz")
        hist = ROOT.gDirectory.Get("h")
        #hist.SetTitle(";"+nn+" DNN, signal score;"+yaxis)
       
        # Axes 
        xax = hist.GetXaxis()
        xax.SetTitle('DNN signal score trained on ' + nn)
        xax.SetTitleSize(0.06)
        xax.SetTitleFont(132)
        xax.SetTitleOffset(1.0)
        xax.SetLabelSize(0.04)
        xax.SetLabelFont(132)
        xax.CenterTitle()
        yax = hist.GetYaxis()
        yax.SetTitle(yaxis)
        yax.SetTitleSize(0.06)
        yax.SetTitleFont(132)
        yax.SetLabelSize(0.04)
        yax.SetLabelFont(132)
        yax.CenterTitle()
        zax = hist.GetZaxis()
        zax.SetTitle('Events / bin')
        zax.SetTitleSize(0.06)
        zax.SetTitleFont(132)
        zax.SetLabelSize(0.04)
        zax.SetLabelFont(132)
        zax.CenterTitle()
        
        myText( 0.17, 0.90, '#sqrt{s} = 14 TeV, %s' % (text) ) 
        myText( 0.17, 0.83, '%s analysis' % (text_ana) ) 

        c.Print("final_plots/"+outfile+"sigscore.png")
        c.SaveAs("final_plots/"+outfile+"sigscore.pdf")

        '''
        t.Draw(var+":nnscore_"+net+"_qcd>>h","","colz")
        ROOT.gDirectory.Get("h").SetTitle(";"+nn+" DNN, QCD score;"+yaxis)
        latex.DrawLatex( 0.5, 0.87, ' #bf{%s }' % (text))
        c.Print("final_plots/"+outfile+"qcdscore.png")

        t.Draw(var+":nnscore_"+net+"_top>>h","","colz")
        ROOT.gDirectory.Get("h").SetTitle(";"+nn+" DNN, t#bar{t} score;"+yaxis)
        latex.DrawLatex( 0.5, 0.87, ' #bf{%s }' % (text))
        c.Print("final_plots/"+outfile+"topscore.png")
        '''
#____________________________________________________________________________
def myText(x, y, text, tsize=0.053) :

  l = ROOT.TLatex()
  l.SetTextSize(tsize)
  l.SetNDC()
  l.SetTextFont(132)
  l.DrawLatex(x,y,text ) 
 
class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val

if __name__ == "__main__":
    main()
