/// \file utils.h
/// General utilities
///

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

#include <ROOT/RDataFrame.hxx>
#include <ROOT/RVec.hxx>
#include <TFile.h>
#include <TLorentzVector.h>
#include <TROOT.h>

#include "classes/DelphesClasses.h"
#include "classes/DelphesFactory.h"
#include "modules/Delphes.h"

extern double f; // untagged to tagged normalization

/// Higgs boson
struct higgs {
  TLorentzVector p4; ///< 4-momentum
  int jet1;          ///< Index of leading jet
  int jet2;          ///< Index of subleading jet

  higgs() : p4(), jet1(0), jet2(0) {}
  higgs(const TLorentzVector &p4, int jet1, int jet2)
      : p4(p4), jet1(jet1), jet2(jet2) {}
};

/*/// Muon
class Muon {
  public:
    TLorentzVector p4; ///< 4-momentum
    float eloss;       ///< E<SUB>loss</SUB> for muon-in-jet correction
};
*/


/// Jet
class OxJet {
public:
  TLorentzVector p4; ///< 4-momentum
  // float btag;        ///< B-tagging score
  bool tagged; ///< Is jet B-tagged?

  OxJet() : p4(), tagged(false) {}
  OxJet(double M, double pT, double eta, long double phi, bool tagged)
      : p4(), tagged(tagged) {
    p4.SetPtEtaPhiM(pT, eta, phi, M);
  }
};


/// Wrapper around Jet constructor
inline OxJet make_jet(Jet &jet) {
  double M = jet.Mass;
  double pT = jet.PT;
  double eta = jet.Eta;
  long double phi = jet.Phi;
  bool tagged = jet.BTag;

  // Because a constructor can't be used as a Callable
  return OxJet(M, pT, eta, phi, tagged);
}

/*
/// Compare jets by B-tagging score then p<SUB>T</SUB>
inline bool operator<(const Jet& lhs, const Jet& rhs) {
    if (lhs.btag == rhs.btag) {
        return lhs.p4.Pt() < rhs.p4.Pt();
    }
    else {
        return lhs.btag < rhs.btag;
    }
}

inline bool operator==(const Jet& lhs, const Jet& rhs) {
    return (lhs.btag == rhs.btag) && (lhs.p4.Pt() == rhs.p4.Pt());
}

inline bool operator!=(const Jet& lhs, const Jet& rhs) {
    return std::rel_ops::operator!=(lhs, rhs);
}
inline bool operator>(const Jet& lhs, const Jet& rhs) {
    return std::rel_ops::operator>(lhs, rhs);
}
inline bool operator<=(const Jet& lhs, const Jet& rhs) {
    return std::rel_ops::operator<=(lhs, rhs);
}
inline bool operator>=(const Jet& lhs, const Jet& rhs) {
    return std::rel_ops::operator>=(lhs, rhs);
}
*/
/// Reconstructed event information
struct reconstructed_event {
  bool valid;                ///< Is event valid
  int64_t ntag;              ///< Number of B-tagged jets
  int64_t njets;             ///< Total number of jets
  double wgt;                ///< Event Weight
  std::array<OxJet, 4> jets; ///< Array of 4 chosen jets

  higgs higgs1; ///< Leading Higgs
  higgs higgs2; ///< Subleading Higgs

  reconstructed_event()
      : valid(true), // set to true if pairing is valid
        jets(), higgs1(), higgs2() {}
};
/*
/// \brief Return indices of `n_to_choose` jets chosen from `n_jets`
///
/// Used for &lt; 4-tag events to choose additional jets
inline std::vector<int>
jet_indices_comb(int n_jets */ /**< [in] Number of jets to choose from */ //,
/*int n_to_choose */ /**< [in] Number of jets to choose */                /*){
    // returns the indices of the jets to choose, according to combinatorics
    namespace view = ranges::view;
    namespace action = ranges::action;
    // hardcode default seed 5 for reproducability
    static std::seed_seq seeds({5});
    static std::mt19937_64 engine(seeds);
               
    std::binomial_distribution<> binom(n_to_choose, f);
    int n_to_return = 0;
    do {
        n_to_return = binom(engine);
    } while (n_to_return < n_to_choose);
               
    return (std::vector<int>(view::ints(0, n_jets)) | action::shuffle(engine)
            | action::take(n_to_return));
}
*/
/// Output format for writing TTrees
struct out_format {
  double m_hh; ///< Di-Higgs mass (m<SUB>hh</SUB> or m<SUB>4j</SUB>)

  double m_h1;   ///< Leading Higgs mass
                 // double E_h1;   ///< Leading Higgs energy
  double pT_h1;  ///< Leading Higgs p<SUB>T</SUB>
  double eta_h1; ///< Leading Higgs &eta;
  double phi_h1; ///< Leading Higgs &Phi;

  double m_h2;   ///< Subleading Higgs mass
                 // double E_h2;   ///< Subleading Higgs energy
  double pT_h2;  ///< Subleading Higgs p<SUB>T</SUB>
  double eta_h2; ///< Subleading Higgs &eta;
  double phi_h2; ///< Subleading Higgs &Phi;

  double m_h1_j1; ///< Leading Higgs leading jet mass
  // double E_h1_j1;   ///< Leading Higgs leading jet energy
  double pT_h1_j1;  ///< Leading Higgs leading jet p<SUB>T</SUB>
  double eta_h1_j1; ///< Leading Higgs leading jet &eta;
  double phi_h1_j1; ///< Leading Higgs leading jet &Phi;

  double m_h1_j2; ///< Leading Higgs subleading jet mass
  // double E_h1_j2;   ///< Leading Higgs subleading jet energy
  double pT_h1_j2;  ///< Leading Higgs subleading jet p<SUB>T</SUB>
  double eta_h1_j2; ///< Leading Higgs subleading jet &eta;
  double phi_h1_j2; ///< Leading Higgs subleading jet &Phi;

  double m_h2_j1; ///< Subleading Higgs leading jet mass
  // double E_h2_j1;   ///< Subleading Higgs leading jet energy
  double pT_h2_j1;  ///< Subleading Higgs leading jet p<SUB>T</SUB>
  double eta_h2_j1; ///< Subleading Higgs leading jet &eta;
  double phi_h2_j1; ///< Subleading Higgs leading jet &Phi;

  double m_h2_j2; ///< Subleading Higgs subleading jet mass
  // double E_h2_j2;   ///< Subleading Higgs subleading jet energy
  double pT_h2_j2;  ///< Subleading Higgs subleading jet p<SUB>T</SUB>
  double eta_h2_j2; ///< Subleading Higgs subleading jet &eta;
  double phi_h2_j2; ///< Subleading Higgs subleading jet &Phi;
};

/// Output format with reweighting variables
struct reweight_format {
  double pT_4;   ///< p<SUB>T</SUB> of 4th jet
  double pT_2;   ///< p<SUB>T</SUB> of 2nd jet
  double eta_i;  ///< &sum;|&eta;<SUB>i</SUB>|
  double dRjj_1; ///< &Delta;R<SUB>jj,1</SUB>
  double dRjj_2; ///< &Delta;R<SUB>jj,2</SUB>
};

/// Check if b is between a and c
template <typename T> bool between(T a, T b, T c) { return (a < b) && (b < c); }

/// Print function
/*
inline void printout(ROOT::VecOps::RVec<Jet> &jet){
  static std::fstream f;
  f.open ("jets_output.txt");
  for (auto j : jet){
    f << "Jet.Phi ="<<j.Phi;
  }
}*/

/// Write result TTree
template <typename Proxied>
void write_tree(ROOT::RDF::RInterface<Proxied> &result, const char *treename,
                TFile &output_file /**< [out] Tree to write to */) {
  using namespace std;
  using namespace ROOT::Experimental;
  namespace view = ranges::view;
  namespace action = ranges::action;
  static bool first_tree = true;


  const char *out_format_leaflist = "m_hh/D:m_h1/D:pT_h1:eta_h1:phi_h1:"
                                    "m_h2/D:pT_h2:eta_h2:phi_h2:"
                                    "m_h1_j1:pT_h1_j1:eta_h1_j1:phi_h1_j1:"
                                    "m_h1_j2:pT_h1_j2:eta_h1_j2:phi_h1_j2:"
                                    "m_h2_j1:pT_h2_j1:eta_h2_j1:phi_h2_j1:"
                                    "m_h2_j2:pT_h2_j2:eta_h2_j2:phi_h2_j2";

  const char *rwgt_leaflist = "pT_4/D:pT_2:eta_i:dRjj_1:dRjj_2";

  int num_threads = ROOT::GetImplicitMTPoolSize();
  vector<unique_ptr<TTree>> out_trees{};
  vector<int> ntag_var(num_threads);
  vector<int> njets_var(num_threads);
  vector<double> mc_sf_var(num_threads);
  vector<unique_ptr<out_format>> out_vars{};
  vector<unique_ptr<reweight_format>> rwgt_vars{};
  for (int i = 0; i < num_threads; ++i) {
    gROOT->cd();
    out_vars.push_back(make_unique<out_format>());
    rwgt_vars.push_back(make_unique<reweight_format>());
    out_trees.push_back(make_unique<TTree>(treename, treename));

    out_trees[i]->SetDirectory(nullptr);
    out_trees[i]->Branch("ntag", &ntag_var[i]);
    out_trees[i]->Branch("njets", &njets_var[i]);
    out_trees[i]->Branch("mc_sf", &mc_sf_var[i]);
    out_trees[i]->Branch("event", out_vars[i].get(), out_format_leaflist);
    out_trees[i]->Branch("rwgt", rwgt_vars[i].get(), rwgt_leaflist);
  }

  if (first_tree) {
    fmt::print("Processing events\n");
  } else {
    fmt::print("Collecting Events...\n");
    first_tree = false;
  }
  result.ForeachSlot(
      [&out_trees, &out_vars, &ntag_var, &njets_var, &rwgt_vars,
       &mc_sf_var](unsigned slot, const reconstructed_event &event){
        auto &&tree = out_trees[slot];
        auto &&vars = out_vars[slot];
        auto &&rwgt = rwgt_vars[slot];


        vars->m_hh = (event.higgs1.p4 + event.higgs2.p4).M();
        ntag_var[slot] = event.ntag;
        njets_var[slot] = event.njets;
        mc_sf_var[slot] = event.wgt;

        vars->m_h1 = event.higgs1.p4.M();
        vars->pT_h1 = event.higgs1.p4.Pt();
        vars->eta_h1 = event.higgs1.p4.Eta();
        vars->phi_h1 = event.higgs1.p4.Phi();

        vars->m_h2 = event.higgs2.p4.M();
        vars->pT_h2 = event.higgs2.p4.Pt();
        vars->eta_h2 = event.higgs2.p4.Eta();
        vars->phi_h2 = event.higgs2.p4.Phi();

        vars->m_h1_j1 = event.jets[event.higgs1.jet1].p4.M();
        vars->pT_h1_j1 = event.jets[event.higgs1.jet1].p4.Pt();
        vars->eta_h1_j1 = event.jets[event.higgs1.jet1].p4.Eta();
        vars->phi_h1_j1 = event.jets[event.higgs1.jet1].p4.Phi();

        vars->m_h1_j2 = event.jets[event.higgs1.jet2].p4.M();
        vars->pT_h1_j2 = event.jets[event.higgs1.jet2].p4.Pt();
        vars->eta_h1_j2 = event.jets[event.higgs1.jet2].p4.Eta();
        vars->phi_h1_j2 = event.jets[event.higgs1.jet2].p4.Phi();

        vars->m_h2_j1 = event.jets[event.higgs2.jet1].p4.M();
        vars->pT_h2_j1 = event.jets[event.higgs2.jet1].p4.Pt();
        vars->eta_h2_j1 = event.jets[event.higgs2.jet1].p4.Eta();
        vars->phi_h2_j1 = event.jets[event.higgs2.jet1].p4.Phi();

        vars->m_h2_j2 = event.jets[event.higgs2.jet2].p4.M();
        vars->pT_h2_j2 = event.jets[event.higgs2.jet2].p4.Pt();
        vars->eta_h2_j2 = event.jets[event.higgs2.jet2].p4.Eta();
        vars->phi_h2_j2 = event.jets[event.higgs2.jet2].p4.Phi();

        // Fill reweighting variables

        auto rwgt_jets = event.jets;
        rwgt_jets |=
            (action::sort(ranges::ordered_less{},
                          [](const auto &jet) { return jet.p4.Pt(); }) |
             action::reverse);
        rwgt->pT_2 = rwgt_jets[1].p4.Pt();
        rwgt->pT_4 = rwgt_jets[3].p4.Pt();
        rwgt->eta_i = ranges::accumulate(rwgt_jets, 0., ranges::plus{},
                                         [](const auto &jet) {
                                           return std::abs(jet.p4.Eta());
                                         }) /
                      4;

        // This would be much easier with C++17
        std::vector<std::tuple<int, int>> rwgt_jet_pairs =
            view::cartesian_product(view::ints(0, 4), view::ints(0, 4)) |
            view::remove_if(
                [](auto &&is) { return std::get<0>(is) <= std::get<1>(is); });
        rwgt_jet_pairs |=
            (action::sort(ranges::ordered_less{}, [&rwgt_jets](auto &&is) {
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

        tree->Fill();
      },
      {"event"});

  fmt::print("Writing TTree - {}...", treename);
  TList temp_list;
  for (auto &&tree : out_trees) {
    temp_list.Add(tree.get());
  }

  output_file.cd();
  TTree *signal_tree = TTree::MergeTrees(&temp_list);
  if (!signal_tree) {
    fmt::print("\nALL TREES EMPTY");
    return;
  }
  signal_tree->SetName(treename);
  signal_tree->Write("", TObject::kOverwrite);
  fmt::print("\n");
}
