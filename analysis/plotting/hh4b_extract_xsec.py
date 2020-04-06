#!/usr/bin/env python

'''
Welcome to hh4b_extract_xsec.py
This makes the 2D MadGraph cross-section plot Fig 2 of paper

Placed under "XSEC-EXTRACTION-FROM-MADGRAPH-LOGS"
is commented out code that can be run once to extract the 
MadGraph LO xsec from the log files.

By default this just makes the 2D plot of the cross-sections
extracted in the accompanying xsec_14TeV_hh.txt file

Run by:

source /cvmfs/sft.cern.ch/lcg/views/LCG_94/x86_64-slc6-gcc8-opt/setup.sh
./hh4b_extract_xsec.py
'''

from ROOT import *
import os, sys, csv
from datetime import datetime

#PHENOPATH = os.environ.get('PHENOSIM')
PHENOPATH = '/home/jesseliu/pheno/fcc/PhenoSim'

DATE    = '#bf{#it{Pheno4b}} 16 Oct 2018'
PROCESS = 'MadGraph5 2.6.2 #sqrt{s} = 14 TeV, p p #rightarrow h h'

mk_dict = False # produce a python-like dictionary
mk_csv  = True  # produce a CSV file 

plot_logz = True
overlay_txt = False # overlay z-axis numbers

#____________________________________________________________________________
def main():

  #-------------------------------------------------------------
  # Path to samples where we calculated cross-sections
  #-------------------------------------------------------------
  SAMP_PATH = PHENOPATH + '/data/samples/14TeV/2018oct15'

  #-------------------------------------------------------------
  # Masses of parent which we calculated cross-sections for
  #-------------------------------------------------------------
  l_TOPYUK  = [0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5]
  #l_SLFCOUP = [-20., -10., -7., -5., -3., -2., -1., -0.5, 0.0, 0.5, 1.0, 2., 3., 5., 7., 10., 20.]
  l_SLFCOUP = [-20., -15., -10., -9., -8., -7., -6., -5., -4, -3, -2., -1.5, -1., -0.5, 0., 0.5, 0.8, 1., 1.2, 1.5, 2., 3., 4., 5., 6., 7., 8., 9., 10., 15, 20.]
  
  #-------------------------------------------------------------
  # Processes where we calculate cross-sections for
  #-------------------------------------------------------------
  l_PROC = ['pp2hh_HeavyHiggsTHDM']

  #-------------------------------------------------------------
  # Output file where we store the cross-sections
  #-------------------------------------------------------------
  if mk_dict:
    out_file = 'xsec_14TeV_hh_dict.txt'
  elif mk_csv:
    out_file = 'xsec_14TeV_hh.txt'
  '''
  # XSEC-EXTRACTION-FROM-MADGRAPH-LOGS
  # Code to extract the MadGraph LO cross-section from log files

  with open(out_file, 'w') as f_out:
    #-------------------------------------------------------------
    # Write the header for the CSV file
    #-------------------------------------------------------------
    if mk_dict:
      f_out.write('name : cross_section_pb\n')
    elif mk_csv:
      f_out.write('process,TopYuk,SlfCoup,cross_section_pb\n')
    
    #-------------------------------------------------------------
    # Find the process being generated 
    #-------------------------------------------------------------
    for proc in l_PROC: 
      for TOPYUK in l_TOPYUK:
        for SLFCOUP in l_SLFCOUP:
          if SLFCOUP < 0:
            SlfCoup = 'm{0:.1f}'.format( abs(SLFCOUP) )
          else:  
            SlfCoup = '{0:.1f}'.format( SLFCOUP )
           
          #-------------------------------------------------------------
          # Path to MadGraph banner file with cross-section
          #-------------------------------------------------------------
          xsec_file = SAMP_PATH + '/' + proc + '/01/TopYuk_{0:.1f}'.format(TOPYUK) + '/SlfCoup_' + SlfCoup + '/Events/pp_0/pp_0_tag_1_banner.txt'
          print('Processing {0}'.format( xsec_file ) )
          try:
            with open(xsec_file) as f_in:
              for line in f_in:
                #--------------------------
                # Extract cross-section
                #--------------------------
                if 'Integrated weight (pb)' in line and 'Matched' not in line:
                  xsec = float( line.strip().split(' : ')[1] )
                  print(xsec)
                  if mk_dict:
                    f_out.write( " 'intermediate_TopYuk_{0:.1f}_SlfCoup_{1:.1f}_pp2hh_HeavyHiggsTHDM' : {2},\n".format(TOPYUK, SLFCOUP, xsec) )
                  elif mk_csv:
                    f_out.write( '{0},{1:.1f},{2:.1f},{3}\n'.format(proc, TOPYUK, SLFCOUP, xsec) )
          except IOError:
           pass
  '''
  
  # ------------------------------------------------------
  #
  # Now commence interpolation and contour extraction
  #
  # ------------------------------------------------------
 
  xCol, yCol, zCol = 'SlfCoup', 'TopYuk', 'cross_section_pb'
   
  d_axis_tlatex = {
    'cross_section_pb' : 'Leading order cross-section [pb]',
  }
 
  contour_out_file = out_file.replace('.txt', '_contour.pdf')

  print( '--------------------------------------------------------------' )
  print( '\nMaking a contour plot from extracted cross-sections...\n' )
  print( 'Input: {0}'.format(out_file) )  
  print( 'Using the column headers: ' )
  print( '  xCol: {0}'.format(xCol) )
  print( '  yCol: {0}'.format(yCol) )
  print( '  zCol: {0}'.format(zCol) )
  print( 'Saving contour coordinates to file:\n  {0}\n'.format(contour_out_file) )
  print( '-----------------------------------------------------------------\n' )


  # ------------------------------------------------------
  # First Convert the csv into lists 
  # where column header is key of dictionary, values as list
  # ------------------------------------------------------
  d_csv = csv_to_lists( out_file )
   
  # ------------------------------------------------------
  # First convert the csv file into a TGraph 2D
  # ------------------------------------------------------
  tg2d = csv_to_graph( d_csv, xCol, yCol, zCol )

  # ------------------------------------------------------
  # Make diagnostic contour plot with numbers overlayed
  # ------------------------------------------------------
  print( 'Making diagnostic contour plot with numbers overlayed' )
  draw_contour_with_points(d_csv, contour_out_file, xCol, yCol, zCol, d_axis_tlatex, tg2d)

#____________________________________________________________________________
def draw_contour_with_points(d_csv, out_file, xCol, yCol, zCol, d_axis_tlatex, tg2d):
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
  tg2d.SetTitle('')
  hist = tg2d.GetHistogram()
  hist.Draw('COLZ')
  #hist.Draw('CONTZ')
  hist.GetXaxis().SetRangeUser(-60,6000)
  hist.GetYaxis().SetRangeUser(-20,1000)
  
  #xtitle = '#kappa(#lambda_{hhh}) = #lambda_{hhh} / #lambda_{hhh}^{SM}'
  #ytitle = '#kappa(#it{y}_{top}) = #it{y}_{top} / #it{y}_{top}^{SM} '
  xtitle = '#kappa_{#lambda}'
  ytitle = '#kappa_{#it{t}}'
  ztitle = '#sigma_{LO} [pb] '
  #ztitle = d_axis_tlatex[zCol]
 
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
    tg.SetPoint(     count, float(x_val), float(y_val) )
      
  #-------------------------------------------------
  # Format the excluded points differently from the not excluded ones
  #-------------------------------------------------
  tg.SetMarkerStyle(20)
  tg.SetMarkerSize(0.7)
  tg.SetMarkerColor(kOrange+2)
  #tg.SetMarkerColor(kGray+1)
  tg.Draw('P same') 

  #-------------------------------------------------
  # Draw values as text for points
  #-------------------------------------------------
  if overlay_txt:
    for x_val, y_val, z_val in zip( d_csv[xCol], d_csv[yCol], d_csv[zCol] ) :
      myText( float(x_val), float(y_val), '{0:.2f}'.format( float(z_val) ), 0.01, kBlack, 0, False)
  
  #-------------------------------------------------
  # Construct and add plots to legend
  #-------------------------------------------------
  xl1=0.65
  yl1=0.965
  xl2=xl1+0.15
  yl2=yl1-0.06
  leg = TLegend(xl1,yl1,xl2,yl2)
  leg.SetBorderSize(0)
  leg.SetTextFont(132)
  leg.SetTextSize(0.04)
  leg.SetNColumns(1)

  leg.AddEntry(tg, 'Points sampled', 'p')
  leg.Draw('same')
  
  # Annotating text to add to top
  #myText(0.20, 0.94, DATE,     0.040, kBlack, 0, True)
  myText(0.17, 0.92, PROCESS,  0.040, kBlack, 0, True)
  
  #-------------------------------------------------
  # Palette (Z axis colourful legend)
  #-------------------------------------------------
  paletteAxis = hist.GetListOfFunctions().FindObject("palette")
  paletteAxis.SetX1NDC(0.79)
  paletteAxis.SetX2NDC(0.84)
  paletteAxis.SetY1NDC(0.19)
  paletteAxis.SetY2NDC(0.88) 
 
  if plot_logz:
    can1.SetLogz()
  
  # Redraw axes
  gPad.Update()
  gPad.RedrawAxis()

  can1.SaveAs( out_file )
  can1.Close() 
 
#____________________________________________________________________________
def csv_to_graph( d_csv, xCol, yCol, zCol, interpolate_logy=False ):

  tg = TGraph2D()

  count = 0

  # Loop over points in CSV and plot them 
  for count, ( x_val, y_val, z_val ) in enumerate( zip( d_csv[xCol], d_csv[yCol], d_csv[zCol] ) ) :
    #print x_val, y_val, z_val
    if interpolate_logy:
      y_val = math.log10( float( y_val ) )
    tg.SetPoint(count, float(x_val), float(y_val), float(z_val) )

  # Granulairty of the contour interpolation
  tg.SetNpx(250)
  tg.SetNpy(100) # for now, use this so slepton contour extends to (183, 180) points say

  # Possibility to draw the contour map
  #can1  = TCanvas('c1','c1',1300,1000)
  #tg.SetTitle('')
  #tg.Draw('COLZ')
  #gStyle.SetPalette(kViridis)
  #can1.SaveAs('hh4b_xsec_contour_plot.pdf')
  #can1.Close() 

  return tg

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
 
  #zax.SetRangeUser(zmin, zmax)
  zax.SetRangeUser(0.0005, 10)
  
  zax.SetTitle(ztitle)
  zax.SetTitleSize(text_size*1.2)
  zax.SetTitleOffset(1.25)    
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

#_________________________________________________________________________
def mk_dir(dirPath):
  '''
  make directory structure to prepare for where MadEvent goes
  '''
  try:
    os.makedirs(dirPath)
    print 'Successfully made new directories ' + dirPath
  except OSError:
    pass

if __name__ == "__main__":
  main()
