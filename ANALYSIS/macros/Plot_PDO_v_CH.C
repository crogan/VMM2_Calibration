#include <iostream>
#include <string>

#include "include/setstyle.hh"
#include "include/VMM_data.hh"

using namespace std;

const string X_label = "Channel [1-64*8]";
const string Y_label = "PDO";
const string Z_label = "Count";

void Plot_PDO_v_CH(const string& filename, int MMFE8 = -1){
  setstyle();
  
  TChain* tree = new TChain("VMM_data","VMM_data");

  tree->AddFile(filename.c_str());

  VMM_data* base = new VMM_data(tree);

  int N = tree->GetEntries();
  
  TH2D* hist = new TH2D("hist","hist",
			64*8, 0.5, 64*8+0.5,
			1100, -0.5, 1099.5);

  for(int i = 0; i < N; i++){
    base->GetEntry(i);

    if(base->MMFE8 != MMFE8 && MMFE8 >= 0)
      continue;

    hist->Fill(base->CHword+64*base->VMM,base->PDO);
  }

  TH1D* histX = hist->ProjectionX("1DX",200,1100);

  TCanvas* c1 = Plot_2D("c1", hist, X_label, Y_label, Z_label, "Harvard chamber Run #");
  TCanvas* c2 = Plot_1D("c2", histX, X_label, Z_label, "Harvard chamber Run #");

  // TCanvas* can = new TCanvas("can","can",600,500);
  // can->SetLeftMargin(0.15);
  // can->SetRightMargin(0.22);
  // can->SetBottomMargin(0.15);
  // can->SetTopMargin(0.08);

  // can->Draw();
  // can->SetGridx();
  // can->SetGridy();
  // can->SetLogz();
  
  // can->cd();

  // hist->Draw("COLZ");

  // hist->GetXaxis()->CenterTitle();
  // hist->GetXaxis()->SetTitleFont(132);
  // hist->GetXaxis()->SetTitleSize(0.06);
  // hist->GetXaxis()->SetTitleOffset(1.06);
  // hist->GetXaxis()->SetLabelFont(132);
  // hist->GetXaxis()->SetLabelSize(0.05);
  // hist->GetXaxis()->SetTitle(varXname.c_str());
  // hist->GetYaxis()->CenterTitle();
  // hist->GetYaxis()->SetTitleFont(132);
  // hist->GetYaxis()->SetTitleSize(0.06);
  // hist->GetYaxis()->SetTitleOffset(1.12);
  // hist->GetYaxis()->SetLabelFont(132);
  // hist->GetYaxis()->SetLabelSize(0.05);
  // hist->GetYaxis()->SetTitle(varYname.c_str());
  // hist->GetZaxis()->CenterTitle();
  // hist->GetZaxis()->SetTitleFont(132);
  // hist->GetZaxis()->SetTitleSize(0.06);
  // hist->GetZaxis()->SetTitleOffset(1.3);
  // hist->GetZaxis()->SetLabelFont(132);
  // hist->GetZaxis()->SetLabelSize(0.05);
  // hist->GetZaxis()->SetTitle(varZname.c_str());
  // hist->GetZaxis()->SetRangeUser(0.9*hist->GetMinimum(),1.1*hist->GetMaximum());

  // TLatex l;
  // l.SetTextFont(132);
  // l.SetNDC();
  // l.SetTextSize(0.05);
  // l.SetTextFont(132);
  // l.DrawLatex(0.5,0.943,"MMFE8 Analysis");
  // l.SetTextSize(0.04);
  // l.SetTextFont(42);
  // l.DrawLatex(0.15,0.943,"#bf{#it{ATLAS}} Internal");

  // l.SetTextSize(0.06);
  // l.SetTextFont(132);
  // l.DrawLatex(0.80,0.04, "Run 5");

  // TCanvas* canP = new TCanvas("canP","canP",600,500);
  // canP->SetLeftMargin(0.15);
  // canP->SetRightMargin(0.05);
  // canP->SetBottomMargin(0.15);
  // canP->SetTopMargin(0.08);
  // canP->Draw();

  // TH1D* histX = hist->ProjectionX("1DX",200,1100);
  // histX->Draw();
  // histX->GetXaxis()->CenterTitle();
  // histX->GetXaxis()->SetTitleFont(132);
  // histX->GetXaxis()->SetTitleSize(0.06);
  // histX->GetXaxis()->SetTitleOffset(1.06);
  // histX->GetXaxis()->SetLabelFont(132);
  // histX->GetXaxis()->SetLabelSize(0.05);
  // histX->GetXaxis()->SetTitle(varXname.c_str());
  // histX->GetYaxis()->CenterTitle();
  // histX->GetYaxis()->SetTitleFont(132);
  // histX->GetYaxis()->SetTitleSize(0.06);
  // histX->GetYaxis()->SetTitleOffset(1.12);
  // histX->GetYaxis()->SetLabelFont(132);
  // histX->GetYaxis()->SetLabelSize(0.05);
  // histX->GetYaxis()->SetTitle(varZname.c_str());
  
}

