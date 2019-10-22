#!/usr/bin/env python
'''

Welcome to contours_to_summary.py

  Overlays contours from chiSq_to_contours.py onto a single plot

'''

# So Root ignores command line inputs so we can use argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import *
import os, sys, time, argparse, math, datetime, csv

SQRTS_LUMI = '#sqrt{s} = 14 TeV, 3000 fb^{#minus1}'
  

#____________________________________________________________________________
def main():
  
  t0 = time.time()
  
  can  = TCanvas('','',1300,1000) 
  
  mkdir('contours')
  
  # ------------------------------------------------------
  # User configurables 
  # ------------------------------------------------------
  
  # ------------------------------------------------------
  # Input/output file names TODO: clumsy, use argparse etc
  # ------------------------------------------------------
  
  l_contours = [
  'boosted-finalSR',
  'intermediate-finalSR', 
  'resolved-finalSR', 
  'resolved-finalSR_intermediate-finalSR_boosted-finalSR_combined',
  'boosted-finalSRNN',
  'intermediate-finalSRNN', 
  'resolved-finalSRNN', 
  'resolved-finalSRNN_intermediate-finalSRNN_boosted-finalSRNN_combined']
  
  d_tlatex = {
    'resolved-finalSR'       : 'Resolved',
    'intermediate-finalSR'   : 'Intermediate',
    'boosted-finalSR'        : 'Boosted',
    'resolved-finalSRNN'     : 'Resolved',
    'intermediate-finalSRNN' : 'Intermediate',
    'boosted-finalSRNN'      : 'Boosted',
    'resolved-finalSR_intermediate-finalSR_boosted-finalSR_combined'       : 'Combined',
    'resolved-finalSRNN_intermediate-finalSRNN_boosted-finalSRNN_combined' : 'Combined'
  }

  xCol, yCol = 'x', 'y'
  save_name = 'figs/summary_contours_2d.pdf'
    
  print( '--------------------------------------------------------------' )
  print( '\nWelcome to contours_to_summary.py\n' )
  print( 'Contours to summarise: {0}'.format(l_contours) )
  print( 'Saving contour coordinates to file:\n  {0}\n'.format(save_name) )
  print( '-----------------------------------------------------------------\n' )
  
  d_tg = {}

  for contour in l_contours:
    
    
    if 'combined' in contour:
      in_file = 'contours/limit2d_{0}_SlfCoup_TopYuk_sum_chiSqSyst1pc.csv'.format(contour)
    else:
      in_file = 'contours/limit2d_{0}_SlfCoup_TopYuk_chiSqSyst1pc.csv'.format(contour)
    print('Reading: {0}'.format(in_file))
    # ------------------------------------------------------
    # First Convert the csv into lists 
    # where column header is key of dictionary, values as list
    # ------------------------------------------------------
    d_csv = csv_to_lists( in_file )
     
    # ------------------------------------------------------
    # First convert the csv file into a TGraph 2D
    # ------------------------------------------------------
    d_tg[contour] = csv_to_graph( d_csv, xCol, yCol )
    
  print( 'Making contour plot' )
  
  # ------------------------------------------------------
  # Make summary plot 
  # ------------------------------------------------------
  mk_plot( l_contours, d_tg, save_name, d_tlatex)

#____________________________________________________________________________
def mk_plot(l_contours, d_tg, save_name, d_tlatex):
  '''
  '''

  # ------------------------------------------------------
  # Make canvas 
  # ------------------------------------------------------
  can1 = TCanvas('','',1300,1000)
  can1.cd()

  # Blues
  myLightBlue     = TColor.GetColor('#9ecae1')
  myMediumBlue    = TColor.GetColor('#0868ac')
  myDarkBlue      = TColor.GetColor('#08306b')

  # Oranges
  myLightOrange   = TColor.GetColor('#fec49f')
  myMediumOrange  = TColor.GetColor('#fe9929')
  myDarkOrange    = TColor.GetColor('#ec7014')
  myDarkerOrange  = TColor.GetColor('#cc4c02')
  
  myDarkRed       = TColor.GetColor('#a50f15')

  # Pinks
  myLightPink     = TColor.GetColor('#fde0dd')
  myMediumPink    = TColor.GetColor('#fcc5c0')
  myDarkPink      = TColor.GetColor('#dd3497')

  # Purples
  myLightPurple   = TColor.GetColor('#dadaeb')
  myMediumPurple  = TColor.GetColor('#9e9ac8')
  myDarkPurple    = TColor.GetColor('#6a51a3')
  
  l_colours = [
    myLightBlue,
    myMediumBlue,
    myDarkBlue,
    myDarkPurple,
    myLightOrange,
    myMediumOrange,
    myDarkRed,
    myDarkPink
    ]
 
  # Dummy graph as first one 
  l_dummy_x = [-30, 30, 30, -30]
  l_dummy_y = [3, 3, -1, -1]
  tg_dummy = TGraph()
  for count, ( x_val, y_val ) in enumerate( zip( l_dummy_x, l_dummy_y ) ) :
    tg_dummy.SetPoint(count, float(x_val), float(y_val) )  
  
  tg_dummy.Draw('AL')
  tg_dummy.SetTitle('')
  tg_dummy.GetXaxis().SetRangeUser(-19,18)
  tg_dummy.GetYaxis().SetRangeUser(0.6,1.4)
  
  xtitle = '#kappa(#lambda_{hhh})'
  ytitle = '#kappa(#it{y}_{top})'
  customise_axes(tg_dummy, xtitle, ytitle)

  # Marker for SM
  tg_sm = TGraph()
  tg_sm.SetPoint(0, 1, 1)
  tg_sm.SetMarkerSize(2.1)
  tg_sm.SetMarkerColor(kGray+2)
  tg_sm.SetMarkerStyle(34)

  #-------------------------------------------------
  # Construct and add plots to legend
  #-------------------------------------------------
  xl1=0.57
  yl1=0.23
  xl2=xl1+0.20
  yl2=yl1+0.17
  # Blues baseline
  leg = TLegend(xl1,yl1,xl2,yl2)
  leg.SetBorderSize(0)
  leg.SetTextFont(132)
  leg.SetTextSize(0.04)
  leg.SetNColumns(1)

  # Oranges DNN
  leg0 = TLegend(xl1-0.06,yl1,xl1+0.15,yl2)
  leg0.SetBorderSize(0)
  leg0.SetTextFont(132)
  leg0.SetTextSize(0.033)
  leg0.SetNColumns(1)

  #-------------------------------------------------
  # Loop over contours and draw them
  #-------------------------------------------------
  for i, contour in enumerate(l_contours):
    tg = d_tg[contour]
    tg.Draw('L same')
    tg.SetLineColor(l_colours[i])
    tg.SetLineWidth(2)
    # Neural network contours
    if 'SRNN' in contour:
      tg.SetLineStyle(1)
      leg0.AddEntry(tg, '', 'L')
    # Baseline contours
    else:
      tg.SetLineStyle(2)
      leg.AddEntry(tg, d_tlatex[contour], 'L')

    if 'resolved' in contour:
      tg.SetLineWidth(4)
    if 'intermediate' in contour:
      tg.SetLineWidth(3)
    if 'boosted' in contour:
      tg.SetLineWidth(2)
    if 'combined' in contour:
      tg.SetLineWidth(5)

  customise_gPad()
  
  # Draw annotating objects
  tg_sm.Draw('P same')
  leg0.Draw('same')
  leg.Draw('same')
  
  #-------------------------------------------------
  # Text
  #-------------------------------------------------
  # Extra text
  top_txt = 'hh #rightarrow 4b, 68% CL contours, 1% systematics'
  # Text at top
  myText(0.18, 0.91, SQRTS_LUMI + ', ' + top_txt, 0.040, kBlack, 0, True)

  # Add text to plot interior
  myText(0.510, 0.41, 'DNN', 0.035, kBlack, 0, True)
  myText(0.575, 0.41, 'Baseline', 0.035, kBlack, 0, True)
  myText(0.60, 0.55,  'SM', 0.04, kGray+2, 0, True)
  
  gPad.RedrawAxis()

  can1.SaveAs( save_name )
  can1.Close() 

#____________________________________________________________________________
def csv_to_graph( d_csv, xCol, yCol ):
  '''
  Specify the the column in the CSV file to plot in the TGraph by 
  '''
  tg = TGraph()
  count = 0 

  for count, ( x_val, y_val ) in enumerate( zip( d_csv[xCol], d_csv[yCol] ) ) :
    tg.SetPoint(count, float(x_val), float(y_val) )  

  return tg

#____________________________________________________________________________
def customise_gPad(top=0.12, bot=0.19, left=0.17, right=0.05):
  gPad.Update()
  gStyle.SetTitleFontSize(0.0)
  
  # gPad margins
  gPad.SetTopMargin(top)
  gPad.SetBottomMargin(bot)
  gPad.SetLeftMargin(left)
  gPad.SetRightMargin(right)
  
  gStyle.SetOptStat(0) # hide usual stats box 
  
  gPad.Update()

#____________________________________________________________________________
#def customise_axes(hist, xtitle, ytitle, ztitle, scaleFactor=1.1, IsLogY=False, xmin=0, xmax=300, ymin=0, ymax=10):
def customise_axes(hist, xtitle, ytitle):

  # set a universal text size
  text_size = 0.055
  #text_size = 50

  TGaxis.SetMaxDigits(4) 
  ##################################
  # X axis
  xax = hist.GetXaxis()
  xax.CenterTitle()
  
  # Times 132
  xax.SetLabelFont(132)
  xax.SetTitleFont(132)
  
  xax.SetTitle(xtitle)
  xax.SetTitleSize(text_size*1.2)
  # top panel
  #if xtitle == '':
  xax.SetLabelSize(text_size)
  xax.SetLabelOffset(0.02)
  xax.SetTitleOffset(1.3)
  xax.SetTickSize(0.03)

 
  #xax.SetRangeUser(50,600) 
  gPad.Update()
  #xax.SetNdivisions(-505) 
  gPad.SetTickx() 
  
  ##################################
  # Y axis
  yax = hist.GetYaxis()
  yax.CenterTitle()
  
  # Times 132
  yax.SetLabelFont(132)
  yax.SetTitleFont(132)
 
  yax.SetTitle(ytitle)
  yax.SetTitleSize(text_size*1.2)
  yax.SetTitleOffset(1.25)    
  #yax.SetNdivisions(-505) 
  #yax.SetRangeUser(0, 250) 
  
  yax.SetLabelOffset(0.015)
  yax.SetLabelSize(text_size)
 
  gPad.SetTicky()

  gPad.Update()

#__________________________________________
def csv_to_lists(csv_file):
  '''
  converts csv to dictionary of lists containing columns
  the dictionary keys is the header
  '''
  with open(csv_file) as input_file:
      reader = csv.reader(input_file)
      col_names = next(reader)
      data = {name: [] for name in col_names}
      for line in reader:
        for pos, name in enumerate(col_names):
          data[name].append(line[pos])
  
  return data

#____________________________________________________________________________
def myText(x, y, text, tsize=0.05, color=kBlack, angle=0, do_NDC=False) :
  
  l = TLatex()
  l.SetTextSize(tsize)
  l.SetTextFont(132)
  if do_NDC:
    # set relative to canvas coordinates rather than histogram coordinates
    l.SetNDC()
  l.SetTextColor(color)
  l.SetTextAngle(angle)
  l.DrawLatex(x,y, text)

#____________________________________________________________________________
def draw_line(xmin, ymin, xmax, ymax, color=kGray+1, style=2, width=2):

  line = TLine(xmin , ymin , xmax, ymax)
  line.SetLineStyle(style)
  line.SetLineColor(color) # 12 = gray
  line.SetLineWidth(width) # 12 = gray
  return line

#_________________________________________________________________________
def mkdir(dirPath):
  '''
  make directory for given input path
  '''
  try:
    os.makedirs(dirPath)
    print 'Successfully made new directory ' + dirPath
  except OSError:
    pass
 
if __name__ == "__main__":
  main()
