/// \file utils.h
// General utilities
//
//

#ifndef INTERMEDIATE_ANALYSIS_UTILS_H
#define INTERMEDIATE_ANALYSIS_UTILS_H

#pragma once
#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include <range/v3/all.hpp>

#include <fmt/format.h>

#include <TFile.h>
#include <TLorentzVector.h>
#include <TROOT.h>
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RVec.hxx>

#include "classes/DelphesClasses.h"
#include "classes/DelphesFactory.h"
#include "modules/Delphes.h"

extern double f;

class OxJet {
  public:
    TLorentzVector p4; ///< 4-momentum
    double btag;        ///< B-tagging score
    bool tagged;       ///< Is jet B-tagged?

    OxJet() : p4(), btag(0), tagged(false) {}
    OxJet(double M, double pT, double eta, long double phi, bool tagged) : p4(), btag(0), tagged(tagged) {
        p4.SetPtEtaPhiM(pT, eta, phi, M);
    }
};

// Higgs boson
struct higgs {
  TLorentzVector p4; ///< 4-momentum
  int jet1;          ///< Index of leading jet
  int jet2;          ///< Index of subleading jet
  std::vector<OxJet> jets; // Vector of jets associated with Higgs candidate

  higgs() : p4(), jet1(0), jet2(0), jets() {}
  higgs(const TLorentzVector& p4, int jet1, int jet2, std::vector<OxJet> jets) : p4(p4), jet1(jet1), jet2(jet2), jets(jets) {}
};

// DiHiggs system object
struct dihiggs {
  higgs higgs1;
  higgs higgs2;

};

// Make jet from Oxjet function
inline OxJet make_oxjet(OxJet& jet) {
    double M    = jet.p4.M();
    double pT   = jet.p4.Pt();
    double eta  = jet.p4.Eta();
    double phi  = jet.p4.Phi();
    bool tagged = jet.tagged;

    return OxJet(M, pT, eta, phi, tagged);
}


class JetPair {
  public:
    double mass_1; // Mass of first Jet
    double mass_2; // Mass of second Jet
    OxJet jet_1;   // First Jet
    OxJet jet_2;   // Second Jet

    JetPair() : mass_1(0), mass_2(0), jet_1(), jet_2() {}
    JetPair(double M_1, double M_2, OxJet first_jet, OxJet second_jet)
        : mass_1(M_1), mass_2(M_2), jet_1(first_jet), jet_2(second_jet) {}

    TLorentzVector p4(){return jet_1.p4 + jet_2.p4;}
};

// Make jet function
inline OxJet make_jet(Jet& jet) {
    double M    = jet.Mass;
    double pT   = jet.PT;
    double eta  = jet.Eta;
    double phi  = jet.Phi;
    bool tagged = jet.BTag;

    // Because a constructor can't be used as a Callable
    return OxJet(M, pT, eta, phi, tagged);
}

// Make jet pair function
inline JetPair make_pair(OxJet& jet1, OxJet& jet2) {

    double m_1 = jet1.p4.M();
    double m_2 = jet2.p4.M();
    OxJet j_1 = jet1;
    OxJet j_2 = jet2;
    //  if (jet1.p4 == jet2.p4) continue;
    return JetPair(m_1, m_2, j_1, j_2);
}

// Function to check angular distance between
// large R jet and small R jet
inline double deltaR(OxJet& jet1, OxJet& jet2) {
    using namespace std;

    double deta = jet1.p4.Eta() - jet2.p4.Eta();
    double dphi = fabs(jet1.p4.Phi() - jet2.p4.Phi());
    while(dphi > TMath::TwoPi()) dphi -= TMath::TwoPi();
    if(dphi > TMath::Pi()) dphi = TMath::TwoPi() - dphi;

    return sqrt(deta*deta + dphi*dphi);
}

// Reconstructed event in the intermediate regime
// Reconstructed event information
struct reconstructed_event {
    bool valid;           ///< Is event valid
    int64_t n_small_tag;  ///< Number of B-tagged smallR jets
    int64_t n_small_jets; ///< Total number of smallR jets
    int64_t n_large_tag;  ///< Number of B-tagged LargeR jets
    int64_t n_large_jets; ///< Total number of LargeR jets
    int64_t n_track_tag;  ///< Number of B-tagged track jets
    int64_t n_track_jets; ///< Total number of track jets
    /*
    int64_t n_h1_assoc_track_tag;  ///< Number of B-tagged track jets associated with leading fat jet
    int64_t n_h1_assoc_track_jets; ///< Total number of track jets associated with leading fat jet
    int64_t n_h2_assoc_track_tag;  ///< Number of B-tagged track jets associated with subleading fat jet
    int64_t n_h2_assoc_track_jets; ///< Total number of track jets associated with subleading fat jet
    */
    double wgt;           ///< Event Weight

    int64_t nElec;  ///< Number of electrons at Delphes level
    int64_t nMuon;  ///< Number of muons at Delphes level

    TLorentzVector met; ///< MET
    TLorentzVector elec1; ///< leading electron
    TLorentzVector muon1; ///< leading muon

    higgs higgs1; ///< Leading Higgs
    higgs higgs2; ///< Subleading Higgs
    
    reconstructed_event()
        : valid(true), // set to true if pairing is valid
          higgs1(),
          higgs2() {}
};

struct out_format {

    //--------------------------------
    // Di-Higgs system
    //--------------------------------
    double m_hh; // Mass 
    double pT_hh; // pT
    double dR_hh; // Di-Higgs dR 
    double dEta_hh; // Di-Higgs deta 
    double dPhi_hh; // Di-Higgs dphi 
    double X_hh;

    //--------------------------------
    // Leading Higgs candidate
    //--------------------------------
    double h1_M;  
    double h1_Pt;  
    double h1_Eta; 
    double h1_Phi; 

      // Leading jet of subleading Higgs candidate
      double h1_j1_M;   
      double h1_j1_Pt;  
      double h1_j1_Eta; 
      double h1_j1_Phi; 

      // Subleading jet of subleading Higgs candidate
      double h1_j2_M;   
      double h1_j2_Pt;  
      double h1_j2_Eta; 
      double h1_j2_Phi; 

      // Delta R between leading Higgs candidate and its jets
      double h1_j1_dR; 
      double h1_j2_dR; 

      // Delta R between the two jets associated to leading Higgs candidate
      double h1_j1_j2_dR; 

    //--------------------------------
    // Subleading Higgs candidate
    //--------------------------------
    double h2_M;  
    double h2_Pt;  
    double h2_Eta; 
    double h2_Phi; 

      // Leading jet of subleading Higgs candidate
      double h2_j1_M;   
      double h2_j1_Pt;  
      double h2_j1_Eta; 
      double h2_j1_Phi; 

      // Subleading jet of subleading Higgs candidate
      double h2_j2_M;   
      double h2_j2_Pt;  
      double h2_j2_Eta; 
      double h2_j2_Phi; 

      // Delta R between leading Higgs candidate and its jets
      double h2_j1_dR; 
      double h2_j2_dR; 
      
      // Delta R between the two jets associated to leading Higgs candidate
      double h2_j1_j2_dR; 
    
    // Leading electron 4-vector
    double elec1_M; 
    double elec1_Pt; 
    double elec1_Eta; 
    double elec1_Phi; 

    // Leading muon 4-vector 
    double muon1_M;  
    double muon1_Pt; 
    double muon1_Eta; 
    double muon1_Phi; 
    
    // Missing transverse momentum (2-component vector)
    double met_Et; 
    double met_Phi;
    
};

template <typename Proxied>
void write_tree(ROOT::RDF::RInterface<Proxied>& result, const char* treename,
              TFile& output_file /**< [out] Tree to write to */) {
  using namespace std;
  using namespace ROOT::Experimental;
  namespace view = ranges::view;
  namespace action = ranges::action;
  static bool first_tree = true;

  const char* out_format_leaflist =
        "m_hh/D:pT_hh:dR_hh:dEta_hh:dPhi_hh:X_hh:"
        "h1_M/D:h1_Pt:h1_Eta:h1_Phi:"
        "h1_j1_M:h1_j1_Pt:h1_j1_Eta:h1_j1_Phi:"
        "h1_j2_M:h1_j2_Pt:h1_j2_Eta:h1_j2_Phi:"
        "h1_j1_dR:h1_j2_dR:h1_j1_j2_dR"
        "h2_M/D:h2_Pt:h2_Eta:h2_Phi:"
        "h2_j1_M:h2_j1_Pt:h2_j1_Eta:h2_j1_Phi:"
        "h2_j2_M:h2_j2_Pt:h2_j2_Eta:h2_j2_Phi:"
        "h2_j1_dR:h2_j2_dR:h2_j1_j2_dR"
        "elec1_M:elec1_Pt:elec1_Eta:elec1_Phi:"
        "muon1_M:muon1_Pt:muon1_Eta:muon1_Phi:"
        "met_Et:met_Phi";

  int num_threads = 1;
  // Uncomment to enable multithreading
  //int num_threads = ROOT::GetImplicitMTPoolSize();
  vector<unique_ptr<TTree>> out_trees{};

  vector<int> n_small_tag_var(num_threads);
  vector<int> n_small_jets_var(num_threads);
  vector<int> n_large_tag_var(num_threads);
  vector<int> n_large_jets_var(num_threads);
  vector<int> n_track_tag_var(num_threads);
  vector<int> n_track_jets_var(num_threads);
  /*
  vector<int> n_h1_assoc_track_tag_var(num_threads);
  vector<int> n_h1_assoc_track_jets_var(num_threads);
  vector<int> n_h2_assoc_track_tag_var(num_threads);
  vector<int> n_h2_assoc_track_jets_var(num_threads);
  */
  vector<int> nElec(num_threads);
  vector<int> nMuon(num_threads);
  vector<double> mc_sf_var(num_threads);
  vector<unique_ptr<out_format>> out_vars{};
  
  // vector<unique_ptr<reweight_format>> rwgt_vars{};
  for (int i = 0; i < num_threads; ++i) {
      gROOT->cd();
      out_vars.push_back(make_unique<out_format>());
      // rwgt_vars.push_back(make_unique<reweight_format>());
      out_trees.push_back(make_unique<TTree>(treename, treename));

      out_trees[i]->SetDirectory(nullptr);
      out_trees[i]->Branch("n_small_tag",  &n_small_tag_var[i]);
      out_trees[i]->Branch("n_small_jets", &n_small_jets_var[i]);
      out_trees[i]->Branch("n_large_jets", &n_large_jets_var[i]);
      out_trees[i]->Branch("n_large_tag",  &n_large_tag_var[i]);
      out_trees[i]->Branch("n_track_tag",  &n_track_tag_var[i]);
      out_trees[i]->Branch("n_track_jets", &n_track_jets_var[i]);
      /*
      out_trees[i]->Branch("n_h1_assoc_track_tag",  &n_h1_assoc_track_tag_var[i]);
      out_trees[i]->Branch("n_h1_assoc_track_jets", &n_h1_assoc_track_jets_var[i]);
      out_trees[i]->Branch("n_h2_assoc_track_tag",  &n_h2_assoc_track_tag_var[i]);
      out_trees[i]->Branch("n_h2_assoc_track_jets", &n_h2_assoc_track_jets_var[i]);
      */
      out_trees[i]->Branch("nElec", &nElec[i]);
      out_trees[i]->Branch("nMuon", &nMuon[i]);
      out_trees[i]->Branch("mc_sf", &mc_sf_var[i]);
      out_trees[i]->Branch("event", out_vars[i].get(), out_format_leaflist);
      // out_trees[i]->Branch("rwgt", rwgt_vars[i].get(), rwgt_leaflist);
  }

  if (first_tree) {
      fmt::print("Processing events\n");
  }
  else {
      fmt::print("Collecting Events...\n");
      first_tree = false;
  }
  
  result.ForeachSlot(
    [&out_trees, 
     &out_vars, 
     &n_small_tag_var, 
     &n_small_jets_var, 
     &n_large_tag_var,
     &n_large_jets_var, /*, &rwgt_vars*/
     &n_track_tag_var, 
     &n_track_jets_var, 
     /*
     &n_h1_assoc_track_tag_var, 
     &n_h1_assoc_track_jets_var, 
     &n_h2_assoc_track_tag_var, 
     &n_h2_assoc_track_jets_var, 
     */
     &nElec, 
     &nMuon, 
     &mc_sf_var
     ](unsigned slot, const reconstructed_event& event) {
      auto&& tree = out_trees[slot];
      auto&& vars = out_vars[slot];
      //  auto &&rwgt = rwgt_vars[slot];

      // Object multiplicities
      n_small_tag_var[slot]  = event.n_small_tag;
      n_small_jets_var[slot] = event.n_small_jets;
      n_large_tag_var[slot]  = event.n_large_tag;
      n_large_jets_var[slot] = event.n_large_jets;
      n_track_tag_var[slot]  = event.n_track_tag;
      n_track_jets_var[slot] = event.n_track_jets;
      /*
      n_h1_assoc_track_tag_var[slot]  = event.n_h1_assoc_track_tag;
      n_h1_assoc_track_jets_var[slot] = event.n_h1_assoc_track_jets;
      n_h2_assoc_track_tag_var[slot]  = event.n_h2_assoc_track_tag;
      n_h2_assoc_track_jets_var[slot] = event.n_h2_assoc_track_jets;
      */
      nElec[slot] = event.nElec;
      nMuon[slot] = event.nMuon;
      mc_sf_var[slot]        = event.wgt;

      // Di-Higgs system
      vars->m_hh    = (event.higgs1.p4 + event.higgs2.p4).M();
      vars->pT_hh   = (event.higgs1.p4 + event.higgs2.p4).Pt();
      vars->dR_hh   = event.higgs1.p4.DeltaR(event.higgs2.p4);
      vars->dEta_hh = fabs( event.higgs1.p4.Eta() - event.higgs2.p4.Eta() );
      vars->dPhi_hh = fabs( event.higgs1.p4.DeltaPhi(event.higgs2.p4) );
      
      double dH1 = ( event.higgs1.p4.M() - 124) / (0.1 * event.higgs1.p4.M() );
      double dH2 = ( event.higgs2.p4.M() - 115) / (0.1 * event.higgs2.p4.M() );
      vars->X_hh = sqrt( pow( dH1, 2) + pow( dH2, 2) );

      // Leading Higgs candidate
      vars->h1_M   = event.higgs1.p4.M();
      vars->h1_Pt  = event.higgs1.p4.Pt();
      vars->h1_Eta = event.higgs1.p4.Eta();
      vars->h1_Phi = event.higgs1.p4.Phi();

        vars->h1_j1_M   = event.higgs1.jets[0].p4.M();
        vars->h1_j1_Pt  = event.higgs1.jets[0].p4.Pt();
        vars->h1_j1_Eta = event.higgs1.jets[0].p4.Eta();
        vars->h1_j1_Phi = event.higgs1.jets[0].p4.Phi();

        vars->h1_j2_M   = event.higgs1.jets[1].p4.M();
        vars->h1_j2_Pt  = event.higgs1.jets[1].p4.Pt();
        vars->h1_j2_Eta = event.higgs1.jets[1].p4.Eta();
        vars->h1_j2_Phi = event.higgs1.jets[1].p4.Phi();

        vars->h1_j1_dR    = event.higgs1.p4.DeltaR( event.higgs1.jets[0].p4 );
        vars->h1_j2_dR    = event.higgs1.p4.DeltaR( event.higgs1.jets[1].p4 );
        vars->h1_j1_j2_dR = event.higgs1.jets[0].p4.DeltaR( event.higgs1.jets[1].p4 );

      // Subleading Higgs candidate
      vars->h2_M   = event.higgs2.p4.M();
      vars->h2_Pt  = event.higgs2.p4.Pt();
      vars->h2_Eta = event.higgs2.p4.Eta();
      vars->h2_Phi = event.higgs2.p4.Phi();

        vars->h2_j1_M   = event.higgs2.jets[0].p4.M();
        vars->h2_j1_Pt  = event.higgs2.jets[0].p4.Pt();
        vars->h2_j1_Eta = event.higgs2.jets[0].p4.Eta();
        vars->h2_j1_Phi = event.higgs2.jets[0].p4.Phi();

        vars->h2_j2_M   = event.higgs2.jets[1].p4.M();
        vars->h2_j2_Pt  = event.higgs2.jets[1].p4.Pt();
        vars->h2_j2_Eta = event.higgs2.jets[1].p4.Eta();
        vars->h2_j2_Phi = event.higgs2.jets[1].p4.Phi();

        vars->h2_j1_dR    = event.higgs2.p4.DeltaR( event.higgs2.jets[0].p4 );
        vars->h2_j2_dR    = event.higgs2.p4.DeltaR( event.higgs2.jets[1].p4 );
        vars->h2_j1_j2_dR = event.higgs2.jets[0].p4.DeltaR( event.higgs2.jets[1].p4 );

      // Electron
      vars->elec1_M   = event.elec1.M();
      vars->elec1_Pt  = event.elec1.Pt();
      vars->elec1_Eta = event.elec1.Eta();
      vars->elec1_Phi = event.elec1.Phi();

      // Muon
      vars->muon1_M   = event.muon1.M();
      vars->muon1_Pt  = event.muon1.Pt();
      vars->muon1_Eta = event.muon1.Eta();
      vars->muon1_Phi = event.muon1.Phi();

      // Missing transverse momentum              
      vars->met_Et   = event.met.Pt();
      vars->met_Phi  = event.met.Phi();

      tree->Fill();
  
    },
    {"event" /*, "mc_sf"*/});

  fmt::print("Writing TTree - {}...", treename);
  TList temp_list;
  for (auto&& tree : out_trees) {
      temp_list.Add(tree.get());
  }

  output_file.cd();
  TTree* signal_tree = TTree::MergeTrees(&temp_list);
  if (!signal_tree) {
      fmt::print("\nALL TREES EMPTY");
      return;
  }
  signal_tree->SetName(treename);
  signal_tree->Write("", TObject::kOverwrite);
  fmt::print("\n");
}

#endif

