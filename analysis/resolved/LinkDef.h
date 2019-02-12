#ifndef __LINKDEF_H_
#define __LINKDEF_H_
#if defined(__ROOTCLING__)
#pragma link C++ nestedclasses;
#pragma link C++ class higgs;
#pragma link C++ class Muon;
#pragma link C++ class Jet;
#pragma link C++ class reconstructed_event;
#pragma link C++ class out_format;
#pragma link C++ class reweight_format;
#pragma link C++ class TriggerTest;
#pragma link C++ class Cutflow;
#pragma link C++ class TLorentzVector;
#pragma link C++ class std::vector<TLorentzVector>;
#endif // __LINKDEF_H_
