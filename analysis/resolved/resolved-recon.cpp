// \file resolved-recon.cpp
// \brief Main implementation file

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

#include <fmt/format.h>
#include <range/v3/all.hpp>

#include <ROOT/RDataFrame.hxx>
#include <ROOT/RVec.hxx>
#include <TH1I.h>
#include <TROOT.h>
#include <TTree.h>

#include "classes/DelphesClasses.h"
#include "classes/DelphesFactory.h"
#include "modules/Delphes.h"

#include "Cutflow.h"
#include "utils.h"

// From ATLAS code double f = 0.16;

using namespace ROOT;
namespace view = ranges::view;
namespace action = ranges::action;

constexpr double GeV = 1.; ///< Set to 1 -- energies and momenta in GeV

// Reconstruct event in the resolved regime
reconstructed_event reconstruct(VecOps::RVec<Jet> &jet,
                                VecOps::RVec<HepMCEvent> &evt) {
  reconstructed_event result{};

  result.wgt = evt[0].Weight;

  // Moving jet from Jet type to OxJet type
  // Selection for resolved regime

  std::vector<OxJet> all_jets =
      view::zip_with(make_jet, jet) | view::filter([](const auto &jet) {
        return jet.p4.Pt() >= 40. * GeV and std::abs(jet.p4.Eta()) < 2.5;
      });

  // Sorting Jets by pT
  ranges::sort(all_jets, ranges::ordered_less{},
               [](auto &&jet) { return jet.p4.Pt(); }); // sorting for pT

  // Decreasing order in pT
  ranges::reverse(all_jets);

  // Count number of btag small R jets
  const int ntag =
      ranges::count(all_jets, true, [](auto &&jet) { return jet.tagged; });

  // split tagged jets and others
  std::vector<OxJet> jets =
      all_jets | view::filter([](auto &&jet) { return jet.tagged; });
  std::vector<OxJet> other_jets =
      all_jets | view::filter([](auto &&jet) { return !jet.tagged; });

  other_jets |= (action::sort(ranges::ordered_less{},
                              [](auto &&jet) { return jet.p4.Pt(); }) |
                 action::reverse);

  if (ntag < 4) {
    //        // need to choose "pseudo-tagged" jets so we have four total
    int n_jets_to_choose = 4 - ntag;
    int n_other_jets = all_jets.size() - ntag;
    if (n_other_jets < n_jets_to_choose) {
      fmt::print(stderr,
                 "We need {} jets, but only have {} to pick from. How?\n",
                 n_jets_to_choose, n_other_jets);
      result.valid = false;
      return result;
    }
    if (other_jets.size() < 4) {
      result.valid = false;
    }

    // Add pseudo_jets
    ranges::copy(other_jets | view::take(n_jets_to_choose),
                 ranges::back_inserter(jets));
  }

  if (jets.size() > 4) {
    jets |= (action::sort(ranges::ordered_less{},
                          [](auto &&jet) { return jet.p4.Pt(); }) |
             action::reverse | action::take(4));
  }

  // All possible combinations of forming two pairs of jets

  const int pairings[3][2][2] = {
      {{0, 1}, {2, 3}}, {{0, 2}, {1, 3}}, {{0, 3}, {1, 2}}};

  std::vector<std::pair<higgs, higgs>> pair_candidates{};
  for (auto &&pairing : pairings) {
    int higgs1_1 = pairing[0][0];
    int higgs1_2 = pairing[0][1];
    int higgs2_1 = pairing[1][0];
    int higgs2_2 = pairing[1][1];

    auto higgs1 = jets[higgs1_1].p4 + jets[higgs1_2].p4;
    auto higgs2 = jets[higgs2_1].p4 + jets[higgs2_2].p4;

    double deltaRjj_lead = jets[higgs1_1].p4.DeltaR(jets[higgs1_2].p4);
    double deltaRjj_sublead = jets[higgs2_1].p4.DeltaR(jets[higgs2_2].p4);
    // if (higgs1.Pt() < higgs2.Pt()) {
    // NOT A BUG
    if ((jets[higgs1_1].p4.Pt() + jets[higgs1_2].p4.Pt()) <
        (jets[higgs2_1].p4.Pt() + jets[higgs2_2].p4.Pt())) {
      // swap so higgs1 is the leading Higgs candidate
      std::swap(higgs1, higgs2);
      std::swap(deltaRjj_lead, deltaRjj_sublead);
      std::swap(higgs1_1, higgs2_1);
      std::swap(higgs1_2, higgs2_2);
    }

    pair_candidates.push_back(std::make_pair(higgs(higgs1, higgs1_1, higgs1_2), higgs(higgs2, higgs2_1, higgs2_2)));
        higgs(higgs1, higgs1_1, higgs1_2), higgs(higgs2, higgs2_1, higgs2_2)));
  }

  if (pair_candidates.empty()) {
    // leave result invalid
    result.valid = false;
    result.ntag = ntag; // For ntag cut
  } else {
    // more than one candidate pair -- determine which to use
    // if there is only one candidate, this won't hurt anything
    auto elem = ranges::min_element(
        pair_candidates, ranges::ordered_less{}, [](auto &&cand) {
          const auto &higgs1 = cand.first;
          const auto &higgs2 = cand.second;

          double Ddijet = std::abs(higgs1.p4.M() - higgs2.p4.M());
          return Ddijet;
        });

    // build result
    ranges::copy(jets, result.jets.begin());
    result.higgs1 = elem->first;
    result.higgs2 = elem->second;
    result.ntag = ntag;
    result.njets = all_jets.size();
    result.valid = true;
  }

  return result;
}

//******************
// Selection functions
//********************

// Require four jets with p<SUB>T</SUB> > 40 GeV, |&eta;| < 2.5 with at least 2
// being b-tagged.
bool four_b_jets_pT_40_eta_25(VecOps::RVec<Jet> &jets) {
  // Filter jets with 4 pT > 40 GeV, |eta| < 2.5 jets with >= 2 b tagged]
  int count = 0;
  int b_count = 0;

  for (auto &&j : jets) {
    if (j.PT >= 40. * GeV and std::abs(j.Eta) < 2.5) {
      count++;
      if (j.BTag)
        b_count++;
    }

    if (count >= 4 and b_count >= 2)
      return true; // we want to keep the 2 tag events too
  }

  return false;
}

// Checkpoint requiring event be marked as valid by reconstruct().
bool valid_check(const reconstructed_event &evt) { return evt.valid; }

// Select m<SUB>hh</SUB> signal region
bool signal(const reconstructed_event &evt) {
  double m_h1 = evt.higgs1.p4.M();
  double m_h2 = evt.higgs2.p4.M();
  // Cut in a mass window of 80 GeV around 125 GeV for both Higgs
  bool higgs1_flag = (std::abs(evt.higgs1.p4.M() - 125.) < 40.) ? true : false;
  bool higgs2_flag = (std::abs(evt.higgs2.p4.M() - 125.) < 40.) ? true : false;
  return (higgs1_flag && higgs2_flag);
}

// Select m<SUB>hh</SUB> sideband region
bool sideband(const reconstructed_event &evt) {
  double m_h1 = evt.higgs1.p4.M();
  double m_h2 = evt.higgs2.p4.M();
  // Cut in a mass window of 80 GeV around 125 GeV for both Higgs
  bool higgs1_flag = (std::abs(evt.higgs1.p4.M() - 125.) < 50.) ? true : false;
  bool higgs2_flag = (std::abs(evt.higgs2.p4.M() - 125.) < 50.) ? true : false;
  return (higgs1_flag && higgs2_flag);
}

// Select m<SUB>hh</SUB> control region
bool control(const reconstructed_event &evt) {
  double m_h1 = evt.higgs1.p4.M();
  double m_h2 = evt.higgs2.p4.M();
  // Cut in a mass window of 80 GeV around 125 GeV for both Higgs
  bool higgs1_flag = (std::abs(evt.higgs1.p4.M() - 125.) < 45.) ? true : false;
  bool higgs2_flag = (std::abs(evt.higgs2.p4.M() - 125.) < 45.) ? true : false;
  return (higgs1_flag && higgs2_flag);
}

//***************
// Main Analysis Code
//**************

int main(int argc, char *argv[]) {
  // Use iostreams for input only and fmt::print for output only, so fine
  std::ios::sync_with_stdio(false); // Needed for fast iostreams
  using vec_string = std::vector<std::string>;

  const std::string file_path = argv[1];
  const std::string output_dir = argv[2];
  const std::string output_filename = argv[3];
  const std::string output_path = output_dir + "/" + output_filename;

  ROOT::EnableImplicitMT();

  //*******************
  // Importing Input File
  //*******************

  RDataFrame frame("Delphes", file_path);

  //****************************
  // Run Resolved Analysis Code
  //***************************

  auto four_jets =
      frame.Filter(four_b_jets_pT_40_eta_25, {"Jet"},
                   u8"4 good jets(pT ≥ 40 GeV, η ≤ 2.5), ≥ 4 tagged");

  auto reconstructed = four_jets.Define("event", reconstruct, {"Jet", "Event"});

  auto valid_evt = reconstructed.Filter(valid_check, {"event"}, u8"ΔR_jj");

  auto signal_result = valid_evt.Filter(signal, {"event"}, "signal");

  auto control_result = valid_evt.Filter(
      [](const reconstructed_event &event) {
        return control(event) && (!signal(event));
      },
      {"event"}, "control");

  auto sideband_result = valid_evt.Filter(
      [](const reconstructed_event &event) {
        return sideband(event) && !control(event);
      },
      {"event"}, "sideband");

  //**************************
  // Writing Output Ntuples
  //*************************

  fmt::print("Writing to {}\n", output_path);
  // To print progress
  auto start_events_proxy = frame.Count();
  start_events_proxy.OnPartialResult(
      1000, [](const unsigned long long &num_events) {
        fmt::print("Processed {} events\n", num_events);
      });

  TFile output_file(output_path.c_str(), "RECREATE");
  write_tree(signal_result, "signal", output_file);

  start_events_proxy.GetValue(); // For printing progress

  write_tree(control_result, "control", output_file);
  write_tree(sideband_result, "sideband", output_file);

  //*********************
  // Writing Cutflows
  // ********************

  auto two_tag_filter = [](const reconstructed_event &evt) {
    return evt.ntag == 2;
  };
  auto four_tag_filter = [](const reconstructed_event &evt) {
    return evt.ntag >= 4;
  };

  Cutflow two_tag_cutflow("TwoTagCutflow", output_file);
  two_tag_cutflow.add(u8"4 good jets(pT ≥ 40 GeV, η ≤ 2.5), ≥ 2 tagged",
                      four_jets.Count());
  two_tag_cutflow.add(u8"Two Tagged",
                      reconstructed.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.add(u8"ΔR_jj",
                      valid_evt.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.add(u8"Signal",
                      signal_result.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.add(u8"Control",
                      control_result.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.add(
      u8"Sideband", sideband_result.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.write();

  Cutflow four_tag_cutflow("FourTagCutflow", output_file);
  four_tag_cutflow.add(u8"4 good jets(pT ≥ 40 GeV, η ≤ 2.5), ≥ 4 tagged",
                       four_jets.Count());
  four_tag_cutflow.add(
      u8"Four Tagged",
      reconstructed.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.add(u8"ΔR_jj",
                       valid_evt.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.add(
      u8"Signal", signal_result.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.add(
      u8"Control", control_result.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.add(
      u8"Sideband", sideband_result.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.write();

  return 0;
}
