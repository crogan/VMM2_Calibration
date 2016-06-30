#include <iostream>

#include "include/setstyle.hh"
#include "include/fit_functions.hh"
#include "include/xADCfitBase.hh"

using namespace std;

int main(int argc, char* argv[]){
  setstyle();

  char inputFileName[400];
  char outputFileName[400];
  
  if ( argc < 2 ){
    cout << "Error at Input: please specify an input .root file";
    cout << " and an (optional) output filename" << endl;
    cout << "Example:   ./Calibrate_xADC input_file.root" << endl;
    cout << "Example:   ./Calibrate_xADC input_file.root -o output_file.root" << endl;
    return 1;
  }

  sscanf(argv[1],"%s", inputFileName);
  bool user_output = false;
  for (int i=0;i<argc;i++){
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
    output_name = input_name+"_xADCcalib.root";
    sprintf(outputFileName,"%s.root",inputFileName);
  } else {
    output_name = string(outputFileName);
  }

  TChain* tree = new TChain("xADC_fit");
  tree->AddFile(inputFileName);

  xADCfitBase* base = new xADCfitBase(tree);

  int N = tree->GetEntries();
  if(N == 0) return 0;

  map<pair<int,int>, int> MMFE8VMM_to_index;
  
  vector<int>             vMMFE8;  // board ID
  vector<int>             vVMM;    // VMM number
  vector<vector<double> > vmeanQ;
  vector<vector<double> > vmeanQerr;
  vector<vector<double> > vDAC;

  int MMFE8;
  int VMM;

  for(int i = 0; i < N; i++){
    base->GetEntry(i);

    MMFE8 = base->MMFE8;
    VMM   = base->VMM;

    // add a new MMFE8+VMM combination 
    if(MMFE8VMM_to_index.count(pair<int,int>(MMFE8,VMM)) == 0){
      int ind = int(vMMFE8.size());
      MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)] = ind;
      vMMFE8.push_back(MMFE8);
      vVMM.push_back(VMM);
      vmeanQ.push_back(vector<double>());
      vmeanQerr.push_back(vector<double>());
      vDAC.push_back(vector<double>());
    }

    // MMFE8+VMM index
    int index = MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)];

    vDAC[index].push_back(base->DAC);
    vmeanQ[index].push_back(base->meanQ);
    vmeanQerr[index].push_back(base->meanQerr);
  }

  int Nindex = vMMFE8.size();

  vector<TGraphErrors*> vgraph;
  vector<double> vsigma;
  for(int index = 0; index < Nindex; index++){
    int Npoint = vDAC[index].size();
    double DAC[Npoint];
    double meanQ[Npoint];
    double meanQerr[Npoint];
    double sigma = 0.;

    for(int p = 0; p < Npoint; p++){
      DAC[p] = vDAC[index][p];
      meanQ[p] = vmeanQ[index][p];
      meanQerr[p] = vmeanQerr[index][p];
      // if(meanQerr[p] > sigma)
      // 	sigma = meanQerr[p];
      sigma += meanQerr[p]/double(Npoint);
    }

    vgraph.push_back(new TGraphErrors(Npoint, DAC, meanQ, 0, meanQerr));
    vsigma.push_back(sigma);
  }

  TFile* fout = new TFile(output_name.c_str(), "RECREATE");

  // write xADCBase tree to outputfile
  TChain* base_tree = new TChain("xADC_data");
  base_tree->AddFile(inputFileName);
  TTree* new_base_tree = base_tree->CloneTree();
  fout->cd();
  new_base_tree->Write();

  // add plots of charge v DAC for each
  // MMFE8+VMM combo to output file
  fout->mkdir("xADCfit_plots");
  fout->cd("xADCfit_plots");
  for(int i = 0; i < Nindex; i++){
    char stitle[50];
    sprintf(stitle, "Board #%d, VMM #%d", vMMFE8[i], vVMM[i]);
    char scan[50];
    sprintf(scan, "c_xADXfit_Board%d_VMM%d", vMMFE8[i], vVMM[i]);
    TCanvas* can = Plot_Graph(scan, vgraph[i], "Test Pulse DAC", "Input Charge (fC)", stitle);
    can->Write();
    delete can;
  }
  fout->cd("");

  // write xADCfitBase tree to outputfile
  TTree* newtree = tree->CloneTree();
  fout->cd();
  newtree->Write();
  delete newtree;
  delete base;
  delete tree;

  // Output xADC calib tree
  double calib_MMFE8;
  double calib_VMM;
  double calib_sigma;
  double calib_c0;
  double calib_A2;
  double calib_t02;
  double calib_d21;
  double calib_chi2;
  double calib_prob;
  
  TTree* calib_tree = new TTree("xADC_calib", "xADC_calib");
  calib_tree->Branch("MMFE8", &calib_MMFE8);
  calib_tree->Branch("VMM", &calib_VMM);
  calib_tree->Branch("sigma", &calib_sigma);
  calib_tree->Branch("c0", &calib_c0);
  calib_tree->Branch("A2", &calib_A2);
  calib_tree->Branch("t02", &calib_t02);
  calib_tree->Branch("d21", &calib_d21);
  calib_tree->Branch("chi2", &calib_chi2);
  calib_tree->Branch("prob", &calib_prob);

  // Perform fits on each vector of 
  // charge v DACMMFE8+VMM graphs
  fout->mkdir("xADCcalib_plots");
  fout->cd("xADCcalib_plots");

  vector<TF1*> vfunc;

  for(int index = 0; index < Nindex; index++){
    char fname[50];
    sprintf(fname, "funcP0P2P1_MMFE8-%d_VMM-%d", 
	    vMMFE8[index], vVMM[index]);
    int ifunc = vfunc.size();
    vfunc.push_back(new TF1(fname, P0_P2_P1, 0., 400., 4));

    vfunc[ifunc]->SetParName(0, "c_{0}");
    vfunc[ifunc]->SetParameter(0, 0.);
    vfunc[ifunc]->SetParName(1, "A_{2}");
    vfunc[ifunc]->SetParameter(1, 0.005);
    vfunc[ifunc]->SetParName(2, "t_{0 , 2}");
    vfunc[ifunc]->SetParameter(2, 40.);
    vfunc[ifunc]->SetParName(3, "d_{2 , 1}");
    vfunc[ifunc]->SetParameter(3, 80.);
    
    vfunc[ifunc]->SetParLimits(3, 0., 10000.);
    
    vgraph[index]->Fit(fname, "EQ");

    char stitle[50];
    sprintf(stitle, "Board #%d, VMM #%d", vMMFE8[index], vVMM[index]);
    char scan[50];
    sprintf(scan, "c_xADXcalib_Board%d_VMM%d", vMMFE8[index], vVMM[index]);
    TCanvas* can = Plot_Graph(scan, vgraph[index], "Test Pulse DAC", "Input Charge (fC)", stitle);
    can->Write();
    delete can;

   calib_MMFE8 = vMMFE8[index];
   calib_VMM = vVMM[index];
   calib_sigma = vsigma[index];
   calib_c0 = vfunc[ifunc]->GetParameter(0);
   calib_A2 = vfunc[ifunc]->GetParameter(1);
   calib_t02 = vfunc[ifunc]->GetParameter(2);
   calib_d21 = vfunc[ifunc]->GetParameter(3);
   calib_chi2 = vfunc[ifunc]->GetChisquare();
   calib_prob = vfunc[ifunc]->GetProb();

   calib_tree->Fill();
  }
  fout->cd("");

  // Write calib_tree to output file
  fout->cd("");
  calib_tree->Write();
  fout->Close();
}

