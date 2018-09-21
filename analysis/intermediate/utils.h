/// \file utils.h
// General utilities
//
//

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

// Higgs Boson
struct higgs {
    TLorentzVector p4; ///< 4-momentum
    // int jet1;          ///< Index of leading jet
    // int jet2;          ///< Index of subleading jet

    higgs() : p4() {}
    higgs(const TLorentzVector& p4) : p4(p4) {}
};

class OxJet {
  public:
    TLorentzVector p4; ///< 4-momentum
    float btag;        ///< B-tagging score
    bool tagged;       ///< Is jet B-tagged?

    OxJet() : p4(), tagged(false) {}
    OxJet(double M, double pT, double eta, long double phi, bool tagged) : p4(), tagged(tagged) {
        p4.SetPtEtaPhiM(pT, eta, phi, M);
    }
};

// Make jet from Oxjet function

inline OxJet make_oxjet(OxJet& jet) {
    double M = jet.p4.M();
    double pT = jet.p4.Pt();
    double eta = jet.p4.Eta();
    double phi = jet.p4.Phi();
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
};

// Make jet function
inline OxJet make_jet(Jet& jet) {
    double M = jet.Mass;
    double pT = jet.PT;
    double eta = jet.Eta;
    double phi = jet.Phi;
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

// Reconstructed event information
struct reconstructed_event {
    bool valid;           ///< Is event valid
    int64_t n_small_tag;  ///< Number of B-tagged smallR jets
    int64_t n_small_jets; ///< Total number of smallR jets
    int64_t n_large_tag;  ///< Number of B-tagged LargeR jets
    int64_t n_large_jets; ///< Total number of LargeR jets
    double wgt;           ///< Event Weight

    OxJet large_jet;
    std::array<OxJet, 2> small_jets; ///< Array of 2 chosen jets

    higgs higgs1; ///< Leading Higgs
    higgs higgs2; ///< Subleading Higgs

    reconstructed_event()
        : valid(true), // set to true if pairing is valid
          large_jet(),
          small_jets(),
          higgs1(),
          higgs2() {}
};

struct out_format {
    double m_hh; ///< Di-Higgs mass (m<SUB>hh</SUB> or m<SUB>4j</SUB>)

    double m_h1;   ///< Leading Higgs mass
    double pT_h1;  ///< Leading Higgs p<SUB>T</SUB>
    double eta_h1; ///< Leading Higgs &eta;
    double phi_h1; ///< Leading Higgs &Phi;

    double m_h2;   ///< Subleading Higgs mass
    double pT_h2;  ///< Subleading Higgs p<SUB>T</SUB>
    double eta_h2; ///< Subleading Higgs &eta;
    double phi_h2; ///< Subleading Higgs &Phi;

    double m_h1_large_jet; ///< Leading Higgs leading jet mass
    // double E_h1_j1;   ///< Leading Higgs leading jet energy
    double pT_h1_large_jet;  ///< Leading Higgs leading jet p<SUB>T</SUB>
    double eta_h1_large_jet; ///< Leading Higgs leading jet &eta;
    double phi_h1_large_jet; ///< Leading Higgs leading jet &Phi;

    double m_h2_j1;   ///< Subleading Higgs leading jet mass
    double pT_h2_j1;  ///< Subleading Higgs leading jet p<SUB>T</SUB>
    double eta_h2_j1; ///< Subleading Higgs leading jet &eta;
    double phi_h2_j1; ///< Subleading Higgs leading jet &Phi;

    double m_h2_j2;   ///< Subleading Higgs subleading jet mass
    double pT_h2_j2;  ///< Subleading Higgs subleading jet p<SUB>T</SUB>
    double eta_h2_j2; ///< Subleading Higgs subleading jet &eta;
    double phi_h2_j2; ///< Subleading Higgs subleading jet &Phi;
};
/*
struct reweight_format {
  double pT_4;   ///< p<SUB>T</SUB> of 4th jet
  double pT_2;   ///< p<SUB>T</SUB> of 2nd jet
  double eta_i;  ///< &sum;|&eta;<SUB>i</SUB>|
  double dRjj_1; ///< &Delta;R<SUB>jj,1</SUB>
  double dRjj_2; ///< &Delta;R<SUB>jj,2</SUB>
};
*/
template <typename Proxied>
void write_tree(ROOT::RDF::RInterface<Proxied>& result, const char* treename,
                TFile& output_file /**< [out] Tree to write to */) {
    using namespace std;
    using namespace ROOT::Experimental;
    namespace view = ranges::view;
    namespace action = ranges::action;
    static bool first_tree = true;

    const char* out_format_leaflist =
          "m_hh/D:m_h1/D:pT_h1:eta_h1:phi_h1:"
          "m_h2/D:pT_h2:eta_h2:phi_h2:"
          "m_h1_large_jet:pT_h1_large_jet:eta_h1_large_jet:phi_h1_large_jet:"
          "m_h2_j1:pT_h2_j1:eta_h2_j1:phi_h2_j1:"
          "m_h2_j2:pT_h2_j2:eta_h2_j2:phi_h2_j2";

    // const char *rwgt_leaflist = "pT_4/D:pT_2:eta_i:dRjj_1:dRjj_2";

    int num_threads = ROOT::GetImplicitMTPoolSize();
    vector<unique_ptr<TTree>> out_trees{};

    vector<int> n_small_tag_var(num_threads);
    vector<int> n_small_jets_var(num_threads);
    vector<int> n_large_tag_var(num_threads);
    vector<int> n_large_jets_var(num_threads);
    vector<double> mc_sf_var(num_threads);
    vector<unique_ptr<out_format>> out_vars{};
    // vector<unique_ptr<reweight_format>> rwgt_vars{};
    for (int i = 0; i < num_threads; ++i) {
        gROOT->cd();
        out_vars.push_back(make_unique<out_format>());
        // rwgt_vars.push_back(make_unique<reweight_format>());
        out_trees.push_back(make_unique<TTree>(treename, treename));

        out_trees[i]->SetDirectory(nullptr);
        out_trees[i]->Branch("n_small_tag", &n_small_tag_var[i]);
        out_trees[i]->Branch("n_small_jets", &n_small_jets_var[i]);
        out_trees[i]->Branch("n_large_jets", &n_large_jets_var[i]);
        out_trees[i]->Branch("n_large_tag", &n_large_tag_var[i]);
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
          [&out_trees, &out_vars, &n_small_tag_var, &n_small_jets_var, &n_large_tag_var,
           &n_large_jets_var /*, &rwgt_vars*/,
           &mc_sf_var](unsigned slot, const reconstructed_event& event) {
              auto&& tree = out_trees[slot];
              auto&& vars = out_vars[slot];
              //  auto &&rwgt = rwgt_vars[slot];

              vars->m_hh = (event.higgs1.p4 + event.higgs2.p4).M();
              n_small_tag_var[slot] = event.n_small_tag;
              n_small_jets_var[slot] = event.n_small_jets;
              n_large_tag_var[slot] = event.n_large_tag;
              n_large_jets_var[slot] = event.n_large_jets;
              mc_sf_var[slot] = event.wgt;

              vars->m_h1 = event.higgs1.p4.M();
              vars->pT_h1 = event.higgs1.p4.Pt();
              vars->eta_h1 = event.higgs1.p4.Eta();
              vars->phi_h1 = event.higgs1.p4.Phi();
              vars->m_h2 = event.higgs2.p4.M();
              vars->pT_h2 = event.higgs2.p4.Pt();
              vars->eta_h2 = event.higgs2.p4.Eta();
              vars->phi_h2 = event.higgs2.p4.Phi();

              vars->m_h1_large_jet = event.large_jet.p4.M();
              vars->pT_h1_large_jet = event.large_jet.p4.Pt();
              vars->eta_h1_large_jet = event.large_jet.p4.Eta();
              vars->phi_h1_large_jet = event.large_jet.p4.Phi();

              vars->m_h2_j1 = event.small_jets[0].p4.M();
              vars->pT_h2_j1 = event.small_jets[0].p4.Pt();
              vars->eta_h2_j1 = event.small_jets[0].p4.Eta();
              vars->phi_h2_j1 = event.small_jets[0].p4.Phi();

              vars->m_h2_j2 = event.small_jets[1].p4.M();
              vars->pT_h2_j2 = event.small_jets[1].p4.Pt();
              vars->eta_h2_j2 = event.small_jets[1].p4.Eta();
              vars->phi_h2_j2 = event.small_jets[1].p4.Phi();

              /*
                      auto rwgt_jets = event.jets;
                      rwgt_jets |=
                          (action::sort(ranges::ordered_less{},
                                        [](const auto &jet) { return jet.p4.Pt(); }) |
                           action::reverse);
                      rwgt->pT_2 = rwgt_jets[1].p4.Pt();
                      rwgt->pT_4 = rwgt_jets[3].p4.Pt();
                      rwgt->eta_i = ranges::accumulate(rwgt_jets, 0., ranges::plus{},
                                                       [](const auto &jet) {
                                                         return
                 std::abs(jet.p4.Eta());
                                                       }) /
                                    4;

                      std::vector<std::tuple<int, int>> rwgt_jet_pairs =
                          view::cartesian_product(view::ints(0, 4), view::ints(0, 4))
                 |
                          view::remove_if(
                              [](auto &&is) { return std::get<0>(is) <=
                 std::get<1>(is); });
                      rwgt_jet_pairs |=
                          (action::sort(ranges::ordered_less{}, [&rwgt_jets](auto
                 &&is) {
                            auto i = std::get<0>(is);
                            auto j = std::get<1>(is);
                            return rwgt_jets[i].p4.DeltaR(rwgt_jets[j].p4);
                          }));
                      auto pair = rwgt_jet_pairs[0]; // tuple
                      std::vector<int> other_pair =
                          view::ints(0, 4) | view::remove_if([&pair](int i) {
                            return i == std::get<0>(pair) || i == std::get<1>(pair);
                          });

                      rwgt->dRjj_1 = rwgt_jets[std::get<0>(pair)].p4.DeltaR(
                          rwgt_jets[std::get<1>(pair)].p4);
                      rwgt->dRjj_2 =
                          rwgt_jets[other_pair[0]].p4.DeltaR(rwgt_jets[other_pair[1]].p4);
              */
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
