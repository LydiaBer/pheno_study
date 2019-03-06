/*! Boosted Analysis */
/*!
 *Two FatJets with pt>200GeV and |eta|< 2.0
 *From the two FatJets we reconstruct the Higgs
 *which must fall in |m_h-125|< 40.
 */
#include <fstream>
#include <iostream>

#include <TH1I.h>
#include <TROOT.h>
#include <TTree.h>
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
double leadPtCut = 450.0;
double sublPtCut = 250.0;
double xhhcut = 1.6;

bool two_large_b_jets(VecOps::RVec<Jet>& jets /*!Input Jets of FastJet <Jet> type*/) {
    /**
     *Filter for events which
     *respect Boosted Category
     *Requirements
     *If events is boosted return true
     *and it passes the selection
     */
    bool leading_found = false;   // Counting Number of Boosted Events
    bool subleading_found = false;   // Counting Number of Boosted Events
    int b_count = 0; // Counting Number of Boosted B-tagged Events

    for (auto&& j : jets) {
        //if (j.PT >= 200. * GeV and std::abs(j.Eta) < 2.0) {
        if ((j.PT >= 420. * GeV)and(!leading_found)) {
            leading_found = true;
        }
        else if ((j.PT >= 250. * GeV)and(!subleading_found)) {
            subleading_found = true;
        }
        //if (count >= 2 and b_count >= 2) return true; // Return Good Events
        if (leading_found and subleading_found) return true; // Return Good Events
    }
    return false;
}

reconstructed_event
reconstruct(VecOps::RVec<Jet>& jet,       // Input Jet of FastJet <Jet> type
            VecOps::RVec<Jet>& trkjet, // Input Event of Delphes <HepMCEvent> type
            VecOps::RVec<HepMCEvent>& evt // Input Event of Delphes <HepMCEvent> type
) {
    /**
     *Event Reconstruction Function
     *Store FastJet Jets in <OxJet> type
     *Filter them for Large-R jets
     *Take the top two in pT
     *Reconstruct the Higgs from leading and subleading Jets
     */
    reconstructed_event result{}; // Initialise result of event type <reconstructed_event>
    result.wgt = evt[0].Weight;   // Store MC weight

    std::vector<OxJet> lj_vec =
          view::zip_with(make_jet, jet)
          | view::filter([](const auto& jet) { // Apply Wrapper for OxJet
                //return jet.p4.Pt() >= 250. * GeV and std::abs(jet.p4.Eta()) < 2.5; // Apply Boosted Filter
                return jet.p4.Pt() >= 250. * GeV ; // Apply Boosted Filter
            });

    std::vector<OxJet> tj_vec =
          view::zip_with(make_jet, trkjet)
          | view::filter([](const auto& trkjet) { // Apply Wrapper for OxJet
            return trkjet.p4.Pt() >= 10. * GeV and std::fabs(trkjet.p4.Eta()) < 2.02; // Apply Boosted Filter
          });

    // Sort Large R Jets in pT
    ranges::sort(lj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });
    ranges::reverse(lj_vec);

    // Sort Large R Jets in pT
    ranges::sort(tj_vec, ranges::ordered_less{}, [](auto&& jet) { return jet.p4.Pt(); });
    ranges::reverse(tj_vec);

    const int count = lj_vec.size(); // Number of Boosted Jets
    const int ntag =                 // Number of B-tagged Boosted Jets
          ranges::count(lj_vec, true, [](auto&& jet) { return jet.tagged; });

    OxJet leading = lj_vec[0];    // Leading Large R Jet
    OxJet subleading = lj_vec[1]; // SubLeading Large R Jet

    //
    //Delta-R associate track-jets to higgs candidates
    //
    std::vector<OxJet> h1_assoTrkJet;
    std::vector<OxJet> h2_assoTrkJet;

    for(auto trackJet : tj_vec){
      if (leading.p4.DeltaR(trackJet.p4) <= 1.0){
        h1_assoTrkJet.push_back(trackJet);
      }
      if (subleading.p4.DeltaR(trackJet.p4) <= 1.0){
        h2_assoTrkJet.push_back(trackJet);
      }
    } 
    //Check if trackjets are pt Ordered 
    if (h1_assoTrkJet.size() > 1 and h1_assoTrkJet[1].p4.Pt() > h1_assoTrkJet[0].p4.Pt()) std::cout<<"Warning:            ********TrackJets aren't pt-ordered****************"<<std::endl;
    if (h2_assoTrkJet.size() > 1 and h2_assoTrkJet[1].p4.Pt() > h2_assoTrkJet[0].p4.Pt()) std::cout<<"Warning:            ********TrackJets aren't pt-ordered****************"<<std::endl;

    // Higgs Reconstruction

    result.higgs1.p4 = leading.p4;
    result.higgs2.p4 = subleading.p4;
    result.jets[0] = leading;
    result.jets[1] = subleading;
    result.ntag = ntag;
    result.njets = count;

    if (h1_assoTrkJet.size() > 0) result.higgs1.trkjet1_isTagged = h1_assoTrkJet[0].tagged;
    if (h1_assoTrkJet.size() > 1) result.higgs1.trkjet2_isTagged = h1_assoTrkJet[1].tagged;
    if (h2_assoTrkJet.size() > 0) result.higgs2.trkjet1_isTagged = h2_assoTrkJet[0].tagged;
    if (h2_assoTrkJet.size() > 1) result.higgs2.trkjet2_isTagged = h2_assoTrkJet[1].tagged;

    if (h1_assoTrkJet.size() > 0) result.higgs1.trkjet1 = h1_assoTrkJet[0];
    if (h1_assoTrkJet.size() > 1) result.higgs1.trkjet2 = h1_assoTrkJet[1];
    if (h2_assoTrkJet.size() > 0) result.higgs2.trkjet1 = h2_assoTrkJet[0];
    if (h2_assoTrkJet.size() > 1) result.higgs2.trkjet2 = h2_assoTrkJet[1];
    int h1_ntag = 0;
    int h2_ntag = 0;
    if (result.higgs1.trkjet1_isTagged) h1_ntag++;
    if (result.higgs1.trkjet2_isTagged) h1_ntag++;
    if (result.higgs2.trkjet1_isTagged) h2_ntag++;
    if (result.higgs2.trkjet2_isTagged) h2_ntag++;

    result.higgs1.ntags = h1_ntag;
    result.higgs2.ntags = h2_ntag;

    if ((h1_ntag < 1 and h2_ntag >= 1)or(h1_ntag >= 1 and h2_ntag < 1)) result.lowTag = true;
    else if (h1_ntag > 0 and h2_ntag > 0){
      result.valid = true;
      result.overTag = false;
      if (h1_ntag > 2 or h2_ntag > 2) result.overTag = true;
    }
    else if (h1_ntag < 1 and h2_ntag < 1) result.valid = false;

    return result; // Return type <reconstructed_event>
}

bool valid_check(const reconstructed_event& evt) { return evt.valid; } // Filter Only Valid Events
bool fatJetMass_check(const reconstructed_event& evt) { return evt.higgs1.p4.M() > 50.0 && evt.higgs2.p4.M() > 50.0; } 
bool fatJetPt_check(const reconstructed_event& evt) { return evt.higgs1.p4.Pt() > leadPtCut && evt.higgs2.p4.Pt() > sublPtCut;} 
bool diJetEta_check(const reconstructed_event& evt) { return evt.higgs1.p4.Eta() < 2.0 && evt.higgs2.p4.Eta() < 2.0; } 
bool dEtaHH_check(const reconstructed_event& evt) { return std::fabs(evt.higgs1.p4.Eta() - evt.higgs2.p4.Eta()) < 1.7;} 
bool bJetSkim_check(const reconstructed_event& evt) { return (evt.higgs1.ntags + evt.higgs2.ntags) >= 2;} 
bool lowTag_check(const reconstructed_event& evt) { return evt.lowTag; } // Filter Only lower tagged Events
bool overTag_check(const reconstructed_event& evt) { return evt.overTag; } // Filter Only lower tagged Events
Float_t getWeight(const reconstructed_event& evt) { return evt.wgt; } 
Float_t getDRjj_h1(const reconstructed_event& evt) { return evt.higgs1.trkjet1.p4.DeltaR(evt.higgs1.trkjet2.p4); } 
Float_t getDRjj_h2(const reconstructed_event& evt) { return evt.higgs2.trkjet1.p4.DeltaR(evt.higgs2.trkjet2.p4); } 

bool signal(const reconstructed_event& evt) {
    /*
     *Filter reconstructed events
     *whose Higgs bosons
     *fall in the signal Mass window
     */
    double Xhh = sqrt((pow(((evt.higgs1.p4.M() - 124) / (0.1 * evt.higgs1.p4.M())), 2) + (pow(((evt.higgs2.p4.M() - 115) / (0.1 * evt.higgs2.p4.M())), 2))));
    bool isSR = Xhh < xhhcut;

    return isSR;
}

bool control(const reconstructed_event& evt) {
    /*
     *Filter reconstructed events
     *whose Higgs bosons
     *fall in the control Mass window
     */
    double Xhh = sqrt((pow(((evt.higgs1.p4.M() - 124) / (0.1 * evt.higgs1.p4.M())), 2) + (pow(((evt.higgs2.p4.M() - 115) / (0.1 * evt.higgs2.p4.M())), 2))));
    bool isSR = Xhh < xhhcut;
    return ((sqrt(pow(evt.higgs1.p4.M() - 124.0, 2) + pow(evt.higgs2.p4.M() - 115.0, 2)) < 33));
}

bool sideband(const reconstructed_event& evt) {

    /*
     *Filter reconstructed events
     *whose Higgs bosons
     *fall in the sideband Mass window
     */
    double Xhh = sqrt((pow(((evt.higgs1.p4.M() - 124) / (0.1 * evt.higgs1.p4.M())), 2) + (pow(((evt.higgs2.p4.M() - 115) / (0.1 * evt.higgs2.p4.M())), 2))));
    bool isSR = Xhh < xhhcut;

    return ((sqrt(pow(evt.higgs1.p4.M() - 124.0, 2) + pow(evt.higgs2.p4.M() - 115.0, 2)) > 33.0) &&(sqrt(pow(evt.higgs1.p4.M() - 134.0, 2) + pow(evt.higgs2.p4.M() - 125.0, 2)) < 58.0));

}

int main(int arc, char* argv[]) {

    std::cout<<"Starting...\n"; 

    const std::string file_path = argv[1];
    const std::string output_dir = argv[2];
    const std::string output_filename = argv[3];
    const std::string output_path = output_dir + "/" + output_filename;

    //ROOT::EnableImplicitMT();

    //********************
    // Importing Input file
    //********************

    RDataFrame frame("Delphes", file_path);
    std::cout<<"Loading file\n"; 
    //RDataFrame frame("Delphes",
    //                   "/data/atlas/atlasdata/jesseliu/pheno/fcc/samples/14TeV/2018sep13/all_merged_delphes/OxHHPh_13Sep2018_MG5_262_Py8_14TeV_NNPDF30NLO_Dlph3_xptb200_4b.root"); // Input file for RDF
    

    //***********************
    // Boosted Analysis
    // Applying Filters
    //**********************
    auto two_b_jets = frame.Filter(two_large_b_jets, {"FatJet"}, u8"At least two FatJets"); 
    auto reconstructed = two_b_jets.Define("event", reconstruct, {"FatJet","TrackJet", "Event"}); 

    auto pass_fatJetMass = reconstructed.Filter(fatJetMass_check, {"event"}, u8"FatJet Mass > 50 "); 

    auto pass_fatJetPt = pass_fatJetMass.Filter(fatJetPt_check, {"event"}, u8"FatJetPt cut (450,250) "); 

    auto pass_diJetEta = pass_fatJetPt.Filter(diJetEta_check, {"event"}, u8"FatJet eta < 2 "); 

    auto pass_dEtaHH = pass_diJetEta.Filter(dEtaHH_check, {"event"}, u8"HH deltaEta < 1.7 "); 

    auto add_MC_weight = pass_dEtaHH.Define("mc_weight", getWeight, {"event"}); 

    add_MC_weight.Snapshot("newtree", "newfile.root", {"event","mc_weight"});

    auto add_dRjj_h1 = add_MC_weight.Define("deltaRjj_h1", getDRjj_h1, {"event"}); 

    auto add_dRjj_h2 = add_dRjj_h1.Define("deltaRjj_h2", getDRjj_h2, {"event"}); 

    auto pass_bJetSkim = add_dRjj_h2.Filter(bJetSkim_check, {"event"}, u8"pass bjet skim "); 

    auto valid_evt = pass_bJetSkim.Filter(valid_check, {"event"}, "valid events"); 

    auto lowTag_evt = add_MC_weight.Filter(lowTag_check,{"event"}, "lowTag events"); 

    auto overTag_evt = add_MC_weight.Filter(overTag_check,{"event"}, "overTag events"); 

    auto signal_result = valid_evt.Filter(signal, {"event"}, "signal"); 

    auto control_result = valid_evt.Filter(
          [](const reconstructed_event& event) { return control(event) && (!sideband(event)) && (!signal(event)); },
          {"event"}, "control"); // Filter Events in the Control Region

    auto sideband_result = valid_evt.Filter(
          [](const reconstructed_event& event) { return sideband(event) && (!signal(event)) && (!control(event)); },
          {"event"}, "sideband"); // Filter Events int the Sideband Region

    auto lowTag_signal_result = lowTag_evt.Filter(signal, {"event"}, "signal, low tag"); 

    auto lowTag_control_result = lowTag_evt.Filter(
          [](const reconstructed_event& event) { return control(event) && (!sideband(event)) && (!signal(event)); },
          {"event"}, "control, low tag"); // Filter Events in the Control Region
    auto lowTag_sideband_result = lowTag_evt.Filter(
          [](const reconstructed_event& event) { return sideband(event) && (!signal(event)) && (!control(event)); },
          {"event"}, "sideband, low tag"); // Filter Events int the Sideband Region

    auto overTag_signal_result = overTag_evt.Filter(signal, {"event"}, "signal, over tag"); 
    auto overTag_control_result = overTag_evt.Filter(
          [](const reconstructed_event& event) { return control(event) && (!sideband(event)) && (!signal(event)); },
          {"event"}, "control, over tag"); // Filter Events in the Control Region
    auto overTag_sideband_result = overTag_evt.Filter(
          [](const reconstructed_event& event) { return sideband(event) && (!signal(event)) && (!control(event)); },
          {"event"}, "sideband, over tag"); // Filter Events int the Sideband Region

    ////*********************
    //// Storing Output
    ////********************

    auto h_dRjj_h1 = add_dRjj_h2.Histo1D({"deltaRjj_h1", "", 45, -0.6,5}, "deltaRjj_h1");
    auto h_dRjj_h2 = add_dRjj_h2.Histo1D({"deltaRjj_h2", "", 45, -0.6,5}, "deltaRjj_h2");

    int   phi_nbins = 40;
    float phi_min   = -4.0;
    float phi_max   = 4.0;
    int   eta_nbins = 30;
    float eta_min   = -3.0;
    float eta_max   = 3.0;

    int   hcandpt_nbins   = 60;
    float hcandpt_min     = 250.0;
    float hcandpt_max     = 1750.;
    int   hcandmass_nbins = 60;
    float hcandmass_min   = 0.0;
    float hcandmass_max   = 300.;

    int   jetpt_nbins   = 50;
    float jetpt_min     = 0.0;
    float jetpt_max     = 500.;
    int   jetmass_nbins = 40;
    float jetmass_min   = 0.0;
    float jetmass_max   = 80.;

    auto checkFJPt100 = [](const reconstructed_event& evt){return evt.higgs1.p4.Pt() > 100.0;};
    auto checkFJPt200 = [](const reconstructed_event& evt){return evt.higgs1.p4.Pt() > 200.0;};
    auto checkFJPt300 = [](const reconstructed_event& evt){return evt.higgs1.p4.Pt() > 300.0;};
    auto checkFJPt400 = [](const reconstructed_event& evt){return evt.higgs1.p4.Pt() > 400.0;};

    auto getHHmass = [](const reconstructed_event& evt){return (evt.higgs1.p4 + evt.higgs2.p4).M();};

    auto getH1mass = [](const reconstructed_event& evt){return evt.higgs1.p4.M();};
    auto getH2mass = [](const reconstructed_event& evt){return evt.higgs2.p4.M();};
    auto getH1pt = [](const reconstructed_event& evt){return evt.higgs1.p4.Pt();};
    auto getH2pt = [](const reconstructed_event& evt){return evt.higgs2.p4.Pt();};
    auto getH1eta = [](const reconstructed_event& evt){return evt.higgs1.p4.Eta();};
    auto getH2eta = [](const reconstructed_event& evt){return evt.higgs2.p4.Eta();};
    auto getH1phi = [](const reconstructed_event& evt){return evt.higgs1.p4.Phi();};
    auto getH2phi = [](const reconstructed_event& evt){return evt.higgs2.p4.Phi();};

    auto getH1J1mass = [](const reconstructed_event& evt){return evt.jets[0].p4.M();};
    auto getH1J2mass = [](const reconstructed_event& evt){return evt.jets[1].p4.M();};
    auto getH1J1pt = [](const reconstructed_event& evt){return evt.jets[0].p4.Pt();};
    auto getH1J2pt = [](const reconstructed_event& evt){return evt.jets[1].p4.Pt();};
    auto getH1J1eta = [](const reconstructed_event& evt){return evt.jets[0].p4.Eta();};
    auto getH1J2eta = [](const reconstructed_event& evt){return evt.jets[1].p4.Eta();};
    auto getH1J1phi = [](const reconstructed_event& evt){return evt.jets[0].p4.Phi();};
    auto getH1J2phi = [](const reconstructed_event& evt){return evt.jets[1].p4.Phi();};

    auto getH2J1mass = [](const reconstructed_event& evt){return evt.jets[0].p4.M();};
    auto getH2J2mass = [](const reconstructed_event& evt){return evt.jets[1].p4.M();};
    auto getH2J1pt = [](const reconstructed_event& evt){return evt.jets[0].p4.Pt();};
    auto getH2J2pt = [](const reconstructed_event& evt){return evt.jets[1].p4.Pt();};
    auto getH2J1eta = [](const reconstructed_event& evt){return evt.jets[0].p4.Eta();};
    auto getH2J2eta = [](const reconstructed_event& evt){return evt.jets[1].p4.Eta();};
    auto getH2J1phi = [](const reconstructed_event& evt){return evt.jets[0].p4.Phi();};
    auto getH2J2phi = [](const reconstructed_event& evt){return evt.jets[1].p4.Phi();};

    auto addHHmass = pass_fatJetMass.Define("hh_m",getHHmass,{"event"});
    auto addH1mass = pass_fatJetMass.Define("h1_m",getH1mass,{"event"});

    auto h_hh_mass_fj100 = addHHmass.Filter(checkFJPt100,{"event"}).Histo1D({"hh_m_fj100", "", 45, 100.0,1000.0}, "hh_m");
    auto h_hh_mass_fj200 = addHHmass.Filter(checkFJPt200,{"event"}).Histo1D({"hh_m_fj200", "", 45, 100.0,1000.0}, "hh_m");
    auto h_hh_mass_fj300 = addHHmass.Filter(checkFJPt300,{"event"}).Histo1D({"hh_m_fj300", "", 45, 100.0,1000.0}, "hh_m");
    auto h_hh_mass_fj400 = addHHmass.Filter(checkFJPt400,{"event"}).Histo1D({"hh_m_fj400", "", 45, 100.0,1000.0}, "hh_m");

    auto h_h1_mass_fj100 = addH1mass.Filter(checkFJPt100,{"event"}).Histo1D({"h1_m_fj100", "", 45, 100.0,1000.0}, "h1_m");
    auto h_h1_mass_fj200 = addH1mass.Filter(checkFJPt200,{"event"}).Histo1D({"h1_m_fj200", "", 45, 100.0,1000.0}, "h1_m");
    auto h_h1_mass_fj300 = addH1mass.Filter(checkFJPt300,{"event"}).Histo1D({"h1_m_fj300", "", 45, 100.0,1000.0}, "h1_m");
    auto h_h1_mass_fj400 = addH1mass.Filter(checkFJPt400,{"event"}).Histo1D({"h1_m_fj400", "", 45, 100.0,1000.0}, "h1_m");

    TH2D h2_hmasses("h1_m_vs_h2_m", ";leading_hcand_mass[GeV];subleading_hcand_mass[GeV];Entries", 20, 50, hcandmass_max, 20, 50, hcandmass_max);
    valid_evt.Foreach(
      [&h2_hmasses](const reconstructed_event& evt) { h2_hmasses.Fill(evt.higgs1.p4.M(),evt.higgs2.p4.M()); },
      {"event"}); // Filter Events in the Control Region
    //TH2D* h2_hmasses = new TH2D("h1_m_vs_h2_m", "h2_hmasses;"";Entries", hcandmass_nbins, hcandmass_min, hcandmass_max, hcandmass_nbins, hcandmass_min, hcandmass_max);
    //

    std::vector <ROOT::RDF::RResultPtr<TH1D>> hvec;

    hvec.push_back(sideband_result.Define("SB_hh_m",getHHmass,{"event"}).Histo1D({"SB_hh_m", "", 45,500, 1400}, "SB_hh_m"));

    hvec.push_back(sideband_result.Define("SB_hcand1_m",getH1mass,{"event"}).Histo1D({"SB_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "SB_hcand1_m"));
    hvec.push_back(sideband_result.Define("SB_hcand2_m",getH2mass,{"event"}).Histo1D({"SB_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "SB_hcand2_m"));
    hvec.push_back(sideband_result.Define("SB_hcand1_pt",getH1pt,{"event"}).Histo1D({"SB_hcand1_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "SB_hcand1_pt"));
    hvec.push_back(sideband_result.Define("SB_hcand2_pt",getH2pt,{"event"}).Histo1D({"SB_hcand2_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "SB_hcand2_pt"));
    hvec.push_back(sideband_result.Define("SB_hcand1_eta",getH1eta,{"event"}).Histo1D({"SB_hcand1_eta", "",  eta_nbins, eta_min, eta_max}, "SB_hcand1_eta"));
    hvec.push_back(sideband_result.Define("SB_hcand2_eta",getH2eta,{"event"}).Histo1D({"SB_hcand2_eta", "",  eta_nbins, eta_min, eta_max}, "SB_hcand2_eta"));
    hvec.push_back(sideband_result.Define("SB_hcand1_phi",getH1phi,{"event"}).Histo1D({"SB_hcand1_phi", "", phi_nbins, phi_min, phi_max}, "SB_hcand1_phi"));
    hvec.push_back(sideband_result.Define("SB_hcand2_phi",getH2phi,{"event"}).Histo1D({"SB_hcand2_phi", "", phi_nbins, phi_min, phi_max}, "SB_hcand2_phi"));

    hvec.push_back(sideband_result.Define("SB_hcand1jet1_m",getH1mass,{"event"}).Histo1D({"SB_hcand1jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "SB_hcand1jet1_m"));
    hvec.push_back(sideband_result.Define("SB_hcand1jet2_m",getH2mass,{"event"}).Histo1D({"SB_hcand1jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "SB_hcand1jet2_m"));
    hvec.push_back(sideband_result.Define("SB_hcand1jet1_pt",getH1pt,{"event"}).Histo1D({"SB_hcand1jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "SB_hcand1jet1_pt"));
    hvec.push_back(sideband_result.Define("SB_hcand1jet2_pt",getH2pt,{"event"}).Histo1D({"SB_hcand1jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "SB_hcand1jet2_pt"));
    hvec.push_back(sideband_result.Define("SB_hcand1jet1_eta",getH1eta,{"event"}).Histo1D({"SB_hcand1jet1_eta", "",  eta_nbins, eta_min, eta_max}, "SB_hcand1jet1_eta"));
    hvec.push_back(sideband_result.Define("SB_hcand1jet2_eta",getH2eta,{"event"}).Histo1D({"SB_hcand1jet2_eta", "",  eta_nbins, eta_min, eta_max}, "SB_hcand1jet2_eta"));
    hvec.push_back(sideband_result.Define("SB_hcand1jet1_phi",getH1phi,{"event"}).Histo1D({"SB_hcand1jet1_phi", "", phi_nbins, phi_min, phi_max}, "SB_hcand1jet1_phi"));
    hvec.push_back(sideband_result.Define("SB_hcand1jet2_phi",getH2phi,{"event"}).Histo1D({"SB_hcand1jet2_phi", "", phi_nbins, phi_min, phi_max}, "SB_hcand1jet2_phi"));

    hvec.push_back(sideband_result.Define("SB_hcand2jet1_m",getH1mass,{"event"}).Histo1D({"SB_hcand2jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "SB_hcand2jet1_m"));
    hvec.push_back(sideband_result.Define("SB_hcand2jet2_m",getH2mass,{"event"}).Histo1D({"SB_hcand2jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "SB_hcand2jet2_m"));
    hvec.push_back(sideband_result.Define("SB_hcand2jet1_pt",getH1pt,{"event"}).Histo1D({"SB_hcand2jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "SB_hcand2jet1_pt"));
    hvec.push_back(sideband_result.Define("SB_hcand2jet2_pt",getH2pt,{"event"}).Histo1D({"SB_hcand2jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "SB_hcand2jet2_pt"));
    hvec.push_back(sideband_result.Define("SB_hcand2jet1_eta",getH1eta,{"event"}).Histo1D({"SB_hcand2jet1_eta", "",  eta_nbins, eta_min, eta_max}, "SB_hcand2jet1_eta"));
    hvec.push_back(sideband_result.Define("SB_hcand2jet2_eta",getH2eta,{"event"}).Histo1D({"SB_hcand2jet2_eta", "",  eta_nbins, eta_min, eta_max}, "SB_hcand2jet2_eta"));
    hvec.push_back(sideband_result.Define("SB_hcand2jet1_phi",getH1phi,{"event"}).Histo1D({"SB_hcand2jet1_phi", "", phi_nbins, phi_min, phi_max}, "SB_hcand2jet1_phi"));
    hvec.push_back(sideband_result.Define("SB_hcand2jet2_phi",getH2phi,{"event"}).Histo1D({"SB_hcand2jet2_phi", "", phi_nbins, phi_min, phi_max}, "SB_hcand2jet2_phi"));
    

    hvec.push_back(control_result.Define("CR_hh_m",getHHmass,{"event"}).Histo1D({"CR_hh_m", "", 45,500, 1400}, "CR_hh_m"));

    hvec.push_back(control_result.Define("CR_hcand1_m",getH1mass,{"event"}).Histo1D({"CR_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "CR_hcand1_m"));
    hvec.push_back(control_result.Define("CR_hcand2_m",getH2mass,{"event"}).Histo1D({"CR_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "CR_hcand2_m"));
    hvec.push_back(control_result.Define("CR_hcand1_pt",getH1pt,{"event"}).Histo1D({"CR_hcand1_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "CR_hcand1_pt"));
    hvec.push_back(control_result.Define("CR_hcand2_pt",getH2pt,{"event"}).Histo1D({"CR_hcand2_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "CR_hcand2_pt"));
    hvec.push_back(control_result.Define("CR_hcand1_eta",getH1eta,{"event"}).Histo1D({"CR_hcand1_eta", "",  eta_nbins, eta_min, eta_max}, "CR_hcand1_eta"));
    hvec.push_back(control_result.Define("CR_hcand2_eta",getH2eta,{"event"}).Histo1D({"CR_hcand2_eta", "",  eta_nbins, eta_min, eta_max}, "CR_hcand2_eta"));
    hvec.push_back(control_result.Define("CR_hcand1_phi",getH1phi,{"event"}).Histo1D({"CR_hcand1_phi", "", phi_nbins, phi_min, phi_max}, "CR_hcand1_phi"));
    hvec.push_back(control_result.Define("CR_hcand2_phi",getH2phi,{"event"}).Histo1D({"CR_hcand2_phi", "", phi_nbins, phi_min, phi_max}, "CR_hcand2_phi"));

    hvec.push_back(control_result.Define("CR_hcand1jet1_m",getH1mass,{"event"}).Histo1D({"CR_hcand1jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "CR_hcand1jet1_m"));
    hvec.push_back(control_result.Define("CR_hcand1jet2_m",getH2mass,{"event"}).Histo1D({"CR_hcand1jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "CR_hcand1jet2_m"));
    hvec.push_back(control_result.Define("CR_hcand1jet1_pt",getH1pt,{"event"}).Histo1D({"CR_hcand1jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "CR_hcand1jet1_pt"));
    hvec.push_back(control_result.Define("CR_hcand1jet2_pt",getH2pt,{"event"}).Histo1D({"CR_hcand1jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "CR_hcand1jet2_pt"));
    hvec.push_back(control_result.Define("CR_hcand1jet1_eta",getH1eta,{"event"}).Histo1D({"CR_hcand1jet1_eta", "",  eta_nbins, eta_min, eta_max}, "CR_hcand1jet1_eta"));
    hvec.push_back(control_result.Define("CR_hcand1jet2_eta",getH2eta,{"event"}).Histo1D({"CR_hcand1jet2_eta", "",  eta_nbins, eta_min, eta_max}, "CR_hcand1jet2_eta"));
    hvec.push_back(control_result.Define("CR_hcand1jet1_phi",getH1phi,{"event"}).Histo1D({"CR_hcand1jet1_phi", "", phi_nbins, phi_min, phi_max}, "CR_hcand1jet1_phi"));
    hvec.push_back(control_result.Define("CR_hcand1jet2_phi",getH2phi,{"event"}).Histo1D({"CR_hcand1jet2_phi", "", phi_nbins, phi_min, phi_max}, "CR_hcand1jet2_phi"));

    hvec.push_back(control_result.Define("CR_hcand2jet1_m",getH1mass,{"event"}).Histo1D({"CR_hcand2jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "CR_hcand2jet1_m"));
    hvec.push_back(control_result.Define("CR_hcand2jet2_m",getH2mass,{"event"}).Histo1D({"CR_hcand2jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "CR_hcand2jet2_m"));
    hvec.push_back(control_result.Define("CR_hcand2jet1_pt",getH1pt,{"event"}).Histo1D({"CR_hcand2jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "CR_hcand2jet1_pt"));
    hvec.push_back(control_result.Define("CR_hcand2jet2_pt",getH2pt,{"event"}).Histo1D({"CR_hcand2jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "CR_hcand2jet2_pt"));
    hvec.push_back(control_result.Define("CR_hcand2jet1_eta",getH1eta,{"event"}).Histo1D({"CR_hcand2jet1_eta", "",  eta_nbins, eta_min, eta_max}, "CR_hcand2jet1_eta"));
    hvec.push_back(control_result.Define("CR_hcand2jet2_eta",getH2eta,{"event"}).Histo1D({"CR_hcand2jet2_eta", "",  eta_nbins, eta_min, eta_max}, "CR_hcand2jet2_eta"));
    hvec.push_back(control_result.Define("CR_hcand2jet1_phi",getH1phi,{"event"}).Histo1D({"CR_hcand2jet1_phi", "", phi_nbins, phi_min, phi_max}, "CR_hcand2jet1_phi"));
    hvec.push_back(control_result.Define("CR_hcand2jet2_phi",getH2phi,{"event"}).Histo1D({"CR_hcand2jet2_phi", "", phi_nbins, phi_min, phi_max}, "CR_hcand2jet2_phi"));

    hvec.push_back(signal_result.Define("SR_hh_m",getHHmass,{"event"}).Histo1D({"SR_hh_m", "", 45,500, 1400}, "SR_hh_m"));

    hvec.push_back(signal_result.Define("SR_hcand1_m",getH1mass,{"event"}).Histo1D({"SR_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "SR_hcand1_m"));
    hvec.push_back(signal_result.Define("SR_hcand2_m",getH2mass,{"event"}).Histo1D({"SR_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "SR_hcand2_m"));
    hvec.push_back(signal_result.Define("SR_hcand1_pt",getH1pt,{"event"}).Histo1D({"SR_hcand1_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "SR_hcand1_pt"));
    hvec.push_back(signal_result.Define("SR_hcand2_pt",getH2pt,{"event"}).Histo1D({"SR_hcand2_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "SR_hcand2_pt"));
    hvec.push_back(signal_result.Define("SR_hcand1_eta",getH1eta,{"event"}).Histo1D({"SR_hcand1_eta", "",  eta_nbins, eta_min, eta_max}, "SR_hcand1_eta"));
    hvec.push_back(signal_result.Define("SR_hcand2_eta",getH2eta,{"event"}).Histo1D({"SR_hcand2_eta", "",  eta_nbins, eta_min, eta_max}, "SR_hcand2_eta"));
    hvec.push_back(signal_result.Define("SR_hcand1_phi",getH1phi,{"event"}).Histo1D({"SR_hcand1_phi", "", phi_nbins, phi_min, phi_max}, "SR_hcand1_phi"));
    hvec.push_back(signal_result.Define("SR_hcand2_phi",getH2phi,{"event"}).Histo1D({"SR_hcand2_phi", "", phi_nbins, phi_min, phi_max}, "SR_hcand2_phi"));

    hvec.push_back(signal_result.Define("SR_hcand1jet1_m",getH1mass,{"event"}).Histo1D({"SR_hcand1jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "SR_hcand1jet1_m"));
    hvec.push_back(signal_result.Define("SR_hcand1jet2_m",getH2mass,{"event"}).Histo1D({"SR_hcand1jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "SR_hcand1jet2_m"));
    hvec.push_back(signal_result.Define("SR_hcand1jet1_pt",getH1pt,{"event"}).Histo1D({"SR_hcand1jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "SR_hcand1jet1_pt"));
    hvec.push_back(signal_result.Define("SR_hcand1jet2_pt",getH2pt,{"event"}).Histo1D({"SR_hcand1jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "SR_hcand1jet2_pt"));
    hvec.push_back(signal_result.Define("SR_hcand1jet1_eta",getH1eta,{"event"}).Histo1D({"SR_hcand1jet1_eta", "",  eta_nbins, eta_min, eta_max}, "SR_hcand1jet1_eta"));
    hvec.push_back(signal_result.Define("SR_hcand1jet2_eta",getH2eta,{"event"}).Histo1D({"SR_hcand1jet2_eta", "",  eta_nbins, eta_min, eta_max}, "SR_hcand1jet2_eta"));
    hvec.push_back(signal_result.Define("SR_hcand1jet1_phi",getH1phi,{"event"}).Histo1D({"SR_hcand1jet1_phi", "", phi_nbins, phi_min, phi_max}, "SR_hcand1jet1_phi"));
    hvec.push_back(signal_result.Define("SR_hcand1jet2_phi",getH2phi,{"event"}).Histo1D({"SR_hcand1jet2_phi", "", phi_nbins, phi_min, phi_max}, "SR_hcand1jet2_phi"));

    hvec.push_back(signal_result.Define("SR_hcand2jet1_m",getH1mass,{"event"}).Histo1D({"SR_hcand2jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "SR_hcand2jet1_m"));
    hvec.push_back(signal_result.Define("SR_hcand2jet2_m",getH2mass,{"event"}).Histo1D({"SR_hcand2jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "SR_hcand2jet2_m"));
    hvec.push_back(signal_result.Define("SR_hcand2jet1_pt",getH1pt,{"event"}).Histo1D({"SR_hcand2jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "SR_hcand2jet1_pt"));
    hvec.push_back(signal_result.Define("SR_hcand2jet2_pt",getH2pt,{"event"}).Histo1D({"SR_hcand2jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "SR_hcand2jet2_pt"));
    hvec.push_back(signal_result.Define("SR_hcand2jet1_eta",getH1eta,{"event"}).Histo1D({"SR_hcand2jet1_eta", "",  eta_nbins, eta_min, eta_max}, "SR_hcand2jet1_eta"));
    hvec.push_back(signal_result.Define("SR_hcand2jet2_eta",getH2eta,{"event"}).Histo1D({"SR_hcand2jet2_eta", "",  eta_nbins, eta_min, eta_max}, "SR_hcand2jet2_eta"));
    hvec.push_back(signal_result.Define("SR_hcand2jet1_phi",getH1phi,{"event"}).Histo1D({"SR_hcand2jet1_phi", "", phi_nbins, phi_min, phi_max}, "SR_hcand2jet1_phi"));
    hvec.push_back(signal_result.Define("SR_hcand2jet2_phi",getH2phi,{"event"}).Histo1D({"SR_hcand2jet2_phi", "", phi_nbins, phi_min, phi_max}, "SR_hcand2jet2_phi"));

    ///overTag region
    hvec.push_back(overTag_sideband_result.Define("overTag_SB_hh_m",getHHmass,{"event"}).Histo1D({"overTag_SB_hh_m", "", 45,500, 1400}, "overTag_SB_hh_m"));

    hvec.push_back(overTag_sideband_result.Define("overTag_SB_hcand1_m",getH1mass,{"event"}).Histo1D({"overTag_SB_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "overTag_SB_hcand1_m"));
    hvec.push_back(overTag_sideband_result.Define("overTag_SB_hcand2_m",getH2mass,{"event"}).Histo1D({"overTag_SB_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "overTag_SB_hcand2_m"));

    hvec.push_back(overTag_control_result.Define("overTag_CR_hh_m",getHHmass,{"event"}).Histo1D({"overTag_CR_hh_m", "", 45,500, 1400}, "overTag_CR_hh_m"));

    hvec.push_back(overTag_control_result.Define("overTag_CR_hcand1_m",getH1mass,{"event"}).Histo1D({"overTag_CR_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "overTag_CR_hcand1_m"));
    hvec.push_back(overTag_control_result.Define("overTag_CR_hcand2_m",getH2mass,{"event"}).Histo1D({"overTag_CR_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "overTag_CR_hcand2_m"));

    hvec.push_back(overTag_signal_result.Define("overTag_SR_hh_m",getHHmass,{"event"}).Histo1D({"overTag_SR_hh_m", "", 45,500, 1400}, "overTag_SR_hh_m"));

    hvec.push_back(overTag_signal_result.Define("overTag_SR_hcand1_m",getH1mass,{"event"}).Histo1D({"overTag_SR_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "overTag_SR_hcand1_m"));
    hvec.push_back(overTag_signal_result.Define("overTag_SR_hcand2_m",getH2mass,{"event"}).Histo1D({"overTag_SR_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "overTag_SR_hcand2_m"));

    ///LowTag region
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hh_m",getHHmass,{"event"}).Histo1D({"lowTag_SB_hh_m", "", 45,500, 1400}, "lowTag_SB_hh_m"));

    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1_m",getH1mass,{"event"}).Histo1D({"lowTag_SB_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "lowTag_SB_hcand1_m"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2_m",getH2mass,{"event"}).Histo1D({"lowTag_SB_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "lowTag_SB_hcand2_m"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1_pt",getH1pt,{"event"}).Histo1D({"lowTag_SB_hcand1_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "lowTag_SB_hcand1_pt"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2_pt",getH2pt,{"event"}).Histo1D({"lowTag_SB_hcand2_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "lowTag_SB_hcand2_pt"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1_eta",getH1eta,{"event"}).Histo1D({"lowTag_SB_hcand1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SB_hcand1_eta"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2_eta",getH2eta,{"event"}).Histo1D({"lowTag_SB_hcand2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SB_hcand2_eta"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1_phi",getH1phi,{"event"}).Histo1D({"lowTag_SB_hcand1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SB_hcand1_phi"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2_phi",getH2phi,{"event"}).Histo1D({"lowTag_SB_hcand2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SB_hcand2_phi"));

    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1jet1_m",getH1mass,{"event"}).Histo1D({"lowTag_SB_hcand1jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_SB_hcand1jet1_m"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1jet2_m",getH2mass,{"event"}).Histo1D({"lowTag_SB_hcand1jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_SB_hcand1jet2_m"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1jet1_pt",getH1pt,{"event"}).Histo1D({"lowTag_SB_hcand1jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_SB_hcand1jet1_pt"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1jet2_pt",getH2pt,{"event"}).Histo1D({"lowTag_SB_hcand1jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_SB_hcand1jet2_pt"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1jet1_eta",getH1eta,{"event"}).Histo1D({"lowTag_SB_hcand1jet1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SB_hcand1jet1_eta"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1jet2_eta",getH2eta,{"event"}).Histo1D({"lowTag_SB_hcand1jet2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SB_hcand1jet2_eta"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1jet1_phi",getH1phi,{"event"}).Histo1D({"lowTag_SB_hcand1jet1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SB_hcand1jet1_phi"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand1jet2_phi",getH2phi,{"event"}).Histo1D({"lowTag_SB_hcand1jet2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SB_hcand1jet2_phi"));

    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2jet1_m",getH1mass,{"event"}).Histo1D({"lowTag_SB_hcand2jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_SB_hcand2jet1_m"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2jet2_m",getH2mass,{"event"}).Histo1D({"lowTag_SB_hcand2jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_SB_hcand2jet2_m"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2jet1_pt",getH1pt,{"event"}).Histo1D({"lowTag_SB_hcand2jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_SB_hcand2jet1_pt"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2jet2_pt",getH2pt,{"event"}).Histo1D({"lowTag_SB_hcand2jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_SB_hcand2jet2_pt"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2jet1_eta",getH1eta,{"event"}).Histo1D({"lowTag_SB_hcand2jet1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SB_hcand2jet1_eta"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2jet2_eta",getH2eta,{"event"}).Histo1D({"lowTag_SB_hcand2jet2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SB_hcand2jet2_eta"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2jet1_phi",getH1phi,{"event"}).Histo1D({"lowTag_SB_hcand2jet1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SB_hcand2jet1_phi"));
    hvec.push_back(lowTag_sideband_result.Define("lowTag_SB_hcand2jet2_phi",getH2phi,{"event"}).Histo1D({"lowTag_SB_hcand2jet2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SB_hcand2jet2_phi"));
    

    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hh_m",getHHmass,{"event"}).Histo1D({"lowTag_CR_hh_m", "", 45,500, 1400}, "lowTag_CR_hh_m"));

    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1_m",getH1mass,{"event"}).Histo1D({"lowTag_CR_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "lowTag_CR_hcand1_m"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2_m",getH2mass,{"event"}).Histo1D({"lowTag_CR_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "lowTag_CR_hcand2_m"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1_pt",getH1pt,{"event"}).Histo1D({"lowTag_CR_hcand1_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "lowTag_CR_hcand1_pt"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2_pt",getH2pt,{"event"}).Histo1D({"lowTag_CR_hcand2_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "lowTag_CR_hcand2_pt"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1_eta",getH1eta,{"event"}).Histo1D({"lowTag_CR_hcand1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_CR_hcand1_eta"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2_eta",getH2eta,{"event"}).Histo1D({"lowTag_CR_hcand2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_CR_hcand2_eta"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1_phi",getH1phi,{"event"}).Histo1D({"lowTag_CR_hcand1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_CR_hcand1_phi"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2_phi",getH2phi,{"event"}).Histo1D({"lowTag_CR_hcand2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_CR_hcand2_phi"));

    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1jet1_m",getH1mass,{"event"}).Histo1D({"lowTag_CR_hcand1jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_CR_hcand1jet1_m"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1jet2_m",getH2mass,{"event"}).Histo1D({"lowTag_CR_hcand1jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_CR_hcand1jet2_m"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1jet1_pt",getH1pt,{"event"}).Histo1D({"lowTag_CR_hcand1jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_CR_hcand1jet1_pt"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1jet2_pt",getH2pt,{"event"}).Histo1D({"lowTag_CR_hcand1jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_CR_hcand1jet2_pt"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1jet1_eta",getH1eta,{"event"}).Histo1D({"lowTag_CR_hcand1jet1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_CR_hcand1jet1_eta"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1jet2_eta",getH2eta,{"event"}).Histo1D({"lowTag_CR_hcand1jet2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_CR_hcand1jet2_eta"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1jet1_phi",getH1phi,{"event"}).Histo1D({"lowTag_CR_hcand1jet1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_CR_hcand1jet1_phi"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand1jet2_phi",getH2phi,{"event"}).Histo1D({"lowTag_CR_hcand1jet2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_CR_hcand1jet2_phi"));

    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2jet1_m",getH1mass,{"event"}).Histo1D({"lowTag_CR_hcand2jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_CR_hcand2jet1_m"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2jet2_m",getH2mass,{"event"}).Histo1D({"lowTag_CR_hcand2jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_CR_hcand2jet2_m"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2jet1_pt",getH1pt,{"event"}).Histo1D({"lowTag_CR_hcand2jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_CR_hcand2jet1_pt"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2jet2_pt",getH2pt,{"event"}).Histo1D({"lowTag_CR_hcand2jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_CR_hcand2jet2_pt"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2jet1_eta",getH1eta,{"event"}).Histo1D({"lowTag_CR_hcand2jet1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_CR_hcand2jet1_eta"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2jet2_eta",getH2eta,{"event"}).Histo1D({"lowTag_CR_hcand2jet2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_CR_hcand2jet2_eta"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2jet1_phi",getH1phi,{"event"}).Histo1D({"lowTag_CR_hcand2jet1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_CR_hcand2jet1_phi"));
    hvec.push_back(lowTag_control_result.Define("lowTag_CR_hcand2jet2_phi",getH2phi,{"event"}).Histo1D({"lowTag_CR_hcand2jet2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_CR_hcand2jet2_phi"));

    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hh_m",getHHmass,{"event"}).Histo1D({"lowTag_SR_hh_m", "", 45,500, 1400}, "lowTag_SR_hh_m"));

    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1_m",getH1mass,{"event"}).Histo1D({"lowTag_SR_hcand1_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "lowTag_SR_hcand1_m"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2_m",getH2mass,{"event"}).Histo1D({"lowTag_SR_hcand2_m", "", hcandmass_nbins, hcandmass_min, hcandmass_max}, "lowTag_SR_hcand2_m"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1_pt",getH1pt,{"event"}).Histo1D({"lowTag_SR_hcand1_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "lowTag_SR_hcand1_pt"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2_pt",getH2pt,{"event"}).Histo1D({"lowTag_SR_hcand2_pt", "",hcandpt_nbins, hcandpt_min, hcandpt_max}, "lowTag_SR_hcand2_pt"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1_eta",getH1eta,{"event"}).Histo1D({"lowTag_SR_hcand1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SR_hcand1_eta"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2_eta",getH2eta,{"event"}).Histo1D({"lowTag_SR_hcand2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SR_hcand2_eta"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1_phi",getH1phi,{"event"}).Histo1D({"lowTag_SR_hcand1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SR_hcand1_phi"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2_phi",getH2phi,{"event"}).Histo1D({"lowTag_SR_hcand2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SR_hcand2_phi"));

    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1jet1_m",getH1mass,{"event"}).Histo1D({"lowTag_SR_hcand1jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_SR_hcand1jet1_m"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1jet2_m",getH2mass,{"event"}).Histo1D({"lowTag_SR_hcand1jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_SR_hcand1jet2_m"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1jet1_pt",getH1pt,{"event"}).Histo1D({"lowTag_SR_hcand1jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_SR_hcand1jet1_pt"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1jet2_pt",getH2pt,{"event"}).Histo1D({"lowTag_SR_hcand1jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_SR_hcand1jet2_pt"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1jet1_eta",getH1eta,{"event"}).Histo1D({"lowTag_SR_hcand1jet1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SR_hcand1jet1_eta"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1jet2_eta",getH2eta,{"event"}).Histo1D({"lowTag_SR_hcand1jet2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SR_hcand1jet2_eta"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1jet1_phi",getH1phi,{"event"}).Histo1D({"lowTag_SR_hcand1jet1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SR_hcand1jet1_phi"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand1jet2_phi",getH2phi,{"event"}).Histo1D({"lowTag_SR_hcand1jet2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SR_hcand1jet2_phi"));

    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2jet1_m",getH1mass,{"event"}).Histo1D({"lowTag_SR_hcand2jet1_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_SR_hcand2jet1_m"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2jet2_m",getH2mass,{"event"}).Histo1D({"lowTag_SR_hcand2jet2_m", "", jetmass_nbins, jetmass_min, jetmass_max}, "lowTag_SR_hcand2jet2_m"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2jet1_pt",getH1pt,{"event"}).Histo1D({"lowTag_SR_hcand2jet1_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_SR_hcand2jet1_pt"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2jet2_pt",getH2pt,{"event"}).Histo1D({"lowTag_SR_hcand2jet2_pt", "",jetpt_nbins, jetpt_min, jetpt_max}, "lowTag_SR_hcand2jet2_pt"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2jet1_eta",getH1eta,{"event"}).Histo1D({"lowTag_SR_hcand2jet1_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SR_hcand2jet1_eta"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2jet2_eta",getH2eta,{"event"}).Histo1D({"lowTag_SR_hcand2jet2_eta", "",  eta_nbins, eta_min, eta_max}, "lowTag_SR_hcand2jet2_eta"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2jet1_phi",getH1phi,{"event"}).Histo1D({"lowTag_SR_hcand2jet1_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SR_hcand2jet1_phi"));
    hvec.push_back(lowTag_signal_result.Define("lowTag_SR_hcand2jet2_phi",getH2phi,{"event"}).Histo1D({"lowTag_SR_hcand2jet2_phi", "", phi_nbins, phi_min, phi_max}, "lowTag_SR_hcand2jet2_phi"));

    std::cout<<"printing histogram\n";

    TString filePath = output_path.c_str();
    std::cout<<"crating histo file  "<<filePath<<std::endl;
    TFile hist_file(filePath, "RECREATE");   // Opening Ouput File
    std::cout<<"plotting histogram\n";

    h2_hmasses.Write();

    h_h1_mass_fj100->Write(); 
    h_h1_mass_fj200->Write(); 
    h_h1_mass_fj300->Write(); 
    h_h1_mass_fj400->Write(); 

    h_hh_mass_fj100->Write(); 
    h_hh_mass_fj200->Write(); 
    h_hh_mass_fj300->Write(); 
    h_hh_mass_fj400->Write(); 
    for(auto  hist: hvec) {
      hist->Write();
    }

    h_dRjj_h1->Write(); 
    h_dRjj_h2->Write();

//    auto colNames = addH1mass.GetColumnNames();
//    for (auto &&colName : colNames) {
//       std::cout << colName << std::endl;
//    }
//  
//

    //**********************
    // Writing Cutflows
    //************************

    Cutflow boosted_cutflow("Boosted_Cutflow",
                            hist_file); // Define Cutflow for the Boosted Analysis
    boosted_cutflow.add(u8"Initial",//before: 2 large good jets(pT ≥ 200 GeV, η ≤ 2.0), ≥ 2 tagged
                        frame.Count());
    boosted_cutflow.add(u8"2 large good jets",//before: 2 large good jets(pT ≥ 200 GeV, η ≤ 2.0), ≥ 2 tagged
                        two_b_jets.Count());
    boosted_cutflow.add(u8"Reconstructed events", reconstructed.Count());
    boosted_cutflow.add(u8"FatJet Mass", pass_fatJetMass.Count());
    boosted_cutflow.add(u8"FatJet pT"+std::to_string(leadPtCut)+","+std::to_string(sublPtCut), pass_diJetEta.Count());
    boosted_cutflow.add(u8"FatJet eta", pass_diJetEta.Count());
    boosted_cutflow.add(u8"FatJet DeltaEta", pass_dEtaHH.Count());
    boosted_cutflow.add(u8"bJetSkim", pass_bJetSkim.Count());
    boosted_cutflow.add(u8"2 large jet Tagged", valid_evt.Count());
    boosted_cutflow.add(u8"Signal", signal_result.Count());
    boosted_cutflow.add(u8"Control", control_result.Count());
    boosted_cutflow.add(u8"Sideband", sideband_result.Count());
    boosted_cutflow.add(u8"Low-tag Signal", lowTag_signal_result.Count());
    boosted_cutflow.add(u8"Low-tag Control", lowTag_control_result.Count());
    boosted_cutflow.add(u8"Low-tag Sideband", lowTag_sideband_result.Count());
    boosted_cutflow.write();

    std::cout << "======================="<< std::endl;
    std::cout << "       Initial: " << boosted_cutflow.get("Initial") << std::endl; 
    std::cout << "       2LR jets in barrel: " << boosted_cutflow.get("2 large good jets") << std::endl; 
    std::cout << "       PassFatJetMass: " << boosted_cutflow.get("FatJet Mass") << std::endl; 
    std::cout << "       PassDijetEta: " << boosted_cutflow.get("FatJet eta") << std::endl; 
    std::cout << "       PassDetaHH: " << boosted_cutflow.get("FatJet DeltaEta") << std::endl; 
    std::cout << "       PassBJetSkim: " << boosted_cutflow.get("bJetSkim") << std::endl; 
    std::cout << "       PassSignal: " << boosted_cutflow.get("Signal") << std::endl; 
    std::cout << "======================="<< std::endl;


    std::cout<<"closing histo file\n";
    hist_file.Write();
    hist_file.Close();
    std::cout<<"Success!\n";

    return 0;
}
