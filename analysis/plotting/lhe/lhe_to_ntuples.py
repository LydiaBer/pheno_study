#!/usr/bin/env python
'''
-------------------------------

Welcome to lhe_to_ntuples.py

2018

-------------------------------

Takes Les Houches Event file as input and outputs ROOT TTree ntuple ready for analysis
 - Calculates truth parton level variables of double Higgs production

------------------------------
Run as
./lhe_to_ntuples -i [path to lhe file] -o [path to output root file]
------------------------------

'''

#https://github.com/lukasheinrich/pylhe
import pylhe
import time, argparse, os, sys, gzip
from array import array
from ROOT  import TFile, TTree, TLorentzVector, TRandom3
from math  import sqrt, fabs, exp, log, cosh, cos, sin, tanh, sinh

#____________________________________________________________________________
def main():

  t0 = time.time()

  # Check user has inputted variables or not

  # Parse in arguments
  parser = argparse.ArgumentParser(description='This parses the .lhe Les Houches Events file and produces .root TTree ntuples. Run as ./lhe_to_ntuples -i unweighted_events.lhe -o out_tree.root')
  parser.add_argument('-i', '--ifile', type=str, nargs='?', help='Input LHE file', default='unweighted_events.lhe')
  parser.add_argument('-o', '--ofile', type=str, nargs='?', help='Name of output .root file', default='out_tree.root')

  args = parser.parse_args()

  if args.ifile:
    in_file = args.ifile
    print( 'Input file: {0}'.format(in_file) )  
    if 'lhe.gz' in in_file:
      print('Unzipping LHE file to read')
      os.system( 'gunzip {0}'.format(in_file) )
      in_file = in_file.replace('.lhe.gz', '.lhe')
  if args.ofile:
    out_file = args.ofile
    print( 'Output file: {0}'.format(out_file) )  

  #------------------------------------------------- 
  # Input LHE file
  #-------------------------------------------------
  print( 'Input .lhe file: {0}'.format(in_file))
  # Use pylhe to parse the LHE file
  lhef = pylhe.readLHE( in_file )

  #------------------------------------------------- 
  # Output tree
  #-------------------------------------------------
  outFile = TFile(out_file, "recreate")
  outTree = TTree( 'tree', 'tree' )

  #------------------------------------------------- 
  # Prepare variables to write to TTree branches
  #------------------------------------------------- 
 
  h1_M   = array('f', [0])
  h1_Pt  = array('f', [0])
  h1_Eta = array('f', [0])
  h1_Phi = array('f', [0])

  h2_M   = array('f', [0])
  h2_Pt  = array('f', [0])
  h2_Eta = array('f', [0])
  h2_Phi = array('f', [0])

  m_hh   = array('f', [0])
  pT_hh  = array('f', [0])
  eta_hh = array('f', [0])
  phi_hh = array('f', [0])
  
  dEta_hh = array('f', [0])

  # Declare TTree branches
  outTree.Branch('h1_M',   h1_M,   'h1_M/F')
  outTree.Branch('h1_Pt',  h1_Pt,  'h1_Pt/F')
  outTree.Branch('h1_Eta', h1_Eta, 'h1_Eta/F')
  outTree.Branch('h1_Phi', h1_Phi, 'h1_Phi/F')

  outTree.Branch('h2_M',   h2_M,   'h2_M/F')
  outTree.Branch('h2_Pt',  h2_Pt,  'h2_Pt/F')
  outTree.Branch('h2_Eta', h2_Eta, 'h2_Eta/F')
  outTree.Branch('h2_Phi', h2_Phi, 'h2_Phi/F')
  
  outTree.Branch('m_hh',   m_hh,   'm_hh/F')
  outTree.Branch('pT_hh',  pT_hh,  'pT_hh/F')
  outTree.Branch('eta_hh', eta_hh, 'eta_hh/F')
  outTree.Branch('phi_hh', phi_hh, 'phi_hh/F')
  
  outTree.Branch('dEta_hh', dEta_hh, 'dEta_hh/F')

  # Declare TLorentzVectors
  tlv_unordered_higgs1 = TLorentzVector()
  tlv_unordered_higgs2 = TLorentzVector()
  tlv_ordered_higgs1   = TLorentzVector()
  tlv_ordered_higgs2   = TLorentzVector()
  tlv_DiHiggs          = TLorentzVector()

  #------------------------------------------------- 
  # Loop through all events in the parsed LHE file
  #------------------------------------------------- 
  for count, event in enumerate( lhef ):
    
    # debug break
    #if count > 10: break 
    
    if count % 1000 == 0:
      sys.stdout.write( '\r Event {0}'.format(count) )
      sys.stdout.flush() 
    
    count_higgs = 0

    #------------------------------------------------- 
    # Loop through all particles
    #------------------------------------------------- 
    for part in event.particles:
      pid = int(part.id)
      # PDG ID of Higgs boson is 25
      if abs(pid) == 25:
        count_higgs += 1
        if count_higgs == 1:
          tlv_unordered_higgs1.SetPxPyPzE(part.px, part.py, part.pz, part.e)
        if count_higgs == 2:
          tlv_unordered_higgs2.SetPxPyPzE(part.px, part.py, part.pz, part.e)

    #------------------------------------------------- 
    # Order Higgs by pT 
    #------------------------------------------------- 
    # if Higgs2Pt is has larger pT than Higgs1Pt, invert the tlv assignment
    if tlv_unordered_higgs2.Pt() > tlv_unordered_higgs1.Pt():
      tlv_ordered_higgs1 = tlv_unordered_higgs2
      tlv_ordered_higgs2 = tlv_unordered_higgs1
    else: 
      tlv_ordered_higgs1 = tlv_unordered_higgs1
      tlv_ordered_higgs2 = tlv_unordered_higgs2

    tlv_DiHiggs = tlv_ordered_higgs1 + tlv_ordered_higgs2

    #------------------------------------------------- 
    # Set variables for TTree 
    #------------------------------------------------- 
    h1_M[0]       = tlv_ordered_higgs1.M()
    h1_Pt[0]      = tlv_ordered_higgs1.Pt()
    h1_Eta[0]     = tlv_ordered_higgs1.Eta()
    h1_Phi[0]     = tlv_ordered_higgs1.Phi()
          
    h2_M[0]       = tlv_ordered_higgs2.M()
    h2_Pt[0]      = tlv_ordered_higgs2.Pt()
    h2_Eta[0]     = tlv_ordered_higgs2.Eta()
    h2_Phi[0]     = tlv_ordered_higgs2.Phi()

    m_hh[0]      = tlv_DiHiggs.M()
    pT_hh[0]     = tlv_DiHiggs.Pt()
    eta_hh[0]    = tlv_DiHiggs.Eta()
    phi_hh[0]    = tlv_DiHiggs.Phi()
    
    dEta_hh[0] = tlv_ordered_higgs1.Eta() - tlv_ordered_higgs2.Eta() 
          
    # Fill the tree
    outTree.Fill()

  print('\nFinished filling tree, closing files...')

  # Close up shop
  outFile.Write()
  outFile.Close()

  os.system('gzip {0}'.format(in_file) )

  dt = time.time() - t0
  print('Finished in {0:.2f} seconds.'.format(dt))

if __name__ == "__main__":
  main()
