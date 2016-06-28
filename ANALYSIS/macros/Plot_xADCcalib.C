#include "include/setstyle.hh"
#include "include/fit_functions.hh"

#include "include/xADCfitBase.hh"

using namespace std;

const string X_label = "Test Pulse DAC";
const string Y_label = "Input Charge (fC)";

const int max_N = 20;

void Plot_xADCcalib(const string& filename, int VMM = 1){
  setstyle();

  TChain* tree = new TChain("xADC_fit");
  
  tree->AddFile(filename.c_str());
  
  xADCfitBase* base = new xADCfitBase(tree);

  int N = tree->GetEntries();

  vector<double> vmeanQ;
  vector<double> vmeanQerr;
  vector<double> vDAC;

  for (int i = 0; i < N; i++){
    base->GetEntry(i);

    if(base->VMM != VMM)
      continue;

    vDAC.push_back(base->DAC);
    vmeanQ.push_back(base->meanQ);
    vmeanQerr.push_back(base->sigmaQ);
  }

  int Npoint = vDAC.size();
  double DAC[Npoint];
  double meanQ[Npoint];
  double meanQerr[Npoint];

  for(int i = 0; i < Npoint; i++){
    DAC[i] = vDAC[i];
    meanQ[i] = vmeanQ[i];
    meanQerr[i] = vmeanQerr[i];
  }

  TGraphErrors* gr = new TGraphErrors(Npoint, DAC, meanQ, 0, meanQerr);

  TCanvas* can = new TCanvas("can","can",1200,1000);
  can->SetTopMargin(0.1);
  can->SetLeftMargin(0.12);
  can->Draw();
  can->SetGridx();
  can->SetGridy();
  can->cd();

  gr->Draw("ap");
  gr->GetXaxis()->SetTitle(X_label.c_str());
  gr->GetXaxis()->CenterTitle();
  gr->GetXaxis()->SetTitleOffset(1.1);
  gr->GetYaxis()->SetTitle(Y_label.c_str());
  gr->GetYaxis()->SetTitleOffset(1.4);
  gr->GetYaxis()->CenterTitle();
  // gr->GetXaxis()->SetRangeUser(0., 220.);
  // gr->GetYaxis()->SetRangeUser(0.,120.);
  gr->SetMarkerStyle(4);
  gr->SetMarkerColor(kAzure + 10);
  gr->SetMarkerSize(3);
 
}
