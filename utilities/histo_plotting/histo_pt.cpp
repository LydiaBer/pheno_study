// Histograms code

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <memory>
#include <set>
#include <string>
#include <utility>
#include <vector>

#include "fmt/format.h"

#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TLegend.h"
#include "TObject.h"
#include "TPaveLabel.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TTree.h"

int histo_pt() {

  constexpr double xl_m = 0.;
  constexpr double xu_m = 1200.;
  constexpr int nbin = 100;

  TFile *f = new TFile("/data/atlas/atlasdata/micheli/validation/root/"
                       "signal_beojan/boosted.root",
                       "READ");

  TTree *pheno;
  f->GetObject("signal", pheno);

  TH1D *h_pt_lj = new TH1D("h_pt_lj", "Signal - Leading Jet Pt - Boosted", nbin,
                           xl_m, xu_m);
  // TH1D *h_m_h2 = new TH1D("h_m_h2","Mass - Subleading H",nbin,xl_m,xu_m);

  pheno->Draw("event.pT_h1_j1>>h_pt_lj", "mc_sf*1000*3000", "goff");
  // pheno->Draw("event.m_h2>>h_m_h2","mc_sf*1000*3000","goff");

  auto c1 = new TCanvas();
  h_pt_lj->SetMarkerStyle(20);
  // h_m_h2->SetMarkerStyle(34);
  h_pt_lj->SetMarkerColor(2);
  // h_m_h2->SetMarkerColor(4);
  h_pt_lj->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_lj->GetYaxis()->SetTitle("Counts");
  gStyle->SetOptStat(00000);
  // auto legend_sig = new TLegend(0.6,0.7,0.9,0.9);
  // legend_sig->SetHeader("Higgs Candidates","C");
  // legend_sig->AddEntry(h_m_hh,"DiHiggs Candidate","lep");
  // legend_sig->AddEntry(h_m_h2,"Subleading Higgs","lep");
  // TPaveLabel *title = new TPaveLabel(.11,.95,.35,.99,"Title","br");
  // title->Draw();

  h_pt_lj->Draw();
  // h_m_h2->Draw("SAME");
  // legend_sig->Draw("SAME");

  // pheno->Draw("event.m_h1:event.m_h2","mc_sf*1000*3000");

  c1->Print("ljpt_sig_boosted.pdf", "pdf");
  return 0;
}
