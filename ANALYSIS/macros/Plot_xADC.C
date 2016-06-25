#include <iostream>
#include <string>
#include <stdlib.h>

#include <TFile.h>
#include <TTree.h>

#include "include/setstyle.hh"
#include "include/xADCBase.hh"
  
const string X_label = "xADC readout (counts, 12-bit 1V full-range)";
const string Y_label = "Count";

void Plot_xADC(const string& filename, int VMM = 1){
  setstyle();
  
  TChain* tree = new TChain("xADC_data");
  tree->AddFile(filename.c_str());
  
  xADCBase* base = new xADCBase(tree);

  int N = tree->GetEntries();

  map<int,TH1D*> vDAC_hist;
  
  vector<TH1D*> vhist;
  vector<string> vlabel;

  for(int i = 0; i < N; i++){
    base->GetEntry(i);

    if(!base->CKTPrunning)
      continue;

    if(base->VMM != VMM)
      continue;

    // make new histogram
    if(vDAC_hist.count(base->PDAC) == 0){
      char sPDAC[10];
      sprintf(sPDAC,"%d",base->PDAC);
    
      TH1D* hist = new TH1D(("h_"+string(sPDAC)).c_str(),
			    ("h_"+string(sPDAC)).c_str(),
			    4096, -0.5, 4095.5);
      vDAC_hist[base->PDAC] = hist;
      vhist.push_back(hist);
      vlabel.push_back("DAC = "+string(sPDAC));
    }

    vDAC_hist[base->PDAC]->Fill(base->XADC);
  }
 
  char stitle[50];
  sprintf(stitle, "VMM #%d , Board #%d", VMM, 0);
  TCanvas* can = Plot_1D("can", vhist, X_label, Y_label, stitle, vlabel);

}
