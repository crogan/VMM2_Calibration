#ifndef SETSTYLE_h
#define SETSTYLE_h

#include <TStyle.h>
#include <TColor.h>

void setstyle(){

  // For the canvas:
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(kWhite);
  gStyle->SetCanvasDefX(0);
  gStyle->SetCanvasDefY(0);
    
  // For the Pad:
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(kWhite);
  gStyle->SetGridColor(0);
  gStyle->SetGridStyle(3);
  gStyle->SetGridWidth(1);
    
  // For the frame:
  gStyle->SetFrameBorderMode(0);
  gStyle->SetFrameBorderSize(1);
  gStyle->SetFrameFillColor(0);
  gStyle->SetFrameFillStyle(0);
  gStyle->SetFrameLineColor(1);
  gStyle->SetFrameLineStyle(1);
  gStyle->SetFrameLineWidth(1);
    
  // set the paper & margin sizes
  gStyle->SetPaperSize(20,26);
  gStyle->SetPadTopMargin(0.09);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadBottomMargin(0.18);
  gStyle->SetPadLeftMargin(0.15);
    
  // use large Times-Roman fonts
  gStyle->SetTitleFont(132,"xyz");  // set the all 3 axes title font
  gStyle->SetTitleFont(132," ");    // set the pad title font
  gStyle->SetTitleSize(0.06,"xyz"); // set the 3 axes title size
  gStyle->SetTitleSize(0.06," ");   // set the pad title size
  gStyle->SetLabelFont(132,"xyz");

  gStyle->SetLabelSize(0.05,"xyz");
  gStyle->SetLabelColor(1,"xyz");
  gStyle->SetTextFont(132);
  gStyle->SetTextSize(0.08);
  gStyle->SetStatFont(132);
    
  // use bold lines and markers
  gStyle->SetMarkerStyle(8);
  gStyle->SetHistLineWidth(2);
  gStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes
	
  //..Get rid of X error bars
  gStyle->SetErrorX(0.001);
    
  // do not display any of the standard histogram decorations
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(11111111);
    
  // put tick marks on top and RHS of plots
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

 int NZPalette = 28;
 double zcolor_s[5] = { 0.00, 0.50, 0.70, 0.82, 1.00 };
 double zcolor_r[5] = { 0.00, 0.00, 0.74, 1.00, 1.00 };
 double zcolor_g[5] = { 0.00, 0.61, 0.82, 0.70, 1.00 };
 double zcolor_b[5] = { 0.31, 0.73, 0.08, 0.00, 1.00 };

 TColor::CreateGradientColorTable(5, zcolor_s, zcolor_r,
				  zcolor_g, zcolor_b, NZPalette);

  gStyle->cd();
}

const TColor blue0(7000,0.749,0.78,0.933);
const TColor blue1(7001,0.424,0.467,0.651);
const TColor blue2(7002,0.255,0.302,0.522);
const TColor blue3(7003,0.114,0.165,0.396);
const TColor blue4(7004,0.024,0.063,0.251);
const TColor green0(7010,0.737,0.949,0.784);
const TColor green1(7011,0.435,0.722,0.498);
const TColor green2(7012,0.239,0.576,0.314);
const TColor green3(7013,0.082,0.439,0.161);
const TColor green4(7014,0,0.275,0.063);
const TColor red0(7020,1,0.796,0.776);
const TColor red1(7021,0.957,0.612,0.576);
const TColor red2(7022,0.765,0.361,0.318);
const TColor red3(7023,0.58,0.157,0.11);
const TColor red4(7024,0.365,0.035,0);
const TColor yellow0(7030,1,0.933,0.776);
const TColor yellow1(7031,0.957,0.843,0.576);
const TColor yellow2(7032,0.765,0.631,0.318);
const TColor yellow3(7033,0.58,0.443,0.11);
const TColor yellow4(7034,0.365,0.259,0);
const TColor purple0(7040,0.937,0.729,0.898);
const TColor purple1(7041,0.753,0.478,0.702);
const TColor purple2(7042,0.6,0.286,0.541);
const TColor purple3(7043,0.42,0.075,0.353);
const TColor purple4(7044,0.196,0,0.161);
const TColor cyan0(7050,0.714,0.898,0.918);
const TColor cyan1(7051,0.424,0.639,0.659);
const TColor cyan2(7052,0.247,0.49,0.51);
const TColor cyan3(7053,0.067,0.329,0.357);
const TColor cyan4(7054,0,0.153,0.169);
const TColor orange0(7060,1,0.882,0.776);
const TColor orange1(7061,1,0.808,0.639);
const TColor orange2(7062,0.839,0.608,0.4);
const TColor orange3(7063,0.584,0.329,0.106);
const TColor orange4(7064,0.275,0.129,0);
const TColor lime0(7070,0.941,0.992,0.769);
const TColor lime1(7071,0.882,0.961,0.612);
const TColor lime2(7072,0.706,0.8,0.38);
const TColor lime3(7073,0.455,0.557,0.098);
const TColor lime4(7074,0.204,0.263,0);

#endif
