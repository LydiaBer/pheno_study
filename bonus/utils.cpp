//Jet Clustering and Tagging

#include "utils.h"
#include "MCUtils/PIDUtils.h" // MCUtils Library (Available in Athena)
#include <cmath>
#include <cstdlib>
#include <vector>

void get_assoc_trkjets(const fastjet::PseudoJet& calojet, std::vector<fastjet::PseudoJet> trkjets,
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
            // 	  if(trkjets.at(iter).pt() > 20. && fabs(trkjets.at(iter).eta()) < 2.5 )
            // matched_trkjets.push_back(trkjets.at(iter));
            matched_trkjets.push_back(trkjets.at(iter));
        }
    }

    // Sort matched jets by pt
    matched_trkjets = sorted_by_pt(matched_trkjets);

    return;
}

void flavour_algo(const std::vector<int> b_tag, const std::vector<int> c_tag,const std::vector<int> ph_tag,
	 	  std::vec<int> s_vec_tag){

		if ( b_tag.at(0) > 0 || b_tag.at(1) >0) s_vec_tag.at(0) = 1; // BTagged
		if ( c_tag.at(0) >0 || c_tag.at(1) >0  && s_vec_tag.at(0)!=1) s_vec_tag.at(1) = 1; // CTagged
		if ( ph_tag.at(0)>0 || ph_tag.at(1) >0 
		    && s_vec_tag.at(0)!= 1 && s_vec_tag.at(1)!=1) s_vec_tag.at(2) = 1; //Light Tagged   

		return;

}

void tagging_algo(	const fastjet::PseudoJet& calojet,
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
