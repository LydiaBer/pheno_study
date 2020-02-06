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
myMediumPink    = TColor.GetColor('#fcc5c0')
myDarkPink      = TColor.GetColor('#dd3497')

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
d_cut_sel_colour = {
                    'SR-res' : myPink, 
                    'SR-int' : myMediumPurple,
                    'SR-bst' : myDarkPurple,
                    'SR_combined' : myMediumBlue,

                    'SRNN-res-lam1' : myPink, 
                    'SRNN-int-lam1' : myMediumPurple,
                    'SRNN-bst-lam1' : myDarkPurple,
                    'SRNN-lam1_combined' : myMediumBlue,

                    'SRNN-res-lam5' : myPink, 
                    'SRNN-int-lam5' : myMediumPurple,
                    'SRNN-bst-lam5' : myDarkPurple,
                    'SRNN-lam5_combined' : myMediumBlue,

                    'SRNN-res-lam7' : myPink, 
                    'SRNN-int-lam7' : myMediumPurple,
                    'SRNN-bst-lam7' : myDarkPurple,
                    'SRNN-lam7_combined' : myMediumBlue,

                    'SRNN-res-lam10' : myPink, 
                    'SRNN-int-lam10' : myMediumPurple,
                    'SRNN-bst-lam10' : myDarkPurple,
                    'SRNN-lam10_combined' : myMediumBlue,

                    'SRNN-res-lamM1' : myPink, 
                    'SRNN-int-lamM1' : myMediumPurple,
                    'SRNN-bst-lamM1' : myDarkPurple,
                    'SRNN-lamM1_combined' : myMediumBlue,

                    'SRNN-res-lamM2' : myPink, 
                    'SRNN-int-lamM2' : myMediumPurple,
                    'SRNN-bst-lamM2' : myDarkPurple,
                    'SRNN-lamM2_combined' : myMediumBlue,

                    'SRNN-res-lamM5' : myPink, 
                    'SRNN-int-lamM5' : myMediumPurple,
                    'SRNN-bst-lamM5' : myDarkPurple,
                    'SRNN-lamM5_combined' : myMediumBlue,

                    'SR_res_multibin_combined' : myPink,
                    'SR_int_multibin_combined' : myMediumPurple,
                    'SR_bst_multibin_combined' : myDarkPurple,
                    'SR_all_multibin_combined' : myMediumBlue,
                    
                    'SRNN_res_multibin_lam1_combined' : myPink,
                    'SRNN_int_multibin_lam1_combined' : myMediumPurple,
                    'SRNN_bst_multibin_lam1_combined' : myDarkPurple,
                    'SRNN_all_multibin_lam1_combined' : myMediumBlue,
                    
                    'SRNN_res_multibin_lam5_combined' : myPink,
                    'SRNN_int_multibin_lam5_combined' : myMediumPurple,
                    'SRNN_bst_multibin_lam5_combined' : myDarkPurple,
                    'SRNN_all_multibin_lam5_combined' : myMediumBlue,
                    
                    'SRNN_res_multibin_lam7_combined' : myPink,
                    'SRNN_int_multibin_lam7_combined' : myMediumPurple,
                    'SRNN_bst_multibin_lam7_combined' : myDarkPurple,
                    'SRNN_all_multibin_lam7_combined' : myMediumBlue,

                    'SRNN_res_multibin_lam10_combined' : myPink,
                    'SRNN_int_multibin_lam10_combined' : myMediumPurple,
                    'SRNN_bst_multibin_lam10_combined' : myDarkPurple,
                    'SRNN_all_multibin_lam10_combined' : myMediumBlue,
                    
                    'SRNN_res_multibin_lamM1_combined' : myPink,
                    'SRNN_int_multibin_lamM1_combined' : myMediumPurple,
                    'SRNN_bst_multibin_lamM1_combined' : myDarkPurple,
                    'SRNN_all_multibin_lamM1_combined' : myMediumBlue,
                    
                    'SRNN_res_multibin_lamM2_combined' : myPink,
                    'SRNN_int_multibin_lamM2_combined' : myMediumPurple,
                    'SRNN_bst_multibin_lamM2_combined' : myDarkPurple,
                    'SRNN_all_multibin_lamM2_combined' : myMediumBlue,
                    
                    'SRNN_res_multibin_lamM5_combined' : myPink,
                    'SRNN_int_multibin_lamM5_combined' : myMediumPurple,
                    'SRNN_bst_multibin_lamM5_combined' : myDarkPurple,
                    'SRNN_all_multibin_lamM5_combined' : myMediumBlue,
                   }

# Labels
SQRTS_LUMI = '#sqrt{s} = 14 TeV, 3000 fb^{#minus1}'

# Switch to true to zoom in on x-axis 
zoom_in = True

#____________________________________________________________________________
def main():

  mkdir('contours')

  # TODO lumi option throughout

  # Default is limits on lambda, if you wish to produce kappa top limit set do_ktop to True
  do_ktop = False
 
  # When lots of samples, put leg outside plot so less crowded
  legend_outside_plot = False

  # chi^2 plots
  #l_zCols = ['chiSqSyst0p3pc', 'chiSqSyst1pc', 'chiSq']
  l_zCols = ['chiSqSystMix']

  IsLogY = False

  # Cut selections
  d_SRsets = {}

  d_SRsets['baseline']   = ['SR_res_multibin_combined', 
                            'SR_int_multibin_combined', 
                            'SR_bst_multibin_combined', 
                            'SR_all_multibin_combined']

  d_SRsets['SRNN_lam1']  = ['SRNN_res_multibin_lam1_combined', 
                            'SRNN_int_multibin_lam1_combined', 
                            'SRNN_bst_multibin_lam1_combined', 
                            'SRNN_all_multibin_lam1_combined']
  
  d_SRsets['SRNN_lam5']  = ['SRNN_res_multibin_lam5_combined', 
                            'SRNN_int_multibin_lam5_combined', 
                            'SRNN_bst_multibin_lam5_combined', 
                            'SRNN_all_multibin_lam5_combined']

  d_SRsets['SRNN_lam7']  = ['SRNN_res_multibin_lam7_combined', 
                            'SRNN_int_multibin_lam7_combined', 
                            'SRNN_bst_multibin_lam7_combined', 
                            'SRNN_all_multibin_lam7_combined']

  '''
  d_SRsets = {}
  d_SRsets['overlay']   = [
                           'SRNN_res_multibin_lam1_combined', 
                           'SRNN_res_multibin_lam5_combined', 
                           'SRNN_res_multibin_lam7_combined', 
                           'SRNN_res_multibin_lam10_combined', 
                           'SRNN_res_multibin_lamM1_combined', 
                           'SRNN_res_multibin_lamM2_combined', 
                           'SRNN_res_multibin_lamM5_combined'] 
  '''

  # acceptance plots, set zoom_in to False
  '''
  l_zCols = ['acceptance']

  IsLogY = True

  d_SRsets = {}
  d_SRsets['baseline-no-mhh-binning']   = ['SR-res', 
                                           'SR-int', 
                                           'SR-bst']
  '''

  d_axis_tlatex = {
    'acceptance'         : 'A #times \epsilon (S / #sigma #times L) [%]',
    'xsec'               : 'xsec [pb]',
    'N_sig'              : 'Signal yield',
    'N_sig_raw'          : 'Raw signal yield',
    'SoverB'             : 'S / B',
    'SoverSqrtB'         : 'S / #sqrt{B}',
    'SoverSqrtBSyst1pc'  : 'S / #sqrt{B + (1%B)^{2}}',
    'chiSq'              : '#chi^{2}',
    'chiSqSyst0p3pc'     : '#chi^{2}',
    'chiSqSyst1pc'       : '#chi^{2}',
    'chiSqSystMix'       : '#chi^{2}',
    'sum_chiSq'          : '#chi^{2}',
    'sum_chiSqSyst1pc'   : '#chi^{2}',
    'sum_chiSqSyst0p5pc' : '#chi^{2}',
    'sum_chiSqSyst0p3pc' : '#chi^{2}',
    'sum_chiSqSystMix'   : '#chi^{2}',
  }

  d_in_data = {}

  for SRset in d_SRsets:
    l_cut_sels = d_SRsets[SRset]
    # Build part of output name, shorten by abbreviating some names
    cut_sel_out_name = ''.join(l_cut_sels).replace("finalSR","SR").replace("resolved","R").replace("intermediate","I").replace("boosted","B").replace("combined","c")
    print( 'Processing SR set: {0}'.format(l_cut_sels)) 
    for zCol in l_zCols: 
      if do_ktop:
        out_file = 'figs/limit1d_TopYuk_vary_SlfCoup_1p0_{0}_{1}'.format(cut_sel_out_name, zCol)
      else: 
        out_file = 'figs/limit1d_TopYuk_1p0_SlfCoup_vary_{0}_{1}'.format(l_cut_sels[-1], zCol)
      
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
  if 'acceptance' in zCol:
    gpLeft = 0.15
  else:
    gpLeft = 0.11
  customise_gPad(top=0.08, bot=0.20, left=gpLeft, right=gpRight)
  
  #------------------------------------------------------
  # Construct legend
  #------------------------------------------------------
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
      xl1, yl1 = 0.43, 0.38
    else:
      xl1, yl1 = 0.43, 0.6
  elif extra_space > 0.:
    if zoom_in: 
      xl1, yl1 = 0.35, 0.54
    else:
      xl1, yl1 = 0.48, 0.50

  #if 'lam10' in l_cut_sels[0]:
  #  xl1 = 0.23 

  if legend_outside_plot:
    xl1 = 0.6

  if zCol == 'acceptance' and not legend_outside_plot:
    xl1 = 0.22
    yl1 = 0.68

  xl2, yl2 = xl1+0.20, yl1+extra_space

  if extra_space > 0.5:
    xl2, yl2 = xl1+0.25, yl1+extra_space-0.2

  leg = TLegend(xl1,yl1,xl2,yl2)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0) # transparent
  leg.SetTextSize(0.045)
  leg.SetTextFont(132)
  
  # ------------------------------------------------------ 
  # ATLAS PHYS-PUB-2018-053 constraints
  # ------------------------------------------------------ 
  
  if 'acceptance' not in zCol:
    # 0% systematics limits
    if 'chiSq' in zCol and 'Syst' not in zCol:
      HLLHC_lam1 = -0.5
      HLLHC_lam2 = 5.0
    # Use 0.3% systematics limits
    else:
      HLLHC_lam1 = -2.5
      HLLHC_lam2 = 6.5
    lim_ATL_HLLHC_left  = TBox (-8.2, 0., HLLHC_lam1, 5.)
    lim_ATL_HLLHC_right = TBox (HLLHC_lam2, 0., 13.5, 5.)
    lim_ATL_HLLHC_left.SetFillColorAlpha(kGray+1,  0.2)
    lim_ATL_HLLHC_right.SetFillColorAlpha(kGray+1, 0.2)
  
    leg.AddEntry(lim_ATL_HLLHC_left, 'ATLAS 3 ab^{#minus1}', 'f')
  
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
      zCol_key = 'sum_' + str(zCol)
    else:
      zCol_key = str(zCol)
    in_z = [float(i) for i in d_csv[zCol_key] ]

    l_SlfCoup_or_TopYuk = []
    l_chiSq   = []

    for x, y, z in sorted(zip(in_x, in_y, in_z)):
      if y == 1.0: 
        l_SlfCoup_or_TopYuk.append(x)
        if zCol == 'acceptance':
          l_chiSq.append(z*100) # convert to percentage # To compare to ATLAS need to also x3 (us inclusive, them 4b i.e. 1/0.33 = 3)
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
  
  #------------------------------------------------------
  # Annotating text for plots
  #------------------------------------------------------
  
    if 'SRNN' in cut_sel:
      analysis = 'DNN'
    else:
      analysis = 'Baseline'

    if 'resolved' in cut_sel and 'intermediate' in cut_sel and 'boosted' in cut_sel:
      cut_txt = 'Combined '
    elif 'resolved' in cut_sel and 'intermediate' in cut_sel:
      cut_txt = 'Res + Int '
    elif 'res' in cut_sel:
      cut_txt = 'Resolved '
    elif 'int' in cut_sel:
      cut_txt = 'Intermediate '
    elif 'bst' in cut_sel or 'boosted' in cut_sel:
      cut_txt = 'Boosted '
    elif 'all' in cut_sel:
      cut_txt = 'Combined '
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
        myText(0.08, 0.07, 'DNN trained on #kappa(#lambda_{hhh}) = 10', 0.035, kGray+2, 0, True)
      elif 'lam5' in cut_sel:
        myText(0.08, 0.07, 'DNN trained on #kappa(#lambda_{hhh}) = 5', 0.035, kGray+2, 0, True)
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
    syst_txt = ', 1% systematics'
  elif 'chiSqSyst0p3pc' in zCol:
    syst_txt = ', 0.3% systematics'
  elif 'chiSq' in zCol and 'Syst' not in zCol:
    syst_txt = ', 0% systematics'
  else:
    syst_txt = ''

    
  if legend_outside_plot:
    myText(0.2, 0.95, SQRTS_LUMI + ', {0} {1}, {2}, {3}'.format('hh #rightarrow 4b',syst_txt, analysis, fixed_coupling), 0.04, kBlack, 0, True)
  else:
    if 'acceptance' in zCol:
      myText(0.15, 0.95, SQRTS_LUMI + ', {0} {1}, {2}, {3}'.format('hh #rightarrow 4b',syst_txt, analysis, fixed_coupling), 0.04, kBlack, 0, True)
    else: 
      myText(0.11, 0.95, SQRTS_LUMI + ', {0} {1}, {2}, {3}'.format('hh #rightarrow 4b',syst_txt, analysis, fixed_coupling), 0.04, kBlack, 0, True)
  customise_axes(d_tgraphs[l_cut_sels[0]], xtitle, ytitle, 2.8, IsLogY, doktop = do_ktop, zCol = zCol)

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
        mymin = -8
        mymax = 13
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
      #if 'lam10' in l_cut_sels[0]:
      #  label_x = 0.3


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
  customise_axes(d_tgraphs[l_cut_sels[0]], xtitle, ytitle, 2.8, IsLogY, doktop = do_ktop, zCol = zCol)
  
  if 'acceptance' not in zCol:
    lim_ATL_HLLHC_left.Draw('same')
    lim_ATL_HLLHC_right.Draw('same')
 

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
def customise_axes(hist, xtitle, ytitle, scaleFactor=1.1, IsLogY=False, enlargeYaxis=False, doktop=False, zCol = 'chiSqSyst0p3pc'):

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
      xax.SetRangeUser(-8,13) 
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
  if 'acceptance' in zCol:
    yax.SetTitleOffset(1.0) 
  else:
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
    hist.SetMinimum(0.005)
  if not IsLogY:
    if doktop:
      hist.SetMaximum(1.5)
    else:
      hist.SetMaximum(5)
    hist.SetMinimum(0.0)
    #hist.SetMaximum(ymax*scaleFactor) 
  if 'A #times \epsilon' in ytitle:
    hist.SetMinimum(5E-3)
    hist.SetMaximum(10.0) 
    yax.SetNdivisions(205)

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
