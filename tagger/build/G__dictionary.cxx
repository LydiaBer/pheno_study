// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME G__dictionary

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "/data/atlas/atlasdata/micheli/tagger/utils.h"
#include "/data/atlas/atlasdata/micheli/tagger/Cutflow.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static void *new_Muon(void *p = 0);
   static void *newArray_Muon(Long_t size, void *p);
   static void delete_Muon(void *p);
   static void deleteArray_Muon(void *p);
   static void destruct_Muon(void *p);
   static void streamer_Muon(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Muon*)
   {
      ::Muon *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Muon >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Muon", ::Muon::Class_Version(), "classes/DelphesClasses.h", 320,
                  typeid(::Muon), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Muon::Dictionary, isa_proxy, 16,
                  sizeof(::Muon) );
      instance.SetNew(&new_Muon);
      instance.SetNewArray(&newArray_Muon);
      instance.SetDelete(&delete_Muon);
      instance.SetDeleteArray(&deleteArray_Muon);
      instance.SetDestructor(&destruct_Muon);
      instance.SetStreamerFunc(&streamer_Muon);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Muon*)
   {
      return GenerateInitInstanceLocal((::Muon*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Muon*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Jet(void *p = 0);
   static void *newArray_Jet(Long_t size, void *p);
   static void delete_Jet(void *p);
   static void deleteArray_Jet(void *p);
   static void destruct_Jet(void *p);
   static void streamer_Jet(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Jet*)
   {
      ::Jet *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Jet >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Jet", ::Jet::Class_Version(), "classes/DelphesClasses.h", 351,
                  typeid(::Jet), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Jet::Dictionary, isa_proxy, 16,
                  sizeof(::Jet) );
      instance.SetNew(&new_Jet);
      instance.SetNewArray(&newArray_Jet);
      instance.SetDelete(&delete_Jet);
      instance.SetDeleteArray(&deleteArray_Jet);
      instance.SetDestructor(&destruct_Jet);
      instance.SetStreamerFunc(&streamer_Jet);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Jet*)
   {
      return GenerateInitInstanceLocal((::Jet*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Jet*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static TClass *higgs_Dictionary();
   static void higgs_TClassManip(TClass*);
   static void *new_higgs(void *p = 0);
   static void *newArray_higgs(Long_t size, void *p);
   static void delete_higgs(void *p);
   static void deleteArray_higgs(void *p);
   static void destruct_higgs(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::higgs*)
   {
      ::higgs *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::higgs));
      static ::ROOT::TGenericClassInfo 
         instance("higgs", "", 37,
                  typeid(::higgs), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &higgs_Dictionary, isa_proxy, 0,
                  sizeof(::higgs) );
      instance.SetNew(&new_higgs);
      instance.SetNewArray(&newArray_higgs);
      instance.SetDelete(&delete_higgs);
      instance.SetDeleteArray(&deleteArray_higgs);
      instance.SetDestructor(&destruct_higgs);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::higgs*)
   {
      return GenerateInitInstanceLocal((::higgs*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::higgs*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *higgs_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::higgs*)0x0)->GetClass();
      higgs_TClassManip(theClass);
   return theClass;
   }

   static void higgs_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *reconstructed_event_Dictionary();
   static void reconstructed_event_TClassManip(TClass*);
   static void *new_reconstructed_event(void *p = 0);
   static void *newArray_reconstructed_event(Long_t size, void *p);
   static void delete_reconstructed_event(void *p);
   static void deleteArray_reconstructed_event(void *p);
   static void destruct_reconstructed_event(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::reconstructed_event*)
   {
      ::reconstructed_event *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::reconstructed_event));
      static ::ROOT::TGenericClassInfo 
         instance("reconstructed_event", "", 307,
                  typeid(::reconstructed_event), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &reconstructed_event_Dictionary, isa_proxy, 0,
                  sizeof(::reconstructed_event) );
      instance.SetNew(&new_reconstructed_event);
      instance.SetNewArray(&newArray_reconstructed_event);
      instance.SetDelete(&delete_reconstructed_event);
      instance.SetDeleteArray(&deleteArray_reconstructed_event);
      instance.SetDestructor(&destruct_reconstructed_event);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::reconstructed_event*)
   {
      return GenerateInitInstanceLocal((::reconstructed_event*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::reconstructed_event*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *reconstructed_event_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::reconstructed_event*)0x0)->GetClass();
      reconstructed_event_TClassManip(theClass);
   return theClass;
   }

   static void reconstructed_event_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *out_format_Dictionary();
   static void out_format_TClassManip(TClass*);
   static void *new_out_format(void *p = 0);
   static void *newArray_out_format(Long_t size, void *p);
   static void delete_out_format(void *p);
   static void deleteArray_out_format(void *p);
   static void destruct_out_format(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::out_format*)
   {
      ::out_format *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::out_format));
      static ::ROOT::TGenericClassInfo 
         instance("out_format", "", 325,
                  typeid(::out_format), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &out_format_Dictionary, isa_proxy, 0,
                  sizeof(::out_format) );
      instance.SetNew(&new_out_format);
      instance.SetNewArray(&newArray_out_format);
      instance.SetDelete(&delete_out_format);
      instance.SetDeleteArray(&deleteArray_out_format);
      instance.SetDestructor(&destruct_out_format);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::out_format*)
   {
      return GenerateInitInstanceLocal((::out_format*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::out_format*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *out_format_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::out_format*)0x0)->GetClass();
      out_format_TClassManip(theClass);
   return theClass;
   }

   static void out_format_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *reweight_format_Dictionary();
   static void reweight_format_TClassManip(TClass*);
   static void *new_reweight_format(void *p = 0);
   static void *newArray_reweight_format(Long_t size, void *p);
   static void delete_reweight_format(void *p);
   static void deleteArray_reweight_format(void *p);
   static void destruct_reweight_format(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::reweight_format*)
   {
      ::reweight_format *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::reweight_format));
      static ::ROOT::TGenericClassInfo 
         instance("reweight_format", "", 352,
                  typeid(::reweight_format), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &reweight_format_Dictionary, isa_proxy, 0,
                  sizeof(::reweight_format) );
      instance.SetNew(&new_reweight_format);
      instance.SetNewArray(&newArray_reweight_format);
      instance.SetDelete(&delete_reweight_format);
      instance.SetDeleteArray(&deleteArray_reweight_format);
      instance.SetDestructor(&destruct_reweight_format);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::reweight_format*)
   {
      return GenerateInitInstanceLocal((::reweight_format*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::reweight_format*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *reweight_format_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::reweight_format*)0x0)->GetClass();
      reweight_format_TClassManip(theClass);
   return theClass;
   }

   static void reweight_format_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *Cutflow_Dictionary();
   static void Cutflow_TClassManip(TClass*);
   static void *new_Cutflow(void *p = 0);
   static void *newArray_Cutflow(Long_t size, void *p);
   static void delete_Cutflow(void *p);
   static void deleteArray_Cutflow(void *p);
   static void destruct_Cutflow(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Cutflow*)
   {
      ::Cutflow *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::Cutflow));
      static ::ROOT::TGenericClassInfo 
         instance("Cutflow", "", 13,
                  typeid(::Cutflow), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &Cutflow_Dictionary, isa_proxy, 0,
                  sizeof(::Cutflow) );
      instance.SetNew(&new_Cutflow);
      instance.SetNewArray(&newArray_Cutflow);
      instance.SetDelete(&delete_Cutflow);
      instance.SetDeleteArray(&deleteArray_Cutflow);
      instance.SetDestructor(&destruct_Cutflow);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Cutflow*)
   {
      return GenerateInitInstanceLocal((::Cutflow*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Cutflow*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *Cutflow_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::Cutflow*)0x0)->GetClass();
      Cutflow_TClassManip(theClass);
   return theClass;
   }

   static void Cutflow_TClassManip(TClass* ){
   }

} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr Muon::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Muon::Class_Name()
{
   return "Muon";
}

//______________________________________________________________________________
const char *Muon::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Muon*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Muon::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Muon*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Muon::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Muon*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Muon::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Muon*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Jet::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Jet::Class_Name()
{
   return "Jet";
}

//______________________________________________________________________________
const char *Jet::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Jet*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Jet::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Jet*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Jet::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Jet*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Jet::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Jet*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void Muon::Streamer(TBuffer &R__b)
{
   // Stream an object of class Muon.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      SortableObject::Streamer(R__b);
      R__b >> PT;
      R__b >> Eta;
      R__b >> Phi;
      R__b >> T;
      R__b >> Charge;
      Particle.Streamer(R__b);
      R__b >> IsolationVar;
      R__b >> IsolationVarRhoCorr;
      R__b >> SumPtCharged;
      R__b >> SumPtNeutral;
      R__b >> SumPtChargedPU;
      R__b >> SumPt;
      R__b.CheckByteCount(R__s, R__c, Muon::IsA());
   } else {
      R__c = R__b.WriteVersion(Muon::IsA(), kTRUE);
      SortableObject::Streamer(R__b);
      R__b << PT;
      R__b << Eta;
      R__b << Phi;
      R__b << T;
      R__b << Charge;
      Particle.Streamer(R__b);
      R__b << IsolationVar;
      R__b << IsolationVarRhoCorr;
      R__b << SumPtCharged;
      R__b << SumPtNeutral;
      R__b << SumPtChargedPU;
      R__b << SumPt;
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Muon(void *p) {
      return  p ? new(p) ::Muon : new ::Muon;
   }
   static void *newArray_Muon(Long_t nElements, void *p) {
      return p ? new(p) ::Muon[nElements] : new ::Muon[nElements];
   }
   // Wrapper around operator delete
   static void delete_Muon(void *p) {
      delete ((::Muon*)p);
   }
   static void deleteArray_Muon(void *p) {
      delete [] ((::Muon*)p);
   }
   static void destruct_Muon(void *p) {
      typedef ::Muon current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_Muon(TBuffer &buf, void *obj) {
      ((::Muon*)obj)->::Muon::Streamer(buf);
   }
} // end of namespace ROOT for class ::Muon

//______________________________________________________________________________
void Jet::Streamer(TBuffer &R__b)
{
   // Stream an object of class Jet.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      SortableObject::Streamer(R__b);
      R__b >> PT;
      R__b >> Eta;
      R__b >> Phi;
      R__b >> T;
      R__b >> Mass;
      R__b >> DeltaEta;
      R__b >> DeltaPhi;
      R__b >> Flavor;
      R__b >> FlavorAlgo;
      R__b >> FlavorPhys;
      R__b >> BTag;
      R__b >> BTagAlgo;
      R__b >> BTagPhys;
      R__b >> TauTag;
      R__b >> Charge;
      R__b >> EhadOverEem;
      R__b >> NCharged;
      R__b >> NNeutrals;
      R__b >> Beta;
      R__b >> BetaStar;
      R__b >> MeanSqDeltaR;
      R__b >> PTD;
      R__b.ReadStaticArray((float*)FracPt);
      R__b.ReadStaticArray((float*)Tau);
      SoftDroppedJet.Streamer(R__b);
      SoftDroppedSubJet1.Streamer(R__b);
      SoftDroppedSubJet2.Streamer(R__b);
      int R__i;
      for (R__i = 0; R__i < 5; R__i++)
         TrimmedP4[R__i].Streamer(R__b);
      for (R__i = 0; R__i < 5; R__i++)
         PrunedP4[R__i].Streamer(R__b);
      for (R__i = 0; R__i < 5; R__i++)
         SoftDroppedP4[R__i].Streamer(R__b);
      R__b >> NSubJetsTrimmed;
      R__b >> NSubJetsPruned;
      R__b >> NSubJetsSoftDropped;
      Constituents.Streamer(R__b);
      Particles.Streamer(R__b);
      Area.Streamer(R__b);
      R__b.CheckByteCount(R__s, R__c, Jet::IsA());
   } else {
      R__c = R__b.WriteVersion(Jet::IsA(), kTRUE);
      SortableObject::Streamer(R__b);
      R__b << PT;
      R__b << Eta;
      R__b << Phi;
      R__b << T;
      R__b << Mass;
      R__b << DeltaEta;
      R__b << DeltaPhi;
      R__b << Flavor;
      R__b << FlavorAlgo;
      R__b << FlavorPhys;
      R__b << BTag;
      R__b << BTagAlgo;
      R__b << BTagPhys;
      R__b << TauTag;
      R__b << Charge;
      R__b << EhadOverEem;
      R__b << NCharged;
      R__b << NNeutrals;
      R__b << Beta;
      R__b << BetaStar;
      R__b << MeanSqDeltaR;
      R__b << PTD;
      R__b.WriteArray(FracPt, 5);
      R__b.WriteArray(Tau, 5);
      SoftDroppedJet.Streamer(R__b);
      SoftDroppedSubJet1.Streamer(R__b);
      SoftDroppedSubJet2.Streamer(R__b);
      int R__i;
      for (R__i = 0; R__i < 5; R__i++)
         TrimmedP4[R__i].Streamer(R__b);
      for (R__i = 0; R__i < 5; R__i++)
         PrunedP4[R__i].Streamer(R__b);
      for (R__i = 0; R__i < 5; R__i++)
         SoftDroppedP4[R__i].Streamer(R__b);
      R__b << NSubJetsTrimmed;
      R__b << NSubJetsPruned;
      R__b << NSubJetsSoftDropped;
      Constituents.Streamer(R__b);
      Particles.Streamer(R__b);
      Area.Streamer(R__b);
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Jet(void *p) {
      return  p ? new(p) ::Jet : new ::Jet;
   }
   static void *newArray_Jet(Long_t nElements, void *p) {
      return p ? new(p) ::Jet[nElements] : new ::Jet[nElements];
   }
   // Wrapper around operator delete
   static void delete_Jet(void *p) {
      delete ((::Jet*)p);
   }
   static void deleteArray_Jet(void *p) {
      delete [] ((::Jet*)p);
   }
   static void destruct_Jet(void *p) {
      typedef ::Jet current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_Jet(TBuffer &buf, void *obj) {
      ((::Jet*)obj)->::Jet::Streamer(buf);
   }
} // end of namespace ROOT for class ::Jet

namespace ROOT {
   // Wrappers around operator new
   static void *new_higgs(void *p) {
      return  p ? new(p) ::higgs : new ::higgs;
   }
   static void *newArray_higgs(Long_t nElements, void *p) {
      return p ? new(p) ::higgs[nElements] : new ::higgs[nElements];
   }
   // Wrapper around operator delete
   static void delete_higgs(void *p) {
      delete ((::higgs*)p);
   }
   static void deleteArray_higgs(void *p) {
      delete [] ((::higgs*)p);
   }
   static void destruct_higgs(void *p) {
      typedef ::higgs current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::higgs

namespace ROOT {
   // Wrappers around operator new
   static void *new_reconstructed_event(void *p) {
      return  p ? new(p) ::reconstructed_event : new ::reconstructed_event;
   }
   static void *newArray_reconstructed_event(Long_t nElements, void *p) {
      return p ? new(p) ::reconstructed_event[nElements] : new ::reconstructed_event[nElements];
   }
   // Wrapper around operator delete
   static void delete_reconstructed_event(void *p) {
      delete ((::reconstructed_event*)p);
   }
   static void deleteArray_reconstructed_event(void *p) {
      delete [] ((::reconstructed_event*)p);
   }
   static void destruct_reconstructed_event(void *p) {
      typedef ::reconstructed_event current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::reconstructed_event

namespace ROOT {
   // Wrappers around operator new
   static void *new_out_format(void *p) {
      return  p ? new(p) ::out_format : new ::out_format;
   }
   static void *newArray_out_format(Long_t nElements, void *p) {
      return p ? new(p) ::out_format[nElements] : new ::out_format[nElements];
   }
   // Wrapper around operator delete
   static void delete_out_format(void *p) {
      delete ((::out_format*)p);
   }
   static void deleteArray_out_format(void *p) {
      delete [] ((::out_format*)p);
   }
   static void destruct_out_format(void *p) {
      typedef ::out_format current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::out_format

namespace ROOT {
   // Wrappers around operator new
   static void *new_reweight_format(void *p) {
      return  p ? new(p) ::reweight_format : new ::reweight_format;
   }
   static void *newArray_reweight_format(Long_t nElements, void *p) {
      return p ? new(p) ::reweight_format[nElements] : new ::reweight_format[nElements];
   }
   // Wrapper around operator delete
   static void delete_reweight_format(void *p) {
      delete ((::reweight_format*)p);
   }
   static void deleteArray_reweight_format(void *p) {
      delete [] ((::reweight_format*)p);
   }
   static void destruct_reweight_format(void *p) {
      typedef ::reweight_format current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::reweight_format

namespace ROOT {
   // Wrappers around operator new
   static void *new_Cutflow(void *p) {
      return  p ? new(p) ::Cutflow : new ::Cutflow;
   }
   static void *newArray_Cutflow(Long_t nElements, void *p) {
      return p ? new(p) ::Cutflow[nElements] : new ::Cutflow[nElements];
   }
   // Wrapper around operator delete
   static void delete_Cutflow(void *p) {
      delete ((::Cutflow*)p);
   }
   static void deleteArray_Cutflow(void *p) {
      delete [] ((::Cutflow*)p);
   }
   static void destruct_Cutflow(void *p) {
      typedef ::Cutflow current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Cutflow

namespace {
  void TriggerDictionaryInitialization_libdictionary_Impl() {
    static const char* headers[] = {
"/data/atlas/atlasdata/micheli/tagger/utils.h",
"/data/atlas/atlasdata/micheli/tagger/Cutflow.h",
0
    };
    static const char* includePaths[] = {
"/cvmfs/sft-nightlies.cern.ch/lcg/views/dev4/Thu/x86_64-slc6-gcc7-opt/include",
"/data/atlas/atlasdata/micheli/tagger/include",
"/cvmfs/sft-nightlies.cern.ch/lcg/nightlies/dev4/Thu/ROOT/v6-14-00-patches/x86_64-slc6-gcc7-opt/include",
"/data/atlas/atlasdata/micheli/tagger/build/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "libdictionary dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  __attribute__((annotate("$clingAutoload$/data/atlas/atlasdata/micheli/tagger/utils.h")))  Muon;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  __attribute__((annotate("$clingAutoload$/data/atlas/atlasdata/micheli/tagger/utils.h")))  Jet;
struct __attribute__((annotate("$clingAutoload$/data/atlas/atlasdata/micheli/tagger/utils.h")))  higgs;
struct __attribute__((annotate("$clingAutoload$/data/atlas/atlasdata/micheli/tagger/utils.h")))  reconstructed_event;
struct __attribute__((annotate("$clingAutoload$/data/atlas/atlasdata/micheli/tagger/utils.h")))  out_format;
struct __attribute__((annotate("$clingAutoload$/data/atlas/atlasdata/micheli/tagger/utils.h")))  reweight_format;
class __attribute__((annotate("$clingAutoload$/data/atlas/atlasdata/micheli/tagger/Cutflow.h")))  Cutflow;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "libdictionary dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
#include "/data/atlas/atlasdata/micheli/tagger/utils.h"
#include "/data/atlas/atlasdata/micheli/tagger/Cutflow.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"Cutflow", payloadCode, "@",
"Jet", payloadCode, "@",
"Muon", payloadCode, "@",
"higgs", payloadCode, "@",
"out_format", payloadCode, "@",
"reconstructed_event", payloadCode, "@",
"reweight_format", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libdictionary",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libdictionary_Impl, {}, classesHeaders, /*has no C++ module*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libdictionary_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libdictionary() {
  TriggerDictionaryInitialization_libdictionary_Impl();
}
