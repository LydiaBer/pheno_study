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
#include "TObject.h"
#include "TROOT.h"
#include "TTree.h"

// Settings for histos

constexpr int nbin = 100;
constexpr double xl_pt = 0.;
constexpr double xu_pt = 200.;
constexpr double xl_eta = -10.;
constexpr double xu_eta = 10.;
constexpr double xl_m = 0.;
constexpr double xu_m = 300.;

constexpr double xl_mhh = 0.;
constexpr double xu_mhh = 1600.;

const double xbl_pt = 150;
const double xbu_pt = 1000;

void produce_resolved(TFile *file, std::string output) {

  TTree *pheno;
  file->GetObject("signal", pheno);

  // booking Histos

  TH1D *h_m_hh = new TH1D("h_m_hh", "DiHiggs Mass", nbin, xl_mhh, xu_mhh);
  TH1D *h_m_h1 = new TH1D("h_m_h1", "Mass - Leading H", nbin, xl_m, xu_m);
  TH1D *h_m_h2 = new TH1D("h_m_h2", "Mass - Subleading H", nbin, xl_m, xu_m);
  TH1D *h_pt_h1 = new TH1D("h_pt_h1", "Pt - Leading H", nbin, xl_pt, xu_pt);
  TH1D *h_pt_h2 = new TH1D("h_pt_h2", "Pt - Subleading H", nbin, xl_pt, xu_pt);
  TH1D *h_eta_h1 =
      new TH1D("h_eta_h1", "Eta - Leading H", nbin, xl_eta, xu_eta);
  TH1D *h_eta_h2 =
      new TH1D("h_eta_h2", "Eta - Subleading H", nbin, xl_eta, xu_eta);
  TH1D *h_phi_h1 =
      new TH1D("h_phi_h1", "Phi - Leading H", nbin, xl_eta, xu_eta);
  TH1D *h_phi_h2 =
      new TH1D("h_phi_h2", "Phi - Subleading H", nbin, xl_eta, xu_eta);
  TH1D *h_pt_h1_j1 =
      new TH1D("h_pt_h1_j1", "pT - Leading Jet H1", nbin, xl_pt, xu_pt);
  TH1D *h_pt_h1_j2 =
      new TH1D("h_pt_h1_j2", "pT - Subleading Jet H1", nbin, xl_pt, xu_pt);
  TH1D *h_pt_h2_j1 =
      new TH1D("h_pt_h2_j1", "pT - Leading Jet H2", nbin, xl_pt, xu_pt);
  TH1D *h_pt_h2_j2 =
      new TH1D("h_pt_h2_j2", "pT - Subleading Jet H2", nbin, xl_pt, xu_pt);
  TH1D *h_eta_h1_j1 =
      new TH1D("h_eta_h1_j1", "Eta - Leading Jet H1", nbin, xl_eta, xu_eta);
  TH1D *h_eta_h1_j2 =
      new TH1D("h_eta_h1_j2", "Eta - Subleading Jet H2", nbin, xl_eta, xu_eta);
  TH1D *h_eta_h2_j1 =
      new TH1D("h_eta_h2_j1", "Eta - Leading Jet H2", nbin, xl_eta, xu_eta);
  TH1D *h_eta_h2_j2 =
      new TH1D("h_eta_h2_j2", "Eta - Subleading Jet H2", nbin, xl_eta, xu_eta);
  TH1D *h_pt_jets = new TH1D("h_pt_jets", "pT Jets", nbin, xl_pt, xu_pt);
  TH1D *h_eta_jets = new TH1D("h_eta_jets", "Eta Jets", nbin, xl_eta, xu_eta);

  pheno->Draw("event.m_hh>>h_m_hh", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.m_h1>>h_m_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.m_h2>>h_m_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h1>>h_pt_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h2>>h_pt_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h1>>h_eta_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h2>>h_eta_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.phi_h1>>h_phi_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.phi_h2>>h_phi_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h1_j1>>h_pt_h1_j1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h1_j2>>h_pt_h1_j2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h2_j1>>h_pt_h2_j1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h2_j2>>h_pt_h2_j2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h1_j1>>h_eta_h1_j1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h1_j2>>h_eta_h1_j2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h2_j1>>h_eta_h2_j1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h2_j2>>h_eta_h2_j2", "mc_sf*1000*3000", "goff");

  h_pt_jets->Add(h_pt_h1_j1);
  h_pt_jets->Add(h_pt_h1_j2);
  h_pt_jets->Add(h_pt_h2_j1);
  h_pt_jets->Add(h_pt_h2_j2);

  h_eta_jets->Add(h_eta_h1_j1);
  h_eta_jets->Add(h_eta_h1_j2);
  h_eta_jets->Add(h_eta_h2_j1);
  h_eta_jets->Add(h_eta_h2_j2);

  auto c1 = new TCanvas();

  std::string open_output = fmt::format("{}{}", output, "(");
  std::string close_output = fmt::format("{}{}", output, ")");

  h_m_hh->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_hh->GetYaxis()->SetTitle("Counts");
  h_pt_jets->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_jets->GetYaxis()->SetTitle("Counts");
  h_m_h1->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h1->GetYaxis()->SetTitle("Counts");
  h_m_h2->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h2->GetYaxis()->SetTitle("Counts");
  h_pt_h1->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_h1->GetYaxis()->SetTitle("Counts");
  h_pt_h2->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_h2->GetYaxis()->SetTitle("Counts");
  h_eta_h1->GetXaxis()->SetTitle("#eta");
  h_eta_h1->GetYaxis()->SetTitle("Counts");
  h_eta_h2->GetXaxis()->SetTitle("#eta");
  h_eta_h2->GetYaxis()->SetTitle("Counts");
  h_eta_jets->GetXaxis()->SetTitle("#eta");
  h_eta_jets->GetYaxis()->SetTitle("Counts");
  h_phi_h1->GetXaxis()->SetTitle("#phi");
  h_phi_h1->GetYaxis()->SetTitle("Counts");
  h_phi_h2->GetXaxis()->SetTitle("#phi");
  h_phi_h2->GetYaxis()->SetTitle("Counts");

  h_pt_jets->Draw("hist");
  c1->Print(open_output.c_str(), "pdf");
  h_eta_jets->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_hh->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_pt_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_pt_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_phi_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_phi_h2->Draw("hist");
  c1->Print(close_output.c_str(), "pdf");
  return;
}

void produce_intermediate(TFile *file, std::string output) {

  TTree *pheno;
  file->GetObject("signal", pheno);

  // booking Histos

  TH1D *h_m_hh = new TH1D("h_m_hh", "DiHiggs Mass", nbin, xl_mhh, xu_mhh);
  TH1D *h_m_h1 = new TH1D("h_m_h1", "Mass - Leading H", nbin, xl_m, xu_m);
  TH1D *h_m_h2 = new TH1D("h_m_h2", "Mass - Subleading H", nbin, xl_m, xu_m);
  TH1D *h_pt_h1 = new TH1D("h_pt_h1", "Pt - Leading H", nbin, xbl_pt, xbu_pt);
  TH1D *h_pt_h2 =
      new TH1D("h_pt_h2", "Pt - Subleading H", nbin, xbl_pt, xbu_pt);
  TH1D *h_eta_h1 =
      new TH1D("h_eta_h1", "Eta - Leading H", nbin, xl_eta, xu_eta);
  TH1D *h_eta_h2 =
      new TH1D("h_eta_h2", "Eta - Subleading H", nbin, xl_eta, xu_eta);
  TH1D *h_phi_h1 =
      new TH1D("h_phi_h1", "Phi - Leading H", nbin, xl_eta, xu_eta);
  TH1D *h_phi_h2 =
      new TH1D("h_phi_h2", "Phi - Subleading H", nbin, xl_eta, xu_eta);
  TH1D *h_pt_fj = new TH1D("h_pt_fj", "Pt - Fat Jet", nbin, xbl_pt, xbu_pt);
  TH1D *h_eta_fj = new TH1D("h_eta_fj", "Eta - Fat Jet", nbin, xl_eta, xu_eta);
  TH1D *h_pt_h2_j1 =
      new TH1D("h_pt_h2_j1", "pT - Leading Jet H2", nbin, xbl_pt, xbu_pt);
  TH1D *h_pt_h2_j2 =
      new TH1D("h_pt_h2_j2", "pT - Subleading Jet H2", nbin, xbl_pt, xbu_pt);
  TH1D *h_eta_h2_j1 =
      new TH1D("h_eta_h2_j1", "Eta - Leading Jet H2", nbin, xl_eta, xu_eta);
  TH1D *h_eta_h2_j2 =
      new TH1D("h_eta_h2_j2", "Eta - Subleading Jet H2", nbin, xl_eta, xu_eta);
  TH1D *h_pt_jets = new TH1D("h_pt_jets", "pT Jets", nbin, xbl_pt, xbu_pt);
  TH1D *h_eta_jets = new TH1D("h_eta_jets", "Eta Jets", nbin, xl_eta, xu_eta);

  pheno->Draw("event.m_hh>>h_m_hh", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.m_h1>>h_m_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.m_h2>>h_m_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h1>>h_pt_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h2>>h_pt_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h1>>h_eta_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h2>>h_eta_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.phi_h1>>h_phi_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.phi_h2>>h_phi_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h1_large_jet>>h_pt_fj", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h2_j1>>h_pt_h2_j1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h2_j2>>h_pt_h2_j2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h1_large_jet>>h_eta_fj", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h2_j1>>h_eta_h2_j1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h2_j2>>h_eta_h2_j2", "mc_sf*1000*3000", "goff");

  h_pt_jets->Add(h_pt_h2_j1);
  h_pt_jets->Add(h_pt_h2_j2);

  h_eta_jets->Add(h_eta_h2_j1);
  h_eta_jets->Add(h_eta_h2_j2);

  auto c1 = new TCanvas();
  std::string open_output = fmt::format("{}{}", output, "(");
  std::string close_output = fmt::format("{}{}", output, ")");

  h_m_hh->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_hh->GetYaxis()->SetTitle("Counts");
  h_pt_jets->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_jets->GetYaxis()->SetTitle("Counts");
  h_m_h1->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h1->GetYaxis()->SetTitle("Counts");
  h_m_h2->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h2->GetYaxis()->SetTitle("Counts");
  h_pt_fj->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_fj->GetYaxis()->SetTitle("Counts");
  h_pt_h1->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_h1->GetYaxis()->SetTitle("Counts");
  h_pt_h2->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_h2->GetYaxis()->SetTitle("Counts");
  h_eta_h1->GetXaxis()->SetTitle("#eta");
  h_eta_h1->GetYaxis()->SetTitle("Counts");
  h_eta_h2->GetXaxis()->SetTitle("#eta");
  h_eta_h2->GetYaxis()->SetTitle("Counts");
  h_eta_jets->GetXaxis()->SetTitle("#eta");
  h_eta_jets->GetYaxis()->SetTitle("Counts");
  h_phi_h1->GetXaxis()->SetTitle("#phi");
  h_phi_h1->GetYaxis()->SetTitle("Counts");
  h_phi_h2->GetXaxis()->SetTitle("#phi");
  h_phi_h2->GetYaxis()->SetTitle("Counts");

  h_pt_jets->Draw("hist");
  c1->Print(open_output.c_str(), "pdf");
  h_eta_jets->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_pt_fj->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_fj->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_pt_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_pt_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_phi_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_phi_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_hh->Draw("hist");
  c1->Print(close_output.c_str(), "pdf");
  return;
}

void produce_boosted(TFile *file, std::string output) {

  TTree *pheno;
  file->GetObject("signal", pheno);

  // booking Histos

  TH1D *h_m_hh = new TH1D("h_m_hh", "DiHiggs Mass", nbin, xl_mhh, xu_mhh);
  TH1D *h_m_h1 = new TH1D("h_m_h1", "Mass - Leading H", nbin, xl_m, xu_m);
  TH1D *h_m_h2 = new TH1D("h_m_h2", "Mass - Subleading H", nbin, xl_m, xu_m);
  TH1D *h_pt_h1 = new TH1D("h_pt_h1", "Pt - Leading H", nbin, xbl_pt, xbu_pt);
  TH1D *h_pt_h2 =
      new TH1D("h_pt_h2", "Pt - Subleading H", nbin, xbl_pt, xbu_pt);
  TH1D *h_eta_h1 =
      new TH1D("h_eta_h1", "Eta - Leading H", nbin, xl_eta, xu_eta);
  TH1D *h_eta_h2 =
      new TH1D("h_eta_h2", "Eta - Subleading H", nbin, xl_eta, xu_eta);
  TH1D *h_phi_h1 =
      new TH1D("h_phi_h1", "Phi - Leading H", nbin, xl_eta, xu_eta);
  TH1D *h_phi_h2 =
      new TH1D("h_phi_h2", "Phi - Subleading H", nbin, xl_eta, xu_eta);
  TH1D *h_pt_fj_1 =
      new TH1D("h_pt_fj_1", "Pt - Leading Fat Jet", nbin, xbl_pt, xbu_pt);
  TH1D *h_eta_fj_1 =
      new TH1D("h_eta_fj_1", "Eta - Leading Fat Jet", nbin, xl_eta, xu_eta);
  TH1D *h_pt_fj_2 =
      new TH1D("h_pt_fj_2", "Pt - Subleading Fat Jet", nbin, xbl_pt, xbu_pt);
  TH1D *h_eta_fj_2 =
      new TH1D("h_eta_fj_2", "Eta - Subleading Fat Jet", nbin, xl_eta, xu_eta);
  // TH1D *h_pt_jets = new TH1D("h_pt_jets","pT Jets",nbin,xl_pt,xu_pt);
  // TH1D *h_eta_jets = new TH1D("h_eta_jets","Eta Jets",nbin,xl_eta,xu_eta);

  pheno->Draw("event.m_hh>>h_m_hh", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.m_h1>>h_m_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.m_h2>>h_m_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h1>>h_pt_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h2>>h_pt_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h1>>h_eta_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h2>>h_eta_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.phi_h1>>h_phi_h1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.phi_h2>>h_phi_h2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h1_j1>>h_pt_fj_1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h1_j1>>h_eta_fj_1", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.pT_h2_j2>>h_pt_fj_2", "mc_sf*1000*3000", "goff");
  pheno->Draw("event.eta_h2_j2>>h_eta_fj_2", "mc_sf*1000*3000", "goff");

  /*
  h_pt_jets->Add(h_pt_h1_j1);
  h_pt_jets->Add(h_pt_h1_j2);
  h_pt_jets->Add(h_pt_h2_j1);
  h_pt_jets->Add(h_pt_h2_j2);

  h_eta_jets->Add(h_eta_h1_j1);
  h_eta_jets->Add(h_eta_h1_j2);
  h_eta_jets->Add(h_eta_h2_j1);
  h_eta_jets->Add(h_eta_h2_j2);
  */

  auto c1 = new TCanvas();
  std::string open_output = fmt::format("{}{}", output, "(");
  std::string close_output = fmt::format("{}{}", output, ")");

  h_m_hh->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_hh->GetYaxis()->SetTitle("Counts");
  h_m_h1->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h1->GetYaxis()->SetTitle("Counts");
  h_m_h2->GetXaxis()->SetTitle("Mass (GeV)");
  h_m_h2->GetYaxis()->SetTitle("Counts");
  h_pt_fj_1->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_fj_1->GetYaxis()->SetTitle("Counts");
  h_pt_fj_2->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_fj_2->GetYaxis()->SetTitle("Counts");
  h_pt_h1->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_h1->GetYaxis()->SetTitle("Counts");
  h_pt_h2->GetXaxis()->SetTitle("pT (GeV)");
  h_pt_h2->GetYaxis()->SetTitle("Counts");
  h_eta_fj_1->GetXaxis()->SetTitle("#eta");
  h_eta_fj_1->GetYaxis()->SetTitle("Counts");
  h_eta_fj_2->GetXaxis()->SetTitle("#eta");
  h_eta_fj_2->GetYaxis()->SetTitle("Counts");
  h_eta_h1->GetXaxis()->SetTitle("#eta");
  h_eta_h1->GetYaxis()->SetTitle("Counts");
  h_eta_h2->GetXaxis()->SetTitle("#eta");
  h_eta_h2->GetYaxis()->SetTitle("Counts");
  h_phi_h1->GetXaxis()->SetTitle("#phi");
  h_phi_h1->GetYaxis()->SetTitle("Counts");
  h_phi_h2->GetXaxis()->SetTitle("#phi");
  h_phi_h2->GetYaxis()->SetTitle("Counts");

  h_pt_fj_1->Draw("hist");
  c1->Print(open_output.c_str(), "pdf");
  h_pt_fj_2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_fj_1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_fj_2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_hh->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_m_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_pt_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_pt_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_eta_h2->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_phi_h1->Draw("hist");
  c1->Print(output.c_str(), "pdf");
  h_phi_h2->Draw("hist");
  c1->Print(close_output.c_str(), "pdf");

  return;
}
/*
 canvas->Print("myFile.pdf[")
for ()
{ canvas->Print("myFile.pdf");}
canvas->Print("myFile.pdf]")
 *
 * */
int histo_all() {
  using namespace std;
  // Load the ROOT file
  std::vector<std::string> folder{"background_beojan", "signal_beojan",
                                  "signal_jesse"};
  std::vector<std::string> tag_background{"4b", "2b2j", "ttbar"};
  std::vector<std::string> tag_analysis{"resolved", "intermediate", "boosted"};

  for (unsigned int i = 0; i < folder.size(); i++) {
    if (i == 0) {
      for (unsigned int j = 0; j < tag_background.size(); j++) {
        for (unsigned int k = 0; k < tag_analysis.size(); k++) {
          string path = fmt::format(
              "/data/atlas/atlasdata/micheli/validation/root/{}/{}/{}.root",
              folder.at(i), tag_background.at(j), tag_analysis.at(k));
          TFile *f = new TFile(path.c_str(), "READ");
          if (k == 0) {

            string output =
                fmt::format("histo_{}_{}_{}.pdf", folder.at(i),
                            tag_background.at(j), tag_analysis.at(k));
            produce_resolved(f, output);
          }

          if (k == 1) {
            string output =
                fmt::format("histo_{}_{}_{}.pdf", folder.at(i),
                            tag_background.at(j), tag_analysis.at(k));
            produce_intermediate(f, output);
          }

          if (k == 2) {
            string output =
                fmt::format("histo_{}_{}_{}.pdf", folder.at(i),
                            tag_background.at(j), tag_analysis.at(k));
            produce_boosted(f, output);
          }
        }
      }
    }
    if (!(i == 0)) {
      for (unsigned int k = 0; k < tag_analysis.size(); k++) {
        string path = fmt::format(
            "/data/atlas/atlasdata/micheli/validation/root/{}/{}.root",
            folder.at(i), tag_analysis.at(k));
        TFile *f = new TFile(path.c_str(), "READ");
        if (k == 0) {

          string output =
              fmt::format("histo_{}_{}.pdf", folder.at(i), tag_analysis.at(k));
          produce_resolved(f, output);
        }

        if (k == 1) {
          string output =
              fmt::format("histo_{}_{}.pdf", folder.at(i), tag_analysis.at(k));
          produce_intermediate(f, output);
        }

        if (k == 2) {
          string output =
              fmt::format("histo_{}_{}.pdf", folder.at(i), tag_analysis.at(k));
          produce_boosted(f, output);
        }
      }
    }
  }
  return 0;
}
