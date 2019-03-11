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

class OxJet {
  public:
    TLorentzVector p4; ///< 4-momentum
                       // float btag;        ///< B-tagging score
    bool tagged;       ///< Is jet B-tagged?

    OxJet() : p4(), tagged(false) {}
    OxJet(double M, double pT, double eta, long double phi, bool tagged) : p4(), tagged(tagged) {
        p4.SetPtEtaPhiM(pT, eta, phi, M);
    }
};

// Higgs Boson

struct higgs {
    TLorentzVector p4; ///< 4-momentum

    higgs() : p4() {}
    higgs(const TLorentzVector& p4) : p4(p4) {}
    bool trkjet1_isTagged;
    bool trkjet2_isTagged;
    OxJet trkjet1;
    OxJet trkjet2;
    int ntags;
};


inline OxJet make_jet(Jet& jet) {
    double M = jet.Mass;
    double pT = jet.PT;
    double eta = jet.Eta;
    long double phi = jet.Phi;
    bool tagged = jet.BTag;

    // Because a constructor can't be used as a Callable
    return OxJet(M, pT, eta, phi, tagged);
}

struct reconstructed_event {
    bool valid;                ///< Is event valid
    bool lowTag;               ///< Is event lower-tagged
    bool overTag;               ///< Is event lower-tagged
    int64_t ntag;              ///< Number of B-tagged jets
    int64_t njets;             ///< Total number of jets
    int64_t nTrackJets;             ///< Total number of jets
    Float_t wgt;                ///< Event Weight
    std::array<OxJet, 2> jets; ///< Array of 4 chosen jets

    higgs higgs1; ///< Leading Higgs
    higgs higgs2; ///< Subleading Higgs

    reconstructed_event()
        : valid(true), // set to true if pairing is valid
          lowTag(false), 
          jets(),
          higgs1(),
          higgs2() {}
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
void write_tree(ROOT::RDF::RInterface<Proxied>& result, const char* treename,
                TFile& output_file /**< [out] Tree to write to */) {
    using namespace std;
    using namespace ROOT::Experimental;
    namespace view = ranges::view;
    namespace action = ranges::action;
    static bool first_tree = true;

    const char* out_format_leaflist = "m_hh/D:m_h1/D:pT_h1:eta_h1:phi_h1:"
                                      "m_h2/D:pT_h2:eta_h2:phi_h2:"
                                      "m_h1_j1:pT_h1_j1:eta_h1_j1:phi_h1_j1:"
                                      "m_h2_j2:pT_h2_j2:eta_h2_j2:phi_h2_j2";

    int num_threads = ROOT::GetImplicitMTPoolSize();
    vector<unique_ptr<TTree>> out_trees{};

    std::cout<<"in write_tree"<<std::endl;

    vector<int> ntag_var(num_threads);
    vector<int> njets_var(num_threads);
    vector<double> mc_sf_var(num_threads);
    vector<unique_ptr<out_format>> out_vars{};
    for (int i = 0; i < num_threads; ++i) {
        gROOT->cd();
        out_vars.push_back(make_unique<out_format>());
        out_trees.push_back(make_unique<TTree>(treename, treename));

        out_trees[i]->SetDirectory(nullptr);
        out_trees[i]->Branch("ntag", &ntag_var[i]);
        out_trees[i]->Branch("njets", &njets_var[i]);
        out_trees[i]->Branch("mc_sf", &mc_sf_var[i]);
        out_trees[i]->Branch("event", out_vars[i].get(), out_format_leaflist);
    }
    std::cout<<"after thread bit"<<std::endl;

    if (first_tree) {
        fmt::print("Processing events\n");
    }
    else {
        fmt::print("Collecting Events...\n");
        first_tree = false;
    }

    std::cout<<"before foreach"<<std::endl;
    result.ForeachSlot(
          [&out_trees, &out_vars, &ntag_var, &njets_var,
           &mc_sf_var](unsigned slot, const reconstructed_event& event
                       /*,double mc_sf*/) {
              std::cout<<"in foreach"<<std::endl;
              auto&& tree = out_trees[slot];
              auto&& vars = out_vars[slot];

              //ntag_var[slot] = event.ntag;
              //njets_var[slot] = event.njets;
              //mc_sf_var[slot] = event.wgt;

              std::cout<<"before assigning first vars"<<std::endl;
              vars->m_hh = (event.higgs1.p4 + event.higgs2.p4).M();
              std::cout<<"after assigning first vars"<<std::endl;

              vars->m_h1 = event.higgs1.p4.M();
              vars->pT_h1 = event.higgs1.p4.Pt();
              vars->eta_h1 = event.higgs1.p4.Eta();
              vars->phi_h1 = event.higgs1.p4.Phi();

              vars->m_h2 = event.higgs2.p4.M();
              vars->pT_h2 = event.higgs2.p4.Pt();
              vars->eta_h2 = event.higgs2.p4.Eta();
              vars->phi_h2 = event.higgs2.p4.Phi();

              //vars->m_h1_j1 = event.jets[0].p4.M();
              //vars->pT_h1_j1 = event.jets[0].p4.Pt();
              //vars->eta_h1_j1 = event.jets[0].p4.Eta();
              //vars->phi_h1_j1 = event.jets[0].p4.Phi();

              //vars->m_h2_j2 = event.jets[1].p4.M();
              //vars->pT_h2_j2 = event.jets[1].p4.Pt();
              //vars->eta_h2_j2 = event.jets[1].p4.Eta();
              //vars->phi_h2_j2 = event.jets[1].p4.Phi();

              std::cout<<"before filling"<<std::endl;
              tree->Fill();
          },
          {"event"});
          //{"event" , "mc_sf"});

    std::cout<<"after foreach"<<std::endl;
    TList temp_list;
    for (auto&& tree : out_trees) {
        temp_list.Add(tree.get());
    }
    std::cout<<"after addtrees"<<std::endl;

    output_file.cd();
    TTree* signal_tree = TTree::MergeTrees(&temp_list);
    if (!signal_tree) {
        fmt::print("\nALL TREES EMPTY");
        return;
    }
    signal_tree->SetName(treename);
    signal_tree->Write("", TObject::kOverwrite);
    fmt::print("\n");
    std::cout<<"done"<<std::endl;
}
