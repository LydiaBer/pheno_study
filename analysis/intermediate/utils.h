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

#include "OutputTree.h"

extern double f;

class OxJet {
  public:
    TLorentzVector p4; ///< 4-momentum
    double btag;       ///< B-tagging score
    bool tagged;       ///< Is jet B-tagged?

    OxJet() : p4(), btag(0), tagged(false) {}
    OxJet(double M, double pT, double eta, long double phi, double btag, bool tagged)
        : p4(), btag(btag), tagged(tagged) {
        p4.SetPtEtaPhiM(pT, eta, phi, M);
    }
};

// Higgs boson
struct higgs {
    TLorentzVector p4;       ///< 4-momentum
    int jet1;                ///< Index of leading jet
    int jet2;                ///< Index of subleading jet
    std::vector<OxJet> jets; // Vector of jets associated with Higgs candidate

    higgs() : p4(), jet1(0), jet2(0), jets() {}
    higgs(const TLorentzVector& p4, int jet1, int jet2, std::vector<OxJet> jets)
        : p4(p4), jet1(jet1), jet2(jet2), jets(jets) {}
};

// DiHiggs system object
struct dihiggs {
  higgs higgs1;
  higgs higgs2;
  bool isValid;

  dihiggs() : isValid(false){}
};

// Make jet from Oxjet function
inline OxJet make_oxjet(OxJet& jet) {
    double M = jet.p4.M();
    double pT = jet.p4.Pt();
    double eta = jet.p4.Eta();
    double phi = jet.p4.Phi();
    bool btag = jet.btag;
    bool tagged = jet.tagged;

    return OxJet(M, pT, eta, phi, btag, tagged);
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

    TLorentzVector p4() { return jet_1.p4 + jet_2.p4; }
};

// Make jet function
inline OxJet make_jet(Jet& jet) {
    double M = jet.Mass;
    double pT = jet.PT;
    double eta = jet.Eta;
    double phi = jet.Phi;
    double btag = jet.BTagWeight;
    bool tagged = jet.BTag;

    // Because a constructor can't be used as a Callable
    return OxJet(M, pT, eta, phi, btag, tagged);
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

// Function to compute angular distance between 2 OxJets
inline double deltaR(OxJet& jet1, OxJet& jet2) { return jet1.p4.DeltaR(jet2.p4); }

// Reconstructed event in the intermediate regime
// Reconstructed event information
struct reconstructed_event {
    bool valid;                ///< Is event valid
    int64_t n_small_tag;       ///< Number of B-tagged smallR jets
    int64_t n_small_jets;      ///< Total number of smallR jets
    int64_t n_large_tag;       ///< Number of B-tagged LargeR jets
    int64_t n_large_jets;      ///< Total number of LargeR jets
    int64_t n_track_tag;       ///< Number of B-tagged track jets
    int64_t n_track_jets;      ///< Total number of track jets
    int64_t n_jets_in_higgs1;  ///< Total number of jets associated with higgs 1
    int64_t n_jets_in_higgs2;  ///< Total number of jets associated with higgs 2
    int64_t n_bjets_in_higgs1; ///< Total number of b-jets associated with higgs 1
    int64_t n_bjets_in_higgs2; ///< Total number of b-jets associated with higgs 2
    double wgt;                ///< Event Weight

    int64_t nElec; ///< Number of electrons at Delphes level
    int64_t nMuon; ///< Number of muons at Delphes level

    TLorentzVector met;   ///< MET
    TLorentzVector elec1; ///< leading electron
    TLorentzVector muon1; ///< leading muon

    higgs higgs1; ///< Leading Higgs
    higgs higgs2; ///< Subleading Higgs

    reconstructed_event()
        : valid(true), // set to true if pairing is valid
          higgs1(),
          higgs2() {}
};

// Output format
// Suppress unused parameter warning
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
// Macro containing argument list
#define BRANCHES const reconstructed_event& evt
OutputTree output_format{
      "", nullptr, 1,
      // Object multiplicities
      std::tuple{"n_small_tag", [](BRANCHES) { return evt.n_small_tag; }},
      std::tuple{"n_small_jets", [](BRANCHES) { return evt.n_small_jets; }},
      std::tuple{"n_large_tag", [](BRANCHES) { return evt.n_large_tag; }},
      std::tuple{"n_large_jets", [](BRANCHES) { return evt.n_large_jets; }},
      std::tuple{"n_track_tag", [](BRANCHES) { return evt.n_track_tag; }},
      std::tuple{"n_track_jets", [](BRANCHES) { return evt.n_track_jets; }},
      std::tuple{"n_jets_in_higgs1", [](BRANCHES) { return evt.n_jets_in_higgs1; }},
      std::tuple{"n_jets_in_higgs2", [](BRANCHES) { return evt.n_jets_in_higgs2; }},
      std::tuple{"nElec", [](BRANCHES) { return evt.nElec; }},
      std::tuple{"nMuon", [](BRANCHES) { return evt.nMuon; }},
      // Weight
      std::tuple{"mc_sf", [](BRANCHES) { return evt.wgt; }},
      // di Higgs system
      std::tuple{"m_hh", [](BRANCHES) { return (evt.higgs1.p4 + evt.higgs2.p4).M(); }},
      std::tuple{"pt_hh", [](BRANCHES) { return (evt.higgs1.p4 + evt.higgs2.p4).Pt(); }},
      std::tuple{"dR_hh", [](BRANCHES) { return evt.higgs1.p4.DeltaR(evt.higgs2.p4); }},
      std::tuple{"dEta_hh",
                 [](BRANCHES) { return fabs(evt.higgs1.p4.Eta() - evt.higgs2.p4.Eta()); }},
      std::tuple{"dPhi_hh", [](BRANCHES) { return fabs(evt.higgs1.p4.DeltaPhi(evt.higgs2.p4)); }},
      std::tuple{"X_hh",
                 [](BRANCHES) {
                     double dH1 = (evt.higgs1.p4.M() - 124.) / (0.1 * evt.higgs1.p4.M());
                     double dH2 = (evt.higgs2.p4.M() - 115.) / (0.1 * evt.higgs2.p4.M());
                     return sqrt(pow(dH1, 2) + pow(dH2, 2));
                 }},

      // Leading Higgs
      std::tuple{"h1_M", [](BRANCHES) { return evt.higgs1.p4.M(); }},
      std::tuple{"h1_Pt", [](BRANCHES) { return evt.higgs1.p4.Pt(); }},
      std::tuple{"h1_Eta", [](BRANCHES) { return evt.higgs1.p4.Eta(); }},
      std::tuple{"h1_Phi", [](BRANCHES) { return evt.higgs1.p4.Phi(); }},

      // Leading Higgs: Jet 1
      std::tuple{"h1_j1_M",
                 [](BRANCHES) {
                     // 0. if no H1 J1
                     if (evt.higgs1.jets.size() <= 0) return 0.;
                     return evt.higgs1.jets[0].p4.M();
                 }},
      std::tuple{"h1_j1_Pt",
                 [](BRANCHES) {
                     // 0. if no H1 J1
                     if (evt.higgs1.jets.size() <= 0) return 0.;
                     return evt.higgs1.jets[0].p4.Pt();
                 }},
      std::tuple{"h1_j1_Eta",
                 [](BRANCHES) {
                     // 0. if no H1 J1
                     if (evt.higgs1.jets.size() <= 0) return 0.;
                     return evt.higgs1.jets[0].p4.Eta();
                 }},
      std::tuple{"h1_j1_Phi",
                 [](BRANCHES) {
                     // 0. if no H1 J1
                     if (evt.higgs1.jets.size() <= 0) return 0.;
                     return evt.higgs1.jets[0].p4.Phi();
                 }},
      std::tuple{"h1_j1_BTagWeight",
                 [](BRANCHES) {
                     // 0. if no H1 J1
                     if (evt.higgs1.jets.size() <= 0) return 0.;
                     return evt.higgs1.jets[0].btag;
                 }},
      std::tuple{"h1_j1_BTag",
                 [](BRANCHES) {
                     // 0. if no H1 J1
                     if (evt.higgs1.jets.size() <= 0) return false;
                     return evt.higgs1.jets[0].tagged;
                 }},
      std::tuple{"h1_j1_dR",
                 [](BRANCHES) {
                     // 0. if no H1 J1
                     if (evt.higgs1.jets.size() <= 0) return 0.;
                     return evt.higgs1.p4.DeltaR(evt.higgs1.jets[0].p4);
                 }},

      // Leading Higgs: Jet 2
      std::tuple{"h1_j2_M",
                 [](BRANCHES) {
                     // 0. if no H1 J2
                     if (evt.higgs1.jets.size() <= 1) return 0.;
                     return evt.higgs1.jets[1].p4.M();
                 }},
      std::tuple{"h1_j2_Pt",
                 [](BRANCHES) {
                     // 0. if no H1 J2
                     if (evt.higgs1.jets.size() <= 1) return 0.;
                     return evt.higgs1.jets[1].p4.Pt();
                 }},
      std::tuple{"h1_j2_Eta",
                 [](BRANCHES) {
                     // 0. if no H1 J2
                     if (evt.higgs1.jets.size() <= 1) return 0.;
                     return evt.higgs1.jets[1].p4.Eta();
                 }},
      std::tuple{"h1_j2_Phi",
                 [](BRANCHES) {
                     // 0. if no H1 J2
                     if (evt.higgs1.jets.size() <= 1) return 0.;
                     return evt.higgs1.jets[1].p4.Phi();
                 }},
      std::tuple{"h1_j2_BTagWeight",
                 [](BRANCHES) {
                     // 0. if no H1 J2
                     if (evt.higgs1.jets.size() <= 1) return 0.;
                     return evt.higgs1.jets[1].btag;
                 }},
      std::tuple{"h1_j2_BTag",
                 [](BRANCHES) {
                     // 0. if no H1 J2
                     if (evt.higgs1.jets.size() <= 1) return false;
                     return evt.higgs1.jets[1].tagged;
                 }},
      std::tuple{"h1_j2_dR",
                 [](BRANCHES) {
                     // 0. if no H1 J2
                     if (evt.higgs1.jets.size() <= 1) return 0.;
                     return evt.higgs1.p4.DeltaR(evt.higgs1.jets[1].p4);
                 }},

      std::tuple{"h1_j1_j2_dR",
                 [](BRANCHES) {
                     // 0. if no H1 J2
                     if (evt.higgs1.jets.size() <= 1) return 0.;
                     return evt.higgs1.jets[0].p4.DeltaR(evt.higgs1.jets[1].p4);
                 }},

      // Subleading Higgs
      std::tuple{"h2_M", [](BRANCHES) { return evt.higgs2.p4.M(); }},
      std::tuple{"h2_Pt", [](BRANCHES) { return evt.higgs2.p4.Pt(); }},
      std::tuple{"h2_Eta", [](BRANCHES) { return evt.higgs2.p4.Eta(); }},
      std::tuple{"h2_Phi", [](BRANCHES) { return evt.higgs2.p4.Phi(); }},

      // Subleading Higgs: Jet 1
      std::tuple{"h2_j1_M",
                 [](BRANCHES) {
                     // 0. if no H2 J1
                     if (evt.higgs2.jets.size() <= 0) return 0.;
                     return evt.higgs2.jets[0].p4.M();
                 }},
      std::tuple{"h2_j1_Pt",
                 [](BRANCHES) {
                     // 0. if no H2 J1
                     if (evt.higgs2.jets.size() <= 0) return 0.;
                     return evt.higgs2.jets[0].p4.Pt();
                 }},
      std::tuple{"h2_j1_Eta",
                 [](BRANCHES) {
                     // 0. if no H2 J1
                     if (evt.higgs2.jets.size() <= 0) return 0.;
                     return evt.higgs2.jets[0].p4.Eta();
                 }},
      std::tuple{"h2_j1_Phi",
                 [](BRANCHES) {
                     // 0. if no H2 J1
                     if (evt.higgs2.jets.size() <= 0) return 0.;
                     return evt.higgs2.jets[0].p4.Phi();
                 }},
      std::tuple{"h2_j1_BTagWeight",
                 [](BRANCHES) {
                     // 0. if no H2 J1
                     if (evt.higgs2.jets.size() <= 0) return 0.;
                     return evt.higgs2.jets[0].btag;
                 }},
      std::tuple{"h2_j1_BTag",
                 [](BRANCHES) {
                     // 0. if no H2 J1
                     if (evt.higgs2.jets.size() <= 0) return false;
                     return evt.higgs2.jets[0].tagged;
                 }},
      std::tuple{"h2_j1_dR",
                 [](BRANCHES) {
                     // 0. if no H2 J1
                     if (evt.higgs2.jets.size() <= 0) return 0.;
                     return evt.higgs2.p4.DeltaR(evt.higgs2.jets[0].p4);
                 }},

      // Subleading Higgs: Jet 2
      std::tuple{"h2_j2_M",
                 [](BRANCHES) {
                     // 0. if no H2 J2
                     if (evt.higgs2.jets.size() <= 1) return 0.;
                     return evt.higgs2.jets[1].p4.M();
                 }},
      std::tuple{"h2_j2_Pt",
                 [](BRANCHES) {
                     // 0. if no H2 J2
                     if (evt.higgs2.jets.size() <= 1) return 0.;
                     return evt.higgs2.jets[1].p4.Pt();
                 }},
      std::tuple{"h2_j2_Eta",
                 [](BRANCHES) {
                     // 0. if no H2 J2
                     if (evt.higgs2.jets.size() <= 1) return 0.;
                     return evt.higgs2.jets[1].p4.Eta();
                 }},
      std::tuple{"h2_j2_Phi",
                 [](BRANCHES) {
                     // 0. if no H2 J2
                     if (evt.higgs2.jets.size() <= 1) return 0.;
                     return evt.higgs2.jets[1].p4.Phi();
                 }},
      std::tuple{"h2_j2_BTagWeight",
                 [](BRANCHES) {
                     // 0. if no H2 J2
                     if (evt.higgs2.jets.size() <= 1) return 0.;
                     return evt.higgs2.jets[1].btag;
                 }},
      std::tuple{"h2_j2_BTag",
                 [](BRANCHES) {
                     // 0. if no H2 J2
                     if (evt.higgs2.jets.size() <= 1) return false;
                     return evt.higgs2.jets[1].tagged;
                 }},
      std::tuple{"h2_j2_dR",
                 [](BRANCHES) {
                     // 0. if no H2 J2
                     if (evt.higgs2.jets.size() <= 1) return 0.;
                     return evt.higgs2.p4.DeltaR(evt.higgs2.jets[1].p4);
                 }},

      std::tuple{"h2_j1_j2_dR",
                 [](BRANCHES) {
                     // 0. if no H2 J2
                     if (evt.higgs2.jets.size() <= 1) return 0.;
                     return evt.higgs2.jets[0].p4.DeltaR(evt.higgs2.jets[1].p4);
                 }},

      // Electron
      std::tuple{"elec1_M", [](BRANCHES) { return evt.elec1.M(); }},
      std::tuple{"elec1_Pt", [](BRANCHES) { return evt.elec1.Pt(); }},
      std::tuple{"elec1_Eta", [](BRANCHES) { return evt.elec1.Eta(); }},
      std::tuple{"elec1_Phi", [](BRANCHES) { return evt.elec1.Phi(); }},

      // Muon
      std::tuple{"muon1_M", [](BRANCHES) { return evt.muon1.M(); }},
      std::tuple{"muon1_Pt", [](BRANCHES) { return evt.muon1.Pt(); }},
      std::tuple{"muon1_Eta", [](BRANCHES) { return evt.muon1.Eta(); }},
      std::tuple{"muon1_Phi", [](BRANCHES) { return evt.muon1.Phi(); }},

      //  MET
      std::tuple{"MET_Et", [](BRANCHES) { return evt.met.Pt(); }},
      std::tuple{"MET_Phi", [](BRANCHES) { return evt.met.Phi(); }}
      // Done
};

#pragma GCC diagnostic pop
#endif
