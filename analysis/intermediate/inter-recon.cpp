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

//-----------------------------------------------
// Keep the preselection fairly loose
// This enables greater flexibility
//-----------------------------------------------
bool one_large_two_b_small_cuts(VecOps::RVec<Jet>& jets, VecOps::RVec<Jet>& fatjets ) {

    int count_small = 0; // Counting small-R jets
    int count_fat = 0; // Counting large-R jets

    // Loose filter small R jets
    for (auto&& j : jets) {
        if (j.PT >= 20.*GeV && std::abs(j.Eta) < 4.5 ) count_small++;
    }

    // Loose filter large R jet
    for (auto&& j : fatjets) {
        if (j.PT >= 100.*GeV &&  std::abs(j.Eta) < 2.5) count_fat++;
    }

    return count_small >= 2 && count_fat >= 1; 
}

//-----------------------------------------------
// Reconstruction routine
//-----------------------------------------------
reconstructed_event reconstruct(VecOps::RVec<Jet>& smalljet, // Delphes Jet 
                                VecOps::RVec<Jet>& largejet, // Delphes FatJet
                                VecOps::RVec<Jet>& trkjet,   // Delphes TrackJet
                                VecOps::RVec<HepMCEvent>& evt) {
    reconstructed_event result{};


    result.wgt = evt[0].Weight;


    // large R jets vector
    std::vector<OxJet> lj_vec =
          view::zip_with(make_jet, largejet) | view::filter([](const auto& jet) {
              return jet.p4.Pt() >= 100. * GeV and std::abs(jet.p4.Eta()) < 2.5;
          });
    
    // small R jets vector
    std::vector<OxJet> sj_vec =
          view::zip_with(make_jet, smalljet) | view::filter([](const auto& jet) {
              return jet.p4.Pt() >= 20. * GeV and std::abs(jet.p4.Eta()) < 4.5;
          });
    
    // track jets vector
    std::vector<OxJet> tj_vec =
          view::zip_with(make_jet, trkjet) | view::filter([](const auto& jet) {
              return jet.p4.Pt() >= 20. * GeV and std::abs(jet.p4.Eta()) < 2.5;
          });

    // Sort Large R jets by pT
    ranges::sort(lj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });

    // Sort small R jets by pT
    ranges::sort(sj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });
    
    // Sort track R jets by pT
    ranges::sort(tj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });

    // Decreasing Order
    ranges::reverse(lj_vec);
    ranges::reverse(sj_vec);
    ranges::reverse(tj_vec);

    const int n_large_tag = // Counting large R jets B tagged
          ranges::count(lj_vec, true, [](auto&& jet) { return jet.tagged; });
    
    const int n_track_tag = // Counting small R jets B tagged
          ranges::count(tj_vec, true, [](auto&& jet) { return jet.tagged; });

    // Assign the leading large R jet as the leading Higgs candidate
    OxJet large_jet = lj_vec[0];
 
    //---------------------------------------------------
    // Associate track jets with large R jet
    //---------------------------------------------------
   
    // A vector of jets associated with leading large R jet 
    std::vector<OxJet> h1_assoTrkJet;
    float max_dR_trackJet_largeJet = 0.8;
    
    for(auto tj : tj_vec){
      if ( tj.p4.DeltaR(large_jet.p4) <= max_dR_trackJet_largeJet){
        h1_assoTrkJet.push_back(tj);
      }
    }
    
    const int n_assoc_track_tag = // Counting track jets associated with large R jet that are B tagged
          ranges::count(h1_assoTrkJet, true, [](auto&& jet) { return jet.tagged; });

    //---------------------------------------------------
    // Assign small R jets to second Higgs candidate
    //---------------------------------------------------

    // If small R jets are less than 2-> Reject event
    if (sj_vec.size() < 2) {
        result.valid = false;
        return result;
    }

    //---------------------------------------------------
    // For all separated jets
    // Both small b-jets and non-b-jets
    // Cut on DeltaR<1.2 between small R jets and Large R jet
    //---------------------------------------------------
    
    // Put all small R jets separated from fat jet into jets_separated
    std::vector<OxJet> jets_separated;
    std::vector<OxJet> jets_notseparated;
    for (auto&& j : sj_vec) {
      if (deltaR(large_jet, j) > 1.2) jets_separated.push_back(j);
      else jets_notseparated.push_back(j);
      
    }
    
    if (jets_separated.size() < 2) {
        int available = jets_notseparated.size();
        int already_there = jets_separated.size();
        int to_push = 2 - already_there;
        if (to_push > available) {
            result.valid = false;
            return result;
        }
        for (int i = 0; i < to_push; i++) {
            jets_separated.push_back(jets_notseparated.at(i));
        }
    }
    
    const int n_separ_tag = // Counting small jets separated from large R jet that are B tagged
      ranges::count(jets_separated, true, [](auto&& jet) { return jet.tagged; });
    
    // Get the pairing that minimizes relative mass difference
    // Make pairs of small r jets

    JetPair bestPair;

    for(unsigned int i = 0; i < jets_separated.size(); i++){
      for(unsigned int j = i+1; j < jets_separated.size(); j++){
        if(i == 0 && j == 1){
          bestPair = make_pair(jets_separated.at(i), jets_separated.at(j));
          continue;
        }
        JetPair thisPair = make_pair(jets_separated.at(i), jets_separated.at(j));
        if(fabs(thisPair.p4().M() - large_jet.p4.M()) < fabs(bestPair.p4().M() - large_jet.p4.M())) bestPair = thisPair;
      }
    }

    // Storing the candidates
    result.higgs2.p4      = bestPair.jet_1.p4 + bestPair.jet_2.p4;
    result.higgs1.p4      = large_jet.p4;
    result.n_small_tag    = n_separ_tag;
    result.n_small_jets   = jets_separated.size();
    result.n_large_tag    = n_large_tag;
    result.n_large_jets   = lj_vec.size();
    result.n_track_tag    = n_track_tag;
    result.n_track_jets   = tj_vec.size();
    result.n_assoc_track_tag  = n_assoc_track_tag;
    result.n_assoc_track_jets = h1_assoTrkJet.size();
    
    result.large_jet      = large_jet;
    if ( h1_assoTrkJet.size() >= 1 ) { result.h1_assoTrkJet1.p4 = h1_assoTrkJet[0].p4; }
    if ( h1_assoTrkJet.size() >= 2 ) { result.h1_assoTrkJet2.p4 = h1_assoTrkJet[1].p4; }
 
    result.small_jets[0]  = bestPair.jet_1;
    result.small_jets[1]  = bestPair.jet_2;
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

    // Uncomment to enable multithreading
    //ROOT::EnableImplicitMT();

    //*******************
    // Importing Input File
    //*******************
    RDataFrame frame("Delphes", file_path);

    //******************
    // Run Intermediate Analysis
    //******************

    auto three_jets =
          frame.Filter(one_large_two_b_small_cuts, {"Jet", "FatJet"},
                       u8"Intermediate analysis cuts"); // Apply Intermediate Events Filter
    
    auto reconstructed =
          three_jets.Define("event", reconstruct, {"Jet", "FatJet", "TrackJet", "Event"}); // Reconstruct Events

    auto valid_evt =
          reconstructed.Filter(valid_check, {"event"}, "valid events"); // Filter only valid Events

    auto signal_result = valid_evt.Filter(signal, {"event"}, "signal"); // Filter Signal Events

    //********************
    // Writing Output Ntuple
    //*******************

    fmt::print("Writing to {}\n", output_path);

    TFile output_file(output_path.c_str(), "RECREATE");
    
    write_tree(signal_result, "signal", output_file);
    write_tree(valid_evt, "preselection", output_file);
    // write_tree(control_result, "control", output_file);
    // write_tree(sideband_result, "sideband", output_file);

    //*********************
    // Writing Cutflows
    //********************
    Cutflow intermediate_cutflow("Intermediate Cutflow", output_file);
    intermediate_cutflow.add(
          u8"(Preselection)  ≥ 2 small jets, ≥ 1 large jet",
          three_jets.Count());
    intermediate_cutflow.add(u8"Reconstructed events", reconstructed.Count());
    intermediate_cutflow.add(u8"(Valid) ≥ 2 small jets", valid_evt.Count());
    //intermediate_cutflow.add(u8"Signal", signal_result.Count());
    // intermediate_cutflow.add(u8"Control", control_result.Count());
    // intermediate_cutflow.add(u8"Sideband", sideband_result.Count());
    intermediate_cutflow.write();

    std::cout << "Finished processing events." << std::endl;
    return 0;
}
