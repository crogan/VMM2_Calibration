#include <iostream>
#include <string>
#include <stdlib.h>

#include <TFile.h>
#include <TTree.h>

#include "include/setstyle.hh"
#include "include/VMM_data.hh"
  
const string X_label = "PDO";
const string Y_label = "Count";

void Plot_PDO(const string& filename, int VMM = 1, int CH = 15){
  setstyle();
  
  TChain* tree = new TChain("VMM_data");
  tree->AddFile(filename.c_str());
  
  VMM_data* base = new VMM_data(tree);

  int N = tree->GetEntries();

  map<int,TH1D*> vDAC_hist;
  
  vector<TH1D*> vhist;
  vector<string> vlabel;

  for(int i = 0; i < N; i++){
    base->GetEntry(i);

    if(base->VMM != VMM)
      continue;

    if(base->CHword != CH)
      continue;

    if(base->CHpulse != CH)
      continue;

    if(base->PDO <=  0)
      continue;

    if(base->TDO <=  0)
      continue;

    // make new histogram
    if(vDAC_hist.count(base->TPDAC) == 0){
      char sPDAC[10];
      sprintf(sPDAC,"%d",base->TPDAC);
    
      TH1D* hist = new TH1D(("h_"+string(sPDAC)).c_str(),
			    ("h_"+string(sPDAC)).c_str(),
			    1100, -0.5, 1099.5);
      vDAC_hist[base->TPDAC] = hist;
      vhist.push_back(hist);
      vlabel.push_back("DAC = "+string(sPDAC));
    }

    vDAC_hist[base->TPDAC]->Fill(base->PDO);
  }
 
  char stitle[50];
  sprintf(stitle, "Board #%d , VMM #%d , CH #%d", 0, VMM, CH);
  TCanvas* can = Plot_1D("can", vhist, X_label, Y_label, stitle, vlabel);

}
