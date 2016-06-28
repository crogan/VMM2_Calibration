//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Feb 19 15:22:04 2016 by ROOT version 5.34/34
// from TTree MMFE8/MMFE8
// found on file: fakefile.dat.root
//////////////////////////////////////////////////////////

#ifndef XADCBASE_h
#define XADCBASE_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class xADCBase {
public :
  TTree          *fChain;   //!pointer to the analyzed TTree or TChain
  Int_t           fCurrent; //!current Tree number in a TChain

  // Declaration of leaf types
  // Int_t           MMFE8;
  Int_t           VMM;
  Int_t           CKTPrunning;
  Int_t           PDAC;
  Int_t           XADC;
  Int_t           MMFE8;

  // List of branches
  // TBranch        *b_MMFE8;
  TBranch        *b_VMM;   //!
  TBranch        *b_CKTPrunning;   //!
  TBranch        *b_PDAC;   //!
  TBranch        *b_XADC;   //!
  TBranch        *b_MMFE8;   //!
  xADCBase(TTree *tree=0);
  virtual ~xADCBase();
  virtual Int_t    Cut(Long64_t entry);
  virtual Int_t    GetEntry(Long64_t entry);
  virtual Long64_t LoadTree(Long64_t entry);
  virtual void     Init(TTree *tree);
  virtual Bool_t   Notify();
  virtual void     Show(Long64_t entry = -1);
};

#endif

inline xADCBase::xADCBase(TTree *tree) : fChain(0)
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

inline xADCBase::~xADCBase()
{
  if (!fChain) return;
  delete fChain->GetCurrentFile();
}

inline Int_t xADCBase::GetEntry(Long64_t entry)
{
  // Read contents of entry.
  if (!fChain) return 0;
  return fChain->GetEntry(entry);
}
inline Long64_t xADCBase::LoadTree(Long64_t entry)
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

inline void xADCBase::Init(TTree *tree)
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
  fChain->SetBranchAddress("CKTPrunning", &CKTPrunning, &b_CKTPrunning);
  fChain->SetBranchAddress("PDAC", &PDAC, &b_PDAC);
  fChain->SetBranchAddress("XADC", &XADC, &b_XADC);
  fChain->SetBranchAddress("MMFE8", &MMFE8, &b_MMFE8);
  Notify();
}

inline Bool_t xADCBase::Notify()
{
  // The Notify() function is called when a new file is opened. This
  // can be either for a new TTree in a TChain or when when a new TTree
  // is started when using PROOF. It is normally not necessary to make changes
  // to the generated code, but the routine can be extended by the
  // user if needed. The return value is currently not used.

  return kTRUE;
}

inline void xADCBase::Show(Long64_t entry)
{
  // Print contents of entry.
  // If entry is not specified, print current entry
  if (!fChain) return;
  fChain->Show(entry);
}

inline Int_t xADCBase::Cut(Long64_t entry)
{
  // This function may be called from Loop.
  // returns  1 if entry is accepted.
  // returns -1 otherwise.
  return 1;
}
