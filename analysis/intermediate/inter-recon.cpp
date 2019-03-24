/* -------------------------------------------------------------

  Welcome to Pheno4b ntuple-making analysis code.

  Implemented resolved, intermediate, and boosted diHiggs4b analyses.

  Input Delphes files.
  Output trees of high level variables reconstructed Higgs candidates.

  This program is structured as follows:

  * dihiggs find_higgs_cands_resolved()
    0 large jets: resolved analysis to form Higgs candidates

  * dihiggs find_higgs_cands_inter_boost()
    1+ large jets: intermediate & boosted analysis to form Higgs candidates

  * reconstructed_event reconstruct()
    Main reconstruction routine
    - Collect, count and organise jets
    - Assigns jets to Higgs candidates
    - Store jets, Higgs candidates, electrons, muons, MET

  * int main()
    Main analysis code 
    - Manages files, calls the main reconstruction routine

  -------------------------------------------------------------
*/ 

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

//------------------------------------------------------------
// Resolved analysis jet assignment to Higgs (0 large jets)
// TODO: Add top veto, Dhh variables etc 
//------------------------------------------------------------
dihiggs find_higgs_cands_resolved(std::vector<OxJet> sj_vec) {
  
  dihiggs higgs_cands {};

  float lead_low = 0., lead_high = 0., sublead_low = 0., sublead_high = 0.;

  // Numbers from https://arxiv.org/abs/1804.06174 §5.1
  float m4j = (sj_vec[0].p4 + sj_vec[1].p4 + sj_vec[2].p4 + sj_vec[3].p4).M();
  if (m4j < 1250. * GeV) {
      lead_low     = 360. / (m4j / GeV) - 0.5   ;
      lead_high    = 653. / (m4j / GeV) + 0.475 ;
      sublead_low  = 235. / (m4j / GeV) ;
      sublead_high = 875. / (m4j / GeV) + 0.35  ;
  }
  else {
      lead_low     = sublead_low = 0.;
      lead_high    = 1.0;
      sublead_high = 1.0;
  }

  // All possible combinations of forming two pairs of jets
  const int pairings[3][2][2] = {{{0, 1}, {2, 3}}, {{0, 2}, {1, 3}}, {{0, 3}, {1, 2}}};

  std::vector<std::pair<higgs, higgs>> pair_candidates{};
  for (auto&& pairing : pairings) {
    // HiggsX_jetY
    int h1_j1 = pairing[0][0];
    int h1_j2 = pairing[0][1];
    int h2_j1 = pairing[1][0];
    int h2_j2 = pairing[1][1];

    auto h1 = sj_vec[h1_j1].p4 + sj_vec[h1_j2].p4;
    auto h2 = sj_vec[h2_j1].p4 + sj_vec[h2_j2].p4;

    std::vector<OxJet> h1_jets;
    std::vector<OxJet> h2_jets;
    h1_jets.push_back( sj_vec[h1_j1] );
    h1_jets.push_back( sj_vec[h1_j2] );
    h2_jets.push_back( sj_vec[h2_j1] );
    h2_jets.push_back( sj_vec[h2_j2] );
    
    float deltaRjj_lead    = sj_vec[h1_j1].p4.DeltaR( sj_vec[h1_j2].p4 );
    float deltaRjj_sublead = sj_vec[h2_j1].p4.DeltaR( sj_vec[h2_j2].p4 );
    // if (higgs1.Pt() < higgs2.Pt()) { // NOT A BUG
    if ((sj_vec[h1_j1].p4.Pt() + sj_vec[h1_j2].p4.Pt())
        < (sj_vec[h2_j1].p4.Pt() + sj_vec[h2_j2].p4.Pt())) {
        // swap so higgs1 is the leading Higgs candidate
        std::swap(h1, h2);
        std::swap(deltaRjj_lead, deltaRjj_sublead);
        std::swap(h1_j1, h2_j1);
        std::swap(h1_j2, h2_j2);
    }

    if (!(lead_low <= deltaRjj_lead && lead_high >= deltaRjj_lead &&
          sublead_low <= deltaRjj_sublead && sublead_high >= deltaRjj_sublead)) {
        continue;
    }
   
    pair_candidates.push_back( std::make_pair(higgs(h1, h1_j1, h1_j2, h1_jets), higgs(h2, h2_j1, h2_j2, h2_jets)) );
  }

  // Choose pairing that minimises mass difference between 2 Higgs candidates
  if (pair_candidates.size() > 0 ) {
    auto elem = ranges::min_element(pair_candidates, ranges::ordered_less{}, [](auto&& cand) {
      const auto& higgs1 = cand.first;
      const auto& higgs2 = cand.second;
      float Ddijet = std::abs(higgs1.p4.M() - higgs2.p4.M());
      return Ddijet;
    });

    // Assign Higgs candidates
    higgs_cands.higgs1 = elem->first;
    higgs_cands.higgs2 = elem->second;
  }

  return higgs_cands;
} // end resolved

//--------------------------------------------------------------
// Intermediate & boosted analysis jet assignment to Higgs
// i.e. events where there are 1+ large jets 
//--------------------------------------------------------------
dihiggs find_higgs_cands_inter_boost(
                     std::vector<OxJet> lj_vec, 
                     std::vector<OxJet> sj_vec, 
                     std::vector<OxJet> tj_vec) {
  
  dihiggs higgs_cands {};
  
  //---------------------------------------------------
  // Associate track jets with large R jet
  //---------------------------------------------------
 
  // Association distance measure
  float max_dR = 1.0;
  
  for(auto tj : tj_vec){
    // Case 1 large jet
    if ( lj_vec.size() >= 1 && tj.p4.DeltaR( lj_vec[0].p4 ) < max_dR ){
      higgs_cands.higgs1.jets.push_back(tj);
    }
    // Case 2 large jets
    if ( lj_vec.size() >= 2 && tj.p4.DeltaR( lj_vec[1].p4 ) < max_dR ){
      higgs_cands.higgs2.jets.push_back(tj);
    }
  }
  
  //---------------------------------------------------
  // Assign large jets to Higgs candidates
  //---------------------------------------------------

  // Case 1+ large jets, assign leading large jet is leading Higgs candidate
  if ( lj_vec.size() >= 1 ) higgs_cands.higgs1.p4 = lj_vec[0].p4;

  // Case 2+ large jets, subleading large jet is subleading Higgs candidate
  if ( lj_vec.size() >= 2 ) { 
    higgs_cands.higgs2.p4 = lj_vec[1].p4;
    return higgs_cands; // end here as boosted analysis implied
  }

  //---------------------------------------------------
  // Assign small jets to subleading Higgs candidate 
  //---------------------------------------------------
  
  // Put all small R jets separated from fat jet into jets_separated
  std::vector<OxJet> jets_separated;
  for (auto&& j : sj_vec) {
    if (deltaR(lj_vec[0], j) > 1.2) jets_separated.push_back(j);
  }
  
  // Get the pairing minimising mass difference between separated jets and large jet
  JetPair bestPair;
  for(unsigned int i = 0; i < jets_separated.size(); i++){
    for(unsigned int j = i+1; j < jets_separated.size(); j++){
      if(i == 0 && j == 1){
        bestPair = make_pair(jets_separated.at(i), jets_separated.at(j));
        continue;
      }
      JetPair thisPair = make_pair(jets_separated.at(i), jets_separated.at(j));
      if(fabs(thisPair.p4().M() - lj_vec[0].p4.M()) < fabs(bestPair.p4().M() - lj_vec[0].p4.M())) bestPair = thisPair;
    }
  }
 
  higgs_cands.higgs2.p4 = bestPair.jet_1.p4 + bestPair.jet_2.p4;

  // Order jets in bestPair by pT 
  if ( bestPair.jet_2.p4.Pt() > bestPair.jet_1.p4.Pt() ) {
    higgs_cands.higgs2.jets.push_back( bestPair.jet_2 );
    higgs_cands.higgs2.jets.push_back( bestPair.jet_1 );
  }
  else {
    higgs_cands.higgs2.jets.push_back( bestPair.jet_1 );
    higgs_cands.higgs2.jets.push_back( bestPair.jet_2 );
  }
  return higgs_cands;
} // end intermediate & boosted 

//-----------------------------------------------
// Main reconstruction routine
//-----------------------------------------------
reconstructed_event reconstruct(VecOps::RVec<Jet>&        smalljet, // Jet 
                                VecOps::RVec<Jet>&        largejet, // FatJet
                                VecOps::RVec<Jet>&        trkjet,   // TrackJet
                                VecOps::RVec<HepMCEvent>& evt,      // Event
                                VecOps::RVec<Electron>&   electron, // Electrons
                                VecOps::RVec<Muon>&       muon,     // Muons
                                VecOps::RVec<MissingET>&  met,      // MissingET 
                                int &NTotEvt  )  // Total events before cuts
                                {
  

  reconstructed_event result{};
  dihiggs higgs_cands{};

  std::cout << "NTotEvents: " << NTotEvt << std::endl;

  result.wgt = evt[0].Weight;

  //----------------------------------------------------
  // Collect, count and organise jets
  //----------------------------------------------------
 
  // large jets vector
  std::vector<OxJet> lj_vec =
        view::zip_with(make_jet, largejet) | view::filter([](const auto& jet) {
            return jet.p4.Pt() >= 250. * GeV and std::abs(jet.p4.Eta()) < 2.0;
        });
  
  // small jets vector
  std::vector<OxJet> sj_vec =
        view::zip_with(make_jet, smalljet) | view::filter([](const auto& jet) {
            return jet.p4.Pt() >= 40. * GeV and std::abs(jet.p4.Eta()) < 2.5;
        });
  
  // track jets vector
  std::vector<OxJet> tj_vec =
        view::zip_with(make_jet, trkjet) | view::filter([](const auto& jet) {
            return jet.p4.Pt() >= 20. * GeV and std::abs(jet.p4.Eta()) < 2.5;
        });

  // Sort jets by pT
  ranges::sort(lj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });
  ranges::sort(sj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });
  ranges::sort(tj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });

  // Decreasing order
  ranges::reverse(lj_vec);
  ranges::reverse(sj_vec);
  ranges::reverse(tj_vec);

  // Counting jets that are b-tagged
  const int n_large_tag = 
        ranges::count(lj_vec, true, [](auto&& jet) { return jet.tagged; });
  
  const int n_small_tag = 
        ranges::count(sj_vec, true, [](auto&& jet) { return jet.tagged; });
  
  const int n_track_tag = 
        ranges::count(tj_vec, true, [](auto&& jet) { return jet.tagged; });
  
  //---------------------------------------------------
  // Assign jets to Higgs candidates
  //---------------------------------------------------

  // Resolved: exactly 0 large jets
  if ( lj_vec.size() == 0 && sj_vec.size() >= 4 ) { 
    higgs_cands = find_higgs_cands_resolved(sj_vec);
  }

  // Intermediate: exactly 1 large jet
  else if ( lj_vec.size() == 1 && sj_vec.size() >= 2 ) { 
    higgs_cands = find_higgs_cands_inter_boost(lj_vec, tj_vec, sj_vec);
  }

  // Boosted: 2 or more large jets
  else if ( lj_vec.size() >= 2 ) { 
    higgs_cands = find_higgs_cands_inter_boost(lj_vec, tj_vec, sj_vec);
  }

  else { result.valid = false; }
  
  // Count b-tagged jets associated to higgs candidates
  const int n_bjets_in_higgs1 = 
        ranges::count(higgs_cands.higgs1.jets, true, [](auto&& jet) { return jet.tagged; });
  
  const int n_bjets_in_higgs2 = 
        ranges::count(higgs_cands.higgs2.jets, true, [](auto&& jet) { return jet.tagged; });

  //----------------------------------------------------
  // Store jets, Higgs candidates, electrons, muons, MET
  //----------------------------------------------------
  
  result.n_small_tag    = n_small_tag;
  result.n_small_jets   = sj_vec.size();
  result.n_large_tag    = n_large_tag;
  result.n_large_jets   = lj_vec.size();
  result.n_track_tag    = n_track_tag;
  result.n_track_jets   = tj_vec.size();

  result.n_jets_in_higgs1  = higgs_cands.higgs1.jets.size();
  result.n_jets_in_higgs2  = higgs_cands.higgs2.jets.size();
  result.n_bjets_in_higgs1 = n_bjets_in_higgs1;
  result.n_bjets_in_higgs2 = n_bjets_in_higgs2;
  
  result.nElec = electron.size();
  result.nMuon = muon.size();

  result.higgs1 = higgs_cands.higgs1;
  result.higgs2 = higgs_cands.higgs2;
  
  // Store leading leptons 
  electron.size() > 0
           ? result.elec1.SetPtEtaPhiM( electron[0].PT, electron[0].Eta, electron[0].Phi, 0.000511 )
           : result.elec1.SetPtEtaPhiM( -1., -9., -9., -1. );
  muon.size() > 0
           ? result.muon1.SetPtEtaPhiM(muon[0].PT, muon[0].Eta, muon[0].Phi, 0.106) 
           : result.muon1.SetPtEtaPhiM(-1., -9., -9., -1.);
  
  // Store missing transverse momentum
  result.met.SetPtEtaPhiE( met[0].MET, met[0].Eta, met[0].Phi, met[0].MET );

  return result;
}

// Select Only Valid Events
bool valid_check(const reconstructed_event& evt) { return evt.valid; }

//-----------------------------------------------
// Main Analysis Code
//-----------------------------------------------
int main(int argc, char* argv[]) {

  if(argc < 4){
    fprintf(stderr, "Not enough arguments provided! Need input filepath, output dir, and output filename.\n");
    return 1;
  }

  std::ios::sync_with_stdio(false);

  const std::string file_path       = argv[1];
  const std::string output_dir      = argv[2];
  const std::string output_filename = argv[3];
  const std::string output_path     = output_dir + "/" + output_filename;

  // Uncomment to enable multithreading
  //ROOT::EnableImplicitMT();

  // Importing Input File
  RDataFrame frame("Delphes", file_path);

  // Run Intermediate Analysis
  auto reco = frame.Define("event", reconstruct,
              {"Jet", "FatJet", "TrackJet", "Event", "Electron", "Muon", "MissingET"}); 

  // Filter only valid Events
  auto valid_evt = reco.Filter(valid_check, {"event"}, "valid events");

  // Writing output ntuple
  fmt::print("Writing to {}\n", output_path);

  TFile output_file(output_path.c_str(), "RECREATE"); 
  write_tree(valid_evt, "preselection", output_file );

  // Write cutflow
  Cutflow loose_cutflow("loose_cutflow", output_file);
  loose_cutflow.add(u8"All", frame.Count());
  loose_cutflow.add(u8"Preselection", valid_evt.Count());
  loose_cutflow.write();

  std::cout << "Finished processing events." << std::endl;
  return 0;
}
