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
ROOT.gROOT.SetBatch(1)

from ROOT import *
import os, sys, time, argparse, math, datetime, csv
from array import array

#DATE       = '#bf{#it{Pheno 4b}}'
SQRTS_LUMI = '#sqrt{s} = 14 TeV, 3000 fb^{#minus1}'
  
interpolate_logy = False
overlay_points = False

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
  # Input/output file names 
  # ------------------------------------------------------
  
  # resolved + intermediate + boosted
  l_zCol = ['acceptance',
            'N_sig',
            'N_sig_raw',
            'SoverB',
            'SoverSqrtB',
            'SoverSqrtBSyst1pc',
            'SoverSqrtBSyst5pc',
            'chiSq',
            'chiSqSyst1pc',
            'chiSqSyst5pc'
            ]
  
  #l_zCol = ['sum_chiSqSyst0p3pc']
  
  l_cut_sels = [
                'SR_res_multibin_combined', 
                'SR_int_multibin_combined', 
                'SR_bst_multibin_combined', 
                'SR_all_multibin_combined',

                'SRNN_res_multibin_lam1_combined', 
                'SRNN_int_multibin_lam1_combined', 
                'SRNN_bst_multibin_lam1_combined', 
                'SRNN_all_multibin_lam1_combined',

                'SRNN_res_multibin_lam5_combined', 
                'SRNN_int_multibin_lam5_combined', 
                'SRNN_bst_multibin_lam5_combined', 
                'SRNN_all_multibin_lam5_combined',

                'SRNN_res_multibin_lam7_combined', 
                'SRNN_int_multibin_lam7_combined', 
                'SRNN_bst_multibin_lam7_combined', 
                'SRNN_all_multibin_lam7_combined',
                ]

  l_zCol = ['sum_chiSqSystMix']
  #l_zCol = ['sum_chiSqSyst0p3pc']
  #l_zCol = ['sum_chiSqSyst1pc']
  #l_zCol = ['sum_chiSqSyst1p5pc']
  #l_zCol = ['sum_chiSqSyst2pc']
  #l_zCol = ['sum_chiSqSyst5pc']

  # ------------------------------------------------------
  # Threshold we want to plot excluded vs viable points
  # ------------------------------------------------------
  #zThreshold = 1e-9
  zThreshold = 1.
             
  # ------------------------------------------------------
  # Set column headers of in_file CSV we want to plot
  # ------------------------------------------------------

  d_axis_tlatex = {
    'acceptance'        : {'zMin':1e-5,  'zMax':1e-1, 'palette':'kBird', 'tlatex':'Acceptance #times efficiency (S / #sigma #times L)'},
    'N_sig'             : {'zMin':0.1,   'zMax':1e3, 'palette':'kBird', 'tlatex':'Signal yield'},
    'N_sig_raw'         : {'zMin':100,   'zMax':1e5, 'palette':'kBird', 'tlatex':'Raw signal yield'},
    'SoverB'            : {'zMin':1e-5,   'zMax':1,  'palette':'kBird', 'tlatex':'S / B'},
    'SoverSqrtB'        : {'zMin':0.1,   'zMax':10,  'palette':'kBird', 'tlatex':'S / #sqrt{B}'},
    'SoverSqrtBSyst1pc' : {'zMin':0.1,   'zMax':10,  'palette':'kBird', 'tlatex':'S / #sqrt{B + (1%B)^{2}}'},
    'SoverSqrtBSyst5pc' : {'zMin':0.1,   'zMax':10,  'palette':'kBird', 'tlatex':'S / #sqrt{B + (5%B)^{2}}'},
    'chiSq'             : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2}'},# = (S #minus S_{SM})^{2} / B'},
    'chiSqSyst1pc'      : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2}'},#_{syst} = (S #minus S_{SM})^{2} / (B + (1%B)^{2})'},
    'chiSqSyst5pc'      : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2}'},#_{syst} = (S #minus S_{SM})^{2} / (B + (5%B)^{2})'},
    'sum_chiSqSyst0p3pc' : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2} (0.3% syst)'},
    'sum_chiSqSyst1pc'   : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2} (1% syst)'},
    'sum_chiSqSyst1p5pc' : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2} (1.5% syst)'},
    'sum_chiSqSyst2pc'   : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2} (2% syst)'},
    'sum_chiSqSyst5pc'   : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2} (5% syst)'},
    'sum_chiSqSystMix'   : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2}'},
    'sum_chiSq'          : {'zMin':0.001, 'zMax':1e3, 'palette':'kTemperatureMap', 'tlatex':'#chi^{2} (0% syst)'},
  }

  xCol, yCol = 'SlfCoup', 'TopYuk'

  for cut_sel in l_cut_sels:
    for zCol in l_zCol: 

      if 'combine' in cut_sel: 
        in_file = 'data/CHISQ_loose_preselection_{0}_{1}.csv'.format(cut_sel, zCol).replace('sum_', '')
      else:
        in_file = 'data/CHISQ_loose_preselection_{0}.csv'.format(cut_sel)
      out_file = 'contours/limit2d_{0}_SlfCoup_TopYuk_{1}.csv'.format(cut_sel, zCol)
      
      # ------------------------------------------------------
      # Now commence interpolation and contour extraction
      # ------------------------------------------------------
      
      print( '--------------------------------------------------------------' )
      print( '\nWelcome to chiSq_to_contour.py\n' )
      print( 'Input: {0}'.format(in_file) )  
      print( 'Using the column headers: ' )
      print( '  xCol: {0}'.format(xCol) )
      print( '  yCol: {0}'.format(yCol) )
      print( '  zCol: {0}'.format(zCol) )
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
      zMin = d_axis_tlatex[zCol]['zMin']
      tg2d = csv_to_graph( d_csv, xCol, yCol, zCol, zMin )
      
      # ------------------------------------------------------
      # Extract the contour and put it into a TGraph (1D)
      # ------------------------------------------------------
      tgraph_cont   = contour_from_graph( tg2d , zThreshold )
      n_pts = tgraph_cont.GetN()
      
      # ------------------------------------------------------
      # Store the x, y coordinates of the contour to file
      # ------------------------------------------------------
      with open(out_file, 'w') as f_out:
        f_out.write( 'x,y\n' )
        for i in range(0, n_pts):
          x = Double()
          y = Double()
          tgraph_cont.GetPoint(i, x, y) 
          out_x = x
          out_y = y
          f_out.write( '{0:.4f},{1:.4f}\n'.format(out_x, out_y) )
          #print('x: {0}, y: {1}'.format(out_x, out_y))
     
      # ------------------------------------------------------

      # ------------------------------------------------------
      # Make diagnostic contour plot with numbers overlayed
      # ------------------------------------------------------
      print( 'Making contour plot with numbers overlayed' )
      contour_ofile = out_file.replace('.csv', '.pdf')
      draw_contour_with_points(d_csv, contour_ofile, xCol, yCol, zCol, zThreshold, cut_sel, tgraph_cont, tg2d, d_axis_tlatex)

#____________________________________________________________________________
def draw_contour_with_points(d_csv, out_file, xCol, yCol, zCol, zThreshold, cut_sel, tgraph_cont, tg2d, d_axis_tlatex):
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
  #hist.Draw('CONTZ')
  hist.Draw('COLZ')
  #hist.GetXaxis().SetRangeUser(-30,6000)
  #hist.GetYaxis().SetRangeUser(-30,1000)
  hist.GetXaxis().SetRangeUser(-20,20)
  #hist.GetXaxis().SetRangeUser(-5,8)
  hist.GetYaxis().SetRangeUser(0.5,1.5)
  #hist.Draw('COLZ')
  #hist.Draw('CONT4Z LIST')
  tgraph_cont.Draw('same')
  tgraph_cont.SetLineColor(kGray+3)
  
  process = 'hh #rightarrow 4b'
  xtitle = '#kappa_{#lambda}'
  ytitle = '#kappa_{#it{t}}'
  ztitle = d_axis_tlatex[zCol]['tlatex']
  zMin = d_axis_tlatex[zCol]['zMin']
  zMax = d_axis_tlatex[zCol]['zMax']
  palette = d_axis_tlatex[zCol]['palette']  
  # Format some text 
  if palette == 'kBird'           : gStyle.SetPalette(kBird)
  if palette == 'kTemperatureMap' : set_palette() #gStyle.SetPalette(kTemperatureMap)
  if palette == 'kViridis'        : gStyle.SetPalette(kViridis)
  customise_gPad()
  customise_axes(hist, xtitle, ytitle, ztitle, zMin, zMax)

  #-------------------------------------------------
  # Plot points on top
  #-------------------------------------------------
  if overlay_points:
    tg = TGraph()
    tg_excl = TGraph()
    for count, ( x_val, y_val, z_val ) in enumerate( zip( d_csv[xCol], d_csv[yCol], d_csv[zCol] ) ) :
      # Make a separate TGraph for points above desired threshold
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
      myText( float(x_val), float(y_val), '{0:.3g}'.format( float(z_val) ), 0.01, kBlack, 0, False)
  
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
  #cut_name = cut_sel.split('-')
  #cut_txt = cut_name[0].capitalize() + ' ' + cut_name[1]
 
  if zCol == 'chiSq':
    syst_txt = ', #zeta_{b} = 0'
  if 'chiSqSyst1pc' in zCol:
    syst_txt = ', #zeta_{b} = 0.01'
  if 'chiSqSyst0p3pc' in zCol:
    syst_txt = ', 0.3% syst'
  else:
    syst_txt = ''

  if 'all' in out_file:
    analysis = 'Combined'
  if 'res' in out_file:
    analysis = 'Resolved'
  if 'int' in out_file:
    analysis = 'Intermediate'
  if 'bst' in out_file:
    analysis = 'Boosted'

  if 'SRNN' in out_file:
    analysis += ' DNN'
    # Add some text to bookkeep which DNN training we're using
    if 'lam1' in cut_sel: 
      klambda = 'DNN trained on #kappa_{#lambda} = 1'
    if 'lam5' in cut_sel: 
      klambda = 'DNN trained on #kappa_{#lambda} = 5'
    if 'lam7' in cut_sel: 
      klambda = 'DNN trained on #kappa_{#lambda} = 7'
    myText(0.07, 0.06, klambda, 0.03, kGray+2, 0, True)
  else:
    analysis += ' Baseline'

  
  myText(0.18, 0.91, SQRTS_LUMI + ', {0}{1}, {2}'.format(process, syst_txt, analysis), 0.040, kBlack, 0, True)
  
  #-------------------------------------------------
  # Palette (Z axis colourful legend)
  #-------------------------------------------------
  paletteAxis = hist.GetListOfFunctions().FindObject("palette")
  paletteAxis.SetX1NDC(0.79)
  paletteAxis.SetX2NDC(0.84)
  paletteAxis.SetY1NDC(0.19)
  paletteAxis.SetY2NDC(0.88) 
 
  can1.SetLogz()

  can1.SaveAs( out_file )
  can1.Close() 

#____________________________________________________________________________
def csv_to_graph( d_csv, xCol, yCol, zCol, zMin=0.001, interpolate_logy=False ):
  '''
  Plot the mSUSY vs deltaM vs Zsignificance from the input CSV f_in
  Specify the the column in the CSV file to plot in the TGraph by 
  x_pos, y_pos, z_pos
  From the format we made parse_json.py,
  0, 2, 8 maps to mSUSY, dM_SUSY_LSP, ZCLsexp
  '''
  tg = TGraph2D()

  count = 0 

  # -----------------------------------------------------------------------------
  # Add dummy points to close contour in kappa(ytop) vs kappa(lambda_hhh) plane
  # -----------------------------------------------------------------------------
  # kappa(lambda_hhh)
  l_dummy_x = [-25., 0., 25., -25., 0., 25.]
  # kappa(ytop)
  l_dummy_y = [0., 0., 0., 2., 2., 2.]
  # chiSq
  l_dummy_z = [200., 20., 200., 200., 20., 200.]

  d_csv[xCol] += l_dummy_x 
  d_csv[yCol] += l_dummy_y 
  d_csv[zCol] += l_dummy_z 

  # -------------------------------------------
  # Loop over points in CSV and plot them 
  # -------------------------------------------
  for count, ( x_val, y_val, z_val ) in enumerate( zip( d_csv[xCol], d_csv[yCol], d_csv[zCol] ) ) :
    if interpolate_logy:
      y_val = math.log10( float( y_val ) )
    if float(z_val) < zMin: z_val = zMin
    tg.SetPoint(count, float(x_val), float(y_val), float(z_val) )  

  # Maximise granulairty of the contour interpolation
  tg.SetNpx(150)
  tg.SetNpy(150) # for now, use this so slepton contour extends to (183, 180) points say
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
  h.GetXaxis().SetRangeUser(-30,30)
  h.GetYaxis().SetRangeUser(0,2)
  h.SetContour( 1 )
  
  gr = gr0.Clone(h.GetName())
  
  # Get the contour whose value corresponds to level_val
  h.SetContourLevel( 0, level_val )
  
  h.Draw("CONT LIST")
  h.SetDirectory(0)
  ROOT.gPad.Update()
  contours = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
  list = contours[0]
  gr = list[0]
  for k in xrange(list.GetSize()):
    if gr.GetN() < list[k].GetN(): gr = list[k]
  gr.SetName(hist.GetName())
  return gr;
 

#____________________________________________________________________________
def customise_gPad(top=0.12, bot=0.19, left=0.17, right=0.22):
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
 
 
  #scaleFactor = 5.6 
  ##################################
  # Z axis
  zax = hist.GetZaxis()
  # Times 132
  zax.SetLabelFont(132)
  zax.SetTitleFont(132)
  zax.CenterTitle()
 
  zax.SetRangeUser(zmin, zmax)
  #zax.SetRangeUser(0.001, 3.5)
  #zax.SetRangeUser(0.001, 1000)
  
  zax.SetTitle(ztitle)
  zax.SetTitleSize(text_size*1.2)
  zax.SetTitleOffset(1.2)    
  #zax.SetNdivisions(-505) 
  
  zax.SetLabelOffset(0.01)
  zax.SetLabelSize(text_size)

  gPad.SetTicky()

  gPad.Update()


#____________________________________________________________________________
def set_palette(name='temperature', ncontours=999):
  '''
  A custom palette for temperature based on
  http://colorbrewer2.org/#type=diverging&scheme=RdYlBu&n=11
  '''
  stops = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
  red   = [0.65, 0.84, 0.96, 0.99, 1.00, 1.00, 0.88, 0.67, 0.45, 0.27, 0.19]
  green = [0.00, 0.19, 0.43, 0.68, 0.90, 1.00, 0.95, 0.85, 0.68, 0.46, 0.21]
  blue  = [0.15, 0.15, 0.26, 0.38, 0.76, 1.00, 0.97, 0.91, 0.82, 0.71, 0.58]

  s = array('d', stops )
  r = array('d', reversed(red) )
  g = array('d', reversed(green) )
  b = array('d', reversed(blue) )

  npoints = len(s)
  TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
  gStyle.SetNumberContours(ncontours)

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
