//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Feb 19 15:22:04 2016 by ROOT version 5.34/34
// from TTree MMFE8/MMFE8
// found on file: fakefile.dat.root
//////////////////////////////////////////////////////////

#ifndef MMFE8Base_h
#define MMFE8Base_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class MMFE8Base {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   // Int_t           MMFE8;
   Int_t           VMM;
   Int_t           CHword;
   Int_t           CHpulse;
   Int_t           PDO;
   Int_t           TDO;
   Int_t           BCID;
   Int_t           BCIDgray;
   Int_t           TPDAC;
   Int_t           THDAC;
   Int_t           Delay;
   Int_t           TACslope;
   Int_t           PeakTime;
   Int_t           PulseNum;

   // List of branches
   // TBranch        *b_MMFE8;
   TBranch        *b_VMM;   //!
   TBranch        *b_CHword;   //!
   TBranch        *b_CHpulse;   //!
   TBranch        *b_PDO;   //!
   TBranch        *b_TDO;   //!
   TBranch        *b_BCID;   //!
   TBranch        *b_BCIDgray;   //!
   TBranch        *b_TPDAC;   //!
   TBranch        *b_THDAC;   //!
   TBranch        *b_Delay;   //!
   TBranch        *b_TACslope;   //!
   TBranch        *b_PeakTime;   //!
   TBranch        *b_PulseNum;   //!

   MMFE8Base(TTree *tree=0);
   virtual ~MMFE8Base();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

inline MMFE8Base::MMFE8Base(TTree *tree) : fChain(0)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("fakefile.dat.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("fakefile.dat.root");
      }
      f->GetObject("MMFE8",tree);

   }
   Init(tree);
}

inline MMFE8Base::~MMFE8Base()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

inline Int_t MMFE8Base::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
inline Long64_t MMFE8Base::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

inline void MMFE8Base::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   // fChain->SetBranchAddress("MMFE8", &MMFE8, &b_MMFE8);
   fChain->SetBranchAddress("VMM", &VMM, &b_VMM);
   fChain->SetBranchAddress("CHword", &CHword, &b_CHword);
   fChain->SetBranchAddress("CHpulse", &CHpulse, &b_CHpulse);
   fChain->SetBranchAddress("PDO", &PDO, &b_PDO);
   fChain->SetBranchAddress("TDO", &TDO, &b_TDO);
   fChain->SetBranchAddress("BCID", &BCID, &b_BCID);
   fChain->SetBranchAddress("BCIDgray", &BCIDgray, &b_BCIDgray);
   fChain->SetBranchAddress("TPDAC", &TPDAC, &b_TPDAC);
   fChain->SetBranchAddress("THDAC", &THDAC, &b_THDAC);
   fChain->SetBranchAddress("Delay", &Delay, &b_Delay);
   fChain->SetBranchAddress("TACslope", &TACslope, &b_TACslope);
   fChain->SetBranchAddress("PeakTime", &PeakTime, &b_PeakTime);
   fChain->SetBranchAddress("PulseNum", &PulseNum, &b_PulseNum);
   Notify();
}

inline Bool_t MMFE8Base::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

inline void MMFE8Base::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}

inline Int_t MMFE8Base::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
