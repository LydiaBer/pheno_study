#include <ROOT/RVec.hxx>
#include <vector>
#include <TLorentzVector.h>

#ifdef __CLING__
#pragma link C++ class TLorentzVector+;
#pragma link C++ class vector<TLorentzVector>+;
#pragma link C++ class vector<TLorentzVector,ROOT::Detail::VecOps::RAdoptAllocator<TLorentzVector> >;
#pragma link C++ class TVector2+;
#pragma link C++ class vector<TVector2>+;
#pragma link C++ class vector<TVector2,ROOT::Detail::VecOps::RAdoptAllocator<TVector2> >;
#endif
