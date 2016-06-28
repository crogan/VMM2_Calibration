#include "include/setstyle.hh"
#include "include/fit_functions.hh"

#include "include/xADCfitBase.hh"

using namespace std;

const string X_label = "Test Pulse DAC";
const string Y_label = "Input Charge (fC)";
const string Yerr_label = "#sigma Charge (fC)";

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

  int MMFE8 = 0;

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

  double min = 1000.;
  for(int i = 0; i < Npoint; i++){
    DAC[i] = vDAC[i];
    meanQ[i] = vmeanQ[i];
    meanQerr[i] = vmeanQerr[i];
    if(meanQ[i] < min)
      min = meanQ[i];
  }

  TGraphErrors* gr = new TGraphErrors(Npoint, DAC, meanQ, 0, meanQerr);

  TF1* func = new TF1("func", P0_P2_P1, 0., 400., 4);

  func->SetParName(0, "c_{0}");
  func->SetParameter(0, min);
  func->SetParName(1, "A_{2}");
  func->SetParameter(1, 0.005);
  func->SetParName(2, "t_{0 , 2}");
  func->SetParameter(2, 40.);
  func->SetParName(3, "d_{2 , 1}");
  func->SetParameter(3, 80.);

  func->SetParLimits(3, 0., 10000.);

  gr->Fit("func", "E");

  char stitle[50];
  sprintf(stitle, "Board #%d , VMM #%d", MMFE8, VMM);
  TCanvas* c1 = Plot_Graph("c1", gr, X_label, Y_label, stitle);

  TGraph* gr2 = new TGraph(Npoint, DAC, meanQerr);

  TCanvas* c2 = Plot_Graph("c2", gr2, X_label, Yerr_label, stitle);
 
}
