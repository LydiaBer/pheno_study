#include <cmath>
#include <functional>
#include <iostream>
#include <list>
#include <map>
#include <set>
#include <tuple>
#include <vector>

#include <range/v3/all.hpp>

#include <classes/DelphesClasses.h>
#include <HepPID/ParticleIDMethods.hh>
#include <fastjet/JetDefinition.hh>
#include <fastjet/NestedDefsPlugin.hh>
#include <fastjet/contrib/VariableR.hh>

#include <TInterpreter.h>
#include <TLorentzVector.h>
#include <TSystem.h>
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RVec.hxx>

using namespace ROOT::VecOps;
using namespace std;
using namespace std::placeholders;
namespace view = ranges::views;
namespace action = ranges::actions;

template <class C>
typename C::size_type iter_to_index(const C& container,
                                    typename C::const_iterator iter) {
    return iter - container.cbegin();
}

bool from_b_quark(GenParticle* part, RVec<GenParticle>& particles) {
    bool result = false;
    // One mother
    if (part->M2 == -1) {
        // if this is a b quark, and parent was a higgs, return true
        if (abs(part->PID) == 5 && (abs(particles[part->M1].PID) == 25)) {
            return true;
        }

        if (part->M1 == -1) {
            // reached initial entry therefore not from a b-quark
            return false;
        }
        result = result || from_b_quark(&particles[part->M1], particles);
    }
    else {
        for (int i = part->M1; i <= part->M2; ++i) {
            result = result || from_b_quark(&particles[i], particles);
            if (result) break;
        }
    }
    return result;
}

auto make_jets_fr(RVec<Jet>& jets, const std::vector<TLorentzVector>& bs) {
    const static fastjet::JetDefinition akt4(fastjet::antikt_algorithm, 0.4);
    std::vector<fastjet::PseudoJet> all_particles =
          view::all(jets)
          | view::filter([](const Jet& jet) { return jet.PT > 5; })
          | view::transform([](const Jet& jet) -> fastjet::PseudoJet {
                auto p = fastjet::PseudoJet();
                double y = std::log(
                      (std::sqrt(std::pow(jet.Mass, 2)
                                 + std::pow(jet.PT * std::cosh(jet.Eta), 2))
                       + jet.PT * std::sinh(jet.Eta))
                      / std::sqrt(std::pow(jet.Mass, 2) + std::pow(jet.PT, 2)));
                p.reset_PtYPhiM(jet.PT, y, jet.Phi, jet.Mass);
                p.set_user_index(0);
                return p;
            })
          | ranges::to<std::vector>();

    int i = 1;
    std::vector<fastjet::PseudoJet> b_pj =
          view::transform(bs,
                          [&i](const TLorentzVector& b) {
                              auto p = fastjet::PseudoJet();
                              p.reset_PtYPhiM(1E-50, b.Eta(), b.Phi(), 4.18);
                              p.set_user_index(i++);
                              return p;
                          })
          | ranges::to<std::vector>;

    ranges::copy(b_pj, ranges::back_inserter(all_particles));

    fastjet::ClusterSequence cs(all_particles, akt4);
    std::vector<TLorentzVector> out(4);

    for (auto&& jet : fastjet::sorted_by_pt(cs.inclusive_jets())) {
        auto parts = jet.constituents();
        int num_jets = ranges::count_if(
              parts, [](auto&& jet) { return jet.user_index() == 0; });
        int num_bs = parts.size() - num_jets;
        if (num_jets == 0 || num_bs == 0) {
            continue;
        }

        if (num_bs == 1) {
            auto&& cons_bs = parts | view::filter([](auto&& x) {
                                 return x.user_index() != 0;
                             });
            auto&& cons_jets = parts | view::filter([](auto&& x) {
                                   return x.user_index() == 0;
                               });
            auto&& b = ranges::front(cons_bs);
            if (num_jets == 1) {
                // one b and one jet -- easy
                auto&& j = ranges::front(cons_jets);
                out[b.user_index() - 1] =
                      TLorentzVector(j.px(), j.py(), j.pz(), j.E());
            }
            else {
                // multiple jets -- pick the one that's closest
                auto&& cons_jets = parts | view::filter([](auto&& x) {
                                       return x.user_index() == 0;
                                   });
                auto&& assoc = *ranges::min_element(
                      cons_jets, std::less{},
                      [&b](auto&& x) { return x.delta_R(b); });
                out[b.user_index() - 1] = TLorentzVector(assoc.px(), assoc.py(),
                                                         assoc.pz(), assoc.E());
            }
        }
        else {
            // multiple bs
            std::vector<fastjet::PseudoJet> bs =
                  parts
                  | view::filter([](auto&& x) { return x.user_index() != 0; })
                  | ranges::to<std::vector>();
            std::vector<fastjet::PseudoJet> cons_jets =
                  parts
                  | view::filter([](auto&& x) { return x.user_index() == 0; })
                  | ranges::to<std::vector>();

            // Define an ordering for b quarks and jets, so we can permute them
            auto pred = [](const fastjet::PseudoJet& a,
                           const fastjet::PseudoJet& b) {
                if (a.pt() == b.pt()) {
                    if (a.eta() == b.eta()) {
                        if (a.phi_std() == b.phi_std()) {
                            return false;
                        }
                        return a.phi_std() < b.phi_std();
                    }
                    return a.eta() < b.eta();
                }
                return a.pt() < b.pt();
            };
            ranges::sort(cons_jets, pred);
            ranges::sort(bs, pred);

            double min_sum = 999999.;
            if (num_bs >= num_jets) {
                // more bs -- assign a b to each jet
                // Find the assignment that minimizes
                // sum of deltaRs between jets and assigned bs
                std::vector<int> jet_assign(0, num_jets);
                do {
                    double sum = ranges::accumulate(
                          view::zip_with(
                                [](auto&& x, auto&& y) { return x.delta_R(y); },
                                bs, cons_jets),
                          0., std::plus{});
                    if (sum < min_sum) {
                        min_sum = sum;
                        jet_assign = bs | view::take(num_jets)
                                     | view::transform([](auto&& x) {
                                           return x.user_index();
                                       })
                                     | ranges::to<std::vector>();
                    }
                } while (ranges::next_permutation(bs, pred));
                for (int j = 0; j < num_jets; ++j) {
                    out[jet_assign[j] - 1] =
                          TLorentzVector(cons_jets[j].px(), cons_jets[j].py(),
                                         cons_jets[j].pz(), cons_jets[j].e());
                }
            }
            else {
                // assign a jet to each b -- save
                do {
                    double sum = ranges::accumulate(
                          view::zip_with(
                                [](auto&& x, auto&& y) { return x.delta_R(y); },
                                bs, cons_jets),
                          0., std::plus{});
                    if (sum < min_sum) {
                        min_sum = sum;
                        for (int j = 0; j < num_bs; ++j) {
                            out[bs[j].user_index() - 1] = TLorentzVector(
                                  cons_jets[j].px(), cons_jets[j].py(),
                                  cons_jets[j].pz(), cons_jets[j].e());
                        }
                    }
                } while (ranges::next_permutation(cons_jets, pred));
            }
        }

        if (num_jets >= 2) {
            cerr << "FR ERROR: Association jet contains more than one original "
                    "jet.\n";
            cerr << "Constituents: \n";
            for (auto&& c : parts) {
                cerr << "    [" << c.pt() << ", " << c.eta() << ", "
                     << c.phi_std() << ", " << c.E() << "] -- "
                     << (c.user_index() ? "B" : "Jet") << "\n";
            }
            cerr << "-------------------------------------------------\n";
            int count = 1;
            int last = parts.size();
            for (auto&& c : parts) {
                int count2 = 1;
                for (auto&& d : parts) {
                    if (count2 == 1) {
                        if (count == 1)
                            cerr << "⎡";
                        else if (count == last)
                            cerr << "⎣";
                        else
                            cerr << "⎢";
                    }
                    cerr << std::setprecision(4) << std::setw(6) << c.delta_R(d)
                         << ((count2 == last) ? "" : " ");
                    if (count2 == last) {
                        if (count == 1)
                            cerr << "⎤";
                        else if (count == last)
                            cerr << "⎦";
                        else
                            cerr << "⎥";
                    }
                    count2++;
                }
                count++;
                cerr << "\n";
            }
            cerr << "SELECTED JETS:\n";
            for (auto&& jet : out) {
                cerr << "[" << jet.Pt() << ", " << jet.Eta() << ", "
                     << jet.Phi() << ", " << jet.E() << "]\n";
            }
            cerr << "\n";
        }
    }
    return out;
}

auto make_jets_vr(RVec<Jet>& jets, const std::vector<TLorentzVector>& bs) {
    fastjet::contrib::VariableRPlugin vr_plug(
          60, 0.2, 7.5, fastjet::contrib::VariableRPlugin::AKTLIKE);
    const static fastjet::JetDefinition jet_def(&vr_plug);
    std::vector<fastjet::PseudoJet> all_particles =
          view::all(jets)
          | view::filter([](const Jet& jet) { return jet.Flavor == 5; })
          | view::transform([](const Jet& jet) -> fastjet::PseudoJet {
                auto p = fastjet::PseudoJet(jet.P4());
                p.set_user_index(0);
                return p;
            })
          | ranges::to<std::vector>();

    int i = 1;
    std::vector<fastjet::PseudoJet> b_pj =
          view::transform(bs,
                          [&i](const TLorentzVector& b) {
                              auto p = fastjet::PseudoJet();
                              p.reset_PtYPhiM(1E-9, b.Rapidity(), b.Phi(), 0.);
                              p.set_user_index(i++);
                              return p;
                          })
          | ranges::to<std::vector>();

    ranges::copy(b_pj, ranges::back_inserter(all_particles));

    fastjet::ClusterSequence cs(all_particles, jet_def);
    std::vector<TLorentzVector> out(4);

    for (auto&& jet : fastjet::sorted_by_pt(cs.inclusive_jets())) {
        auto parts = jet.constituents();
        int num_jets = ranges::count_if(
              parts, [](auto&& jet) { return jet.user_index() == 0; });
        int num_bs = parts.size() - num_jets;
        if (num_jets == 0 || num_bs == 0) {
            continue;
        }

        if (num_bs == 1) {
            auto&& cons_bs = parts | view::filter([](auto&& x) {
                                 return x.user_index() != 0;
                             });
            auto&& cons_jets = parts | view::filter([](auto&& x) {
                                   return x.user_index() == 0;
                               });
            auto&& b = ranges::front(cons_bs);
            if (num_jets == 1) {
                // one b and one jet -- easy
                auto&& j = ranges::front(cons_jets);
                out[b.user_index() - 1] =
                      TLorentzVector(j.px(), j.py(), j.pz(), j.E());
            }
            else {
                // multiple jets -- pick the one that's closest
                auto&& cons_jets = parts | view::filter([](auto&& x) {
                                       return x.user_index() == 0;
                                   });
                auto&& assoc = *ranges::min_element(
                      cons_jets, std::less{},
                      [&b](auto&& x) { return x.delta_R(b); });
                out[b.user_index() - 1] = TLorentzVector(assoc.px(), assoc.py(),
                                                         assoc.pz(), assoc.E());
            }
        }
        else {
            // multiple bs
            std::vector<fastjet::PseudoJet> bs =
                  parts
                  | view::filter([](auto&& x) { return x.user_index() != 0; })
                  | ranges::to<std::vector>();
            std::vector<fastjet::PseudoJet> cons_jets =
                  parts
                  | view::filter([](auto&& x) { return x.user_index() == 0; })
                  | ranges::to<std::vector>();

            // Define an ordering for b quarks and jets, so we can permute them
            auto pred = [](const fastjet::PseudoJet& a,
                           const fastjet::PseudoJet& b) {
                if (a.pt() == b.pt()) {
                    if (a.eta() == b.eta()) {
                        if (a.phi_std() == b.phi_std()) {
                            return false;
                        }
                        return a.phi_std() < b.phi_std();
                    }
                    return a.eta() < b.eta();
                }
                return a.pt() < b.pt();
            };
            ranges::sort(cons_jets, pred);
            ranges::sort(bs, pred);

            double min_sum = 999999.;
            if (num_bs >= num_jets) {
                // more bs -- assign a b to each jet
                // Find the assignment that minimizes
                // sum of deltaRs between jets and assigned bs
                std::vector<int> jet_assign(0, num_jets);
                do {
                    double sum = ranges::accumulate(
                          view::zip_with(
                                [](auto&& x, auto&& y) { return x.delta_R(y); },
                                bs, cons_jets),
                          0., std::plus{});
                    if (sum < min_sum) {
                        min_sum = sum;
                        jet_assign = bs | view::take(num_jets)
                                     | view::transform([](auto&& x) {
                                           return x.user_index();
                                       })
                                     | ranges::to<std::vector>();
                    }
                } while (ranges::next_permutation(bs, pred));
                for (int j = 0; j < num_jets; ++j) {
                    out[jet_assign[j] - 1] =
                          TLorentzVector(cons_jets[j].px(), cons_jets[j].py(),
                                         cons_jets[j].pz(), cons_jets[j].e());
                }
            }
            else {
                // assign a jet to each b -- save
                do {
                    double sum = ranges::accumulate(
                          view::zip_with(
                                [](auto&& x, auto&& y) { return x.delta_R(y); },
                                bs, cons_jets),
                          0., std::plus{});
                    if (sum < min_sum) {
                        min_sum = sum;
                        for (int j = 0; j < num_bs; ++j) {
                            out[bs[j].user_index() - 1] = TLorentzVector(
                                  cons_jets[j].px(), cons_jets[j].py(),
                                  cons_jets[j].pz(), cons_jets[j].e());
                        }
                    }
                } while (ranges::next_permutation(cons_jets, pred));
            }
        }

        if (num_jets >= 2 || num_bs >= 2) {
            cerr << "VR ERROR: Association jet contains more than one original "
                    "jet.\n";
            cerr << "Constituents: \n";
            for (auto&& c : parts) {
                cerr << "    [" << c.pt() << ", " << c.eta() << ", "
                     << c.phi_std() << ", " << c.E() << "] -- "
                     << (c.user_index() ? "B" : "Jet") << "\n";
            }
            cerr << "-------------------------------------------------\n";
            int count = 1;
            int last = parts.size();
            for (auto&& c : parts) {
                int count2 = 1;
                for (auto&& d : parts) {
                    if (count2 == 1) {
                        if (count == 1)
                            cerr << "⎡";
                        else if (count == last)
                            cerr << "⎣";
                        else
                            cerr << "⎢";
                    }
                    cerr << std::setprecision(4) << std::setw(6) << c.delta_R(d)
                         << ((count2 == last) ? "" : " ");
                    if (count2 == last) {
                        if (count == 1)
                            cerr << "⎤";
                        else if (count == last)
                            cerr << "⎦";
                        else
                            cerr << "⎥";
                    }
                    count2++;
                }
                count++;
                cerr << "\n";
            }
            cerr << "SELECTED JETS:\n";
            for (auto&& jet : out) {
                cerr << "[" << jet.Pt() << ", " << jet.Eta() << ", "
                     << jet.Phi() << ", " << jet.E() << "]\n";
            }
            cerr << "\n";
        }
    }

    return out;
}

void ExtractTruth(const char* output, vector<string> input) {
    auto df = ROOT::RDataFrame("Delphes", input);
    auto is_hh4b = df.Filter(
          [](RVec<GenParticle>& particles) {
              int n_higgs = 0;
              for (auto&& particle : particles) {
                  // Also skip intermediate, propagating, Higgs bosons
                  if (abs(particle.PID) != 25 or particle.D1 == particle.D2) {
                      continue;
                  }
                  ++n_higgs;
                  if (abs(particles[particle.D1].PID) != 5
                      or abs(particles[particle.D2].PID) != 5) {
                      // Non bb̅ decay of Higgs
                      return false;
                  }
              }
              if (n_higgs != 2) {
                  cout << "n_higgs = " << n_higgs << ", not 2\n";
                  return false;
              }
              return true;
          },
          {"Particle"}, "is_hh4b");

    auto bquarks = is_hh4b.Define(
          "b_quarks",
          [](RVec<GenParticle>& particles) {
              std::vector<TLorentzVector> bs{};
              for (auto&& particle : particles) {
                  if (abs(particle.PID) != 25 or particle.D1 == particle.D2) {
                      continue;
                  }
                  bs.push_back(particles[particle.D1].P4());
                  bs.push_back(particles[particle.D2].P4());
              }
              return bs;
          },
          {"Particle"});

    auto truth_jets =
          bquarks.Define("truth_jets", make_jets_fr, {"GenJet", "b_quarks"})
                .Define("truth_jets_vr", make_jets_vr, {"GenJetVR", "b_quarks"});
    auto truth_jets_nu =
          truth_jets
                .Define("truth_jets_nu", make_jets_fr, {"GenJetNu", "b_quarks"})
                .Define("truth_jets_vr_nu", make_jets_vr,
                        {"GenJetVRNu", "b_quarks"});
    auto reco_jets =
          truth_jets_nu.Define("reco_jets", make_jets_fr, {"Jet", "b_quarks"});
    auto cached =
          reco_jets.Cache({"b_quarks", "truth_jets", "truth_jets_nu",
                           "truth_jets_vr", "truth_jets_vr_nu", "reco_jets"});

    cached.Report()->Print();
    cout << "Defined" << endl;
    cached.Snapshot("truth", output,
                    {"b_quarks", "truth_jets", "truth_jets_nu", "truth_jets_vr",
                     "truth_jets_vr_nu", "reco_jets"});
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cout << "Usage: ExtractTruth output.root input_files\n";
        return 1;
    }

    vector<string> input{};
    for (int i = 2; i < argc; ++i) {
        input.push_back(argv[i]);
    }
    ExtractTruth(argv[1], input);
    return 0;
}
