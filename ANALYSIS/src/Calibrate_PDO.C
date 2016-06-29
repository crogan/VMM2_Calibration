#include <iostream>

#include "include/setstyle.hh"
#include "include/fit_functions.hh"
#include "include/DACToCharge.hh"
#include "include/PDOfitBase.hh"

using namespace std;

int main(int argc, char* argv[]){
  setstyle();

  char inputFileName[400];
  char outputFileName[400];
  char xADCFileName[400];
  
  if ( argc < 4 ){
    cout << "Error at Input: please specify an input .root file, ";
    cout << "an xADC calibration file, ";
    cout << " and an (optional) output filename" << endl;
    cout << "Example:   ./Calibrate_PDO input_file.root -x xADCcalib_file.root" << endl;
    cout << "Example:   ./Calibrate_PDO input_file.root -x xADCcalib_file.root -o output_file.root" << endl;
    return 1;
  }

  sscanf(argv[1],"%s", inputFileName);
  bool user_output = false;
  bool user_xADC   = false;
  for (int i=0;i<argc;i++){
    if (strncmp(argv[i],"-o",2)==0){
      sscanf(argv[i+1],"%s", outputFileName);
      user_output = true;
    }
    if (strncmp(argv[i],"-x",2)==0){
      sscanf(argv[i+1],"%s", xADCFileName);
      user_xADC = true;
    }
  }

  if(!user_xADC){
    cout << "Error at Input: please specify an xADC calibration file: " << endl;
    cout << "Example:   ./Calibrate_PDO input_file.root -x xADCcalib_file.root" << endl;
    cout << "Example:   ./Calibrate_PDO input_file.root -x xADCcalib_file.root -o output_file.root" << endl;
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
    output_name = input_name+"_PDOcalib.root";
    sprintf(outputFileName,"%s.root",inputFileName);
  } else {
    output_name = string(outputFileName);
  }

  // xADC calibration object
  DACToCharge DAC2Charge(xADCFileName);

  TChain* tree = new TChain("PDO_fit");
  tree->AddFile(inputFileName);

  PDOfitBase* base = new PDOfitBase(tree);

  int N = tree->GetEntries();
  if(N == 0) return 0;

  map<pair<int,int>, int> MMFE8VMM_to_index;
  vector<map<int,int> >   vCH_to_index;
  
  vector<int>             vMMFE8;               // board ID
  vector<int>             vVMM;                 // VMM number
  vector<vector<int> >    vCH;                  // channel number
  vector<vector<vector<double> > > vmeanPDO;    // mean PDO
  vector<vector<vector<double> > > vmeanPDOerr; // mean PDO err
  vector<vector<vector<int> > >    vDAC;        // DAC value

  int MMFE8;
  int VMM;
  int CH;

  for(int i = 0; i < N; i++){
    base->GetEntry(i);

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
      vmeanPDO.push_back(vector<vector<double> >());
      vmeanPDOerr.push_back(vector<vector<double> >());
      vDAC.push_back(vector<vector<int> >());
    }

    // MMFE8+VMM index
    int index = MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)];

    // add a new channel if is new for
    // this MMFE8+VMM combination
    if(vCH_to_index[index].count(CH) == 0){
      int ind = int(vCH[index].size());
      vCH_to_index[index][CH] = ind;
      vCH[index].push_back(CH);
      vmeanPDO[index].push_back(vector<double>());
      vmeanPDOerr[index].push_back(vector<double>());
      vDAC[index].push_back(vector<int>());
    }

    // CH index
    int cindex = vCH_to_index[index][CH];

    vDAC[index][cindex].push_back(base->DAC);
    vmeanPDO[index][cindex].push_back(base->meanPDO);
    vmeanPDOerr[index][cindex].push_back(base->sigmaPDO);
  }

  int Nindex = vMMFE8.size();

  vector<vector<TGraphErrors*> > vgraph;
  vector<vector<TGraphErrors*> > vgraph_DAC;
  vector<vector<double> > vmax;
  vector<vector<double> > vQmax;
  for(int i = 0; i < Nindex; i++){
    vgraph.push_back(vector<TGraphErrors*>());
    vgraph_DAC.push_back(vector<TGraphErrors*>());
    vmax.push_back(vector<double>());
    vQmax.push_back(vector<double>());
    int Ncindex = vCH[i].size();
    for(int c = 0; c < Ncindex; c++){
      int Npoint = vDAC[i][c].size();
      double DAC[Npoint];
      double meanPDO[Npoint];
      double meanPDOerr[Npoint];
      double meanQ[Npoint];
      double meanQerr[Npoint];
      vmax[i].push_back(-1.);
      vQmax[i].push_back(-1.);
      for(int p = 0; p < Npoint; p++){
	DAC[p] = vDAC[i][c][p];
	meanPDO[p] = vmeanPDO[i][c][p];
	meanPDOerr[p] = vmeanPDOerr[i][c][p];
	meanQ[p] = DAC2Charge.GetCharge(DAC[p], vMMFE8[i], vVMM[i]);
	meanQerr[p] = DAC2Charge.GetChargeError(DAC[p], vMMFE8[i], vVMM[i]);
	if(meanPDO[p] > 1.02*vmax[i][c]){
	  vmax[i][c]  = meanPDO[p];
	  vQmax[i][c] = meanQ[p];
	}
      }
      vgraph[i].push_back(new TGraphErrors(Npoint, meanQ, meanPDO, meanQerr, meanPDOerr));
      vgraph_DAC[i].push_back(new TGraphErrors(Npoint, DAC, meanPDO, 0, meanPDOerr));
    }
  }

  TFile* fout = new TFile(output_name.c_str(), "RECREATE");

  // write VMM_data tree to outputfile
  TChain* base_tree = new TChain("VMM_data");
  base_tree->AddFile(inputFileName);
  TTree* new_base_tree = base_tree->CloneTree();
  fout->cd();
  new_base_tree->Write();

  // add plots of PDO v DAC for each
  // MMFE8+VMM combo to output file
  fout->mkdir("PDOfit_plots");
  fout->cd("PDOfit_plots");
  for(int i = 0; i < Nindex; i++){
    char sfold[50];
    sprintf(sfold, "PDOfit_plots/Board%d_VMM%d", vMMFE8[i], vVMM[i]);
    fout->mkdir(sfold);
    fout->cd(sfold);

    int Ncindex = vCH[i].size();
    for(int c = 0; c < Ncindex; c++){
      char stitle[50];
      sprintf(stitle, "Board #%d, VMM #%d , CH #%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      char scan[50];
      sprintf(scan, "c_PDOvDAC_Board%d_VMM%d_CH%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      TCanvas* can = Plot_Graph(scan, vgraph_DAC[i][c], "Test Pulse DAC", "PDO", stitle);
      can->Write();
      delete can;
    }
  }
  fout->cd("");

  // write PDOfitBase tree to outputfile
  TTree* newtree = tree->CloneTree();
  fout->cd();
  newtree->Write();
  delete newtree;
  delete base;
  delete tree;

  // Output PDO calib tree
  double calib_MMFE8;
  double calib_VMM;
  double calib_CH;
  double calib_c0;
  double calib_A2;
  double calib_t02;
  double calib_d21;
  double calib_chi2;
  double calib_prob;
  
  TTree* calib_tree = new TTree("PDO_calib", "PDO_calib");
  calib_tree->Branch("MMFE8", &calib_MMFE8);
  calib_tree->Branch("VMM", &calib_VMM);
  calib_tree->Branch("CH", &calib_CH);
  calib_tree->Branch("c0", &calib_c0);
  calib_tree->Branch("A2", &calib_A2);
  calib_tree->Branch("t02", &calib_t02);
  calib_tree->Branch("d21", &calib_d21);
  calib_tree->Branch("chi2", &calib_chi2);
  calib_tree->Branch("prob", &calib_prob);

  // Perform fits on each vector of 
  // PDO v charge graphs
  fout->mkdir("PDOcalib_plots");
  fout->cd("PDOcalib_plots");

  vector<TF1*> vfunc;
  for(int i = 0; i < Nindex; i++){
    char sfold[50];
    sprintf(sfold, "PDOcalib_plots/Board%d_VMM%d", vMMFE8[i], vVMM[i]);
    fout->mkdir(sfold);
    fout->cd(sfold);

    int Ncindex = vCH[i].size();
    for(int c = 0; c < Ncindex; c++){
      char fname[50];
      sprintf(fname, "funcP1P2P0_MMFE8-%d_VMM-%d_CH-%d", 
	      vMMFE8[i], vVMM[i], vCH[i][c]);
      int ifunc = vfunc.size();
      vfunc.push_back(new TF1(fname, P1_P2_P0, 0., 400., 4));

      vfunc[ifunc]->SetParName(0, "c_{0}");
      vfunc[ifunc]->SetParameter(0, vmax[i][c]);
      vfunc[ifunc]->SetParName(1, "A_{2}");
      vfunc[ifunc]->SetParameter(1, -0.5);
      vfunc[ifunc]->SetParName(2, "t_{0 , 2}");
      vfunc[ifunc]->SetParameter(2, vQmax[i][c]);
      vfunc[ifunc]->SetParName(3, "d_{2 , 1}");
      vfunc[ifunc]->SetParameter(3, -10.);
      
      vfunc[ifunc]->SetParLimits(3, -10000., 0.);
      
      if(vVMM[i] != 0 && vVMM[i] != 1){
	cout << vVMM[i] << " " << vCH[i][c] << endl;
	cout << vmax[i][c] << " " << vQmax[i][c] << endl;
	vgraph[i][c]->Fit(fname, "EQ");
      }

      char stitle[50];
      sprintf(stitle, "Board #%d, VMM #%d , CH #%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      char scan[50];
      sprintf(scan, "c_PDOvQ_Board%d_VMM%d_CH%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      TCanvas* can = Plot_Graph(scan, vgraph[i][c], "Injected Charge (fC)", "PDO", stitle);
      can->Write();
      delete can;
      
      calib_MMFE8 = vMMFE8[i];
      calib_VMM = vVMM[i];
      calib_CH = vCH[i][c];
      calib_c0 = vfunc[ifunc]->GetParameter(0);
      calib_A2 = vfunc[ifunc]->GetParameter(1);
      calib_t02 = vfunc[ifunc]->GetParameter(2);
      calib_d21 = vfunc[ifunc]->GetParameter(3);
      calib_chi2 = vfunc[ifunc]->GetChisquare();
      calib_prob = vfunc[ifunc]->GetProb();

      calib_tree->Fill();
    }  
  }
  fout->cd("");
 
  // Write calib_tree to output file
  fout->cd("");
  calib_tree->Write();
  fout->Close();
}

