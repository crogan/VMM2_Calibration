#include <iostream>
#include <vector>
#include <string>
#include <TCanvas.h>
#include <TH1D.h>
#include <TF1.h>
#include <TStyle.h>
#include <TLegend.h>

#include "../include/xADCBase.hh"

using namespace std;

// Function prototype
double double_gaus_function(double* xs, double* par);

// Constants
const string tree_name = "xADC_data";
const string func_name = "double_gauss";
// const int min_tpDAC = 40;
// const int max_tpDAC = 200;
const double fC_per_xADC_count = 1.2 / 4.096;
const float min_Q = -0.1465;
const float max_Q = 1199.8535;
const double max_chi2 = 50;

int main(int argc, char* argv[]){
  char inputFileName[400];

  if ( argc != 2 ){
    cout << "Error at Input: please specify an input .dat file";
    cout << "Example:   ./dat2root input_file.dat" << endl;
    return 1;
  }

  sscanf(argv[1],"%s", inputFileName);

  TChain* tree = new TChain(tree_name.c_str(), tree_name.c_str());
  tree->AddFile(inputFileName);
  xADCBase* base = new xADCBase(tree);

  // Create map
  map <int, TH1D*> hists[8];

  // Output tree
  double meanQ, sigQ, chi2;
  int vmm, tpDAC;
  TTree* fit_tree = new TTree("TPFit", "TPFit");
  fit_tree->Branch("VMM", &vmm);
  fit_tree->Branch("TPDAC", &tpDAC);
  fit_tree->Branch("MeanQ", &meanQ);
  fit_tree->Branch("SigmaQ", &sigQ);
  fit_tree->Branch("ChiSquare", &chi2);

  // Output file
  TFile* ofile = new TFile(inputFileName, "UPDATE");

  // Loop over data points, filling in hists
  const unsigned int N = tree->GetEntries();
  for (unsigned int i = 0; i < N; i++){
    base->GetEntry(i);
    if (!(hists[base->VMM - 1].count(base->PDAC))){
      char hist_name[100];
      sprintf(hist_name, "VMM %d, tpDAC %d", base->VMM, base->PDAC);
      hists[base->VMM - 1][base->PDAC] = new TH1D(hist_name, hist_name, 4096,
        min_Q, max_Q);
    }
    hists[base->VMM - 1][base->PDAC]->Fill(base->XADC * fC_per_xADC_count);
  }

  TF1* fun = new TF1(func_name.c_str(), double_gaus_function, min_Q,
                              max_Q, 6);
  TF1* low_gauss = new TF1("low_gauss", "gaus", min_Q, 60);
  TF1* high_gauss = new TF1("high_gauss", "gaus", 60, max_Q);

  // Do fit thing
  for (unsigned int i = 0; i < 8; i++){
    vmm = i + 1;
    for (map<int, TH1D*>::iterator j = hists[i].begin(), end = hists[i].end();
          j != end; j++){
      tpDAC = j->first;
      TH1D* hist = j->second;
      float mu_tot = hist->GetMean();
      float sig_tot = hist->GetStdDev();
      double N_tot = hist->GetEntries();

      // set defaults
      fun->SetParameter(0, N_tot / 2); // N0 = N1 = Ntot/2
      fun->SetParameter(3, N_tot / 2);
      fun->SetParameter(1, mu_tot - sig_tot); // mu0
      fun->SetParameter(4, mu_tot + sig_tot);
      fun->SetParameter(2, 2 * fC_per_xADC_count); // sig0 (estimate from previous xADC fits)
      fun->SetParameter(5, 2 * fC_per_xADC_count);

      // Limits:
      fun->SetParLimits(0, 0, 10 * N_tot); // 0 < N0, N1 < 2Ntot
      fun->SetParLimits(3, 0, 10 * N_tot);
      fun->SetParLimits(1, 0, mu_tot); // 0 < mu0 < mu_tot
      fun->SetParLimits(4, mu_tot, 2 * max_Q);
      fun->SetParLimits(2, 0, max_Q); // 0 < sig0, sig1 < large number
      fun->SetParLimits(5, 0, max_Q);

      // Perform fit
      hist->Fit(func_name.c_str(), "E");
      double low_mean = fun->GetParameter(1);
      double low_sig = fun->GetParameter(2);
      double high_mean = fun->GetParameter(4);
      double high_sig = fun->GetParameter(5);
      chi2 = fun->GetChisquare();

      if (chi2 > max_chi2) {
        /* This is triggered if we go above the threshold.  Usually means that
         * the fit failed due to instability.  Resort to naive fit (one Gaussian
         * on each side of the overall histogram mean).
         */
        low_gauss->SetRange(min_Q, mu_tot);
        high_gauss->SetRange(mu_tot, max_Q);
        hist->Fit("low_gauss", "R"); // "R" uses the range of the TF1
        hist->Fit("high_gauss", "R");
        if (low_gauss->GetChisquare() + high_gauss->GetChisquare() < chi2){
          chi2 = low_gauss->GetChisquare() + high_gauss->GetChisquare();
          low_mean = low_gauss->GetParameter("Mean");
          low_sig = low_gauss->GetParameter("Sigma");
          high_mean = high_gauss->GetParameter("Mean");
          high_sig = high_gauss->GetParameter("Sigma");
        }
      }

      // Calculate the difference.
      meanQ = high_mean - low_mean;

      // This is correct unless there's low-frequency noise that would give
      // covariance. General formula sigma = sqrt(s1^2 + s2^2 - 2*covariance)
      sigQ = sqrt(pow(high_sig, 2) + pow(low_sig, 2));

      fit_tree->Fill();
    }
  }

  // Store parameters in root file
  ofile->cd();
  fit_tree->Write();
  ofile->Close();
}



// General normal distribution with integral N
double normal_distribution(double N, double mu, double sg, double x){
  double pi = atan(1.)*4;
  double G = exp(-pow(x - mu,2) / (2 * pow(sg,2))) / (sqrt(2 * pi) * sg);
  return N * G;
}

// Custom function for test pulse DAC fit, two Gaussians.
// Invariants: parameters: {N0, mu0, sig0, N1, mu1, sig1}
double double_gaus_function(double* xs, double* par){
  float x = xs[0];
  double G0 = normal_distribution(par[0], par[1], par[2], x);
  double G1 = normal_distribution(par[3], par[4], par[5], x);
  return G0 + G1;
}
