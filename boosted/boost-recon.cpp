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



bool two_large_b_jets(VecOps::RVec<Jet> &jets){

	int count =0;
	int b_count = 0;

	for (auto &&j:jets){
	if (j.PT>=20.*GeV and std::abs(j.Eta)<2.5){
	count ++;
	if (j.BTag) b_count ++; 
	}
	if (count >2 and b_count>2) return true; 
	}
}



reconstructed_event reconstruct(VecOps::RVec<Jet> &jet, VecOps::RVec<HepMCEvent> &evt){

	reconstructed_event result{};
	result.wgt = evt[0].Weight;

	std::vector<OxJet> lj_vec=
	view::zip_with(make_jet,jet) | view::filter([](const auto &jet){
	return jet.p4.Pt() >=20.*GeV and std::abs(jet.p4.Eta())<2.5;
	});	

	ranges::sort(lj_vec, ranges::ordered_less{},
			[](auto &&jet){return jet.p4.Pt();});
	ranges::reverse(lj_vec);
	const int count = lj_vec.size();
	const int ntag =
        ranges::count(lj_vec, true, [](auto &&jet){return jet.tagged;});


	OxJet leading = lj_vec[0];
	OxJet subleading = lj_vec[1]; 

	if (leading.tagged == false or subleading.tagged == false){
	result.valid = false;
	return result;
	}
	
	//Higgs Reconstruction
	result.higgs1.p4 = leading.p4;
	result.higgs2.p4 = subleading.p4;
	result.jets[0]= leading;
	result.jets[1]= subleading;
	result.ntag = ntag;
	result.njets = count;

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


auto two_b_jets = frame.Filter(two_large_b_jets,{"FatJet"},u8"Resolved analysis cuts");

auto reconstructed = two_b_jets.Define("event", reconstruct, {"FatJet","Event"});

auto valid_evt = reconstructed.Filter(valid_check,{"event"},"valid events");

//auto signal_result = reconstructed.Filter(signal,{"event"},"signal");





std::string output_filename = "pheno_boosted.root";

fmt::print("Writing to {}\n", output_filename);

auto start_events_proxy = frame.Count();
start_events_proxy.OnPartialResult(
      10000, [](const unsigned long long &num_events) {
      fmt::print("Processed {} events\n", num_events);
      });

TFile output_file(output_filename.c_str(), "RECREATE");
write_tree(valid_evt, "signal", output_file);

start_events_proxy.GetValue();

return 0;


} 
