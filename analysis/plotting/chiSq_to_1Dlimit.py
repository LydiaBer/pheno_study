#!/usr/bin/env python
import matplotlib as mplt
mplt.use('Agg') # So we can use without X forwarding
import os, math, csv

from matplotlib import pyplot as plt
import matplotlib.lines   as mlines
import matplotlib.patches as mpatches
import matplotlib.ticker  as ticker

# So we can produce PDFs
from matplotlib.backends.backend_pdf import PdfPages

from pprint import pprint
from ROOT import *

# Blues
myLighterBlue   = TColor.GetColor('#deebf7')
myLightBlue     = TColor.GetColor('#9ecae1')
myMediumBlue    = TColor.GetColor('#2171b5')
myDarkBlue      = TColor.GetColor('#08519c')
myDarkerBlue    = TColor.GetColor('#08306b')

# Greens
myLightGreen    = TColor.GetColor('#c7e9c0')
myMediumGreen   = TColor.GetColor('#41ab5d')
myDarkGreen     = TColor.GetColor('#006d2c')

# Oranges
myLighterOrange = TColor.GetColor('#ffeda0')
myLightOrange   = TColor.GetColor('#fec49f')
myMediumOrange  = TColor.GetColor('#fe9929')
myDarkOrange    = TColor.GetColor('#ec7014')
myDarkerOrange  = TColor.GetColor('#cc4c02')

# Greys
myLightestGrey  = TColor.GetColor('#f0f0f0')
myLighterGrey   = TColor.GetColor('#e3e3e3')
myLightGrey     = TColor.GetColor('#969696')

# Pinks
myLightPink     = TColor.GetColor('#fde0dd')
myMediumPink    = TColor.GetColor('#fcc5c0')
myDarkPink      = TColor.GetColor('#dd3497')

# Purples
myLightPurple   = TColor.GetColor('#dadaeb')
myMediumPurple  = TColor.GetColor('#9e9ac8')
myDarkPurple    = TColor.GetColor('#6a51a3')

#____________________________________________________________________________
def main():

  mkdir('contours')
  
  # Cut selections
  l_cut_sels = ['resolved-finalSR', 'intermediate-finalSR', 'boosted-finalSR' ] 
  #
  l_zCols = ['chiSq', 'chiSqSyst1pc']

  d_axis_latex = {
    'SoverB'            : r'$S / B$',
    'SoverSqrtB'        : r'$S / \sqrt{B}$',
    'SoverSqrtBSyst1pc' : r'$S / \sqrt{B + (1\%B)^{2}}$',
    'SoverSqrtBSyst5pc' : r'$S / \sqrt{B + (5\%B)^{2}}$',
    'chiSq'             : r'$\chi^{2} = (S - S_\mathrm{SM})^{2} / B$',
    'chiSqSyst1pc'      : r'$\chi^{2}_\mathrm{syst} = (S - S_\mathrm{SM})^{2} / (B + (1\%B)^{2})$',
    'chiSqSyst5pc'      : r'$\chi^{2}_\mathrm{syst} = (S - S_{SM})^{2} / (B + (5\%B)^{2})$',
  }
  d_axis_tlatex = {
    'acceptance'        : 'Acceptance #times efficiency (S / #sigma #times L)',
    'N_sig'             : 'Signal yield',
    'N_sig_raw'         : 'Raw signal yield',
    'SoverB'            : 'S / B',
    'SoverSqrtB'        : 'S / #sqrt{B}',
    'SoverSqrtBSyst1pc' : 'S / #sqrt{B + (1%B)^{2}}',
    'SoverSqrtBSyst5pc' : 'S / #sqrt{B + (5%B)^{2}}',
    'chiSq'             : '#chi^{2} = (S #minus S_{SM})^{2} / B',
    'chiSqSyst1pc'      : '#chi^{2}_{syst} = (S #minus S_{SM})^{2} / (B + (1%B)^{2})',
    'chiSqSyst5pc'      : '#chi^{2}_{syst} = (S #minus S_{SM})^{2} / (B + (5%B)^{2})',
  }

  d_in_data = {}

  for cut_sel in l_cut_sels:
    # Input file made from ntuples_to_chiSq.py
    d_in_data[cut_sel]  = 'data/CHISQ_loose_preselection_{0}.csv'.format(cut_sel)
  
  for zCol in l_zCols: 
    # Yield file is the input file with the background yield from plot.py
    out_file = 'figs/limit1d_TopYuk_1p0_SlfCoup_vary_{0}'.format(zCol)
    
    print('Output file to store chi squares: {0}'.format( out_file  ) )

    make_plot( d_in_data, out_file, l_cut_sels, zCol, d_axis_tlatex )

#____________________________________________________________________________
def make_plot( d_in_data, out_file, l_cut_sels, zCol, d_axis_tlatex ):

  '''
  fig, ax = plt.subplots()
  fig.set_size_inches(11, 8)

  plt.rcParams['text.usetex'] = True
  plt.rcParams['font.family'] = 'serif'
  plt.rcParams['font.serif']  = 'times'
  '''

  l_colours = [myDarkBlue, myDarkGreen, myMediumOrange ]
  l_widths  = [5, 4, 3]
  # gPad left/right margins
  can  = TCanvas('','',1000,800)

  #==========================================================
  # Build canvas   

  gpLeft = 0.21
  gpRight = 0.05
  customise_gPad(top=0.07, bot=0.19, left=gpLeft, right=gpRight)
  
  # construct legend
  xl1, yl1 = 0.45, 0.68
  xl2, yl2 = xl1+0.25, yl1+0.20
  leg = TLegend(xl1,yl1,xl2,yl2)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0) # transparent
  leg.SetTextSize(0.055)
  leg.SetTextFont(132)

  #------------------------------------------------------
  # Get and organise data
  #------------------------------------------------------
  
  d_tgraphs = {}

  for cut_sel, width, colour in zip( l_cut_sels, l_widths, l_colours ):
    in_file = d_in_data[cut_sel]
    print "Opening: ", in_file
    d_csv = csv_to_lists(in_file)
    #pprint( d_csv )

    in_x = [float(i) for i in d_csv['SlfCoup'] ]
    in_y = [float(i) for i in d_csv['TopYuk'] ]
    in_z = [float(i) for i in d_csv[zCol] ]

    l_SlfCoup = []
    l_chiSq   = []

    for x, y, z in sorted(zip(in_x, in_y, in_z)):
      if y == 1.0: 
        l_SlfCoup.append(x)
        l_chiSq.append(z)

    tg = TGraph( len(l_chiSq) )
    tg.SetMarkerColor(colour)
    tg.SetMarkerSize(width)
    tg.SetLineColor(colour)
    tg.SetLineWidth(width)
    tg.SetTitle('')

    for i, (x, y) in enumerate( zip( l_SlfCoup, l_chiSq) ):
      tg.SetPoint(i, x, y)
    d_tgraphs[cut_sel] = tg
   
    cut_name = cut_sel.split('-')
    cut_txt = cut_name[0].capitalize()# + ' ' + cut_name[1] 
    leg.AddEntry(tg, cut_txt, 'l')
    
    #plt.plot(l_SlfCoup, l_chiSq, colour, linewidth=width, zorder=2, linestyle='-', label=cut_txt)

  d_tgraphs['resolved-finalSR'].Draw('PLA')
  d_tgraphs['intermediate-finalSR'].Draw('PL same')
  d_tgraphs['boosted-finalSR'].Draw('PL same')

  leg.Draw('same')

  myText(0.26, 0.95, '#sqrt{s} = 14 TeV, 3000 fb^{#minus1}, hh #rightarrow 4b, finalSR' , 0.05, kBlack)
  myText(0.26, 0.86, '#kappa(#it{y}_{top}) = 1.0' , 0.04, kBlack)

  xtitle = '#lambda_{hhh} / #lambda_{hhh}^{SM}'
  ytitle = d_axis_tlatex[zCol]
  customise_axes(d_tgraphs['resolved-finalSR'], xtitle, ytitle, 2.8)

  line = TLine(-20,1,20,1);
  line.SetLineColor(kGray+1)
  line.SetLineWidth(2)
  line.Draw()

  gPad.RedrawAxis() 
  
  #==========================================================
  # save everything
  can.cd()
  can.SaveAs(out_file + '.pdf')
  can.Close()
  
  '''
  plt.xlim(-20, 20)
  plt.ylim(0.0, 10)

  x_txt = r'$\lambda_{hhh} / \lambda_{hhh}^\mathrm{SM}$'
  y_txt = d_axis_latex[zCol]

  # Axis label properties
  plt.xlabel(x_txt, labelpad=15, size=35)
  plt.ylabel(y_txt, labelpad=15, size=35)

  line1 = plt.plot([-20, 20], [1, 1], myGrey, linewidth=2, linestyle='--', zorder=-1)
  fig.text(0.16, 0.95, r'$\sqrt{s} = 14~\mathrm{TeV}, 3000~\mathrm{fb}^{-1}, hh\rightarrow 4b$', color='Black', size=24)
  #fig.text(0.16, 0.95, r'$\sqrt{s} = 14 \mathrm{TeV}, 3000 \mathrm{fb}^{-1}, hh\rightarrow 4b$', color='Black', size=24)

  # Adjust axis ticks
  ax.minorticks_on()
  ax.tick_params('x', length=12, width=1, which='major', labelsize='28', pad=10)
  ax.tick_params('x', length=6,  width=1, which='minor')
  ax.tick_params('y', length=12, width=1, which='major', labelsize='28', pad=10)
  ax.tick_params('y', length=6,  width=1, which='minor')

  plt.tight_layout(pad=0.3)
  plt.subplots_adjust( top=0.93 )
  
  legend = ax.legend(loc='upper center', shadow=False, frameon=False, prop={'size':28} )
  
  save_name = out_file
  print('Saving as {0}'.format(save_name))
  plt.savefig(save_name + '.pdf', format='pdf', dpi=50)
  plt.savefig(save_name + '.png', format='png', dpi=300)
  '''

#__________________________________________
def csv_to_lists(csv_file):
  '''
  converts csv to dictionary of lists containing columns
  the dictionary keys is the header
  '''
  with open(csv_file) as input_file:
      reader = csv.reader(input_file)
      col_names = next(reader)
      data = {}
      for name in col_names:
        data[name] = []
      for line in reader:
        for pos, name in enumerate(col_names):
          data[name].append(line[pos])

  return data

#____________________________________________________________________________
def customise_axes(hist, xtitle, ytitle, scaleFactor=1.1, IsLogY=False, enlargeYaxis=False):

  # set a universal text size
  text_size = 0.06

  #text_size = 35

  TGaxis.SetMaxDigits(4) 
  ##################################
  # X axis
  xax = hist.GetXaxis()
  xax.CenterTitle() 
  # precision 3 Helvetica (specify label size in pixels)
  xax.SetLabelFont(132)
  xax.SetTitleFont(132)
 
  xax.SetTitle(xtitle)
  xax.SetTitleSize(text_size*1.2)
  # top panel
  xax.SetLabelSize(text_size)

  xax.SetLabelOffset(0.02)
  xax.SetTitleOffset(1.2)
  xax.SetTickSize(0.05)
 
  xax.SetRangeUser(-20,20) 
  #xax.SetNdivisions(-505) 
  gPad.SetTickx() 
  
  ##################################
  # Y axis
  yax = hist.GetYaxis()
  yax.CenterTitle()
  # precision 3 Helvetica (specify label size in pixels)
  yax.SetLabelFont(132)
  yax.SetTitleFont(132)
 
  
  yax.SetTitle(ytitle)
  yax.SetTitleSize(text_size*1.2)
  yax.SetTitleOffset(1.3) 
  
  yax.SetLabelOffset(0.015)
  yax.SetLabelSize(text_size)
 
  ymax = hist.GetMaximum()
  ymin = hist.GetMinimum()
 
 
  scaleFactor = 3.2
  yax.SetNdivisions(505) 
  if IsLogY:
    hist.SetMaximum(ymax)
    hist.SetMinimum(ymin)
  if not IsLogY:
    hist.SetMaximum(10)
    #hist.SetMaximum(ymax*scaleFactor) 
    hist.SetMinimum(0.0)

  gPad.SetTicky()

  gPad.Update()

#____________________________________________________________________________
def customise_gPad(top=0.06, bot=0.17, left=0.17, right=0.08):

  gPad.Update()
  gStyle.SetTitleFontSize(0.0)

  # gPad margins
  gPad.SetTopMargin(top)
  gPad.SetBottomMargin(bot)
  gPad.SetLeftMargin(left)
  gPad.SetRightMargin(right)

  gStyle.SetOptStat(0) # hide usual stats box 
  gStyle.SetTextFont(132)
  gPad.Update()

#____________________________________________________________________________
def myText(x, y, text, tsize=0.05, color=kBlack, angle=0) :

  l = TLatex()
  l.SetTextSize(tsize)
  l.SetNDC()
  l.SetTextFont(132)
  l.SetTextColor(color)
  l.SetTextAngle(angle)
  l.DrawLatex(x,y, text)

#_________________________________________________________________________
def mkdir(dirPath):

  # Makes new directory @dirPath

  try:
    os.makedirs(dirPath)
    print 'Successfully made new directory ' + dirPath
  except OSError:
    pass

if __name__ == "__main__":
  main()
