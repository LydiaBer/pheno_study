//Reconstruction of Intermediate Events

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

#include "utils.h"
#include "Cutflow.h"


using namespace ROOT;
namespace view = ranges::view;
namespace action = ranges::action;

constexpr double GeV = 1.; ///< Set to 1 -- energies and momenta in GeV


bool one_b_large_two_b_small_cuts(VecOps::RVec<Jet> &jets,VecOps::RVec<Jet> &fatjets){

	int count_small = 0;
	int b_count_small = 0; // Counting b tagged small-R jets
	int count_fat= 0;
	int b_count_fat= 0; // Counting b tagged large-R jets
	bool fat_jet = false;
	bool small_jet = false;


	//Filter small R jets with 2 pT>40 and |eta|< 2.5 & btagged
	for ( auto &&j:jets){
	if (j.PT >=40. *GeV and std::abs(j.Eta) <2.5){
	count_small ++;
	if (j.BTag) b_count_small++; 
		}
	}
	if (count_small >=2 and b_count_small>= 2) small_jet = true;


	//Filter large R jet 1 pT>200 and |eta|<2. & btagged
	for ( auto &&j:fatjets) {
	if (j.PT >20. *GeV and std::abs(j.Eta)< 2.0){
	count_fat ++;
	if (j.BTag)
	b_count_fat ++;}
	}
	if ( count_fat > 1 and b_count_fat == 1){
		fat_jet=true ; 
	}

	//std::cout<<"Jet"<<count_small<<std::endl;
	if (b_count_fat !=0) std::cout<<"Fat_b_Jet"<<b_count_fat<<std::endl;

	if ( fat_jet && small_jet){return true;}
	else {return false;}


}

double deltaR(OxJet &jet1, OxJet &jet2){
	using namespace std;
	
	double dphi = jet1.p4.Phi() - jet2.p4.Phi();
	double deta = jet1.p4.Eta() - jet2.p4.Eta();
	
	double dR = sqrt(pow(dphi,2.) + pow(deta,2.));
}

//Reconstructed event in the intermediate regime
reconstructed_event reconstruct(VecOps::RVec<Jet> &smalljet,VecOps::RVec<Jet> &largejet,
				 VecOps::RVec<HepMCEvent> &evt){
	reconstructed_event result{};
 	
	result.wgt = evt[0].Weight;
	//large R jets vector
	std::vector<OxJet> lj_vec = 
		view::zip_with(make_jet,largejet) | view::filter([](const auto &jet){
		return jet.p4.Pt() >= 20. *GeV and std::abs(jet.p4.Eta()) <2.0;
		});
	//small R jets vector
	std::vector<OxJet> sj_vec =
		view::zip_with(make_jet,smalljet) | view::filter([](const auto &jet){
		return jet.p4.Pt() >= 40. *GeV and std::abs(jet.p4.Eta())< 2.5;
		});

	ranges::sort(lj_vec, ranges::ordered_less{},
			[](auto &&jet) {return jet.p4.Pt();});
        ranges::sort(sj_vec, ranges::ordered_less{},
                        [](auto &&jet) {return jet.p4.Pt();});	
	ranges::reverse(lj_vec);
	ranges::reverse(sj_vec);

	const int n_small_tag =
	ranges::count(sj_vec, true, [](auto &&jet) {return jet.tagged;});
	const int n_large_tag = 
	ranges::count(lj_vec, true, [](auto &&jet){return jet.tagged;});
	

//	std::cout<<"Small_tagged"<<n_small_tag<<std::endl;
//	std::cout<<"Large_tagged"<<n_large_tag<<std::endl;

	
	OxJet large_jet = lj_vec[0];
	std::vector<OxJet> small_jets = sj_vec | view::filter([](auto &&jet){ return jet.tagged;});
	std::vector<OxJet> other_jets = sj_vec | view::filter([](auto &jet){return !jet.tagged;});

	//There could be only one non btag jet. Maybe change it because not strictly necessary
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
	if (n_small_tag <2){
	result.valid = false;
	return result;}
	
	//Cut on DeltaR<1.2 between small R jets and Large R jet
	
	std::vector<OxJet> bjets_separated;
	for (auto &&j: small_jets){
	if ( deltaR(large_jet,j) < 1.2) continue;
	
	if (bjets_separated.size()<2){
	bjets_separated.push_back(j);	
	} 
	}
 	  
	if (bjets_separated.size()<2){
	result.valid = false; 
	return result;}
	//Get the pairing that minimizes relative mass difference
	
	 
	std::vector<JetPair> jets_pair= 
	view::zip_with(make_pair,bjets_separated,bjets_separated);
 
	jets_pair |= (action::sort(ranges::ordered_less{},[large_jet]
	(auto && jet_pair) {
	double mass_a = jet_pair.mass_1;
	double mass_b = jet_pair.mass_2;
	std::cout<<"mass 2"<< mass_b <<std::endl;
	double djmassdiff = std::fabs(large_jet.p4.M() - (mass_a+mass_b));
	//std::cout<<"dijets mass difference"<<djmassdiff<<std::endl;

	return djmassdiff;
	}) |
	action::take(1));  	


	//Printing
	std::cout<<"Jets Pair 0"<<jets_pair[0].jet_1.p4.M()<<std::endl;
	std::cout<<"Jets Pair 1"<<jets_pair[0].jet_2.p4.M()<<std::endl;
	std::cout<<"Large jet"<<large_jet.p4.M()<<std::endl;
	//Storing the candidates
	
	result.higgs2.p4 = jets_pair[0].jet_1.p4 + jets_pair[0].jet_2.p4;
	result.higgs1.p4 = large_jet.p4;
	result.n_small_tag = n_small_tag; 	
	result.n_small_jets = sj_vec.size(); 
	result.n_large_tag = n_large_tag;
	result.n_large_jets = lj_vec.size();			
	result.large_jet = large_jet;
	result.small_jets[0] = jets_pair[0].jet_1;
	result.small_jets[1] = jets_pair[0].jet_2;

	if(result.small_jets[1].p4.Pt() > result.small_jets[0].p4.Pt()){
	result.small_jets[0] = jets_pair[0].jet_2;
	result.small_jets[1] = jets_pair[0].jet_1;
	}
	
return result;
}



bool valid_check(const reconstructed_event &evt){return evt.valid;}

bool signal(const reconstructed_event &evt) {
  double m_h1 = evt.higgs1.p4.M();
  double m_h2 = evt.higgs2.p4.M();
  // Cut in a mass window of 80 GeV around 125 GeV for both Higgs
  bool higgs1_flag = (std::abs(evt.higgs1.p4.M() - 125.) < 40.) ? true : false;
  bool higgs2_flag = (std::abs(evt.higgs2.p4.M() - 125.) < 40.) ? true : false;
  return (higgs1_flag && higgs2_flag);
}



int main( int arc, char *argv[]){

std::ios::sync_with_stdio(false);
using vec_string= std::vector<std::string>;


ROOT::EnableImplicitMT();

//RDataFrame frame("Delphes","/data/atlas/atlasdata/micheli/4b/Events/run_02/tag_1_delphes_events.root");
RDataFrame frame("Delphes","/data/atlas/atlasdata/micheli/delphes_out.root");

//std::cout<<"Flag 1"<<std::endl;
 
auto three_jets = frame.Filter(one_b_large_two_b_small_cuts,{"Jet","FatJet"},u8"Intermediate analysis cuts");

//std::cout<<"flag 2"<<std::endl;
auto reconstructed = three_jets.Define("event", reconstruct,{"Jet","FatJet","Event"});

auto valid_evt = reconstructed.Filter(valid_check,{"event"},"valid events");

//auto signal_result = reconstructed.Filter(signal, {"event"}, "signal");
/*auto control_result = deltaRjj_cut.Filter(
      [](const reconstructed_event &event) {
        return control(event) && (!signal(event));
      },
      {"event"}, "control");
  auto sideband_result = deltaRjj_cut.Filter(
      [](const reconstructed_event &event) {
        return sideband(event) && !control(event);
      },
      {"event"}, "sideband");
*/

 std::string output_filename = "pheno_intermediate.root";

  fmt::print("Writing to {}\n", output_filename);

auto start_events_proxy = frame.Count();
start_events_proxy.OnPartialResult(
      10000, [](const unsigned long long &num_events) {
      fmt::print("Processed {} events\n", num_events);
      });

TFile output_file(output_filename.c_str(), "RECREATE");


write_tree(valid_evt, "signal", output_file);
//write_tree(control_result, "control", output_file);
//write_tree(sideband_result, "sideband", output_file);

start_events_proxy.GetValue(); // For printing progress

 // Write cutflows
//   auto intermediate_tag_filter = [](const reconstructed_event &evt) {
  //      return evt.n_small_tag == 2 and evt.n_large_tag == 1;
    //      };

Cutflow intermediate_cutflow("Intermediate Cutflow", output_file);
  	intermediate_cutflow.add(u8"2 small good jets(pT ≥ 40 GeV, η ≤ 2.5), ≥ 2 tagged, 1 large good jet",
                      three_jets.Count());
 	intermediate_cutflow.add(u8"Reconstructed events",
                      reconstructed.Count());
 	intermediate_cutflow.add(u8"1 large jet  and 2 small jets Tagged",
                      valid_evt.Count());
 	//intermediate_cutflow.add(u8"Signal",
          //            signal_result.Count());

	intermediate_cutflow.write();


return 0;



}
