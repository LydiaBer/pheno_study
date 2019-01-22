// Reconstruction of Intermediate Events

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

#include <TH1I.h>
#include <TROOT.h>
#include <TTree.h>
#include <TMath.h>
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RVec.hxx>

#include "classes/DelphesClasses.h"
#include "classes/DelphesFactory.h"
#include "modules/Delphes.h"

#include "Cutflow.h"
#include "utils.h"

using namespace ROOT;
namespace view = ranges::view;
namespace action = ranges::action;

constexpr double GeV = 1.; ///< Set to 1 -- energies and momenta in GeV

bool one_b_large_two_b_small_cuts(VecOps::RVec<Jet>& jets, VecOps::RVec<Jet>& fatjets) {

    int b_count_small = 0; // Counting b tagged small-R jets
    int b_count_fat = 0; // Counting b tagged large-R jets

    // Filter small R jets with 2 pT>40 and |eta|< 2.5 & btagged
    for (auto&& j : jets) {
        if (j.PT >= 40.*GeV && fabs(j.Eta) < 2.5 && j.BTag) b_count_small++;
    }

    // Filter large R jet 1 pT>200 and |eta|<2. & btagged
    for (auto&& j : fatjets) {
        if (j.PT >= 200.*GeV && fabs(j.Eta) < 2.0 && j.BTag) b_count_fat++;
    }

    return b_count_small >= 2 && b_count_fat == 1;
}

reconstructed_event reconstruct(VecOps::RVec<Jet>& smalljet, VecOps::RVec<Jet>& largejet,
                                VecOps::RVec<HepMCEvent>& evt) {
    reconstructed_event result{};

    result.wgt = evt[0].Weight;

    // large R jets vector
    std::vector<OxJet> lj_vec =
          view::zip_with(make_jet, largejet) | view::filter([](const auto& jet) {
              return jet.p4.Pt() >= 200. * GeV and std::abs(jet.p4.Eta()) < 2.0;
          });

    // small R jets vector
    std::vector<OxJet> sj_vec =
          view::zip_with(make_jet, smalljet) | view::filter([](const auto& jet) {
              return jet.p4.Pt() >= 40. * GeV and std::abs(jet.p4.Eta()) < 2.5;
          });

    // Sort Large R jets by pT
    ranges::sort(lj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });

    // Sort small R jets by pT
    ranges::sort(sj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });

    // Decreasing Order
    ranges::reverse(lj_vec);
    ranges::reverse(sj_vec);

    const int n_small_tag = // Counting small R jets B tagged
          ranges::count(sj_vec, true, [](auto&& jet) { return jet.tagged; });

    const int n_large_tag = // Counting large R jets B tagged
          ranges::count(lj_vec, true, [](auto&& jet) { return jet.tagged; });

    OxJet large_jet = lj_vec[0];

    // Separating B Tagged small r jets from non-B Tagged
    std::vector<OxJet> small_jets = sj_vec | view::filter([](auto&& jet) { return jet.tagged; });

    std::vector<OxJet> other_jets = sj_vec | view::filter([](auto& jet) { return !jet.tagged; });

    // There could be only one non btag jet. Maybe change it because not strictly
    // necessary
    /*if (n_small_tag< 2) {
    int n_jets_to_choose = 2-n_small_tag;
    int n_other_jets = sj_vec.size() - n_small_tag;
    if (n_other_jets < n_jets_to_choose){
    fmt::print(stderr,
            "We need {} jets; but only have {} to pick from. How? \n",
            n_jets_to_choose, n_other_jets);
    result.valid=false;
    return result;
    }
    if(n_other_jets < 1){
    result.valid=false;
    }

    ranges::copy(other_jets | view::take(n_jets_to_choose),
            ranges::back_inserter(small_jets));
    }

    */

    // If small R jets tagged are less than 2-> Reject event

    if (n_small_tag < 2) {
        result.valid = false;
        return result;
    }

    // Cut on DeltaR<1.2 between small R jets and Large R jet

    std::vector<OxJet> bjets_separated;
    std::vector<OxJet> bjets_notseparated;
    for (auto&& j : small_jets) {
        if (deltaR(large_jet, j) > 1.2) bjets_separated.push_back(j);
        else bjets_notseparated.push_back(j);
    }

    if (bjets_separated.size() < 2) {
        int available = bjets_notseparated.size();
        int already_there = bjets_separated.size();
        int to_push = 2 - already_there;
        if (to_push > available) {
            result.valid = false;
            return result;
        }
        for (int i = 0; i < to_push; i++) {
            bjets_separated.push_back(bjets_notseparated.at(i));
        }
    }

    // Get the pairing that minimizes relative mass difference
    // Make pairs of small r jets

    JetPair bestPair;

    for(unsigned int i = 0; i < bjets_separated.size(); i++){
      for(unsigned int j = i+1; j < bjets_separated.size(); j++){
        if(i == 0 && j == 1){
          bestPair = make_pair(bjets_separated.at(i), bjets_separated.at(j));
          continue;
        }
        JetPair thisPair = make_pair(bjets_separated.at(i), bjets_separated.at(j));
        if(fabs(thisPair.p4().M() - large_jet.p4.M()) < fabs(bestPair.p4().M() - large_jet.p4.M())) bestPair = thisPair;
      }
    }

    // Storing the candidates

    result.higgs2.p4 = bestPair.jet_1.p4 + bestPair.jet_2.p4;
    result.higgs1.p4 = large_jet.p4;
    result.n_small_tag = n_small_tag;
    result.n_small_jets = sj_vec.size();
    result.n_large_tag = n_large_tag;
    result.n_large_jets = lj_vec.size();
    result.large_jet = large_jet;
    result.small_jets[0] = bestPair.jet_1;
    result.small_jets[1] = bestPair.jet_2;

    // If leading is subleading and viceversa then exchange
    if (result.small_jets[1].p4.Pt() > result.small_jets[0].p4.Pt()) {
        result.small_jets[0] = bestPair.jet_2;
        result.small_jets[1] = bestPair.jet_1;
    }

    return result;
}

// Select Only Valid Events

bool valid_check(const reconstructed_event& evt) { return evt.valid; }

bool signal(const reconstructed_event& evt) {
    // Cut in a mass window of 80 GeV around 125 GeV for both Higgs
    bool higgs1_flag = (std::abs(evt.higgs1.p4.M() - 125.) < 40.);
    bool higgs2_flag = (std::abs(evt.higgs2.p4.M() - 125.) < 40.);
    return (higgs1_flag && higgs2_flag);
}

bool control(const reconstructed_event& evt) {
    // Cut in a mass window of 90 GeV around 125 GeV for both Higgs
    bool higgs1_flag = (std::abs(evt.higgs1.p4.M() - 125.) < 45.);
    bool higgs2_flag = (std::abs(evt.higgs2.p4.M() - 125.) < 45.);
    return (higgs1_flag && higgs2_flag);
}

bool sideband(const reconstructed_event& evt) {
    // Cut in a mass window of 100 GeV around 125 GeV for both Higgs
    bool higgs1_flag = (std::abs(evt.higgs1.p4.M() - 125.) < 50.);
    bool higgs2_flag = (std::abs(evt.higgs2.p4.M() - 125.) < 50.);
    return (higgs1_flag && higgs2_flag);
}

//***************
// Main Analysis Code
//***************

int main(int argc, char* argv[]) {

    if(argc < 4){
      fprintf(stderr, "Not enough arguments provided! Need input filepath, output dir, and output filename.\n");
      return 1;
    }

    std::ios::sync_with_stdio(false);

    const std::string file_path = argv[1];
    const std::string output_dir = argv[2];
    const std::string output_filename = argv[3];
    const std::string output_path = output_dir + "/" + output_filename;

    // ROOT::EnableImplicitMT();

    //*******************
    // Importing Input File
    //*******************

    RDataFrame frame("Delphes", file_path);

    //******************
    // Run Intermediate Analysis
    //******************

    auto three_jets =
          frame.Filter(one_b_large_two_b_small_cuts, {"Jet", "FatJet"},
                       u8"Intermediate analysis cuts"); // Apply Intermediate Events Filter

    auto reconstructed =
          three_jets.Define("event", reconstruct, {"Jet", "FatJet", "Event"}); // Reconstruct Events

    auto valid_evt =
          reconstructed.Filter(valid_check, {"event"}, "valid events"); // Filter only valid Events

    auto signal_result = valid_evt.Filter(signal, {"event"}, "signal"); // Filter Signal Events
                                                                        /*
                                                                          auto control_result = valid_evt.Filter(  // Filter Events in the Control
                                                                          Region
                                                                              [](const reconstructed_event &event) {
                                                                                return control(event) && (!signal(event));
                                                                              },
                                                                              {"event"}, "control");
                                                                    
                                                                          auto sideband_result = valid_evt.Filter(  // Filter Events in the Control
                                                                          Region
                                                                              [](const reconstructed_event &event) {
                                                                                return sideband(event) && !control(event);
                                                                              },
                                                                              {"event"}, "sideband");
                                                                          */

    //********************
    // Writing Output Ntuple
    //*******************

    fmt::print("Writing to {}\n", output_path);

    TFile output_file(output_path.c_str(), "RECREATE");

    write_tree(signal_result, "signal", output_file);
    write_tree(valid_evt, "pre-selection", output_file);
    // write_tree(control_result, "control", output_file);
    // write_tree(sideband_result, "sideband", output_file);

    //*********************
    // Writing Cutflows
    //********************
    Cutflow intermediate_cutflow("Intermediate Cutflow", output_file);
    intermediate_cutflow.add(
          u8"2 small good jets(pT ≥ 40 GeV, η ≤ 2.5), ≥ 2 tagged, 1 large good jet",
          three_jets.Count());
    intermediate_cutflow.add(u8"Reconstructed events", reconstructed.Count());
    intermediate_cutflow.add(u8"(Valid) 1 large jet  and 2 small jets Tagged", valid_evt.Count());
    intermediate_cutflow.add(u8"Signal", signal_result.Count());
    // intermediate_cutflow.add(u8"Control", control_result.Count());
    // intermediate_cutflow.add(u8"Sideband", sideband_result.Count());
    intermediate_cutflow.write();

    return 0;
}
