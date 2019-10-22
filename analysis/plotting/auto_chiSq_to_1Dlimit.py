#!/usr/bin/env python
import matplotlib as mplt
mplt.use('Agg') # So we can use without X forwarding
import os, sys, math, csv

from matplotlib import pyplot as plt
import matplotlib.lines   as mlines
import matplotlib.patches as mpatches
import matplotlib.ticker  as ticker

# So we can produce PDFs
from matplotlib.backends.backend_pdf import PdfPages

from pprint import pprint
from ROOT import *

#myPurple        = TColor.GetColor('#6c3483')
#myRedPink       = TColor.GetColor('#ff1b27')

# Greens
myLightGreen    = TColor.GetColor('#c7e9b4')
myMediumGreen   = TColor.GetColor('#249e82')
myGreen         = TColor.GetColor('#238b45')
myDarkGreen     = TColor.GetColor('#195e30')
myBrightGreen   = TColor.GetColor('#11ed35')

# Red Pinks
myRedPink3      = TColor.GetColor('#d4b9da')
myRedPink6      = TColor.GetColor('#e7298a')
myRedPink9      = TColor.GetColor('#980043')
myRed           = TColor.GetColor('#ef3b2c')
myPink          = TColor.GetColor('#ef7ae0')

# Purples Greys
myLightPurple    = TColor.GetColor('#dadaeb')
myMediumPurple   = TColor.GetColor('#9e9ac8')
myDarkPurple     = TColor.GetColor('#6a51a3')
myVeryDarkPurple = TColor.GetColor('#362a52')
myGrey          = TColor.GetColor('#a5a5ad')

# Oranges Browns and Yellow
myMediumOrange  = TColor.GetColor('#fe9929')
myDarkOrange    = TColor.GetColor('#ec7014')
myDarkerOrange  = TColor.GetColor('#cc4c02')
myBrown         = TColor.GetColor('#857063')
myYellow        = TColor.GetColor('#cfb940')

# Blues Blacks
myVeryLightBlue  = TColor.GetColor('#9ecae1')
myLightBlue      = TColor.GetColor('#4292c6')
myMediumBlue     = TColor.GetColor('#0868ac')
myDarkBlue       = TColor.GetColor('#08306b')
myBlack          = TColor.GetColor('#000105')

# cut_sel colour dictionary
d_cut_sel_colour = {'resolved-finalSR' : myRedPink3,
                    'intermediate-finalSR' : myRedPink6,
                    'boosted-finalSR' : myRedPink9,
                    'resolved-finalSR_AND_intermediate-finalSR_combined' : myRed,
                    'boosted-finalSR_AND_resolved-finalSR_AND_intermediate-finalSR_combined_combined' : myPink,

                    'resolved-finalSRNNQCD' : myVeryLightBlue,
                    'intermediate-finalSRNNQCD' : myLightBlue,
                    'boosted-finalSRNNQCD' : myMediumBlue,
                    'resolved-finalSRNNQCD_AND_intermediate-finalSRNNQCD_combined' : myDarkBlue,
                    'boosted-finalSRNNQCD_AND_resolved-finalSRNNQCD_AND_intermediate-finalSRNNQCD_combined_combined' : myBlack,

                    'resolved-finalSRNNQCDTop' : myMediumOrange,
                    'intermediate-finalSRNNQCDTop' : myDarkOrange,
                    'boosted-finalSRNNQCDTop' : myDarkerOrange,
                    'resolved-finalSRNNQCDTop_AND_intermediate-finalSRNNQCDTop_combined' : myBrown,
                    'boosted-finalSRNNQCDTop_AND_resolved-finalSRNNQCDTop_AND_intermediate-finalSRNNQCDTop_combined_combined' : myYellow,
                    
                    #'resolved-finalSRNNlow_AND_resolved-finalSRNN_combined': myLightPurple,
                    #'intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined': myMediumPurple,
                    #'boosted-finalSRNNlow_AND_boosted-finalSRNN_combined': myDarkPurple, 

                    'resolved-finalSRNN' : myDarkPurple,
                    'intermediate-finalSRNN' : myMediumPurple,
                    'boosted-finalSRNN' : myLightPurple,
                    #'resolved-finalSRNN_AND_intermediate-finalSRNN_combined' : myVeryDarkPurple,
                    'resolved-finalSRNNlam10_intermediate-finalSRNNlam10_boosted-finalSRNNlam10_combined': myMediumBlue,
                    'resolved-finalSRNN_intermediate-finalSRNN_boosted-finalSRNN_combined': myMediumBlue,
                    'resolved-finalSR_intermediate-finalSR_boosted-finalSR_combined' : myMediumBlue,
                    #boosted-finalSRNN_AND_resolved-finalSRNN_AND_intermediate-finalSRNN_combined_combined' : myGrey,

                    'resolved-finalSRNNlow_AND_resolved-finalSRNN_combined' : myBrightGreen,
                    'intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined' : myMediumGreen,
                    'boosted-finalSRNNlow_AND_boosted-finalSRNN_combined' : myDarkGreen,
                    'resolved-finalSRNNlow_AND_resolved-finalSRNN_combined_AND_intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined_combined' : myMediumBlue,
                    'boosted-finalSRNNlow_AND_boosted-finalSRNN_combined_AND_resolved-finalSRNNlow_AND_resolved-finalSRNN_combined_AND_intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined_combined_combined' : myRed,


                    'resolved-finalSRNNlam10low_AND_resolved-finalSRNNlam10_combined' : myBrightGreen,
                    'intermediate-finalSRNNlam10low_AND_intermediate-finalSRNNlam10_combined' : myMediumGreen,
                    'boosted-finalSRNNlam10low_AND_boosted-finalSRNNlam10_combined' : myDarkGreen,
                    'resolved-finalSRNNlam10low_AND_resolved-finalSRNNlam10_combined_AND_intermediate-finalSRNNlam10low_AND_intermediate-finalSRNNlam10_combined_combined' : myMediumBlue,
                    'boosted-finalSRNNlam10low_AND_boosted-finalSRNNlam10_combined_AND_resolved-finalSRNNlam10low_AND_resolved-finalSRNNlam10_combined_AND_intermediate-finalSRNNlam10low_AND_intermediate-finalSRNNlam10_combined_combined_combined' : myRed,

                    'resolved-finalSRN$lam' : myDarkerOrange,
                    'intermediate-finalSRNNlam' : myDarkOrange,
                    'boosted-finalSRNNlam' : myMediumOrange,
                    
                    'resolved-finalSRNNlamm5' : myDarkerOrange,
                    'intermediate-finalSRNNlamm5' : myDarkOrange,
                    'boosted-finalSRNNlamm5' : myMediumOrange,
                    
                    'resolved-finalSRNNlam10' : myDarkerOrange,
                    'intermediate-finalSRNNlam10' : myDarkOrange,
                    'boosted-finalSRNNlam10' : myMediumOrange,
                    
                    'resolved-finalSRNNlam10' : myDarkPurple,
                    'intermediate-finalSRNNlam10' : myMediumPurple,
                    'boosted-finalSRNNlam10' : myLightPurple,
                   }

# Labels
SQRTS_LUMI = '#sqrt{s} = 14 TeV, 3000 fb^{#minus1}'

# Switch to true to zoom in on x-axis 
zoom_in = False

#____________________________________________________________________________
def main():

  mkdir('contours')

  # TODO lumi option throughout

  # Default is limits on lambda, if you wish to produce kappa top limit set do_ktop to True
  do_ktop = False
 
  # When lots of samples, put leg outside plot so less crowded
  legend_outside_plot = False
 
  # Cut selections
  # all step by step improvements 
  ###
  #l_cut_sels = ['resolved-finalSR','resolved-finalSRNNQCD', 'resolved-finalSRNNQCDTop','resolved-finalSRNN', 'resolved-finalSRNNlow_AND_resolved-finalSRNN_combined']
  #l_cut_sels = ['intermediate-finalSR','intermediate-finalSRNNQCD', 'intermediate-finalSRNNQCDTop','intermediate-finalSRNN', 'intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined']
  #l_cut_sels = ['boosted-finalSR','boosted-finalSRNNQCD', 'boosted-finalSRNNQCDTop','boosted-finalSRNN', 'boosted-finalSRNNlow_AND_boosted-finalSRNN_combined']

  # combos
  l_cut_sels = ['resolved-finalSR', 'intermediate-finalSR', 'boosted-finalSR', 'resolved-finalSR_intermediate-finalSR_boosted-finalSR_combined']
  l_cut_sels = ['resolved-finalSRNNlam10', 'intermediate-finalSRNNlam10', 'boosted-finalSRNNlam10', 'resolved-finalSRNNlam10_intermediate-finalSRNNlam10_boosted-finalSRNNlam10_combined']
  l_cut_sels = ['resolved-finalSRNN', 'intermediate-finalSRNN', 'boosted-finalSRNN', 'resolved-finalSRNN_intermediate-finalSRNN_boosted-finalSRNN_combined']
  #resolved-finalSR_AND_intermediate-finalSR_combined','boosted-finalSR_AND_resolved-finalSR_AND_intermediate-finalSR_combined_combined'] 
  #l_cut_sels = ['resolved-finalSRNNlow_AND_resolved-finalSRNN_combined', 'intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined','boosted-finalSRNNlow_AND_boosted-finalSRNN_combined','resolved-finalSRNNlow_AND_resolved-finalSRNN_combined_AND_intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined_combined','boosted-finalSRNNlow_AND_boosted-finalSRNN_combined_AND_resolved-finalSRNNlow_AND_resolved-finalSRNN_combined_AND_intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined_combined_combined']
  ###
  #l_cut_sels = ['resolved-finalSRNNlow_AND_resolved-finalSRNN_combined', 'intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined','boosted-finalSRNNlow_AND_boosted-finalSRNN_combined','resolved-finalSRNNlow_AND_resolved-finalSRNN_combined_AND_intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined_combined']
  #l_cut_sels = ['resolved-finalSRNNlam10low_AND_resolved-finalSRNNlam10_combined', 'intermediate-finalSRNNlam10low_AND_intermediate-finalSRNNlam10_combined','boosted-finalSRNNlam10low_AND_boosted-finalSRNNlam10_combined','resolved-finalSRNNlam10low_AND_resolved-finalSRNNlam10_combined_AND_intermediate-finalSRNNlam10low_AND_intermediate-finalSRNNlam10_combined_combined']

  #l_cut_sels = ['resolved-finalSRNNlam','intermediate-finalSRNNlam','boosted-finalSRNNlam']
  #l_cut_sels = ['resolved-finalSRNNlamm5','intermediate-finalSRNNlamm5','boosted-finalSRNNlamm5']
  #l_cut_sels = ['resolved-finalSRNNlam10','intermediate-finalSRNNlam10','boosted-finalSRNNlam10','resolved-finalSRNN','intermediate-finalSRNN','boosted-finalSRNN']

  #l_cut_sels = ['resolved-finalSRNN', 'intermediate-finalSRNN', 'boosted-finalSRNN', 'resolved-finalSRNN_AND_intermediate-finalSRNN_combined','boosted-finalSRNN_AND_resolved-finalSRNN_AND_intermediate-finalSRNN_combined_combined'] 
  #l_cut_sels = ['resolved-finalSRNN', 'intermediate-finalSRNN', 'boosted-finalSRNN', 'resolved-finalSRNNlow_AND_resolved-finalSRNN_combined','intermediate-finalSRNNlow_AND_intermediate-finalSRNN_combined','boosted-finalSRNNlow_AND_boosted-finalSRNN_combined'] 
  # sequential improvements
  #l_cut_sels = ['resolved-finalSR','resolved-finalSRNNQCD', 'intermediate-finalSR','intermediate-finalSRNNQCD', 'boosted-finalSR','boosted-finalSRNNQCD']#, 'resolved-finalSR_AND_intermediate-finalSR_combined','resolved-finalSRNNQCD_AND_intermediate-finalSRNNQCD_combined','boosted-finalSR_AND_resolved-finalSR_AND_intermediate-finalSR_combined_combined','boosted-finalSRNNQCD_AND_resolved-finalSRNNQCD_AND_intermediate-finalSRNNQCD_combined_combined'] 
  #l_cut_sels = ['resolved-finalSRNNQCD','resolved-finalSRNNQCDTop', 'intermediate-finalSRNNQCD','intermediate-finalSRNNQCDTop', 'boosted-finalSRNNQCD','boosted-finalSRNNQCDTop'] 
  #l_cut_sels = ['resolved-finalSRNNQCDTop','resolved-finalSRNN', 'intermediate-finalSRNNQCDTop','intermediate-finalSRNN', 'boosted-finalSRNNQCDTop','boosted-finalSRNN']
 
  #l_zCols = ['chiSq', 'chiSqSyst1pc']
  l_zCols = ['chiSqSyst1pc']
  
  IsLogY = False
  
  #l_cut_sels = ['resolved-finalSR', 'intermediate-finalSR', 'boosted-finalSR'] 
  #l_zCols = ['xsec','acceptance']
  #IsLogY = True

  d_axis_tlatex = {
    'acceptance'        : 'A #times \epsilon (S / #sigma #times L) [%]',
    'xsec'              : 'xsec [pb]',
    'N_sig'             : 'Signal yield',
    'N_sig_raw'         : 'Raw signal yield',
    'SoverB'            : 'S / B',
    'SoverSqrtB'        : 'S / #sqrt{B}',
    'SoverSqrtBSyst1pc' : 'S / #sqrt{B + (1%B)^{2}}',
    'chiSq'             : '#chi^{2}',
    'chiSqSyst1pc'      : '#chi^{2}',
    'sum_chiSq'         : '#chi^{2}',
    'sum_chiSqSyst1pc'  : '#chi^{2}',
  }

  d_in_data = {}

  # Build part of output name, shorten by abbreviating some names
  cut_sel_out_name = ''.join(l_cut_sels).replace("finalSR","SR").replace("resolved","R").replace("intermediate","I").replace("boosted","B").replace("combined","c")
 
  for zCol in l_zCols: 
    if do_ktop:
      out_file = 'figs/limit1d_TopYuk_vary_SlfCoup_1p0_{0}_{1}'.format(cut_sel_out_name, zCol)
    else: 
      out_file = 'figs/limit1d_TopYuk_1p0_SlfCoup_vary_{0}_{1}'.format(cut_sel_out_name, zCol)
    
    for cut_sel in l_cut_sels:
      print(cut_sel)
      # Input file made from ntuples_to_chiSq.py
      if 'combined' in cut_sel:
        d_in_data[cut_sel]  = 'data/CHISQ_loose_preselection_{0}_{1}.csv'.format(cut_sel, zCol)
      else:
        d_in_data[cut_sel]  = 'data/CHISQ_loose_preselection_{0}.csv'.format(cut_sel)
 
    print('Output file to store chi squares: {0}'.format( out_file  ) )
    make_plot( d_in_data, out_file, l_cut_sels, do_ktop, zCol, d_axis_tlatex, IsLogY, legend_outside_plot)

#____________________________________________________________________________
def make_plot( d_in_data, out_file, l_cut_sels, do_ktop, zCol, d_axis_tlatex, IsLogY, legend_outside_plot ):

  print( d_in_data )

  # TODO remove l_colours = [myDarkBlue, myDarkGreen, myMediumOrange, myMediumPurple, myMediumPink ]
  l_widths  = [5]*10 
  if legend_outside_plot:
    gpRight = 0.4
    can  = TCanvas('','',1200,800)
  else:
    # gPad left/right margins
    gpRight = 0.05
    can  = TCanvas('','',1000,800)

  if IsLogY:
    can.SetLogy()
  #==========================================================
  # Build canvas   

  #gpLeft = 0.21
  gpLeft = 0.11
  customise_gPad(top=0.08, bot=0.20, left=gpLeft, right=gpRight)
  
  # construct legend
  #xl1, yl1 = 0.45, 0.68
  #xl2, yl2 = xl1+0.25, yl1+0.20
  extra_space = (0.05*len(l_cut_sels))+(0.03*str(l_cut_sels).count("combined"))
  print('Extra space: {0}'.format(extra_space))
  
  if extra_space > 0.5:
    if zoom_in: 
      xl1, yl1 = 0.45, 0.35
    else:
      xl1, yl1 = 0.45, 0.5
  elif extra_space > 0.25:
    if zoom_in: 
      xl1, yl1 = 0.45, 0.54
    else:
      xl1, yl1 = 0.45, 0.6
  elif extra_space > 0.:
    if zoom_in: 
      xl1, yl1 = 0.45, 0.54
    else:
      xl1, yl1 = 0.48, 0.50

  if 'lam10' in l_cut_sels[0]:
    xl1 = 0.23 

  if legend_outside_plot:
    xl1 = 0.6

  if zCol == 'acceptance':
    xl1 = 0.25

  xl2, yl2 = xl1+0.20, yl1+extra_space

  if extra_space > 0.5:
    xl2, yl2 = xl1+0.25, yl1+extra_space-0.2

  leg = TLegend(xl1,yl1,xl2,yl2)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0) # transparent
  leg.SetTextSize(0.045)
  leg.SetTextFont(132)
  
  #------------------------------------------------------
  # Get and organise data
  #------------------------------------------------------
  
  d_tgraphs = {}

  count = 0

  for cut_sel, width in zip( l_cut_sels, l_widths ):
    in_file = d_in_data[cut_sel]
    print "Opening: ", in_file
    d_csv = csv_to_lists(in_file)
    #pprint( d_csv )

    if do_ktop:
      in_x = [float(i) for i in d_csv['TopYuk'] ]
      in_y = [float(i) for i in d_csv['SlfCoup'] ]
    else:
      in_x = [float(i) for i in d_csv['SlfCoup'] ]
      in_y = [float(i) for i in d_csv['TopYuk'] ]

    if 'combined' in cut_sel:
      print(zCol)
      zCol = 'sum_' + str(zCol)
    in_z = [float(i) for i in d_csv[zCol] ]

    l_SlfCoup_or_TopYuk = []
    l_chiSq   = []

    for x, y, z in sorted(zip(in_x, in_y, in_z)):
      if y == 1.0: 
        l_SlfCoup_or_TopYuk.append(x)
        if zCol == 'acceptance':
          l_chiSq.append(z*300) # convert to percentage and x3 to compare to ATLAS (us inclusive, them 4b i.e. 1/0.33 = 3)
        else:
          l_chiSq.append(z)
        #l_chiSq.append(z)

    tg = TGraph( len(l_chiSq) )
    tg.SetMarkerColor(d_cut_sel_colour[cut_sel])
    tg.SetMarkerSize(width)
    tg.SetLineColor(d_cut_sel_colour[cut_sel])
    tg.SetLineWidth(width)
    tg.SetTitle('')

    for i, (x, y) in enumerate( zip( l_SlfCoup_or_TopYuk, l_chiSq) ):
      tg.SetPoint(i, x, y)
    d_tgraphs[cut_sel] = tg
  
    if 'SRNN' in cut_sel:
      analysis = 'DNN'
    else:
      analysis = 'Baseline'

    if 'resolved' in cut_sel and 'intermediate' in cut_sel and 'boosted' in cut_sel:
      cut_txt = 'Combined '
    elif 'resolved' in cut_sel and 'intermediate' in cut_sel:
      cut_txt = 'Res + Int '
    elif 'resolved' in cut_sel:
      cut_txt = 'Resolved '
    elif 'intermediate' in cut_sel:
      cut_txt = 'Intermediate '
    elif 'boosted' in cut_sel:
      cut_txt = 'Boosted '
    else:
      cut_name = cut_sel.split('-')
      cut_txt = cut_name[0].capitalize()# + ' ' + cut_name[1] 

    if 'NNQCDTop' in cut_sel:
     cut_txt += ' QT'
    elif 'NNQCD' in cut_sel:
     cut_txt += ' Q'
    elif 'low_AND' in cut_sel:
     cut_txt += ' QT Shape'
    elif 'NNlow' in cut_sel:
     cut_txt += ' QTS Low'
    elif 'NN' in cut_sel:
     #cut_txt += ' QTS'
     cut_txt += ''
  
    if 'NN' in cut_sel: 
      if 'lam10' in cut_sel:
        #cut_txt += ' #lambda_{10} '
        myText(0.08, 0.07, 'DNN trained on #kappa(#lambda_{hhh}) = 10', 0.035, kGray+2, 0, True)
      else:
        myText(0.08, 0.07, 'DNN trained on #kappa(#lambda_{hhh}) = 1', 0.035, kGray+2, 0, True)

    leg.AddEntry(tg, cut_txt, 'l')

    #plt.plot(l_SlfCoup, l_chiSq, colour, linewidth=width, zorder=2, linestyle='-', label=cut_txt)

    tg = d_tgraphs[str(cut_sel)]
    if count==0:
      tg.Draw('PLA')
    else:
      tg.Draw('PL same')
    
    count+=1
    # ------------------------------------------------------ 
    # Attempt to search x where chiSq = 1, 3.84 points
    # ------------------------------------------------------ 
    search_min, search_max = -20., 20. # x-axis range to search
    N_scan = 200 # number of search steps
    threshold = 0.1
    # lambda values satisfying 68% CL and 95% CL
    l_68CL = []
    l_95CL = []
    for i in range( N_scan+1 ):
      # calculate search steps
      dx = ( i * ( search_max - search_min ) ) / N_scan
      x = search_min + dx
      y = tg.Eval(x)

      if abs( y - 1.) < threshold: 
        l_68CL.append(x)
      if abs( y - 3.84 ) < threshold:
        l_95CL.append(x)
      #print('x: {0:.4g}, TGraph eval: {1:.4g}'.format( x, tg.Eval(x) ))
    print('68% CL: {0}'.format(l_68CL))
    print('95% CL: {0}'.format(l_95CL))
  #d_tgraphs['resolved-finalSR'].Draw('PLA')
  #d_tgraphs['intermediate-finalSR'].Draw('PL same')
  #d_tgraphs['boosted-finalSR'].Draw('PL same')
  #d_tgraphs['resolved-finalSR_AND_intermediate-finalSR_combined'].Draw('PL same')
  #d_tgraphs['boosted-finalSR_AND_resolved-finalSR_AND_intermediate-finalSR_combined_combined'].Draw('PL same')

  if zCol != 'xsec':
    leg.Draw('same')

  if legend_outside_plot:
    label_x = 0.01
    label_y = 0.96
  else:
    label_x = 0.83
    label_y = 0.84
  
  if do_ktop:
    fixed_coupling = '#kappa(#lambda_{hhh}) = 1'
  else:
    fixed_coupling = '#kappa(#it{y}_{top}) = 1'

  if do_ktop:
    xtitle = '#kappa(#it{y}_{top})'
  else:
    xtitle = '#kappa(#lambda_{hhh})'

  ytitle = d_axis_tlatex[zCol]

  if 'chiSqSyst1pc' in zCol:
    syst_txt = '1% systematics'
  elif 'chiSq' in zCol and 'pc' not in zCol:
    syst_txt = '0% systematics'
  else:
    syst_txt = ''

    
  if legend_outside_plot:
    myText(0.2, 0.95, SQRTS_LUMI + ', {0}, {1}, {2}, {3}'.format('hh #rightarrow 4b',syst_txt, analysis, fixed_coupling), 0.04, kBlack, 0, True)
  else:
    myText(0.11, 0.95, SQRTS_LUMI + ', {0}, {1}, {2}, {3}'.format('hh #rightarrow 4b',syst_txt, analysis, fixed_coupling), 0.04, kBlack, 0, True)

  #customise_axes(d_tgraphs['resolved-finalSR'], xtitle, ytitle, 2.8, IsLogY)
  customise_axes(d_tgraphs[l_cut_sels[0]], xtitle, ytitle, 2.8, IsLogY, doktop = do_ktop)#, 2.8)

  xax = d_tgraphs[l_cut_sels[0]].GetXaxis()
  xmin = xax.GetXmin()
  xmax = xax.GetXmax()
 
  if 'chiSq' in zCol:
    if do_ktop:
      if zoom_in:
        mymin = -0.2
        mymax = 1.4
      else:
        mymin = 0.5
        mymax = 1.5
    else:
      if zoom_in:
        mymin = -10
        mymax = 10
      else:
        mymin = -20
        mymax = 20
        #mymin = -15.5
        #mymax = 15.5
 
    # 68% CL line, chi2 = 1
    line = TLine(mymin,1,mymax,1);
    line.SetLineColor(kGray+1)
    line.SetLineWidth(3)
    line.Draw("same")
   
    if legend_outside_plot:
      label_x = 0.135
    else:
      label_x = 0.55
      if 'lam10' in l_cut_sels[0]:
        label_x = 0.3


    if do_ktop:
      myText(label_x, 0.7, '68% CL', 0.037, kGray+1, 0, True)
    else:
      myText(label_x, 0.305, '68% CL', 0.037, kGray+1, 0, True)
  
    # 95% CL line, chi2 = 3.84
    line1 = TLine(mymin,3.84,mymax,3.84);
    line1.SetLineColor(kGray+1)
    line1.SetLineWidth(3)
    line1.Draw("same")
    if not do_ktop: 
      myText(label_x, 0.77, '95% CL', 0.037, kGray+1, 0, True)
  
  gPad.RedrawAxis() 
  #customise_axes(d_tgraphs['resolved-finalSR'], xtitle, ytitle, 2.8, IsLogY)
  customise_axes(d_tgraphs[l_cut_sels[0]], xtitle, ytitle, 2.8, IsLogY, doktop = do_ktop)#, 2.8)
  
  #==========================================================
  # save everything
  can.cd()
  can.SaveAs(out_file + '.pdf')
  can.Close()
  
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
def customise_axes(hist, xtitle, ytitle, scaleFactor=1.1, IsLogY=False, enlargeYaxis=False, doktop=False):

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
 
  #xax.SetRangeUser(-20,20)

  if doktop: 
    if zoom_in:
      xax.SetRangeUser(-0.2,1.4) 
    else:
      xax.SetRangeUser(0.5,1.5) 
  else:
    if zoom_in:
      xax.SetRangeUser(-10,10) 
    else:
      xax.SetRangeUser(-20,20) 
      #xax.SetRangeUser(-15,15) 
 
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
  #yax.SetTitleOffset(1.3) 
  yax.SetTitleOffset(0.7) 
  
  yax.SetLabelOffset(0.015)
  yax.SetLabelSize(text_size)
 
  ymax = hist.GetMaximum()
  ymin = hist.GetMinimum()
 
  scaleFactor = 3.2
  yax.SetNdivisions(505) 
  if IsLogY:
    hist.SetMaximum(ymax)
    hist.SetMinimum(ymin)
    hist.SetMaximum(10)
    hist.SetMinimum(0.01)
  if not IsLogY:
    if doktop:
      hist.SetMaximum(1.5)
    else:
      hist.SetMaximum(5)
    hist.SetMinimum(0.0)
    #hist.SetMaximum(ymax*scaleFactor) 

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
def myText(x, y, text, tsize=0.05, color=kBlack, angle=0, do_NDC=False) :

  l = TLatex()
  l.SetTextSize(tsize)
  l.SetNDC()
  l.SetTextFont(132)
  if do_NDC:
    # set relative to canvas coordinates rather than histogram coordinates
    l.SetNDC()
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
