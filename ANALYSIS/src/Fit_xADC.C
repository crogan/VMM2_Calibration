#include <iostream>

#include "include/setstyle.hh"
#include "include/fit_functions.hh"
#include "../include/xADCBase.hh"

using namespace std;

const double fC_per_xADC_count = 1.2 / 4.096;

int main(int argc, char* argv[]){
  char inputFileName[400];
  char outputFileName[400];

  if ( argc < 2 ){
    cout << "Error at Input: please specify an input .root file";
    cout << " and an (optional) output filename" << endl;
    cout << "Example:   ./Fit_xADC input_file.root" << endl;
    cout << "Example:   ./Fit_xADC input_file.root -o output_file.root" << endl;
    return 1;
  }

  bool user_output = false;
  for (int i=0;i<argc;i++){
    sscanf(argv[1],"%s", inputFileName);
    if (strncmp(argv[i],"-o",2)==0){
      sscanf(argv[i+1],"%s", outputFileName);
      user_output = true;
    }
  }

  string output_name;
  if(!user_output){
    string input_name = string(inputFileName);
    // strip path from input name
    while(input_name.find("/") != string::npos)
      input_name.erase(input_name.begin(),
		       input_name.begin()+
		       input_name.find("/")+1);
    if(input_name.find(".root") != string::npos)
      input_name.erase(input_name.find(".root"),5);
    output_name = input_name+"_xADCfit.root";
    sprintf(outputFileName,"%s.root",inputFileName);
  } else {
    output_name = string(outputFileName);
  }

  TChain* tree = new TChain("xADC_data");
  tree->AddFile(inputFileName);

  xADCBase* base = new xADCBase(tree);

  int N = tree->GetEntries();
  if(N == 0) return 0;

  map<pair<int,int>, int> MMFE8VMM_to_index;

  vector<map<int, TH1D*> > vDAC_to_hist;
  
  vector<int>             vMMFE8;  // board ID
  vector<int>             vVMM;    // VMM number
  vector<vector<TH1D*> >  vhist;   // xADC histograms
  vector<vector<int> >    vDAC;    // DAC values
  vector<vector<string> > vlabel;  // labels

  int MMFE8;
  int VMM;
  int DAC;
  for (int i = 0; i < N; i++){
    base->GetEntry(i);

    if(!base->CKTPrunning)
      continue;

    MMFE8 = 0; // replace this with MMFE8 number from tree when available
    //MMFE8 = base->MMFE8;
    VMM   = base->VMM;
    DAC   = base->PDAC;
    
    // add a new vDAC_to_hist map if it 
    // is a new MMFE8+VMM combination
    if(MMFE8VMM_to_index.count(pair<int,int>(MMFE8,VMM)) == 0){
      vDAC_to_hist.push_back(map<int,TH1D*>());
      int ind = int(vDAC_to_hist.size())-1;
      MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)] = ind;
      vMMFE8.push_back(MMFE8);
      vVMM.push_back(VMM);
      vhist.push_back(vector<TH1D*>());
      vDAC.push_back(vector<int>());
      vlabel.push_back(vector<string>());
    }

    // MMFE8+VMM index
    int index = MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)];

    // add a new histogram if this DAC
    // combination is new for the MMFE8+VMM combo
    if(vDAC_to_hist[index].count(DAC) == 0){
      char sDAC[20];
      sprintf(sDAC,"%d",DAC);
      char shist[20];
      sprintf(shist,"%d_%d_%d",MMFE8,VMM,DAC);
      TH1D* hist = new TH1D(("h_"+string(shist)).c_str(),
			    ("h_"+string(shist)).c_str(),
			    4096, -0.5, 4095.5);
      vDAC_to_hist[index][DAC] = hist;
      vhist[index].push_back(hist);
      vDAC[index].push_back(DAC);
      vlabel[index].push_back("DAC = "+string(sDAC));
    }

    vDAC_to_hist[index][DAC]->Fill(base->XADC);
  }

  int Nindex = vMMFE8.size();

  TFile* fout = new TFile(output_name.c_str(), "RECREATE");

  // add plots of xADC values for each
  // MMFE8+VMM combo to output file
  fout->mkdir("xADC_plots");
  fout->cd("xADC_plots");
  for(int i = 0; i < Nindex; i++){
    char stitle[50];
    sprintf(stitle, "Board #%d, VMM #%d", vMMFE8[i], vVMM[i]);
    char scan[50];
    sprintf(scan, "c_xADC_Board%d_VMM%d", vMMFE8[i], vVMM[i]);
    TCanvas* can = Plot_1D(scan, vhist[i], "xADC Readout", "Count", stitle, vlabel[i]);
    can->Write();
    delete can;
  }
  fout->cd("");

  // write xADCBase tree to outputfile
  TTree* newtree = tree->CloneTree();
  fout->cd();
  newtree->Write();
  delete newtree;
  delete base;
  delete tree;

  // Output xADC fit tree
  double fit_MMFE8;
  double fit_VMM;
  double fit_DAC;
  double fit_meanQ;
  double fit_meanQerr;
  double fit_sigmaQ;
  double fit_sigmaQerr;
  double fit_chi2;
  double fit_prob;
  
  TTree* fit_tree = new TTree("xADC_fit", "xADC_fit");
  fit_tree->Branch("MMFE8", &fit_MMFE8);
  fit_tree->Branch("VMM", &fit_VMM);
  fit_tree->Branch("DAC", &fit_DAC);
  fit_tree->Branch("meanQ", &fit_meanQ);
  fit_tree->Branch("meanQerr", &fit_meanQerr);
  fit_tree->Branch("sigmaQ", &fit_sigmaQ);
  fit_tree->Branch("sigmaQerr", &fit_sigmaQerr);
  fit_tree->Branch("chi2", &fit_chi2);
  fit_tree->Branch("prob", &fit_prob);

  // Perform fits on each vector of MMFE8+VMM histograms
  fout->mkdir("xADCfit_plots");
  fout->cd("xADCfit_plots");

  vector<TF1*> vfunc;

  for(int index = 0; index < Nindex; index++){
    char sfold[50];
    sprintf(sfold, "xADCfit_plots/Board%d_VMM%d", vMMFE8[index], vVMM[index]);
    fout->mkdir(sfold);
    fout->cd(sfold);

    int Ndac = vhist[index].size();

    // check to see whether xADC histograms actually have 
    // two peaks for higher DAC
    bool two_peak = false;

    for(int d = 0; d < Ndac; d++){
      double h_mean = vhist[index][d]->GetMean();
      double h_max  = vhist[index][d]->GetMaximumBin()-1.;
      if(fabs(h_mean-h_max) > 8.){
	two_peak = true;
	break;
      }
    }

    if(two_peak){
      // go through and perform fits for well-separated peaks
      // to get lower peak fit parameters
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
      for(int d = 0; d < Ndac; d++){
	double Nhist = vhist[index][d]->Integral();
	if(Nhist <= 0.) continue;
	
	double h_mean = vhist[index][d]->GetMean();
	
	char fname[50];
	sprintf(fname, "func_MMFE8-%d_VMM-%d_DAC-%d", 
		vMMFE8[index], vVMM[index], vDAC[index][d]);
	int ifunc = vfunc.size();
	vfunc.push_back(new TF1(fname, DoubleGaus, 
				0., 4000., 6));
	vfunc[ifunc]->SetLineColorAlpha(kWhite,0);
	
	vfunc[ifunc]->SetParName(0, "N");
	vfunc[ifunc]->SetParameter(0, Nhist/2.);
	vfunc[ifunc]->SetParName(3, "N_{0}");
	vfunc[ifunc]->SetParameter(3, Nhist/2.);
	
	double mu, mu0;
	double bmax = -1.;
	for(int b = 0; b < int(h_mean); b++){
	  if(vhist[index][d]->GetBinContent(b+1) > bmax){
	    mu0 = b;
	    bmax = vhist[index][d]->GetBinContent(b+1);
	  }
	}
	bmax = -1.;
	for(int b = int(h_mean); b < 2000.; b++){
	  if(vhist[index][d]->GetBinContent(b+1) > bmax){
	    mu = b;
	    bmax = vhist[index][d]->GetBinContent(b+1);
	  }
	}
	
	vfunc[ifunc]->SetParName(1, "#mu-#mu_{0}");
	vfunc[ifunc]->SetParameter(1, fabs(mu-mu0)); 
	vfunc[ifunc]->SetParName(4, "#mu_{0}");
	vfunc[ifunc]->SetParameter(4, mu0);
	
	vfunc[ifunc]->SetParName(2, "#sigma");
	vfunc[ifunc]->SetParameter(2, 2.); 
	vfunc[ifunc]->SetParName(5, "#sigma_{0}");
	vfunc[ifunc]->SetParameter(5, 2.);
	
	vfunc[ifunc]->SetParLimits(1, 0., 10000.);
	vfunc[ifunc]->SetParLimits(4, 0., h_mean);
	
	vhist[index][d]->Fit(fname, "EIQ");
	  
	if(vfunc[ifunc]->GetChisquare() > 50.){
	  cout << "Chi2 > 50:";
	  cout << " MMFE8 = " << vMMFE8[index];
	  cout << " VMM = " << vVMM[index];
	  cout << " DAC = " << vDAC[index][d] << endl;
	  cout << " Chi2 = " << vfunc[ifunc]->GetChisquare();
	}

	fit_MMFE8 = vMMFE8[index];
	fit_VMM = vVMM[index];
	fit_DAC = vDAC[index][d];
	fit_meanQ = vfunc[ifunc]->GetParameter(1)*fC_per_xADC_count;
	fit_meanQerr = vfunc[ifunc]->GetParError(1)*fC_per_xADC_count;
	fit_sigmaQ = sqrt(pow(vfunc[ifunc]->GetParameter(2),2)+
			  pow(vfunc[ifunc]->GetParameter(5),2))*fC_per_xADC_count;
	fit_sigmaQerr = sqrt(pow(vfunc[ifunc]->GetParameter(2)*vfunc[ifunc]->GetParError(2),2)+
			     pow(vfunc[ifunc]->GetParameter(5)*vfunc[ifunc]->GetParError(5),2))/
	  sqrt(pow(vfunc[ifunc]->GetParameter(2),2)+
	       pow(vfunc[ifunc]->GetParameter(5),2))*fC_per_xADC_count;
	fit_chi2 = vfunc[ifunc]->GetChisquare();
	fit_prob = vfunc[ifunc]->GetProb();

	fit_tree->Fill();

	char stitle[50];
	sprintf(stitle, "Board #%d, VMM #%d, DAC = %d", vMMFE8[index], vVMM[index], vDAC[index][d]);
	char scan[50];
	sprintf(scan, "c_xADC_Board%d_VMM%d_DAC%d", vMMFE8[index], vVMM[index], vDAC[index][d]);
	TCanvas* can = Plot_1D(scan, vhist[index][d], "xADC Readout", "Count", stitle);
	can->Write();
	delete can;
	
	vmu0.push_back(vfunc[ifunc]->GetParameter(4));
	vmu0_err.push_back(vfunc[ifunc]->GetParError(4));
	mu0_mean += vfunc[ifunc]->GetParameter(4);
	
	vsig0.push_back(vfunc[ifunc]->GetParameter(5));
	vsig0_err.push_back(vfunc[ifunc]->GetParError(5));
	sig0_mean += vfunc[ifunc]->GetParameter(5);
	
	vA.push_back(vfunc[ifunc]->GetParameter(0));
	vA_err.push_back(vfunc[ifunc]->GetParError(0));
	vA0.push_back(vfunc[ifunc]->GetParameter(3));
	vA0_err.push_back(vfunc[ifunc]->GetParError(3));
      }
      
      int Nfit = vmu0.size();
      mu0_mean /= double(Nfit);
      sig0_mean /= double (Nfit);
      
      char shist[20];
      sprintf(shist,"_%d_%d",vMMFE8[index],vVMM[index]);
      TH1D* hist_mu0 = new TH1D(("h_mu0"+string(shist)).c_str(),
				("h_mu0"+string(shist)).c_str(),
				100,mu0_mean-5,mu0_mean+5);
      TH1D* hist_sig0 = new TH1D(("h_sig0"+string(shist)).c_str(),
				 ("h_sig0"+string(shist)).c_str(),
				 100,sig0_mean-2,sig0_mean+2);
      TH1D* hist_dA = new TH1D(("h_dA"+string(shist)).c_str(),
			       ("h_dA"+string(shist)).c_str(),
			       100,0.8,1.2);
      TH1D* hist_mu0_pull = new TH1D(("h_mu0_pull"+string(shist)).c_str(),
				     ("h_mu0_pull"+string(shist)).c_str(),
				     100,-5,5);
      TH1D* hist_sig0_pull = new TH1D(("h_sig0_pull"+string(shist)).c_str(),
				      ("h_sig0_pull"+string(shist)).c_str(),
				      100,-5,5);
      TH1D* hist_dA_pull = new TH1D(("h_dA_pull"+string(shist)).c_str(),
				    ("h_dA_pull"+string(shist)).c_str(),
				    100,-5,5);
      
      for(int i = 0; i < Nfit; i++){
	hist_mu0->Fill(vmu0[i]);
	hist_sig0->Fill(vsig0[i]);
	hist_dA->Fill(vA0[i]/vA[i]);
	hist_mu0_pull->Fill((vmu0[i]-mu0_mean)/vmu0_err[i]);
	hist_sig0_pull->Fill((vsig0[i]-sig0_mean)/vsig0_err[i]);
	hist_dA_pull->Fill((vA0[i]-vA[i])/sqrt(vA_err[i]*vA_err[i]+vA0_err[i]*vA0_err[i]));
      }
      
      char stitle[50];
      sprintf(stitle, "Board #%d, VMM #%d", vMMFE8[index], vVMM[index]);
      char scan[50];
      sprintf(scan, "_Board%d_VMM%d", vMMFE8[index], vVMM[index]);
      TCanvas* c_mu0  = Plot_1D(("c_mu0"+string(scan)).c_str(), hist_mu0, 
				"#mu_{0}", "N fits", stitle);
      TCanvas* c_sig0 = Plot_1D(("c_sig0"+string(scan)).c_str(), hist_sig0, 
				"#sigma_{0}", "N fits", stitle);
      TCanvas* c_dA   = Plot_1D(("c_dA"+string(scan)).c_str(), hist_dA, 
				"A_{0} / A", "N fits", stitle);
      TCanvas* c_mu0_pull  = Plot_1D(("c_mu0_pull"+string(scan)).c_str(), hist_mu0_pull, 
				     "(#mu_{0} - #bar{#mu}_{0}) / #sigma_{#mu_{0}}", "N fits", stitle);
      TCanvas* c_sig0_pull = Plot_1D(("c_sig0_pull"+string(scan)).c_str(), hist_sig0_pull, 
				     "(#sigma_{0} - #bar{#sigma}_{0}) / #sigma_{#sigma_{0}}", "N fits", stitle);
      TCanvas* c_dA_pull   = Plot_1D(("c_dA_pull"+string(scan)).c_str(), hist_dA_pull, 
				     "(A_{0} - A) / #sigma_{A_{0}-A}", "N fits", stitle);
      c_mu0->Write();
      c_sig0->Write();
      c_dA->Write();
      c_mu0_pull->Write();
      c_sig0_pull->Write();
      c_dA_pull->Write();
      delete c_mu0;
      delete c_sig0;
      delete c_dA;
      delete c_mu0_pull;
      delete c_sig0_pull;
      delete c_dA_pull;
      
    } else {
      for(int d = 0; d < Ndac; d++){
	char fname[50];
	sprintf(fname, "func1G_MMFE8-%d_VMM-%d_DAC-%d", 
		vMMFE8[index], vVMM[index], vDAC[index][d]);
	int ifunc = vfunc.size();
	
	vfunc.push_back(new TF1(fname, Gaus, 0., 4000., 3));
	vfunc[ifunc]->SetLineColorAlpha(kWhite,0);
	
	double Nhist = vhist[index][d]->Integral();
	if(Nhist <= 0.) return 0;
	
	double h_mean = vhist[index][d]->GetMean();
	
	vfunc[ifunc]->SetParName(0, "N");
	vfunc[ifunc]->SetParameter(0, Nhist/2.);
	
	vfunc[ifunc]->SetParName(1, "#mu");
	vfunc[ifunc]->SetParameter(1, h_mean); 
	
	vfunc[ifunc]->SetParName(2, "#sigma");
	vfunc[ifunc]->SetParameter(2, 2.); 
	
	vhist[index][d]->Fit(fname, "EIQ");
	
	char stitle[50];
	sprintf(stitle, "Board #%d, VMM #%d, DAC = %d", vMMFE8[index], vVMM[index], vDAC[index][d]);
	char scan[50];
	sprintf(scan, "c_xADC_Board%d_VMM%d_DAC%d", vMMFE8[index], vVMM[index], vDAC[index][d]);
	TCanvas* can = Plot_1D(scan, vhist[index][d], "xADC Readout", "Count", stitle);
	can->Write();
	delete can;

	// write fit parameters
	fit_MMFE8 = vMMFE8[index];
	fit_VMM = vVMM[index];
	fit_DAC = vDAC[index][d];
	fit_meanQ = vfunc[ifunc]->GetParameter(1)*fC_per_xADC_count;
	fit_meanQerr = vfunc[ifunc]->GetParError(1)*fC_per_xADC_count;
	fit_sigmaQ = vfunc[ifunc]->GetParameter(2)*fC_per_xADC_count;
	fit_sigmaQerr = vfunc[ifunc]->GetParError(2)*fC_per_xADC_count;
	fit_chi2 = vfunc[ifunc]->GetChisquare();
	fit_prob = vfunc[ifunc]->GetProb();
	
	fit_tree->Fill();
      }
    }

    char stitle[50];
    sprintf(stitle, "Board #%d, VMM #%d", vMMFE8[index], vVMM[index]);
    char scan[50];
    sprintf(scan, "c_xADC_Board%d_VMM%d_all", vMMFE8[index], vVMM[index]);
    TCanvas* can = Plot_1D(scan, vhist[index], "xADC Readout", "Count", stitle, vlabel[index]);
    can->Write();
    delete can;
    fout->cd("xADCfit_plots");
  }

  // Write fit_tree to output file
  fout->cd("");
  fit_tree->Write();
  fout->Close();
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
