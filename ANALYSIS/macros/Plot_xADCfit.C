#include <TH1I.h>
#include <TF1.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <cmath>
#include <string>
#include <iostream>

#include "include/setstyle.hh"
#include "include/fit_functions.hh"
#include "include/xADCBase.hh"

using namespace std;

const string X_label = "xADC readout (counts, 12-bit 1V full-range)";
const string Y_label = "Number of events (count)";

void Plot_xADCfit(const string& filename, int VMM = 1, int DAC = 200){
  setstyle();

  TChain* tree = new TChain("xADC_data");
  tree->AddFile(filename.c_str());

  xADCBase* base = new xADCBase(tree);

  int N = tree->GetEntries();

  TH1D* hist = new TH1D("hist", "hist", 4096, -0.5, 4095.5);

  for (int i = 0; i < N; i++){
    base->GetEntry(i);

    if(!base->CKTPrunning)
      continue;

    if(base->VMM != VMM)
      continue;

    if(base->PDAC != DAC)
      continue;

    hist->Fill(base->XADC);
  }
  double Nhist = hist->Integral();
  if(N <= 0.) return;

  double h_mean = hist->GetMean();
  double h_max  = hist->GetMaximumBin();

  bool b_two_peak = fabs(h_mean-h_max) < 8. ? false : true;

  TF1* func;
  if(b_two_peak){
    func = new TF1("func", DoubleGaus, 
		   0., 4000., 6);
    
    func->SetParName(0, "N");
    func->SetParameter(0, Nhist/2.);
    func->SetParName(3, "N_{0}");
    func->SetParameter(3, N/2.);

    double mu, mu0;
    if(h_mean > h_max){
      mu  = 2.*h_mean-h_max;
      mu0 = h_max;
    } else {
      mu  = h_max;
      mu0 = 2.*h_mean-h_max;
    }
    func->SetParName(1, "#mu");
    func->SetParameter(1, mu); 
    func->SetParName(4, "#mu_{0}");
    func->SetParameter(4, mu0);
    
    func->SetParName(2, "#sigma");
    func->SetParameter(2, 2.); 
    func->SetParName(5, "#sigma_{0}");
    func->SetParameter(5, 2.);
    
    func->SetParLimits(1, h_mean, 4000.);
    func->SetParLimits(4, 0., h_mean);
  
    hist->Fit("func", "EI");

  } else {
    func = new TF1("func", Gaus, 
		   0., 4000., 3);

    func->SetParName(0, "N");
    func->SetParameter(0, Nhist/2.);
    
    func->SetParName(1, "#mu");
    func->SetParameter(1, h_mean); 
    
    func->SetParName(2, "#sigma");
    func->SetParameter(2, 1.5); 
  
    hist->Fit("func", "EI");
  }

  func->SetLineColor(7000);
  func->SetMarkerColor(7000);
  func->SetFillColor(7000);

  char stitle[50];
  sprintf(stitle, "Board #%d, VMM #%d, DAC = %d", 0, VMM, DAC);
  TCanvas* can = Plot_1D("c1", hist, X_label, Y_label, stitle);
}
