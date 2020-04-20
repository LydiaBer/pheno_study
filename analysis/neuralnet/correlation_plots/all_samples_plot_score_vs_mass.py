import collections
from ROOT import gSystem,TTree,TFile,TCanvas
import ROOT


def main():
  inFileList = [
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_200_to_500_2b2j.ro.boosted_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_200_to_500_2b2j.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_500_to_1000_2b2j.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_1000_to_infty_2b2j.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_500_to_1000_2b2j.ro.boosted_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_20_to_200_4b.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_200_to_500_4b.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_500_to_1000_4b.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_1000_to_infty_2b2j.ro.boosted_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_1000_to_infty_4b.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_0.5_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_20_to_200_4b.ro.boosted_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_10.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_200_to_500_4b.ro.boosted_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_1.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_20.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_2.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_500_to_1000_4b.ro.boosted_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_3.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_5.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_7.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m0.5_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m10.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m1.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_1000_to_infty_4b.ro.boosted_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m20.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m2.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m5.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_0.5_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m7.0_merged.ro.intermediate_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_10.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_ttbar.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_1.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_20.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_bbh.ro.intermediate_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_2.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_3.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_5.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_7.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m0.5_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m10.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m1.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m20.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m2.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m5.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m7.0_merged.ro.boosted_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_ttbar.ro.resolved_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_20_to_200_2b2j.ro.resolved_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_200_to_500_2b2j.ro.resolved_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_500_to_1000_2b2j.ro.resolved_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_20_to_200_4b.ro.resolved_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_200_to_500_4b.ro.resolved_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_ptj1_500_to_1000_4b.ro.resolved_2_background_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_0.5_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_10.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_1.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_20.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_2.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_3.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_5.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_7.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m0.5_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m10.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m1.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m20.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m2.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m5.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_4b_highstats_signal_hh_TopYuk_1.0_SlfCoup_m7.0_merged.ro.resolved_2_withNNs.root",
      "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/nn_score_ntuples/loose_noGenFilt_ttbar.ro.boosted_2_background_withNNs.root"
      ]

  varList = ["event.h1_M","event.h2_M","event.m_hh"]
  #netList = ["nnscore_w_OPsgdEP30BS100DO05","nnscore_w_OPadamaxEP30BS100DO03"]
  netList = ["EP15_LR0p005"]
  for fileName in inFileList:
    f = TFile(fileName)
    t = f.Get("preselection")
    for var in varList:
      for net in netList:
        text = "text"
        if fileName.find("pp2hh_4b_HeavyHiggsTHDM") > 0:
          text = "Signal sample, "
        elif fileName.find("bkg_ttbar") > 0:
          text = "ttbar sample, "
        else:
          text = "QCD bkg sample, "
        if fileName.find(".ro.resolved") > 0:
          text = text + "resolved"
        elif fileName.find(".ro.boosted") > 0:
          text = text + "boosted"
        elif fileName.find(".ro.intermediate") > 0:
          text = text + "intermediate"

        c = TCanvas()
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextFont( 42 )
        latex.SetTextSize( 0.035 )
        latex.SetTextColor( 1 )
        latex.SetTextAlign( 12 )

        t.Draw(var+":nnscore_"+net+"_sig","","colz")
        latex.DrawLatex( 0.22, 0.87, ' #bf{%s }' % (text))
        c.Print(fileName+var+"VSnnscore_"+net+"_sig.png")
        t.Draw(var+":nnscore_"+net+"_qcd","","colz")
        latex.DrawLatex( 0.22, 0.87, ' #bf{%s }' % (text))
        c.Print(fileName+var+"VSnnscore_"+net+"_qcd.png")
        t.Draw(var+":nnscore_"+net+"_top","","colz")
        latex.DrawLatex( 0.22, 0.87, ' #bf{%s }' % (text))
        c.Print(fileName+var+"VSnnscore_"+net+"_top.png")
      
  
class MyDict(collections.OrderedDict):
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val

if __name__ == "__main__":
    main()
