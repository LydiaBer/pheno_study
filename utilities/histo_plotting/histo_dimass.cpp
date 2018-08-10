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

int histo_dimass() {

  constexpr double xl_m = 0.;
  constexpr double xu_m = 1800.;
  constexpr int nbin = 100;

  TFile *f = new TFile("/data/atlas/atlasdata/micheli/validation/root/"
                       "background_beojan/4b/boosted.root",
                       "READ");

  TTree *pheno;
  f->GetObject("signal", pheno);

  TH1D *h_m_hh = new TH1D("h_m_hh", "Background - DiHiggs Mass - Boosted", nbin,
                          xl_m, xu_m);
  // TH1D *h_m_h2 = new TH1D("h_m_h2","Mass - Subleading H",nbin,xl_m,xu_m);

  pheno->Draw("event.m_hh>>h_m_hh", "mc_sf*1000*3000", "goff");
  // pheno->Draw("event.m_h2>>h_m_h2","mc_sf*1000*3000","goff");

  auto c1 = new TCanvas();
  h_m_hh->SetMarkerStyle(20);
  // h_m_h2->SetMarkerStyle(34);
  h_m_hh->SetMarkerColor(2);
  // h_m_h2->SetMarkerColor(4);
  h_m_hh->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_hh->GetYaxis()->SetTitle("Counts");
  gStyle->SetOptStat(00000);
  // auto legend_sig = new TLegend(0.6,0.7,0.9,0.9);
  // legend_sig->SetHeader("Higgs Candidates","C");
  // legend_sig->AddEntry(h_m_hh,"DiHiggs Candidate","lep");
  // legend_sig->AddEntry(h_m_h2,"Subleading Higgs","lep");
  // TPaveLabel *title = new TPaveLabel(.11,.95,.35,.99,"Title","br");
  // title->Draw();

  h_m_hh->Draw();
  // h_m_h2->Draw("SAME");
  // legend_sig->Draw("SAME");

  // pheno->Draw("event.m_h1:event.m_h2","mc_sf*1000*3000");

  c1->Print("dihiggs_back_boosted.pdf", "pdf");
  return 0;
}
