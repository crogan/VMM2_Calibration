#include <iostream>

#include "include/setstyle.hh"
#include "include/fit_functions.hh"
#include "include/TDOfitBase.hh"

using namespace std;

int main(int argc, char* argv[]){
  setstyle();

  char inputFileName[400];
  char outputFileName[400];
  
  if ( argc < 2 ){
    cout << "Error at Input: please specify an input .root file ";
    cout << "and an (optional) output filename" << endl;
    cout << "Example:   ./Calibrate_TDO input_file.root" << endl;
    cout << "Example:   ./Calibrate_TDO input_file.root -o output_file.root" << endl;
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
    output_name = input_name+"_TDOcalib.root";
    sprintf(outputFileName,"%s.root",inputFileName);
  } else {
    output_name = string(outputFileName);
  }

  TChain* tree = new TChain("TDO_fit");
  tree->AddFile(inputFileName);

  TDOfitBase* base = new TDOfitBase(tree);

  int N = tree->GetEntries();
  if(N == 0) return 0;

  map<pair<int,int>, int> MMFE8VMM_to_index;
  vector<map<int,int> >   vCH_to_index;
  
  vector<int>             vMMFE8;               // board ID
  vector<int>             vVMM;                 // VMM number
  vector<vector<int> >    vCH;                  // channel number
  vector<vector<vector<double> > > vminTDO;     // min TDO
  vector<vector<vector<double> > > vmeanTDO;    // mean TDO
  vector<vector<vector<double> > > vmeanTDOerr; // mean TDO err
  vector<vector<vector<int> > >    vDelay;      // Delay value

  int MMFE8;
  int VMM;
  int CH;

  for(int i = 0; i < N; i++){
    base->GetEntry(i);

    // exclude cases where TDO is split 
    // between low/high due to BCID jump
    if(base->sigmaTDO > 3.)
      continue;

    MMFE8 = base->MMFE8;
    VMM   = base->VMM;
    CH    = base->CH;

    // add a new MMFE8+VMM combination 
    if(MMFE8VMM_to_index.count(pair<int,int>(MMFE8,VMM)) == 0){
      int ind = int(vMMFE8.size());
      MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)] = ind;
      vMMFE8.push_back(MMFE8);
      vVMM.push_back(VMM);
      vCH.push_back(vector<int>());
      vCH_to_index.push_back(map<int,int>());
      vminTDO.push_back(vector<vector<double> >());
      vmeanTDO.push_back(vector<vector<double> >());
      vmeanTDOerr.push_back(vector<vector<double> >());
      vDelay.push_back(vector<vector<int> >());
    }

    // MMFE8+VMM index
    int index = MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)];

    // add a new channel if is new for
    // this MMFE8+VMM combination
    if(vCH_to_index[index].count(CH) == 0){
      int ind = int(vCH[index].size());
      vCH_to_index[index][CH] = ind;
      vCH[index].push_back(CH);
      vminTDO[index].push_back(vector<double>());
      vmeanTDO[index].push_back(vector<double>());
      vmeanTDOerr[index].push_back(vector<double>());
      vDelay[index].push_back(vector<int>());
    }

    // CH index
    int cindex = vCH_to_index[index][CH];

    vDelay[index][cindex].push_back(base->Delay);
    vminTDO[index][cindex].push_back(base->minTDO);
    vmeanTDO[index][cindex].push_back(base->meanTDO);
    vmeanTDOerr[index][cindex].push_back(base->meanTDOerr);
  }

  int Nindex = vMMFE8.size();

  vector<vector<TGraphErrors*> > vgraph_Delay;
  for(int i = 0; i < Nindex; i++){
    vgraph_Delay.push_back(vector<TGraphErrors*>());
    int Ncindex = vCH[i].size();
    for(int c = 0; c < Ncindex; c++){
      int Npoint = vDelay[i][c].size();
      double Delay[Npoint];
      double meanTDO[Npoint];
      double meanTDOerr[Npoint];
      for(int p = 0; p < Npoint; p++){
	Delay[p] = vDelay[i][c][p];
	meanTDO[p] = vmeanTDO[i][c][p];
	meanTDOerr[p] = vmeanTDOerr[i][c][p];
      }
      vgraph_Delay[i].push_back(new TGraphErrors(Npoint, Delay, meanTDO, 0, meanTDOerr));
    }
  }

  TFile* fout = new TFile(output_name.c_str(), "RECREATE");

  // write VMM_data tree to outputfile
  // TChain* base_tree = new TChain("VMM_data");
  // base_tree->AddFile(inputFileName);
  // TTree* new_base_tree = base_tree->CloneTree();
  // fout->cd();
  // new_base_tree->Write();

  // add plots of TDO v Delay for each
  // MMFE8+VMM combo to output file
  fout->mkdir("TDOfit_plots");
  fout->cd("TDOfit_plots");
  for(int i = 0; i < Nindex; i++){
    char sfold[50];
    sprintf(sfold, "TDOfit_plots/Board%d_VMM%d", vMMFE8[i], vVMM[i]);
    fout->mkdir(sfold);
    fout->cd(sfold);

    int Ncindex = vCH[i].size();
    for(int c = 0; c < Ncindex; c++){
      char stitle[50];
      sprintf(stitle, "Board #%d, VMM #%d , CH #%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      char scan[50];
      sprintf(scan, "c_TDOvDelay_Board%d_VMM%d_CH%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      TCanvas* can = Plot_Graph(scan, vgraph_Delay[i][c], "Delay (x5 ns)", "TDO", stitle);
      can->Write();
      delete can;
    }
  }
  fout->cd("");

  // write TDOfitBase tree to outputfile
  TTree* newtree = tree->CloneTree();
  fout->cd();
  newtree->Write();
  delete newtree;
  delete base;
  delete tree;

  // Output TDO calib tree
  double calib_MMFE8;
  double calib_VMM;
  double calib_CH;
  double calib_C;
  double calib_S;
  double calib_chi2;
  double calib_prob;
  
  TTree* calib_tree = new TTree("TDO_calib", "TDO_calib");
  calib_tree->Branch("MMFE8", &calib_MMFE8);
  calib_tree->Branch("VMM", &calib_VMM);
  calib_tree->Branch("CH", &calib_CH);
  calib_tree->Branch("C", &calib_C);
  calib_tree->Branch("S", &calib_S);
  calib_tree->Branch("chi2", &calib_chi2);
  calib_tree->Branch("prob", &calib_prob);

  // Perform fits on each vector of 
  // TDO v converted delay graphs
  fout->mkdir("TDOcalib_plots");
  fout->cd("TDOcalib_plots");
  
  vector<TF1*> vfunc;
  vector<vector<TGraphErrors*> > vgraph;
  for(int i = 0; i < Nindex; i++){
    char sfold[50];
    sprintf(sfold, "TDOcalib_plots/Board%d_VMM%d", vMMFE8[i], vVMM[i]);
    fout->mkdir(sfold);
    fout->cd(sfold);

    vgraph.push_back(vector<TGraphErrors*>());
    int Ncindex = vCH[i].size();
    for(int c = 0; c < Ncindex; c++){
      int Npoint = vDelay[i][c].size();
     
      if(Npoint < 2) 
	continue;

      double max_TDO = 0.;
      int max_delay = 0;
      for(int p = 0; p < Npoint; p++){
	if(vmeanTDO[i][c][p] > max_TDO){
	  max_TDO = vmeanTDO[i][c][p];
	  max_delay = vDelay[i][c][p];
	}
      }

      int max_diff = 0;
      for(int p = 0; p < Npoint; p++){
	double diff;
	if(vDelay[i][c][p] < max_delay)
	  diff = vDelay[i][c][p]+5-max_delay;
	else
	  diff = vDelay[i][c][p]-max_delay;
	if(diff > max_diff)
	  max_diff = diff;
      }

      double meanTDO[Npoint];
      double meanTDOerr[Npoint];
      double meanD[Npoint];
      double meanDerr[Npoint];
      for(int p = 0; p < Npoint; p++){
  	meanTDO[p] = vmeanTDO[i][c][p];
  	meanTDOerr[p] = vmeanTDOerr[i][c][p];
  	if(vDelay[i][c][p] < max_delay){
	  meanD[p] = 5.*max_diff-5.*(vDelay[i][c][p]+5-max_delay);
	} else {
	  meanD[p] = 5.*max_diff-5.*(vDelay[i][c][p]-max_delay);
	}
  	meanDerr[p] = 0.;
      }
      int igraph = vgraph[i].size();
      vgraph[i].push_back(new TGraphErrors(Npoint, meanD, meanTDO, meanDerr, meanTDOerr));

      char fname[50];
      sprintf(fname, "funcP1_MMFE8-%d_VMM-%d_CH-%d", 
  	      vMMFE8[i], vVMM[i], vCH[i][c]);
      
      int ifunc = vfunc.size();
      vfunc.push_back(new TF1(fname, P1, 0., 400., 2));
      
      vfunc[ifunc]->SetParName(0, "C");
      vfunc[ifunc]->SetParName(1, "S");
      
      vgraph[i][igraph]->Fit(fname, "EQ");

      char stitle[50];
      sprintf(stitle, "Board #%d, VMM #%d , CH #%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      char scan[50];
      sprintf(scan, "c_TDOvDelay_Board%d_VMM%d_CH%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      TCanvas* can = Plot_Graph(scan, vgraph[i][igraph], "Converted Time Delay [ns]", "TDO", stitle);
      can->Write();
      delete can;

      calib_MMFE8 = vMMFE8[i];
      calib_VMM = vVMM[i];
      calib_CH = vCH[i][c];
      //calib_C = vfunc[ifunc]->GetParameter(0);
      calib_S = vfunc[ifunc]->GetParameter(1);
      calib_chi2 = vfunc[ifunc]->GetChisquare();
      calib_prob = vfunc[ifunc]->GetProb();

      // set min to 12.5 ns
      calib_C = vminTDO[i][c][0] - calib_S*12.5;

      calib_tree->Fill();
    }
  }
  fout->cd("");
 
  // Write calib_tree to output file
  fout->cd("");
  calib_tree->Write();
  fout->Close();
}

