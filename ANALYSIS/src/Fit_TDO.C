#include <iostream>

#include "include/setstyle.hh"
#include "include/fit_functions.hh"
#include "include/VMM_data.hh"

using namespace std;

int main(int argc, char* argv[]){
  setstyle();

  char inputFileName[400];
  char outputFileName[400];

  if ( argc < 2 ){
    cout << "Error at Input: please specify an input .root file ";
    cout << "and an (optional) output filename" << endl;
    cout << "Example:   ./Fit_TDO input_file.root" << endl;
    cout << "Example:   ./Fit_TDO input_file.root -o output_file.root" << endl;
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
    output_name = input_name+"_TDOfit.root";
    sprintf(outputFileName,"%s.root",inputFileName);
  } else {
    output_name = string(outputFileName);
  }

  TChain* tree = new TChain("VMM_data");
  tree->AddFile(inputFileName);

  VMM_data* base = new VMM_data(tree);

  int N = tree->GetEntries();
  if(N == 0) return 0;

  map<pair<int,int>, int> MMFE8VMM_to_index;
  vector<map<int,int> >   vCH_to_index;
  vector<map<int,int> >   vCH_to_maxDAC;

  vector<vector<map<int, TH1D*> > > vDelay_to_hist;
  
  vector<int>             vMMFE8;               // board ID
  vector<int>             vVMM;                 // VMM number
  vector<vector<int> >    vCH;                  // channel number
  vector<vector<TH1D*> >           vhist_all;   // all TDO histograms
  vector<vector<vector<TH1D*> > >  vhist;       // TDO histograms by delay
  vector<vector<vector<int> > >    vDelay;      // Delay value
  vector<vector<vector<string> > > vlabel;      // label

  int MMFE8;
  int VMM;
  int Delay;
  int CH;
  cout << "Processing Trees" << endl;
  for (int i = 0; i < N; i++){
    base->GetEntry(i);

    if(base->CHword != base->CHpulse)
      continue;

    if(base->PDO <=  0)
      continue;

    if(base->TDO <=  0)
      continue;

    // only take first 5 delays
    // if(base->Delay > 4)
    //   continue;

    MMFE8 = base->MMFE8;
    VMM   = base->VMM;
    //Delay = base->Delay;
    Delay = base->Delay%5;
    CH    = base->CHword;
    
    // add a new MMFE8+VMM entry if
    // is a new MMFE8+VMM combination
    if(MMFE8VMM_to_index.count(pair<int,int>(MMFE8,VMM)) == 0){
      int ind = int(vMMFE8.size());
      MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)] = ind;
      vMMFE8.push_back(MMFE8);
      vVMM.push_back(VMM);
      vCH.push_back(vector<int>());
      vCH_to_index.push_back(map<int,int>());
      vCH_to_maxDAC.push_back(map<int,int>());
      vDelay_to_hist.push_back(vector<map<int,TH1D*> >());
      vhist.push_back(vector<vector<TH1D*> >());
      vDelay.push_back(vector<vector<int> >());
      vlabel.push_back(vector<vector<string> >());
      vhist_all.push_back(vector<TH1D*>());
    }

    // MMFE8+VMM index
    int index = MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)];

    // add a new channel if is new for
    // this MMFE8+VMM combination
    if(vCH_to_index[index].count(CH) == 0){
      int ind = int(vCH[index].size());
      vCH_to_index[index][CH] = ind;
      vCH_to_maxDAC[index][CH] = base->TPDAC;
      vCH[index].push_back(CH);
      vDelay_to_hist[index].push_back(map<int,TH1D*>());
      vhist[index].push_back(vector<TH1D*>());
      vDelay[index].push_back(vector<int>());
      vlabel[index].push_back(vector<string>());
      char shist_all[20];
      sprintf(shist_all,"%d_%d_%d_all",MMFE8,VMM,CH);
      TH1D* hist = new TH1D(("h_"+string(shist_all)).c_str(),
			    ("h_"+string(shist_all)).c_str(),
			    4096, -0.5, 4095.5);
      vhist_all[index].push_back(hist);
    }

    // CH index
    int cindex = vCH_to_index[index][CH];

    vhist_all[index][cindex]->Fill(base->TDO);

    if(base->TPDAC > vCH_to_maxDAC[index][CH])
      vCH_to_maxDAC[index][CH] = base->TPDAC;
  }

  for (int i = 0; i < N; i++){
    base->GetEntry(i);

    if(base->CHword != base->CHpulse)
      continue;

    if(base->PDO <=  0)
      continue;

    if(base->TDO <=  0)
      continue;

    MMFE8 = base->MMFE8;
    VMM   = base->VMM;
    //Delay = base->Delay;
    Delay = base->Delay%5;
    CH    = base->CHword;

    // MMFE8+VMM index
    int index = MMFE8VMM_to_index[pair<int,int>(MMFE8,VMM)];

    // CH index
    int cindex = vCH_to_index[index][CH];

    // take only max DAC
    // if(base->TPDAC != 200)
    //   continue;
    if(base->TPDAC != vCH_to_maxDAC[index][CH])
      continue;

    // add a new histogram if this Delay
    // combination is new for the MMFE8+VMM+CH combo
    if(vDelay_to_hist[index][cindex].count(Delay) == 0){
      char sDelay[20];
      sprintf(sDelay,"%d",Delay);
      char shist[20];
      sprintf(shist,"%d_%d_%d_%d",MMFE8,VMM,CH,Delay);
      TH1D* hist = new TH1D(("h_"+string(shist)).c_str(),
			    ("h_"+string(shist)).c_str(),
			    4096, -0.5, 4095.5);
      vDelay_to_hist[index][cindex][Delay] = hist;
      vhist[index][cindex].push_back(hist);
      vDelay[index][cindex].push_back(Delay);
      vlabel[index][cindex].push_back("Delay = "+string(sDelay));
    }

    vDelay_to_hist[index][cindex][Delay]->Fill(base->TDO);
  }

  int Nindex = vMMFE8.size();

  TFile* fout = new TFile(output_name.c_str(), "RECREATE");

  // add plots of TDO values for each
  // MMFE8+VMM+CH combo to output file
  fout->mkdir("TDO_plots");
  fout->cd("TDO_plots");
  cout << "Drawing Histograms" << endl;
  for(int i = 0; i < Nindex; i++){ 
    char sfold[50];
    sprintf(sfold, "TDO_plots/Board%d_VMM%d", vMMFE8[i], vVMM[i]);
    fout->mkdir(sfold);
    fout->cd(sfold);

    int Ncindex = vCH[i].size();
    for(int c = 0; c < Ncindex; c++){
      char stitle[50];
      sprintf(stitle, "Board #%d, VMM #%d , CH #%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      if(vhist[i][c].size() > 0){
	char scan[50];
	sprintf(scan, "c_TDO_Board%d_VMM%d_CH%d", vMMFE8[i], vVMM[i], vCH[i][c]);
	TCanvas* can = Plot_1D(scan, vhist[i][c], "TDO", "Count", stitle, vlabel[i][c]);
	can->Write();
	delete can;
      }
      char scan_all[100];
      sprintf(scan_all, "c_allTDO_Board%d_VMM%d_CH%d", vMMFE8[i], vVMM[i], vCH[i][c]);
      TCanvas* can_all = Plot_1D(scan_all, vhist_all[i][c], "TDO", "Count", stitle);
      can_all->Write();
      delete can_all;
    }
  }
  fout->cd("");

  // write VMM_data tree to outputfile
  // TTree* newtree = tree->CloneTree();
  // fout->cd();
  // newtree->Write();
  // delete newtree;
  // delete base;
  // delete tree;

  // Output PDO fit tree
  double fit_MMFE8;
  double fit_VMM;
  double fit_CH;
  double fit_Delay;
  double fit_meanTDO;
  double fit_sigmaTDO;
  double fit_meanTDOerr;
  double fit_sigmaTDOerr;
  double fit_chi2;
  double fit_prob;
  double fit_minTDO;
  double fit_maxTDO;
  
  TTree* fit_tree = new TTree("TDO_fit", "TDO_fit");
  fit_tree->Branch("MMFE8", &fit_MMFE8);
  fit_tree->Branch("VMM", &fit_VMM);
  fit_tree->Branch("CH", &fit_CH);
  fit_tree->Branch("Delay", &fit_Delay);
  fit_tree->Branch("meanTDO", &fit_meanTDO);
  fit_tree->Branch("meanTDOerr", &fit_meanTDOerr);
  fit_tree->Branch("sigmaTDO", &fit_sigmaTDO);
  fit_tree->Branch("sigmaTDOerr", &fit_sigmaTDOerr);
  fit_tree->Branch("chi2", &fit_chi2);
  fit_tree->Branch("prob", &fit_prob);
  fit_tree->Branch("minTDO", &fit_minTDO);
  fit_tree->Branch("maxTDO", &fit_maxTDO);

  cout << "Extracting TDO values" << endl;

  // currently, no fit performed extracting TDO values
  for(int i = 0; i < Nindex; i++){
    fit_MMFE8 = vMMFE8[i];
    fit_VMM = vVMM[i];
    int Ncindex = vCH[i].size();
    for(int c = 0; c < Ncindex; c++){
      if(vhist[i][c].size() <= 0)
	 continue;
      fit_CH = vCH[i][c];

      fit_minTDO = 0; 
      fit_maxTDO = 4000;
      for(int b = 1; b < 4000; b++){
	if(vhist_all[i][c]->GetBinContent(b) > 0){
	  fit_minTDO = b-1;
	  break;
	}
      }
      for(int b = 4000; b >= 1; b--){
	if(vhist_all[i][c]->GetBinContent(b) > 0){
	  fit_maxTDO = b-1;
	  break;
	}
      }

      int Ndelay = vDelay[i][c].size();
      for(int d = 0; d < Ndelay; d++){
	fit_Delay = vDelay[i][c][d];
	double I = vhist[i][c][d]->Integral();
	fit_meanTDO = vhist[i][c][d]->GetMean();
	fit_meanTDOerr = max(vhist[i][c][d]->GetRMS()/sqrt(I),1.);
	fit_sigmaTDO = max(vhist[i][c][d]->GetRMS(),1.);
	fit_sigmaTDOerr = max(vhist[i][c][d]->GetRMSError(),1.);
	fit_chi2 = 0.;
	fit_prob = 1.;
	
	fit_tree->Fill();
      }
    }
  }

  // Write fit_tree to output file
  fout->cd("");
  fit_tree->Write();
  fout->Close();
}
