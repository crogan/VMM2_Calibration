#include <iostream>
#include <string>
#include <stdlib.h>

#include <TFile.h>
#include <TTree.h>

#include "include/setstyle.hh"
#include "include/DACToCharge.hh"
#include "include/VMM_data.hh"
  
const string X_label = "Injected Charge (fC)";
const string Y_label = "PDO";

void Plot_PDOcalib(const string& filename, const string& xADCcalib_file, int VMM = 2, int CH = 15){
  setstyle();
  
  // Get a DACToCharge object
  DACToCharge DAC2Charge(xADCcalib_file);

  TChain* tree = new TChain("VMM_data");
  tree->AddFile(filename.c_str());
  
  VMM_data* base = new VMM_data(tree);

  int N = tree->GetEntries();

  map<int,TH1D*> vDAC_hist;
  
  vector<TH1D*> vhist;
  vector<double> vcharge;
  vector<double> vcharge_err;
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
			    2000, -0.5, 1999.5);
      vDAC_hist[base->TPDAC] = hist;
      vhist.push_back(hist);
      vcharge.push_back(DAC2Charge.GetCharge(base->TPDAC,base->MMFE8,VMM));
      //vcharge.push_back(base->TPDAC);
      vcharge_err.push_back(DAC2Charge.GetChargeError(base->TPDAC,base->MMFE8,VMM));
      vlabel.push_back("DAC = "+string(sPDAC));
    }

    vDAC_hist[base->TPDAC]->Fill(base->PDO);
  }

  int Ndac = vhist.size();
  int Npoint = 0;
  
  double Y_pdo[Ndac];
  double Yerr_pdo[Ndac];
  double X_Q[Ndac];
  double Xerr_Q[Ndac];
  int index = 0;
  for(int i = 0; i < Ndac; i++){
    double I = vhist[i]->Integral();
    if(I <= 0.)
      continue;
    Y_pdo[index] = vhist[i]->GetMean();
    Yerr_pdo[index] = max(vhist[i]->GetRMS(), 1.);
    X_Q[index] = vcharge[i];
    Xerr_Q[index] = vcharge_err[i];

    index++;
    Npoint++;
  }
  
  if(Npoint < 2) return;
  TGraphErrors* gr = new TGraphErrors(Npoint, X_Q, Y_pdo, Xerr_Q, Yerr_pdo);

  TF1* func = new TF1("func", P1_P2_P0, 0., 400., 4);

  func->SetParName(0, "c_{0}");
  func->SetParameter(0,1000.);
  func->SetParName(1, "A_{2}");
  func->SetParameter(1, -0.5);
  func->SetParName(2, "t_{0 , 2}");
  func->SetParameter(2, 60.);
  func->SetParName(3, "d_{2 , 1}");
  func->SetParameter(3, -10.);

  func->SetParLimits(3, -10000., 0.);

  // gr->Draw("ap");
  // func->Draw("same");

  gr->Fit("func", "E");

  char stitle[50];
  sprintf(stitle, "Board #%d , VMM #%d , CH #%d", 0, VMM, CH);
  TCanvas* c1 = Plot_Graph("c1", gr, X_label, Y_label, stitle);
}
