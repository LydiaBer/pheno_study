#!/usr/bin/env python
'''

Welcome to chiSq_to_contour.py

 - This script takes in the CSV file made by ntuples_to_chiSq.py
 - This performs linear interpolation using ROOT's CONTZ.
 - Outputs the (x, y) coordinates of the corresponding contour as a CSV ready to plot.

TODO: lots of work left
e.g. configure so can choose what to plot using argparse
clean up lots of relics from previous use of this script
'''

# So Root ignores command line inputs so we can use argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import *
import os, sys, time, argparse, math, datetime, csv

DATE       = '#bf{#it{Pheno 4b}}, ' + '{0}, Intermediate'.format( datetime.date.today().strftime('%B %d, %Y') )
SQRTS_LUMI = '14 TeV, SR-1ibsmall-2ibtrk'
  
interpolate_logy = False

# Transform to deltaM plane, interpolate there 
# - Tends to be better for contours in compressed region set True 
# - Tends to be better for non-compressed regions, so set False
interpolate_deltaM = False

#____________________________________________________________________________
def main():
  
  t0 = time.time()
  
  can  = TCanvas('','',1300,1000) 
  
  mkdir('contours')
  
  # ------------------------------------------------------
  #
  # User configurables 
  #
  # ------------------------------------------------------
  
  # ------------------------------------------------------
  # Input/output file names TODO: clumsy, use argparse etc
  # ------------------------------------------------------
  
  
  in_file = 'data/SR-1ibsmall-2ibtrk_3000invfb_5pcSyst.txt'
  in_file = 'data/SR-1ibsmall-2ibtrk_300invfb_5pcSyst.txt'
  out_file = 'contours/SR-1ibsmall-2ibtrk_3000invfb_5pcSyst-SoverSqrtBSyst.csv'
  out_file = 'contours/SR-1ibsmall-2ibtrk_3000invfb_5pcSyst-SoverSqrtB.csv'
  out_file = 'contours/SR-1ibsmall-2ibtrk_3000invfb_5pcSyst-acc.csv'
  out_file = 'contours/SR-1ibsmall-2ibtrk_3000invfb_5pcSyst-Nsig.csv'
  out_file = 'contours/SR-1ibsmall-2ibtrk_3000invfb_5pcSyst-N_raw_sig.csv'
  out_file = 'contours/SR-1ibsmall-2ibtrk_3000invfb_5pcSyst-chiSqSyst1pc.csv'
  out_file = 'contours/SR-1ibsmall-2ibtrk_3000invfb_5pcSyst-chiSqSyst.csv'
  out_file = 'contours/SR-1ibsmall-2ibtrk_300invfb_5pcSyst-chiSqSyst.csv'
 
  # ------------------------------------------------------
  # Set column headers of in_file CSV we want to plot
  # ------------------------------------------------------
  xCol, yCol, zCol = 'SlfCoup', 'TopYuk', 'SoverSqrtBSyst'
  xCol, yCol, zCol = 'SlfCoup', 'TopYuk', 'SoverSqrtB'
  xCol, yCol, zCol = 'SlfCoup', 'TopYuk', 'acc'
  xCol, yCol, zCol = 'SlfCoup', 'TopYuk', 'N_sig'
  xCol, yCol, zCol = 'SlfCoup', 'TopYuk', 'N_sig_raw'
  xCol, yCol, zCol = 'SlfCoup', 'TopYuk', 'chiSqSyst1pc'
  xCol, yCol, zCol = 'SlfCoup', 'TopYuk', 'chiSqSyst'
   
  d_axis_tlatex = {
    'acc'            : 'Acceptance #times efficiency (S / N_{gen})',
    'N_sig'          : 'Signal yield (3000 fb^{#minus1})',
    'N_sig_raw'      : 'Raw signal yield',
    'SoverSqrtB'     : 'S / #sqrt{B}',
    'SoverSqrtBSyst' : 'S / #sqrt{B + (5%B)^{2}}',
    'chiSqSyst'      : '#chi^{2}_{syst} = (S #minus S_{SM})^{2} / (B + (5%B)^{2})',
    'chiSqSyst1pc'   : '#chi^{2}_{syst} = (S #minus S_{SM})^{2} / (B + (1%B)^{2})',
    #'SoverSqrtBSyst' : 'Z = S / #sqrt{B + (0.2 B)^{2}}',
    'Omega' : '#Omega(#tilde{#chi}^{0}_{1})h^{2}'
  }
 
  # ------------------------------------------------------
  # Threshold we want to plot excluded vs viable points
  # ------------------------------------------------------
  zThreshold = 0.00008
  zThreshold = 4
  zThreshold = 2
  zThreshold = 8e-9
  #zThreshold = 0.12 # Relic density
 
  # ------------------------------------------------------
  #
  # Now commence interpolation and contour extraction
  #
  # ------------------------------------------------------
  
  print( '--------------------------------------------------------------' )
  print( '\nWelcome to significance_to_contour.py\n' )
  print( 'Input: {0}'.format(in_file) )  
  print( 'Using the column headers: ' )
  print( '  xCol: {0}'.format(xCol) )
  print( '  yCol: {0}'.format(yCol) )
  print( '  zCol: {0}'.format(zCol) )
  print( 'Interpolating in deltaM vs M(mediator) plane: {0}'.format(interpolate_deltaM) )
  print( 'Extract contour with z-axis level zThreshold: {0}'.format(zThreshold) )
  print( 'Saving contour coordinates to file:\n  {0}\n'.format(out_file) )
  print( '-----------------------------------------------------------------\n' )
  
  # ------------------------------------------------------
  # First Convert the csv into lists 
  # where column header is key of dictionary, values as list
  # ------------------------------------------------------
  d_csv = csv_to_lists( in_file )
   
  # ------------------------------------------------------
  # First convert the csv file into a TGraph 2D
  # ------------------------------------------------------
  tg2d = csv_to_graph( d_csv, xCol, yCol, zCol )
  
  # ------------------------------------------------------
  # Extract the contour and put it into a TGraph (1D)
  # ------------------------------------------------------
  tgraph_cont = contour_from_graph( tg2d , zThreshold )
  #save_cont_to_root(tgraph_cont, out_file)  
  
  tg_interpLogY = TGraph()
  tg_N1_vs_SUSY = TGraph()

  n_pts = tgraph_cont.GetN()
  
  # ------------------------------------------------------
  # Store the x, y coordinates of the contour to file
  # ------------------------------------------------------
  with open(out_file, 'w') as f_out:
    f_out.write( 'mSUSY,mN1\n' )

    for i in range(0, n_pts):
      x = Double()
      y = Double()
      tgraph_cont.GetPoint(i, x, y) 
      out_x = x
      if interpolate_logy:
        out_y = 10 ** y
      elif interpolate_deltaM:
        out_y = x - y
      else:
        out_y = y
      # For y-interpolated contours, save the contour transformed back to linear scale
      tg_interpLogY.SetPoint(i, out_x, out_y)
      f_out.write( '{0:.4f},{1:.4f}\n'.format(out_x, out_y) )
  
      # Transform to N1 vs C1 plane for presenting in summary plots
      # This only works for the wino-bino (mC1 = mN2, and mSlep)
      mN1 = out_x - out_y
      #print('x: {0}, y: {1}, mN1: {2}'.format(out_x, out_y, mN1))
      tg_N1_vs_SUSY.SetPoint(i, out_x, mN1)
  # ------------------------------------------------------

  can.cd()
  tgraph_cont.Draw('same')
  tgraph_cont.SetLineColor(kBlack)
  tgraph_cont.SetLineWidth(2)
  save_name = out_file.replace('.csv', '.pdf') 
  #can.SaveAs(save_name + '.C')
  can.SaveAs(save_name)
  print( 'Saving 95% CL contour as pdf to {0}'.format(save_name) )
  can.Close() 
  
  # ------------------------------------------------------
  # Make diagnostic contour plot with numbers overlayed
  # ------------------------------------------------------
  print( 'Making diagnostic contour plot with numbers overlayed' )
  contour_ofile = out_file.replace('.csv', '_contz.pdf')
  draw_contour_with_points(d_csv, contour_ofile, xCol, yCol, zCol, zThreshold, tgraph_cont, tg2d, d_axis_tlatex)

#____________________________________________________________________________
def save_cont_to_root(tgraph_cont, outfile, mN1_vs_mSUSY=False):
  '''
  Store TGraph in root file for hepdata etc
  '''
  # Add titles and save to hepdata ready root file  
  if mN1_vs_mSUSY:
    tgname = 'N1yax_' + outfile.split('.')[0] 
  else:
    tgname = outfile.split('.')[0]
  tgraph_cont.SetName(tgname)
  tgraph_cont.SetTitle(tgname)
  
  # hepdata entries support mathjax
  if mN1_vs_mSUSY:
    if 'Slep' in outfile:
      xtitle = r'$m(\tilde{\ell})$ IN GEV'
    else:  
      xtitle = r'$m(\tilde{\chi}^0_2)$ IN GEV'
    ytitle = r'$m(\tilde{\chi}^0_1)$ IN GEV'
  else:
    if 'Slep' in outfile:
      xtitle = r'$m(\tilde{\ell})$ IN GEV'
      ytitle = r'$\Delta m(\tilde{\ell}, \tilde{\chi}^0_1)$ IN GEV'
    else:
      xtitle = r'$m(\tilde{\chi}^0_2)$ IN GEV'
      ytitle = r'$\Delta m(\tilde{\chi}^0_2, \tilde{\chi}^0_1)$ IN GeV'
  tgraph_cont.GetXaxis().SetTitle(xtitle)
  tgraph_cont.GetYaxis().SetTitle(ytitle)

  oRootFile = TFile(tgname + '.root','RECREATE')
  print('Storing contour as TGraph to ' + outfile + '.root' )
  tgraph_cont.Write()
  oRootFile.Close()

#____________________________________________________________________________
def transform_to_c1_axes(mN2, dM_N2_N1):
  '''
  Given an input mN2, dM_N2_N1 values, transform contour to 
  mC1 and dM_C1_N1 coordinates
  assuming the Higgsino m(C1) = (mN1 + mN2)/2
  '''

  mC1      = mN2 - dM_N2_N1 / 2.
  dM_C1_N1 = dM_N2_N1 / 2.

  return mC1, dM_C1_N1

#____________________________________________________________________________
def draw_contour_with_points(d_csv, out_file, xCol, yCol, zCol, zThreshold, tgraph_cont, tg2d, d_axis_tlatex):
  '''
  d_csv: dictionary of lists from the CSV. Key is column header, list has values of column
  xCol, yCol, zCol: column headers we want to plot
  zThreshold: is the threshold we want to separate the two TGraphs excluded vs not excluded
  tgraph_cont: is the contour extracted from interpolation
  tg2d: the contour plot
  d_axis_tlatex: dictionary mapping to axis label
  '''

  # In case one wants to draw the contour directly here
  #th2f_nom = TH2F('', '', 150, 0, 500, 40, 0, 200)
  
  #-------------------------------------------------
  # Draw the contz with the contour overlayed
  #-------------------------------------------------
  can1 = TCanvas('','',1300,1000)
  can1.cd()
  tgraph_cont.SetTitle('')
  tg2d.SetTitle('')
  hist = tg2d.GetHistogram()
  hist.Draw('CONTZ')
  hist.GetXaxis().SetRangeUser(-30,6000)
  hist.GetYaxis().SetRangeUser(-30,1000)
  #hist.Draw('COLZ')
  #hist.Draw('CONT4Z LIST')
  tgraph_cont.Draw('same')
  tgraph_cont.SetLineColor(kGray+3)

  process = ''
  if 'Slep' in out_file:
    process = 'Slepton'
  elif 'Higgsino' in out_file:
    process = 'Higgsino'
  elif 'Wino' in out_file:
    process = 'Wino-bino'
  else:
    process = 'pp #rightarrow hh'
  ztitle = d_axis_tlatex[zCol]
  
  # Customise axes
  if 'Slep' in process:
    xtitle = '#font[12]{m}(#tilde{#font[12]{l}}) [GeV]'
    ytitle = '#font[12]{m}(#tilde{#chi}^{0}_{1}) [GeV]'
    if interpolate_deltaM: 
      ytitle = '#Delta#font[12]{m}(#tilde{#font[12]{l}}, #tilde{#chi}^{0}_{1}) [GeV]'
  else:
    xtitle = '#kappa_{#lambda} = #lambda_{hhh} / #lambda_{hhh}^{SM}'
    ytitle = '#kappa_{top} = y_{top} / y_{top}^{SM}'
 
  # Format some text 
  gStyle.SetPalette(kBird)
  #gStyle.SetPalette(kViridis)
  customise_gPad()
  customise_axes(hist, xtitle, ytitle, ztitle)

  #-------------------------------------------------
  # Plot points on top
  #-------------------------------------------------
  tg = TGraph()
  tg_excl = TGraph()
  for count, ( x_val, y_val, z_val ) in enumerate( zip( d_csv[xCol], d_csv[yCol], d_csv[zCol] ) ) :
    # Make a separate TGraph for points above desired threshold
    if interpolate_deltaM:
      y_val = float(x_val) - float(y_val)
    if float(z_val) > zThreshold: 
      tg_excl.SetPoint(count, float(x_val), float(y_val) )
    else:         
      tg.SetPoint(     count, float(x_val), float(y_val) )
      
  #-------------------------------------------------
  # Format the excluded points differently from the not excluded ones
  #-------------------------------------------------
  tg.SetMarkerStyle(20)
  tg.SetMarkerSize(0.8)
  tg.SetMarkerColor(kGray+2)
  tg.Draw('P same') 
  
  tg_excl.SetMarkerStyle(21)
  tg_excl.SetMarkerSize(0.8)
  tg_excl.SetMarkerColor(kOrange+2)
  tg_excl.Draw('P same') 

  #-------------------------------------------------
  # Draw values as text for points
  #-------------------------------------------------
  for x_val, y_val, z_val in zip( d_csv[xCol], d_csv[yCol], d_csv[zCol] ) :
    if interpolate_deltaM:
      y_val = float(x_val) - float(y_val)
    myText( float(x_val), float(y_val), '{0:.2f}'.format( float(z_val) ), 0.01, kBlack, 0, False)
  
  #-------------------------------------------------
  # Construct and add plots to legend
  #-------------------------------------------------
  xl1=0.22
  yl1=0.71
  xl2=xl1+0.15
  yl2=yl1-0.15
  leg = TLegend(xl1,yl1,xl2,yl2)
  leg.SetBorderSize(0)
  leg.SetTextFont(132)
  leg.SetTextSize(0.04)
  leg.SetNColumns(1)

  leg.AddEntry(tgraph_cont, 'Z = 2',    'l')
  leg.AddEntry(tg,          'Z #leq 2', 'p')
  leg.AddEntry(tg_excl,     'Z > 2',    'p')

  #leg.Draw('same')
  
  # Annotating text to add to top
  myText(0.22, 0.79, SQRTS_LUMI + ', {0}'.format(process), 0.040, kBlack, 0, True)
  myText(0.22, 0.74, DATE, 0.040, kBlack, 0, True)
  
  #-------------------------------------------------
  # Palette (Z axis colourful legend)
  #-------------------------------------------------
  paletteAxis = hist.GetListOfFunctions().FindObject("palette")
  paletteAxis.SetX1NDC(0.80)
  paletteAxis.SetX2NDC(0.85)
  paletteAxis.SetY1NDC(0.17)
  paletteAxis.SetY2NDC(0.85) 
  
  can1.SetLogz()

  can1.SaveAs( out_file )
  can1.Close() 

#____________________________________________________________________________
def csv_to_graph( d_csv, xCol, yCol, zCol, interpolate_logy=False ):
  '''
  Plot the mSUSY vs deltaM vs Zsignificance from the input CSV f_in
  Specify the the column in the CSV file to plot in the TGraph by 
  x_pos, y_pos, z_pos
  From the format we made parse_json.py,
  0, 2, 8 maps to mSUSY, dM_SUSY_LSP, ZCLsexp
  '''
  tg = TGraph2D()

  count = 0 
 
  # Loop over points in CSV and plot them 
  for count, ( x_val, y_val, z_val ) in enumerate( zip( d_csv[xCol], d_csv[yCol], d_csv[zCol] ) ) :
    if interpolate_logy:
      y_val = math.log10( float( y_val ) )
    if interpolate_deltaM:
      y_val = float(x_val) - float(y_val)
    tg.SetPoint(count, float(x_val), float(y_val), float(z_val) )  

  # Maximise granulairty of the contour interpolation
  tg.SetNpx(500)
  tg.SetNpy(500) # for now, use this so slepton contour extends to (183, 180) points say
  # Possibility to draw the contour map
  #can1  = TCanvas('c1','c1',1300,1000)
  #tg.SetTitle('')
  #tg.Draw('COLZ')
  #gStyle.SetPalette(kViridis)
  #can1.SaveAs('save_contour_plot.pdf')
  #can1.Close() 

  return tg

#____________________________________________________________________________
def contour_from_graph( tg2d, level_val=1.64458 ):
  '''
  Takes a TH2F histogram of the m_x, m_y, Zsignificance 
  Returns a contour as a TGraph interpolated at significance = 1.64458
  (corresponding to CLs = 0.05)
  '''
  # First have to convert to histogram
  hist = tg2d.GetHistogram()
  
  gr0 = ROOT.TGraph()
  h = hist.Clone()
  #h.Print()
  h.GetYaxis().SetRangeUser(-30,30)
  h.GetXaxis().SetRangeUser(0,2)
  gr = gr0.Clone(h.GetName())
  h.SetContour( 1 )
  
  # Get the contour whose value corresponds to 1.64458 (Zsignificance for CLs=0.05)
  h.SetContourLevel( 0, level_val )
  
  h.Draw("CONT LIST")
  h.SetDirectory(0)
  ROOT.gPad.Update()
  contours = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
  #print contours
  list = contours[0]
  #list.Print()
  gr = list[0]
  #gr.Print()
  #grTmp = ROOT.TGraph()
  for k in xrange(list.GetSize()):
    if gr.GetN() < list[k].GetN(): gr = list[k]
  gr.SetName(hist.GetName())
  #print gr
  return gr;
 

#____________________________________________________________________________
def customise_gPad(top=0.15, bot=0.17, left=0.17, right=0.21):
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
def customise_axes(hist, xtitle, ytitle, ztitle, zmin=0, zmax=1):

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
  xax.SetTitleSize(text_size)
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
  yax.SetTitleSize(text_size)
  yax.SetTitleOffset(1.4)    
  #yax.SetNdivisions(-505) 
  #yax.SetRangeUser(0, 250) 
  
  yax.SetLabelOffset(0.015)
  yax.SetLabelSize(text_size)
 
 
  #scaleFactor = 5.6 
  ##################################
  # Z axis
  zax = hist.GetZaxis()
  # Times 132
  zax.SetLabelFont(132)
  zax.SetTitleFont(132)
  zax.CenterTitle()
 
  #zax.SetRangeUser(zmin, zmax)
  #zax.SetRangeUser(0.001, 3.5)
  zax.SetRangeUser(0.0001, 1000)
  
  zax.SetTitle(ztitle)
  zax.SetTitleSize(text_size)
  zax.SetTitleOffset(1.3)    
  #zax.SetNdivisions(-505) 
  
  zax.SetLabelOffset(0.01)
  zax.SetLabelSize(text_size)

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
