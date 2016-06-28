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

void Plot_xADCfit_VMM(const string& filename, int VMM = 1){
  setstyle();

  TChain* tree = new TChain("xADC_data");
  tree->AddFile(filename.c_str());

  xADCBase* base = new xADCBase(tree);

  int N = tree->GetEntries();

  map<int,TH1D*> vDAC_hist;
  
  vector<TH1D*> vhist;
  vector<int> vDAC;
  vector<string> vlabel;

  for (int i = 0; i < N; i++){
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
      vDAC.push_back(base->PDAC);
      vlabel.push_back("DAC = "+string(sPDAC));
    }

    vDAC_hist[base->PDAC]->Fill(base->XADC);
  }

  bool two_peak = false;
  int Ndac = vDAC.size();

  // check whether there are DAC histograms with 
  // two peaks

  for(int i = 0; i < Ndac; i++){
    double h_mean = vhist[i]->GetMean();
    double h_max  = vhist[i]->GetMaximumBin();
    if(fabs(h_mean-h_max) > 6.){
      two_peak = true;
      break;
    }
  }

  // if two-peaks observed, assume it is true for all
  // xADC histograms for this VMM
  if(two_peak){
    double mu0_mean = 0.;
    double sig0_mean = 0;

    vector<double> vmu0;
    vector<double> vmu0_err;
    vector<double> vsig0;
    vector<double> vsig0_err;
    vector<double> vA;
    vector<double> vA_err;
    vector<double> vA0;
    vector<double> vA0_err;
    for(int i = 0; i < Ndac; i++){
      double Nhist = vhist[i]->Integral();
      if(Nhist <= 0.) continue;

      double h_mean = vhist[i]->GetMean();
      double h_max  = vhist[i]->GetMaximumBin();

      bool b_two_peak = fabs(h_mean-h_max) < 3. ? false : true;
      
      char fname[50];
      sprintf(fname, "func_VMM%d_DAC%d", VMM, vDAC[i]);
      TF1* func = new TF1(fname, DoubleGaus, 
			  0., 4000., 6);
      
      func->SetParName(0, "N");
      func->SetParameter(0, Nhist/2.);
      func->SetParName(3, "N_{0}");
      func->SetParameter(3, Nhist/2.);

      double mu, mu0;
      double bmax = -1.;
      for(int b = 0; b < int(h_mean); b++){
	if(vhist[i]->GetBinContent(b+1) > bmax){
	  mu0 = b;
	  bmax = vhist[i]->GetBinContent(b+1);
	}
      }
      bmax = -1.;
      for(int b = int(h_mean); b < 2000.; b++){
	if(vhist[i]->GetBinContent(b+1) > bmax){
	  mu = b;
	  bmax = vhist[i]->GetBinContent(b+1);
	}
      }
      func->SetParName(1, "#mu-#mu_{0}");
      func->SetParameter(1, fabs(mu-mu0)); 
      func->SetParName(4, "#mu_{0}");
      func->SetParameter(4, mu0);
      
      func->SetParName(2, "#sigma");
      func->SetParameter(2, 2.); 
      func->SetParName(5, "#sigma_{0}");
      func->SetParameter(5, 2.);
      
      func->SetParLimits(1, 0., 10000.);
      func->SetParLimits(4, 0., h_mean);
  
      vhist[i]->Fit(fname, "EI");

      vmu0.push_back(func->GetParameter(4));
      vmu0_err.push_back(func->GetParError(4));
      mu0_mean += func->GetParameter(4);

      vsig0.push_back(func->GetParameter(5));
      vsig0_err.push_back(func->GetParError(5));
      sig0_mean += func->GetParameter(5);

      vA.push_back(func->GetParameter(0));
      vA_err.push_back(func->GetParError(0));
      vA0.push_back(func->GetParameter(3));
      vA0_err.push_back(func->GetParError(3));
    }

    int Nfit = vmu0.size();
    mu0_mean /= double(Nfit);
    sig0_mean /= double (Nfit);

    TH1D* hist_mu0 = new TH1D("h_mu0","h_mu0",100,mu0_mean-5,mu0_mean+5);
    TH1D* hist_sig0 = new TH1D("h_sig0","h_sig0",100,sig0_mean-2,sig0_mean+2);
    TH1D* hist_dA = new TH1D("h_dA","h_dA",100,0.8,1.2);
    TH1D* hist_mu0_pull = new TH1D("h_mu0_pull","h_mu0_pull",100,-5,5);
    TH1D* hist_sig0_pull = new TH1D("h_sig0_pull","h_sig0_pull",100,-5,5);
    TH1D* hist_dA_pull = new TH1D("h_dA_pull","h_dA_pull",100,-5,5);

    for(int i = 0; i < Nfit; i++){
      hist_mu0->Fill(vmu0[i]);
      hist_sig0->Fill(vsig0[i]);
      hist_dA->Fill(vA0[i]/vA[i]);
      hist_mu0_pull->Fill((vmu0[i]-mu0_mean)/vmu0_err[i]);
      hist_sig0_pull->Fill((vsig0[i]-sig0_mean)/vsig0_err[i]);
      hist_dA_pull->Fill((vA0[i]-vA[i])/sqrt(vA_err[i]*vA_err[i]+vA0_err[i]*vA0_err[i]));
      // cout << "mu0 " << vmu0[i] << " " << mu0_mean << " " << vmu0_err[i] << endl;
      // cout << "sig0 " << vsig0[i] << " " << sig0_mean << " " << vsig0_err[i] << endl;
      // cout << "dA " << vA0[i] << " " << vA[i] << " " << sqrt(vA_err[i]*vA_err[i]+vA0_err[i]*vA0_err[i]) << endl;
    }

    char stitle[50];
    sprintf(stitle, "VMM #%d , Board #%d", VMM, 0);
    TCanvas* c_mu0  = Plot_1D("c_mu0", hist_mu0, "#mu_{0}", "N fits", stitle);
    TCanvas* c_sig0 = Plot_1D("c_sig0", hist_sig0, "#sigma_{0}", "N fits", stitle);
    TCanvas* c_dA   = Plot_1D("c_dA", hist_dA, "A_{0} / A", "N fits", stitle);
    TCanvas* c_mu0_pull  = Plot_1D("c_mu0_pull", hist_mu0_pull, "(#mu_{0} - #bar{#mu}_{0}) / #sigma_{#mu_{0}}", "N fits", stitle);
    TCanvas* c_sig0_pull = Plot_1D("c_sig0_pull", hist_sig0_pull, "(#sigma_{0} - #bar{#sigma}_{0}) / #sigma_{#sigma_{0}}", "N fits", stitle);
    TCanvas* c_dA_pull   = Plot_1D("c_dA_pull", hist_dA_pull, "(A_{0} - A) / #sigma_{A_{0}-A}", "N fits", stitle);

  }
  // double Nhist = hist->Integral();
  // if(N <= 0.) return;

  // double h_mean = hist->GetMean();
  // double h_max  = hist->GetMaximumBin();

  // bool b_two_peak = fabs(h_mean-h_max) < 8. ? false : true;

  // TF1* func;
  // if(b_two_peak){
  //   func = new TF1("func", DoubleGaus, 
  // 		   0., 4000., 6);
    
  //   func->SetParName(0, "N");
  //   func->SetParameter(0, Nhist/2.);
  //   func->SetParName(3, "N_{0}");
  //   func->SetParameter(3, N/2.);

  //   double mu, mu0;
  //   if(h_mean > h_max){
  //     mu  = 2.*h_mean-h_max;
  //     mu0 = h_max;
  //   } else {
  //     mu  = h_max;
  //     mu0 = 2.*h_mean-h_max;
  //   }
  //   func->SetParName(1, "#mu");
  //   func->SetParameter(1, mu); 
  //   func->SetParName(4, "#mu_{0}");
  //   func->SetParameter(4, mu0);
    
  //   func->SetParName(2, "#sigma");
  //   func->SetParameter(2, 2.); 
  //   func->SetParName(5, "#sigma_{0}");
  //   func->SetParameter(5, 2.);
    
  //   func->SetParLimits(1, h_mean, 4000.);
  //   func->SetParLimits(4, 0., h_mean);
  
  //   hist->Fit("func", "EI");

  // } else {
  //   func = new TF1("func", Gaus, 
  // 		   0., 4000., 3);

  //   func->SetParName(0, "N");
  //   func->SetParameter(0, Nhist/2.);
    
  //   func->SetParName(1, "#mu");
  //   func->SetParameter(1, h_mean); 
    
  //   func->SetParName(2, "#sigma");
  //   func->SetParameter(2, 1.5); 
  
  //   hist->Fit("func", "EI");
  // }

  // func->SetLineColor(7000);
  // func->SetMarkerColor(7000);
  // func->SetFillColor(7000);

  char stitle[50];
  sprintf(stitle, "VMM #%d , Board #%d", VMM, 0);
  TCanvas* can = Plot_1D("can", vhist, X_label, Y_label, stitle, vlabel);
}
