/// \file resolved-recon.cpp
/// \brief Main implementation file
///
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

double f = 0.16;

using namespace ROOT;
namespace view = ranges::view;
namespace action = ranges::action;

constexpr double GeV = 1.; ///< Set to 1 -- energies and momenta in GeV
// constexpr double pi = 3.1415926535896;
constexpr double pi = 3.13;
/// Reconstruct event in the resolved regime
reconstructed_event reconstruct(VecOps::RVec<Jet> &jet,
                                VecOps::RVec<HepMCEvent> &evt) {
  reconstructed_event result{};

  result.wgt = evt[0].Weight;
  // std::cout<<wgt<<std::endl;

  std::vector<OxJet> all_jets =
      view::zip_with(make_jet, jet) | view::filter([](const auto &jet) {
        return jet.p4.Pt() >= 40. * GeV and std::abs(jet.p4.Eta()) < 2.5;
      });
  //    // TODO Delphes doesn't have a score
  //    // sort by MV2 score (descending)
  ranges::sort(all_jets, ranges::ordered_less{},
               [](auto &&jet) { return jet.p4.Pt(); }); // sorting for pT
  ranges::reverse(all_jets);

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
  // if (other_jets.size() < 4) {
  //  std::cout << "OTHER JETS SIZE LESS THAN" << std::endl;
  // }
  // for (auto &&j : other_jets) {
  //  std::cout << "other_jets pt" << j.p4.Pt() << std::endl;
  // }

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
    // for (auto &&j : jets) {
    //  if (j.p4.Pt() == 0.) {
    //  std::cout << "Jet pt equals 0" << std::endl;
    // }
    // fmt::print("Flag 1");
  }

  if (jets.size() > 4) {
    jets |= (action::sort(ranges::ordered_less{},
                          [](auto &&jet) { return jet.p4.Pt(); }) |
             action::reverse | action::take(4));
  }

  //  double m4j = (jets[0].p4 + jets[1].p4 + jets[2].p4 + jets[3].p4).M();

  // limits for pairing condition
  // See NOTE, condition is magic
  //  double lead_low = 0.;
  //  double lead_high = 0.;
  //  double sublead_low = 0.;
  //  double sublead_high = 0.;

  // Try exact numbers from old code
  //  if (m4j < 1250 * GeV) {
  //    lead_low = 360 / (m4j / GeV) - 0.5;
  //    lead_high = 652.863 / (m4j / GeV) + 0.474449;
  //    sublead_low = 235.242 / (m4j / GeV) + 0.0162996;
  //    sublead_high = 874.890 / (m4j / GeV) + 0.347137;
  //  }
  //  else {
  //  if (m4j < 1250 * GeV) {
  //    lead_low = 360 / (m4j / GeV) - 0.5;
  //    lead_high = 652.863 / (m4j / GeV) + 0.474449;
  //    sublead_low = 235.242 / (m4j / GeV) + 0.0162996;
  //    sublead_high = 874.890 / (m4j / GeV) + 0.347137;
  //  }
  //  else {
  //    lead_low = sublead_low = 0.;
  //    lead_high = 0.9967394;
  //    sublead_high = 1.047049;
  //  }
  // All possible combinations of forming two pairs of jets
  //
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

    // delta R jet-jet condition
    //    if (!(between(lead_low, deltaRjj_lead, lead_high)
    //      && between(sublead_low, deltaRjj_sublead, sublead_high))) {
    //      continue;}

    pair_candidates.push_back(std::make_pair(
        higgs(higgs1, higgs1_1, higgs1_2), higgs(higgs2, higgs2_1, higgs2_2)));
  }

  if (pair_candidates.empty()) {
    //        // leave result invalid
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

/// ## Selection functions
///

/// \brief Require four jets with p<SUB>T</SUB> > 40 GeV, |&eta;| < 2.5
/// with at least 2 being b-tagged.
bool four_b_jets_pT_40_eta_25(VecOps::RVec<Jet> &jets) {
  // Filter jets with 4 pT > 40 GeV, |eta| < 2.5 jets with >= 2 b tagged]
  int count = 0;
  int b_count = 0;
  for (auto &&j : jets) {
    // fmt::print("{} {:.4f} {:.4f}\n", tagged[i], pT[i], eta[i]);
    if (j.PT >= 40. * GeV and std::abs(j.Eta) < 2.5) {
      count++;
      if (j.BTag)
        b_count++;
    }
    if (count >= 4 and b_count >= 2 /* 4 */)
      return true;
    // we want to keep the 2 tag events too
  }
  return false;
}

/// \brief Require &Delta;R<SUB>jj</SUB> condition is satisfied. Implemented by
/// requiring event be marked as valid by reconstruct().
bool deltaRjj(const reconstructed_event &evt) { return evt.valid; }

/// Require p<SUB>T</SUB>(h)s are in the appropriate range
// bool pT_hs(const reconstructed_event& evt) {
// double m4j = (evt.higgs1.p4 + evt.higgs2.p4).M();

// This uses leading and subleading *pT* higgs
//  const auto& lead =
// (evt.higgs1.p4.Pt() >= evt.higgs2.p4.Pt()) ? evt.higgs1 : evt.higgs2;
// const auto& sublead =
//(evt.higgs1.p4.Pt() >= evt.higgs2.p4.Pt()) ? evt.higgs2 : evt.higgs1;

// Numbers also incorrect
// Const was 90 GeV
//  return (lead.p4.Pt() > (0.513333 * m4j - 103.3333 * GeV)
// Const was 70 GeV
//   && sublead.p4.Pt() > (0.33333 * m4j - 73.3333 * GeV));
//}

/// Require &Delta;&eta;(hh) < 1.5
//    bool delta_eta_hh(const reconstructed_event& evt) {
//      return abs(evt.higgs1.p4.Eta() - evt.higgs2.p4.Eta()) < 1.5;
//    }

/// \brief Veto top quarks using X<SUB>wt</SUB>
///
/// Requires plain branches again to reconstruct tops
//    bool remove_ttbar(const reconstructed_event& evt, const
//    std::vector<float>& E,
//      const std::vector<float>& pT, const std::vector<float>& eta,
//      const std::vector<float>& phi, const std::vector<float>& btag,
//      const std::vector<int>& tagged, long long evtNum) {
// Switch off top veto if not requested on command line

//      std::vector<Jet> jets =
//      view::zip_with(make_jet, E, pT, eta, phi, btag, tagged)
//      | view::filter([](const auto& jet) {
//        return jet.p4.Pt() >= 40 * GeV and abs(jet.p4.Eta()) < 2.5;
//      });

//      const auto& hc_jets = evt.jets;

//      std::vector<double> Xwts{};
//      for (auto&& hc_jet : hc_jets) {
//        std::vector<Jet> non_hc_jets =
//        jets | view::remove_if([&hc_jet](auto&& jet) {
//          return jet == hc_jet;
//        });
//        for (auto&& w_jets :
//         view::cartesian_product(non_hc_jets, non_hc_jets)) {
//          auto&& w_jet1 = std::get<0>(w_jets);
//        auto&& w_jet2 = std::get<1>(w_jets);
//            // Drop pairs where two W constituents are the same jet
//        if (w_jet1 == w_jet2) {
//          continue;
//        }
// // Drop pairs where both W constituents are b tagged
// if (w_jet1.tagged && w_jet2.tagged) continue;
// Drop if hc_jet isn't highest MV2
//        if ((hc_jet.btag < w_jet1.btag
//         and (ranges::find(hc_jets, w_jet1) != std::end(hc_jets)))
//          or (hc_jet.btag < w_jet2.btag
//            and (ranges::find(hc_jets, w_jet2) != std::end(hc_jets)))) {
//          continue;
//      }

//      double Mw = (w_jet1.p4 + w_jet2.p4).M();
//      double Mt = (w_jet1.p4 + w_jet2.p4 + hc_jet.p4).M();
//      double Xwt = sqrt(pow((Mw - 80.4 * GeV) / (0.1 * Mw), 2)
//        + pow((Mt - 172.5 * GeV) / (0.1 * Mt), 2));
//      Xwts.push_back(Xwt);
//    }
//  }
//  if (Xwts.empty()) {
//        // fmt::print(top_deb, "Xwts is empty\n");
//    return true;
//  }
//  else {
//    return !(*ranges::min_element(Xwts) < 1.5);
//  }
//}

/// Select m<SUB>hh</SUB> signal region
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
/// Select m<SUB>hh</SUB> sideband region (old)
//  double m_h1 = evt.higgs1.p4.M();
//  double m_h2 = evt.higgs2.p4.M();

//  double desc = sqrt(pow(m_h1 - 120 * 1.05 * GeV, 2)
//   + pow(m_h2 - 110 * 1.05 * GeV, 2));
//  return desc < 45 * GeV;
//}
/// Select m<SUB>hh</SUB> control region
bool control(const reconstructed_event &evt) {
  double m_h1 = evt.higgs1.p4.M();
  double m_h2 = evt.higgs2.p4.M();
  // Cut in a mass window of 80 GeV around 125 GeV for both Higgs
  bool higgs1_flag = (std::abs(evt.higgs1.p4.M() - 125.) < 45.) ? true : false;
  bool higgs2_flag = (std::abs(evt.higgs2.p4.M() - 125.) < 45.) ? true : false;
  return (higgs1_flag && higgs2_flag);
}
/// Select m<SUB>hh</SUB> control region (old)
// bool control(const reconstructed_event& evt) {
// double m_h1 = evt.higgs1.p4.M();
// double m_h2 = evt.higgs2.p4.M();

//  double desc = sqrt(pow(m_h1 - 120 * 1.03 * GeV, 2)
//   + pow(m_h2 - 110 * 1.03 * GeV, 2));
//  return desc < 30 * GeV;
//}

int main(int argc, char *argv[]) {
  // Use iostreams for input only and fmt::print for output only, so fine
  std::ios::sync_with_stdio(false); // Needed for fast iostreams
  using vec_string = std::vector<std::string>;

  ROOT::EnableImplicitMT();
  RDataFrame frame("Delphes", "/data/atlas/atlasdata/micheli/4b/Events/run_02/"
                              "tag_1_delphes_events.root");
  // TODO Do something about btag_name since Delphes provides no score.

  auto four_jets =
      frame.Filter(four_b_jets_pT_40_eta_25, {"Jet"},
                   u8"4 good jets(pT ≥ 40 GeV, η ≤ 2.5), ≥ 4 tagged");

  /*auto reconstructed = four_jets.Define(
          "event", reconstruct,
          {"Jet.Mass", "Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.BTag"}); */
  auto reconstructed = four_jets.Define("event", reconstruct, {"Jet", "Event"});
  // f.close();
  // auto mc_sf = four_jets.Define("mc_sf","Event.Weight");
  auto deltaRjj_cut = reconstructed.Filter(deltaRjj, {"event"}, u8"ΔR_jj");
  // auto pT_cut = deltaRjj_cut.Filter(pT_hs, {"event"}, "pT(h)s");
  // auto delta_eta_cut = pT_cut.Filter(delta_eta_hh, {"event"}, u8"Δη_hh");
  // auto result = Xwt_cut.Filter(pass_triggers, {"passedTriggers"},
  // "Triggers");

  //
  // auto signal_result = result.Filter(signal, {"event"}, "signal");
  auto signal_result = deltaRjj_cut.Filter(signal, {"event"}, "signal");
  auto control_result = deltaRjj_cut.Filter(
      [](const reconstructed_event &event) {
        return control(event) && (!signal(event));
      },
      {"event"}, "control");
  auto sideband_result = deltaRjj_cut.Filter(
      [](const reconstructed_event &event) {
        return sideband(event) && !control(event);
      },
      {"event"}, "sideband");
  // std::string output_filename = parsed_options["output"].as<std::string>();
  // //?
  std::string output_filename = "pheno_resolved.root";

  fmt::print("Writing to {}\n", output_filename);
  // To print progress
  auto start_events_proxy = frame.Count();
  start_events_proxy.OnPartialResult(
      10000, [](const unsigned long long &num_events) {
        fmt::print("Processed {} events\n", num_events);
      });
  // Write trees
  TFile output_file(output_filename.c_str(), "RECREATE");
  write_tree(signal_result, "signal", output_file);

  start_events_proxy.GetValue(); // For printing progress

  write_tree(control_result, "control", output_file);
  write_tree(sideband_result, "sideband", output_file);

  // Write cutflows
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
                      deltaRjj_cut.Filter(two_tag_filter, {"event"}).Count());

  //  deltaRjj_cut.Filter(two_tag_filter, {"event"}).Count());
  // two_tag_cutflow.add(u8"pT(h)s",
  //                      pT_cut.Filter(two_tag_filter, {"event"}).Count());
  //  two_tag_cutflow.add(
  //       u8"Δη_hh", delta_eta_cut.Filter(two_tag_filter, {"event"}).Count());
  // two_tag_cutflow.add(u8"Xwt",
  //                     Xwt_cut.Filter(two_tag_filter, {"event"}).Count());
  // two_tag_cutflow.add(u8"Trigger",
  //          result.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.add(u8"Signal",
                      signal_result.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.add(u8"Control",
                      control_result.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.add(
      u8"Sideband", sideband_result.Filter(two_tag_filter, {"event"}).Count());
  two_tag_cutflow.write();
  //
  Cutflow four_tag_cutflow("FourTagCutflow", output_file);
  four_tag_cutflow.add(u8"4 good jets(pT ≥ 40 GeV, η ≤ 2.5), ≥ 4 tagged",
                       four_jets.Count());
  four_tag_cutflow.add(
      u8"Four Tagged",
      reconstructed.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.add(u8"ΔR_jj",
                       deltaRjj_cut.Filter(four_tag_filter, {"event"}).Count());
  //  four_tag_cutflow.add(u8"pT(h)s",
  //                      pT_cut.Filter(four_tag_filter, {"event"}).Count());
  //  four_tag_cutflow.add(
  //       u8"Δη_hh", delta_eta_cut.Filter(four_tag_filter, {"event"}).Count());
  //  four_tag_cutflow.add(u8"Xwt",
  //                       Xwt_cut.Filter(four_tag_filter, {"event"}).Count());
  // four_tag_cutflow.add(u8"Trigger",
  //                      result.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.add(
      u8"Signal", signal_result.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.add(
      u8"Control", control_result.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.add(
      u8"Sideband", sideband_result.Filter(four_tag_filter, {"event"}).Count());
  four_tag_cutflow.write();
  return 0;
}
