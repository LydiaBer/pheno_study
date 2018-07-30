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
#include <cstdlib>

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
#include "MCUtils/PIDUtils.h"

//Higgs Boson
struct higgs {
  TLorentzVector p4; ///< 4-momentum

  higgs() : p4() {}
  higgs(const TLorentzVector &p4)
      : p4(p4) {}
};

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


inline void flavour_algo(const std::vector<int> b_tag, const std::vector<int> c_tag,
			const std::vector<int> ph_tag,std::vec<int> s_vec_tag){

                if ( b_tag.at(0) > 0 || b_tag.at(1) >0) s_vec_tag.at(0) = 1; // BTagged
                if ( c_tag.at(0) >0 || c_tag.at(1) >0  && s_vec_tag.at(0)!=1) s_vec_tag.at(1) = 1; // CTagged
                if ( ph_tag.at(0)>0 || ph_tag.at(1) >0
                    && s_vec_tag.at(0)!= 1 && s_vec_tag.at(1)!=1) s_vec_tag.at(2) = 1; //Light Tagged   

                return;

}


inline void tagging_algo(      const fastjet::PseudoJet& calojet,
                        const std::vector<fastjet::PseudoJet>& matched_trkjets){
                fastjet::PseudoJet leading_trkjet = matched_trkjets[0];
                fastjet::PseudoJet subleading_trkjet = matched_trkjets[1];

                std::vector<fastjet::PseudoJet> lead_trks = leading_trkjet.constituents();
                std::vector<fastjet::PseudoJet> sublead_trks = subleading_trkjet.constituents();
                //Vector for switching different taggin for the calo jet
                //First entry : B Tagged
                //Second Entry : C Tagged
                //Third Entry : Light Tagged
                std::vector<int> switch_tag = {0,0,0};

                const std::vector<int> b_tag = {0,0};
                const std::vector<int> c_tag = {0,0};
                const std::vector<int> ph_tag = {0,0};

                for(const auto& trk : lead_trks) {
                        //Following PDGId number convention


                        if (PID::hasBottom(trk.user_index())) b_tag.at(0)++;
                        if (PID::hasCharm(trk.user_index())) c_tag.at(0)++;
                        if (PID::isPhoton(pid)) ph_taga.at(0)++;
                }

                for(const auto& trk : sublead_trks) {
                        //Following PDGId number convention


                        if (PID::hasBottom(trk.user_index())) b_tag.at(1)++;
                        if (PID::hasCharm(trk.user_index()))  c_tag.at(1)++;
                        if (PID::isPhoton(pid)) ph_tag.at(1)++;
                }


                flavour_algo(b_tag,c_tag,ph_tag,switch_tag);

                if (switch_tag.at(0) !=0) calojet.set_user_index(5);
                if (switch_tag.at(1) !=0) calojet.set_user_index(4);
                if (switch_tag.at(2) !=0) calojet.set_user_index(22);

                return;

}

inline void get_assoc_trkjets(const fastjet::PseudoJet& calojet, std::vector<fastjet::PseudoJet> trkjets,
                       std::vector<fastjet::PseudoJet>& matched_trkjets, bool debug = false) {

    // vector to hold input clusters and ghosts
    std::vector<fastjet::PseudoJet> input_particles;
    input_particles.clear();

    // jet clusters from large-R jet
    vector<fastjet::PseudoJet> constituents = calojet.constituents();

    if (debug) std::cout << "calo constituents size = " << constituents.size() << std::endl;

    for (auto noghost : constituents) {

        noghost.reset_PtYPhiM(noghost.pt(), noghost.rapidity(), noghost.phi(), 0.0);
        if (noghost.E() < 0.) continue;

        // set user index for calo clusters to -1 to differentiate them from "track" constituents
        // later
        noghost.set_user_index(-1);
        input_particles.push_back(noghost);
    }

    if (debug)
        std::cout << "calo only input particles size = " << input_particles.size() << std::endl;

    // make ghost PseudoJets out of track jet direction
    for (unsigned int trackJetItr = 0; trackJetItr < trkjets.size(); ++trackJetItr) {

        fastjet::PseudoJet myghost = trkjets.at(trackJetItr);
        // if( myghost.pt() <= 20.0 || fabs( myghost.rapidity() ) >= 2.5 ) continue;

        myghost.reset_PtYPhiM(1e-12, myghost.rapidity(), myghost.phi(), 0.0);
        if (myghost.E() < 0.) continue;

        myghost.set_user_index(trackJetItr);
        input_particles.push_back(myghost);
    }

    if (debug)
        std::cout << "calo+track jets input particles size = " << input_particles.size()
                  << std::endl;

    // do ghost association and get list of pseudojet track jets that are associated
    double                       Rparam        = 1.0;
    fastjet::Strategy            strategy      = fastjet::Best;     // according to atlas reco
    fastjet::RecombinationScheme recomb_scheme = fastjet::E_scheme; // according to atlas reco
    fastjet::JetDefinition jet_def(fastjet::antikt_algorithm, Rparam, recomb_scheme, strategy);

    // run the jet clustering with the above jet definition
    fastjet::ClusterSequence   clust_seq(input_particles, jet_def);
    vector<fastjet::PseudoJet> sorted_jets = fastjet::sorted_by_pt(clust_seq.inclusive_jets());

    if (debug) std::cout << "number of sorted jets = " << sorted_jets.size() << std::endl;

    fastjet::PseudoJet newJet =
          sorted_jets.at(0); // there are more jets in the vector, but they all have pT ~0
    if (debug)
        std::cout << "new jet constituent size = " << newJet.constituents().size() << std::endl;
    vector<fastjet::PseudoJet> newJet_constituents = newJet.constituents();
    for (const auto& constit : newJet_constituents) {
        if (debug)
            std::cout << " user index = " << constit.user_index()
                      << ", pt of constit = " << constit.pt() << std::endl;
        if (constit.user_index() >= 0) {
            int iter = constit.user_index();
            //    if(trkjets.at(iter).pt() > 20. && fabs(trkjets.at(iter).eta()) < 2.5 )
            // matched_trkjets.push_back(trkjets.at(iter));
            matched_trkjets.push_back(trkjets.at(iter));
        }
    }

    // Sort matched jets by pt
    matched_trkjets = sorted_by_pt(matched_trkjets);

    tagging_algo(calojet,matched_trkjets);

    return;
}



inline OxJet make_jet(Jet &jet) {
  double M = jet.Mass;
  double pT = jet.PT;
  double eta = jet.Eta;
  long double phi = jet.Phi;
  bool tagged=false;

  if (jet.user_index() == 5) tagged = true; 
  // Because a constructor can't be used as a Callable
  return OxJet(M, pT, eta, phi, tagged);
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

  double m_h1; ///< Leading Higgs mass
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
  //                            // double E_h1_j1;   ///< Leading Higgs leading jet energy
  double pT_h1_j1;  ///< Leading Higgs leading jet p<SUB>T</SUB>
  double eta_h1_j1; ///< Leading Higgs leading jet &eta;
  double phi_h1_j1; ///< Leading Higgs leading jet &Phi;
 
  double m_h2_j2; ///< Subleading Higgs subleading jet mass
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
      [&out_trees, &out_vars, &ntag_var, &njets_var, &rwgt_vars
       ,&mc_sf_var](unsigned slot, const reconstructed_event &event
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
                                           return std::abs(jet.p4.Eta());
                                         }) /4;



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
*/
        tree->Fill();
      }, {"event" /*, "mc_sf"*/});

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

	               
