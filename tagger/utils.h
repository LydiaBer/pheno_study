#pragma once
#include <array>
#include <cmath>
#include <cstdlib>
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
#include "include/PIDUtils.h"
#include "modules/Delphes.h"

#include <fastjet/ClusterSequence.hh>
#include <fastjet/JetDefinition.hh>
#include <fastjet/PseudoJet.hh>

namespace view = ranges::view;
namespace action = ranges::action;

// Higgs Boson
struct higgs {
  TLorentzVector p4; ///< 4-momentum

  higgs() : p4() {}
  higgs(const TLorentzVector &p4) : p4(p4) {}
};

class OxJet {
public:
  TLorentzVector p4; ///< 4-momentum
                     // float btag;        ///< B-tagging score
  bool tagged;       ///< Is jet B-tagged?

  OxJet() : p4(), tagged(false) {}
  OxJet(double M, double pT, double eta, long double phi, bool tag)
      : p4(), tagged(tag) {
    p4.SetPtEtaPhiM(pT, eta, phi, M);
  }
};

class TaggedJet {

public:
  TLorentzVector p4; ///< 4-momentum
  // float btag;        ///< B-tagging score
  bool tagged; ///< Is jet B-tagged?
  int ntag;
  std::vector<OxJet> constituents;
  TaggedJet() : p4(), tagged(false) {}
  TaggedJet(double M, double pT, double eta, long double phi, bool tag)
      : p4(), tagged(tag), ntag(0) {
    p4.SetPtEtaPhiM(pT, eta, phi, M);
  }
  TaggedJet(double M, double pT, double eta, long double phi, bool tag,
            int numberB)
      : p4(), tagged(tag), ntag(numberB) {
    p4.SetPtEtaPhiM(pT, eta, phi, M);
  }
  TaggedJet(OxJet calojet, std::vector<OxJet> child, int numberB)
      : p4(), tagged(true), ntag(numberB) {
    p4.SetPtEtaPhiM(calojet.p4.Pt(), calojet.p4.Eta(), calojet.p4.Phi(),
                    calojet.p4.M());
    for (int i = 0; i < child.size(); i++) {
      constituents.push_back(child[i]);
    }
  }
};

class MyInfo : public fastjet::PseudoJet::UserInfoBase {
public:
  MyInfo(int id) : tagging_score(id){};
  int tagged() const { return tagging_score; }
  int tagging_score;
};

inline fastjet::PseudoJet make_pseudo(Jet &jet) {

  TLorentzVector p4;
  double M = jet.Mass;
  double pT = jet.PT;
  double eta = jet.Eta;
  double phi = jet.Phi;
  int tag = jet.BTag;

  p4.SetPtEtaPhiM(pT, eta, phi, M);
  fastjet::PseudoJet trk_pseudo = fastjet::PseudoJet(p4);
  trk_pseudo.set_user_info(new MyInfo(tag));

  return trk_pseudo;
}

inline OxJet undo_pseudo(fastjet::PseudoJet &jet) {
  double M = jet.m();
  double pT = jet.perp();
  double eta = jet.eta();
  double phi = jet.phi();
  bool tagged;
  if (jet.user_info<MyInfo>().tagged() == 1)
    tagged = true;
  if (jet.user_info<MyInfo>().tagged() == 0)
    tagged = false;

  return OxJet(M, pT, eta, phi, tagged);
}

inline TaggedJet make_tagged(OxJet &calojet, std::vector<OxJet> &subjets,
                             int ntag) {

  return TaggedJet(calojet, subjets, ntag);
}

inline OxJet make_jet(Jet &jet) {
  double M = jet.Mass;
  double pT = jet.PT;
  double eta = jet.Eta;
  long double phi = jet.Phi;
  bool tagged = false;

  if (jet.Flavor == 5)
    tagged = true;
  // Because a constructor can't be used as a Callable
  return OxJet(M, pT, eta, phi, tagged);
}

inline fastjet::PseudoJet make_tower(const Tower &tower) {

  TLorentzVector p4;
  double E = tower.E;
  double ET = tower.ET;
  double eta = tower.Eta;
  double phi = tower.Phi;

  p4.SetPtEtaPhiE(ET, eta, phi, E);
  fastjet::PseudoJet pseudo_tower = fastjet::PseudoJet(p4);

  return pseudo_tower;
}

inline void tagging_algo(OxJet &calojet, std::vector<OxJet> &matched_trkjets,
                         TaggedJet tagged_fatjet) {

  ranges::sort(matched_trkjets, ranges::ordered_less{},
               [](auto &&jet) { return jet.p4.Pt(); });
  ranges::reverse(matched_trkjets);

  std::vector<OxJet> top_four;
  top_four.push_back(matched_trkjets[0]);
  top_four.push_back(matched_trkjets[1]);
  top_four.push_back(matched_trkjets[2]);
  top_four.push_back(matched_trkjets[3]);

  // Vector for switching different taggin for the calo jet
  // First entry : B Tagged
  // Second Entry : C Tagged
  // Third Entry : Light Tagged

  int btag = 0;

  for (auto &trk : top_four) {

    if (trk.tagged == true)
      btag++;
  }

  tagged_fatjet = make_tagged(calojet, top_four, btag);

  return;
}

inline void get_assoc_trkjets(Jet &calojet, ROOT::VecOps::RVec<Jet> trkjets,
                              TaggedJet &tagged_fatjet, bool debug = false) {

  // Initializing Pseudo Calo and Pseudo Trks
  fastjet::PseudoJet pseudo_calo;
  std::vector<fastjet::PseudoJet> pseudo_trkjets;

  // Generating pseudo_trksjets
  pseudo_trkjets = view::zip_with(make_pseudo, trkjets);
  std::cout << "Track Jets Imported" << std::endl;

  // vector to hold input clusters and ghosts
  std::vector<fastjet::PseudoJet> input_particles;
  input_particles.clear();
  std::cout << "Starting Importing Towers" << std::endl;
  // jet clusters from large-R jet
  std::vector<fastjet::PseudoJet> pseudo_calo_const;
  for (int j = 0; j < calojet.Constituents.GetEntriesFast(); ++j) {
    auto *tower = calojet.Constituents.At(j);
    if (tower == nullptr)
      continue;
    const Tower &local_tower = *dynamic_cast<Tower *>(tower);
    std::cout << "Static Cast done" << std::endl;
    fastjet::PseudoJet local_pseudo = make_tower(local_tower);
    pseudo_calo_const.push_back(local_pseudo); // Calorimeter Towers
  }
  std::cout << "Towers Imported" << std::endl;

  // if (debug) std::cout << "calo constituents size = " << constituents.size()
  // << std::endl;
  std::cout << "Starting Ghost Association" << std::endl;
  for (auto noghost : pseudo_calo_const) {

    noghost.reset_PtYPhiM(noghost.pt(), noghost.rapidity(), noghost.phi(), 0.0);
    if (noghost.E() < 0.)
      continue;

    // set user index for calo clusters to -1 to differentiate them from "track"
    // constituents
    // later
    noghost.set_user_index(-1);
    input_particles.push_back(noghost);
  }

  // if (debug)
  //  std::cout << "calo only input particles size = " << input_particles.size()
  //  << std::endl;

  // make ghost PseudoJets out of track jet direction
  for (unsigned int trackJetItr = 0; trackJetItr < pseudo_trkjets.size();
       ++trackJetItr) {

    fastjet::PseudoJet myghost = pseudo_trkjets.at(trackJetItr);
    // if( myghost.pt() <= 20.0 || fabs( myghost.rapidity() ) >= 2.5 ) continue;

    myghost.reset_PtYPhiM(1e-12, myghost.rapidity(), myghost.phi(), 0.0);
    if (myghost.E() < 0.)
      continue;

    myghost.set_user_index(trackJetItr);
    input_particles.push_back(myghost);
  }

  if (debug)
    std::cout << "calo+track jets input particles size = "
              << input_particles.size() << std::endl;

  // do ghost association and get list of pseudojet track jets that are
  // associated
  double Rparam = 1.0;
  fastjet::Strategy strategy = fastjet::Best; // according to atlas reco
  fastjet::RecombinationScheme recomb_scheme =
      fastjet::E_scheme; // according to atlas reco
  fastjet::JetDefinition jet_def(fastjet::antikt_algorithm, Rparam,
                                 recomb_scheme, strategy);

  // run the jet clustering with the above jet definition
  fastjet::ClusterSequence clust_seq(input_particles, jet_def);
  std::vector<fastjet::PseudoJet> sorted_jets =
      fastjet::sorted_by_pt(clust_seq.inclusive_jets());
  std::cout << "Clustering Done" << std::endl;
  if (debug)
    std::cout << "number of sorted jets = " << sorted_jets.size() << std::endl;
  std::cout << "Before NewJet" << std::endl;
  fastjet::PseudoJet newJet = sorted_jets.at(
      0); // there are more jets in the vector, but they all have pT ~0
  std::cout << "After NewJet" << std::endl;

  if (debug)
    std::cout << "new jet constituent size = " << newJet.constituents().size()
              << std::endl;

  std::cout << "Before NewJet Constituents" << std::endl;
  std::vector<fastjet::PseudoJet> newJet_constituents = newJet.constituents();
  std::cout << "After NewJet constituents" << std::endl;
  std::vector<fastjet::PseudoJet> matched_pseudo_trkjets;

  for (const auto &constit : newJet_constituents) {
    if (debug)
      std::cout << " user index = " << constit.user_index()
                << ", pt of constit = " << constit.pt() << std::endl;
    if (constit.user_index() >= 0) {
      int iter = constit.user_index();
      //    if(trkjets.at(iter).pt() > 20. && fabs(trkjets.at(iter).eta()) < 2.5
      //    )
      // matched_trkjets.push_back(trkjets.at(iter));
      matched_pseudo_trkjets.push_back(newJet_constituents.at(iter));
    }
  }

  // Sort matched jets by pt
  matched_pseudo_trkjets = sorted_by_pt(matched_pseudo_trkjets);

  // Undo PseudoJet
  std::vector<OxJet> out_matched =
      view::zip_with(undo_pseudo, matched_pseudo_trkjets);

  OxJet out_jet = make_jet(calojet);

  tagging_algo(out_jet, out_matched, tagged_fatjet);

  return;
}

struct reconstructed_event {
  bool valid;                ///< Is event valid
  int64_t ntag;              ///< Number of B-tagged jets
  int64_t njets;             ///< Total number of jets
  double wgt;                ///< Event Weight
  std::array<OxJet, 2> jets; ///< Array of 4 chosen jets

  higgs higgs1; ///< Leading Higgs
  higgs higgs2; ///< Subleading Higgs

  reconstructed_event()
      : valid(true), // set to true if pairing is valid
        jets(), higgs1(), higgs2() {}
};

struct out_format {
  double m_hh; ///< Di-Higgs mass (m<SUB>hh</SUB> or m<SUB>4j</SUB>)

  double m_h1;   ///< Leading Higgs mass
  double pT_h1;  ///< Leading Higgs p<SUB>T</SUB>
  double eta_h1; ///< Leading Higgs &eta;
  double phi_h1; ///< Leading Higgs &Phi;
  //
  double m_h2; ///< Subleading Higgs mass
  //               // double E_h2;   ///< Subleading Higgs energy
  double pT_h2;  ///< Subleading Higgs p<SUB>T</SUB>
  double eta_h2; ///< Subleading Higgs &eta;
  double phi_h2; ///< Subleading Higgs &Phi;
  //
  double m_h1_j1; ///< Leading Higgs leading jet mass
  //                            // double E_h1_j1;   ///< Leading Higgs leading
  //                            jet energy
  double pT_h1_j1;  ///< Leading Higgs leading jet p<SUB>T</SUB>
  double eta_h1_j1; ///< Leading Higgs leading jet &eta;
  double phi_h1_j1; ///< Leading Higgs leading jet &Phi;

  double m_h2_j2;   ///< Subleading Higgs subleading jet mass
  double pT_h2_j2;  ///< Subleading Higgs subleading jet p<SUB>T</SUB>
  double eta_h2_j2; ///< Subleading Higgs subleading jet &eta;
  double phi_h2_j2; ///< Subleading Higgs subleading jet &Phi;
};

struct reweight_format {

  double pT_4;   ///< p<SUB>T</SUB> of 4th jet
  double pT_2;   ///< p<SUB>T</SUB> of 2nd jet
  double eta_i;  ///< &sum;|&eta;<SUB>i</SUB>|
  double dRjj_1; ///< &Delta;R<SUB>jj,1</SUB>
  double dRjj_2; ///< &Delta;R<SUB>jj,2</SUB>
};

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
       &mc_sf_var](unsigned slot, const reconstructed_event &event
                   /*,double mc_sf*/) {
        auto &&tree = out_trees[slot];
        auto &&vars = out_vars[slot];
        auto &&rwgt = rwgt_vars[slot];

        ntag_var[slot] = event.ntag;
        njets_var[slot] = event.njets;
        mc_sf_var[slot] = event.wgt;

        vars->m_hh = (event.higgs1.p4 + event.higgs2.p4).M();

        vars->m_h1 = event.higgs1.p4.M();
        vars->pT_h1 = event.higgs1.p4.Pt();
        vars->eta_h1 = event.higgs1.p4.Eta();
        vars->phi_h1 = event.higgs1.p4.Phi();

        vars->m_h2 = event.higgs2.p4.M();
        vars->pT_h2 = event.higgs2.p4.Pt();
        vars->eta_h2 = event.higgs2.p4.Eta();
        vars->phi_h2 = event.higgs2.p4.Phi();

        vars->m_h1_j1 = event.jets[0].p4.M();
        vars->pT_h1_j1 = event.jets[0].p4.Pt();
        vars->eta_h1_j1 = event.jets[0].p4.Eta();
        vars->phi_h1_j1 = event.jets[0].p4.Phi();

        vars->m_h2_j2 = event.jets[1].p4.M();
        vars->pT_h2_j2 = event.jets[1].p4.Pt();
        vars->eta_h2_j2 = event.jets[1].p4.Eta();
        vars->phi_h2_j2 = event.jets[1].p4.Phi();

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
                                                 }) /4;



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
