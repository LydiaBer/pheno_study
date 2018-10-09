'''

Welcome to format.py

This has general plot formatting functions 

'''
from ROOT import *

#____________________________________________________________________________
def format_hist(hist, l_width=2, l_color=kBlue+2, l_style=1, f_color=0, f_style=1001, l_alpha=1.0):
  
  # Lines
  hist.SetLineColorAlpha(l_color, l_alpha)
  hist.SetLineStyle(l_style)
  hist.SetLineWidth(l_width)
  
  # Fills
  hist.SetFillColor(f_color)
  hist.SetFillStyle(f_style)

  # Markers
  hist.SetMarkerColor(l_color)
  hist.SetMarkerSize(1.1)
  hist.SetMarkerStyle(20)

#____________________________________________________________________________
def customise_gPad(top=0.03, bot=0.15, left=0.17, right=0.08):

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
def customise_axes(hist, xtitle, ytitle, scaleFactor=1.1, IsLogY=False, enlargeYaxis=False):
  # set a universal text size
  #text_size = 0.055
  text_size = 45
  TGaxis.SetMaxDigits(4) 
  ##################################
  # X axis
  xax = hist.GetXaxis()
  xax.CenterTitle() 
  
  # precision 3 Helvetica (specify label size in pixels)
  xax.SetLabelFont(133)
  xax.SetTitleFont(133)
  #xax.SetTitleFont(13) # times
  
  xax.SetTitle(xtitle)
  xax.SetTitleSize(text_size)
  # top panel
  #if xtitle == '':
  #if 'Events' in ytitle:
  #if False:
  #  xax.SetLabelSize(0)
  #  xax.SetLabelOffset(0.02)
  #  xax.SetTitleOffset(2.0)
  #  xax.SetTickSize(0.04)  
  # bottom panel
  #else:
  xax.SetLabelSize(text_size - 7)
  xax.SetLabelOffset(0.03)
  xax.SetTitleOffset(1.15)
  xax.SetTickSize(0.08)

  #xax.SetRangeUser(0,2000) 
  #xax.SetNdivisions(-505) 
  gPad.SetTickx() 
  
  ##################################
  # Y axis
  yax = hist.GetYaxis()
  # precision 3 Helvetica (specify label size in pixels)
  yax.SetLabelFont(133)
  yax.SetTitleFont(133)
  yax.CenterTitle() 
 
  
  yax.SetTitle(ytitle)
  yax.SetTitleSize(text_size)
  yax.SetTitleOffset(1.1)    
  
  yax.SetLabelOffset(0.015)
  yax.SetLabelSize(text_size - 7)
 
  ymax = hist.GetMaximum()
  ymin = hist.GetMinimum()
  
  # top events panel
  #if xtitle == '':
  if 'Events' in ytitle:
    yax.SetNdivisions(505) 
    if IsLogY:
      if enlargeYaxis:
        ymax = 2 * 10 ** 13
        ymin = 20
      else:
        #ymax = 3 * 10 ** 4
        #ymin = 0.5
        ymax = 3 * 10 ** 3
        ymin = 0.005
      hist.SetMaximum(ymax)
      hist.SetMinimum(ymin)
    else:
      hist.SetMaximum(ymax*scaleFactor)
      #hist.SetMaximum(100)
      #hist.SetMaximum(30)
      #hist.SetMaximum(60)
      hist.SetMinimum(0.0)
  # bottom panel 
  elif 'Significance' in ytitle:
    hist.SetMinimum(0.0)
    hist.SetMaximum(4.5) 
    yax.SetNdivisions(205)
   
  gPad.SetTicky()
  gPad.Update()


#____________________________________________________________________________
def myText(x, y, text, tsize=0.03, color=kBlack, angle=0) :
  
  l = TLatex()
  l.SetTextSize(tsize)
  l.SetNDC()
  l.SetTextColor(color)
  l.SetTextAngle(angle)
  l.DrawLatex(x,y,'#bf{' + text + '}')
  l.SetTextFont(4)


#____________________________________________________________________________
def add_cut_arrow_to_plot(h_bkg, d_vars, var, hXmax, IsLogY):

  print('Drawing arrow to indicate where cut is in N-1 plot')
   
  #---------------------------------------
  #
  # Set height of arrow
  ymin_Ar = gPad.GetUymin()
  ymax_Ar = h_bkg.GetMaximum()
  if IsLogY:     ymax_Ar = 80
  if not IsLogY: ymax_Ar = 0.8*ymax_Ar
  
  # Arrow horizontal length is 6% of the maximum x-axis bin 
  arr_width = hXmax * 0.06
  
  # Case 1-sided cut 
  cut_pos = d_vars[var]['cut_pos']
  cut_dir = d_vars[var]['cut_dir']
  cutAr = cut_arrow(cut_pos, ymin_Ar, cut_pos, ymax_Ar, cut_dir, 0.012, arr_width)
  cutAr[0].Draw()
  cutAr[1].Draw()
  
  # Case 2-sided cuts, add an extra arrow
  if 'cut_pos2' in d_vars[var].keys():
    cut_pos2 = d_vars[var]['cut_pos2']
    cut_dir2 = d_vars[var]['cut_dir2']
    cutAr2   = cut_arrow(cut_pos2, ymin_Ar, cut_pos2, ymax_Ar, cut_dir2, 0.012, arr_width)
    cutAr2[0].Draw()
    cutAr2[1].Draw()
  #---------------------------------------

#____________________________________________________________________________
def cut_arrow(x1, y1, x2, y2, direction='right', ar_size=1.0, ar_width=10, color=kGray+3, style=1) :
  
  # Draw an arrow to indicate the cut position of a variable
  l = TLine(x1, y1, x2, y2)
  if direction == 'right':
    ar = TArrow(x1-0.02, y2, x1+ar_width, y2, ar_size, '|>')
  if direction == 'left':
    ar = TArrow(x1-ar_width+0.02, y2, x1, y2, ar_size, '<|')
  if direction == 'up':
    ar = TArrow(x1, y1, x1, y2, ar_size, '|>')
  if direction == 'down':
    ar = TArrow(x1, y1, x1, y2, ar_size, '<|')
  
  l.SetLineWidth(4)
  l.SetLineStyle(style)
  l.SetLineColor(color) 
  ar.SetLineWidth(4)
  ar.SetLineStyle(style)
  ar.SetLineColor(color) 
  ar.SetFillColor(color)  
  return [l, ar]

#____________________________________________________________________________
def draw_line(xmin, ymin, xmax, ymax, color=kGray+1, style=2) :

  # Function to draws lines given locations @xmin, ymin, xmax, ymax

  line = TLine(xmin , ymin , xmax, ymax)
  line.SetLineWidth(2)
  line.SetLineStyle(style)
  line.SetLineColor(color) # 12 = gray
  return line
 
