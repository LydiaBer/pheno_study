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
#include "TLatex.h"
#include "TLegend.h"
#include "TObject.h"
#include "TPaveLabel.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TTree.h"

int histo_res() {

  constexpr double xl_m = 0.;
  constexpr double xu_m = 600.;
  constexpr double xu = 300.;
  constexpr int nbin = 100;

  TFile *tt = new TFile("/data/atlas/atlasdata/micheli/validation/root/"
                        "no_mass_window/ttbar/resolved.root",
                        "READ");
  TFile *sig = new TFile("/data/atlas/atlasdata/micheli/validation/root/"
                         "signal_beojan/resolved.root",
                         "READ");
  TFile *b = new TFile("/data/atlas/atlasdata/micheli/validation/root/"
                       "background_beojan/4b/resolved.root",
                       "READ");

  TTree *ttree_sig;
  sig->GetObject("signal", ttree_sig);
  TTree *ttree_tt;
  tt->GetObject("signal", ttree_tt);
  TTree *ttree_b;
  b->GetObject("signal", ttree_b);

  TH1D *h_m_h1_sig = new TH1D(
      "h_m_h1_sig", "Signal - Higgs Candidate Mass - Resolved", nbin, xl_m, xu);
  TH1D *h_m_h2_sig =
      new TH1D("h_m_h2_sig", "Mass - Subleading H", nbin, xl_m, xu);
  TH1D *h_m_h1_4b = new TH1D(
      "h_m_h1_4b", "4b - Higgs Candidate Mass - Resolved", nbin, xl_m, xu);
  TH1D *h_m_h2_4b =
      new TH1D("h_m_h2_4b", "Mass - Subleading H", nbin, xl_m, xu);
  TH1D *h_m_h1_tt =
      new TH1D("h_m_h1_tt", "t#bar{t} - Top Quark Candidate Mass - Resolved",
               nbin, xl_m, xu_m);
  TH1D *h_m_h2_tt =
      new TH1D("h_m_h2_tt", "Mass - Subleading H", nbin, xl_m, xu_m);

  ttree_sig->Draw("event.m_h1>>h_m_h1_sig", "mc_sf*1000*3000", "goff");
  ttree_sig->Draw("event.m_h2>>h_m_h2_sig", "mc_sf*1000*3000", "goff");

  ttree_tt->Draw("event.m_h1>>h_m_h1_tt", "mc_sf*1000*3000", "goff");
  ttree_tt->Draw("event.m_h2>>h_m_h2_tt", "mc_sf*1000*3000", "goff");

  ttree_b->Draw("event.m_h1>>h_m_h1_4b", "mc_sf*1000*3000", "goff");
  ttree_b->Draw("event.m_h2>>h_m_h2_4b", "mc_sf*1000*3000", "goff");

  auto c1 = new TCanvas();
  gStyle->SetOptStat(00000);
  h_m_h1_sig->SetMarkerStyle(20);
  h_m_h2_sig->SetMarkerStyle(34);
  h_m_h1_4b->SetMarkerStyle(20);
  h_m_h2_4b->SetMarkerStyle(34);
  h_m_h1_tt->SetMarkerStyle(20);
  h_m_h2_tt->SetMarkerStyle(34);
  h_m_h1_sig->SetMarkerColor(2);
  h_m_h2_sig->SetMarkerColor(4);
  h_m_h1_4b->SetMarkerColor(2);
  h_m_h2_4b->SetMarkerColor(4);
  h_m_h1_tt->SetMarkerColor(2);
  h_m_h2_tt->SetMarkerColor(4);
  h_m_h1_sig->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h1_sig->GetYaxis()->SetTitle("Counts");
  h_m_h1_4b->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h1_4b->GetYaxis()->SetTitle("Counts");
  h_m_h1_tt->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h1_tt->GetYaxis()->SetTitle("Counts");

  auto legend_sig = new TLegend(0.6, 0.7, 0.9, 0.9);
  legend_sig->SetHeader("Higgs Candidates", "C");
  legend_sig->AddEntry(h_m_h1_sig, "Leading Higgs", "lep");
  legend_sig->AddEntry(h_m_h2_sig, "Subleading Higgs", "lep");

  auto legend_4b = new TLegend(0.6, 0.7, 0.9, 0.9);
  legend_4b->SetHeader("Higgs Candidates", "C");
  legend_4b->AddEntry(h_m_h1_4b, "Leading Higgs", "lep");
  legend_4b->AddEntry(h_m_h2_4b, "Subleading Higgs", "lep");

  auto legend_tt = new TLegend(0.6, 0.7, 0.9, 0.9);
  legend_tt->SetHeader("Top Candidates", "C");
  legend_tt->AddEntry(h_m_h1_tt, "Leading Top", "lep");
  legend_tt->AddEntry(h_m_h2_tt, "Subleading Top", "lep");

  h_m_h1_sig->Draw();
  h_m_h2_sig->Draw("SAME");
  legend_sig->Draw("SAME");
  c1->Print("resolved_overlaid.pdf(", "pdf");

  h_m_h1_4b->Draw();
  h_m_h2_4b->Draw("SAME");
  legend_4b->Draw("SAME");
  c1->Print("resolved_overlaid.pdf", "pdf");

  h_m_h1_tt->Draw();
  h_m_h2_tt->Draw("SAME");
  legend_tt->Draw("SAME");
  c1->Print("resolved_overlaid.pdf)", "pdf");
  // pheno->Draw("event.m_h1:event.m_h2","mc_sf*1000*3000");

  // c1->Print("signal_overlaid.pdf","pdf");
  return 0;
}
