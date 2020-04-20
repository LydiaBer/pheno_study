import collections
from ROOT import gSystem,TTree,TFile,TCanvas
import ROOT


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
  varList = ["event.h1_M"]
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
    ROOT.gStyle.SetOptTitle(0)
    for var in varList:
      for net in netList:

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
          yaxis = 'Di-Higgs System Mass [GeV]'

        if fileName.find("_signal_") > 0:
          text = "Signal sample "
          outfile += 'sig'
        elif fileName.find("ttbar.ro") > 0:
          text = "ttbar sample, "
          outfile += 'top'
        else:
          text = "QCD bkg sample, "
          outfile += 'qcd'

        if net.find("_5")>0:
          nn = '#lambda_{hhh} = 5'
          if fileName.find("_signal_") > 0:
            text += nn+", "
          outfile += '5_'
        elif net.find("_1")>0:
          nn = '#lambda_{hhh} = 1'
          if fileName.find("_signal_") > 0:
            text += nn+", "
          outfile += '1_'

        if fileName.find(".ro.resolved") > 0:
          text = text + "resolved"
          outfile += 'resolved_'
        elif fileName.find(".ro.boosted") > 0:
          text = text + "boosted"
          outfile += 'boosted_'
        elif fileName.find(".ro.intermediate") > 0:
          text = text + "intermediate"
          outfile += 'intermediate_'

        c = TCanvas()
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextFont( 42 )
        latex.SetTextSize( 0.035 )
        latex.SetTextColor( 1 )
        latex.SetTextAlign( 12 )

        t.Draw(var+":nnscore_"+net+"_sig>>h","","colz")
        ROOT.gDirectory.Get("h").SetTitle(";"+nn+" DNN, signal score;"+yaxis)
        latex.DrawLatex( 0.50, 0.87, ' #bf{%s }' % (text))
        c.Print("final_plots/"+outfile+"sigscore.png")

        t.Draw(var+":nnscore_"+net+"_qcd>>h","","colz")
        ROOT.gDirectory.Get("h").SetTitle(";"+nn+" DNN, QCD score;"+yaxis)
        latex.DrawLatex( 0.5, 0.87, ' #bf{%s }' % (text))
        c.Print("final_plots/"+outfile+"qcdscore.png")

        t.Draw(var+":nnscore_"+net+"_top>>h","","colz")
        ROOT.gDirectory.Get("h").SetTitle(";"+nn+" DNN, t#bar{t} score;"+yaxis)
        latex.DrawLatex( 0.5, 0.87, ' #bf{%s }' % (text))
        c.Print("final_plots/"+outfile+"topscore.png")
      
  
class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val

if __name__ == "__main__":
    main()
