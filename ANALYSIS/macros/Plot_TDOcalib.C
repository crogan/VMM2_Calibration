#include <iostream>
#include <string>
#include <stdlib.h>

#include <TFile.h>
#include <TTree.h>

#include "include/setstyle.hh"
#include "include/fit_functions.hh"
#include "include/VMM_data.hh"
  
const string X_label = "Delay (x 25 ns)";
const string Y_label = "TDO";

void Plot_TDOcalib(const string& filename, int VMM = 1, int CH = 15){
  setstyle();

  TChain* tree = new TChain("VMM_data");
  tree->AddFile(filename.c_str());
  
  VMM_data* base = new VMM_data(tree);

  int N = tree->GetEntries();

  map<int,TH1D*> vDelay_hist;
  
  vector<TH1D*> vhist;
  vector<double> vDelay;
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

    if(base->TPDAC !=  200)
      continue;

    if(base->Delay > 10)
      continue;

    // make new histogram
    if(vDelay_hist.count(base->Delay) == 0){
      char sDelay[10];
      sprintf(sDelay,"%d",base->Delay);
    
      TH1D* hist = new TH1D(("h_"+string(sDelay)).c_str(),
			    ("h_"+string(sDelay)).c_str(),
			    2000, -0.5, 1999.5);
      vDelay_hist[base->Delay] = hist;
      vhist.push_back(hist);
      vDelay.push_back(base->Delay+1);
      vlabel.push_back("Delay = "+string(sDelay));
    }

    vDelay_hist[base->Delay]->Fill(base->TDO);
  }

  char stitle[50];
  sprintf(stitle, "Board #%d , VMM #%d , CH #%d", 0, VMM, CH);
  TCanvas* can = Plot_1D("can", vhist, "TDO", "Counts", stitle, vlabel);

  int Ndac = vhist.size();
  int Npoint = 0;
  
  double Y_tdo[Ndac];
  double Yerr_tdo[Ndac];
  double X_D[Ndac];
  double Xerr_D[Ndac];
  int index = 0;
  for(int i = 0; i < Ndac; i++){
    double I = vhist[i]->Integral();
    if(I <= 0.)
      continue;
    //Y_tdo[index] = vhist[i]->GetMaximumBin();
    Y_tdo[index] = vhist[i]->GetMean();
    Yerr_tdo[index] = max(vhist[i]->GetRMS()/sqrt(I), 1.);
    X_D[index] = vDelay[i];
    Xerr_D[index] = 0.;

    index++;
    Npoint++;
  }
  
  if(Npoint < 2) return;
  TGraphErrors* gr = new TGraphErrors(Npoint, X_D, Y_tdo, Xerr_D, Yerr_tdo);

  TF1* func = new TF1("func", P1, 0., 400., 2);

  func->SetParName(0, "c");
  func->SetParName(1, "m");

  gr->Fit("func", "E");

  TCanvas* c1 = Plot_Graph("c1", gr, "Delay (x5 ns)", "TDO", stitle);
}
