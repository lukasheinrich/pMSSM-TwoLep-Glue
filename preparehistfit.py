import ROOT
ROOT.gROOT.SetBatch(True)
import csv
import ntuplereader
import xsecinfo


LUMI = 20300.0
EL_MASS,MU_MASS = 0.510998,105.658367



def channel(e):
  l1 = e['lepton1_pdgid']
  l2 = e['lepton2_pdgid']
  if l1==11 and l2==11:
    return 'ee'
  if l1==13 and l2==13:
    return 'mm'
  if (l1==11 and l2==13) or  (l1==13 and l2==11):
    return 'em'
  return 'unknown'
  
def mktlv(event,leptonstr):
  mass_table = {11:EL_MASS,13:MU_MASS}
  pdg = leptonstr+'_pdgid'
  mass = mass_table[event[pdg]]

  v = ROOT.TLorentzVector()
  v.SetPtEtaPhiM(event[leptonstr+'_pt'],
                 event[leptonstr+'_eta'],
                 event[leptonstr+'_phi'],
                 mass)
  return v


def lumi_weight(event,targetlumi,norm_data,filtereff_data, XSEC_INFO):
  finalState = event['finalState']

  if finalState == 0:
    print "WARNING final state == 0"
    return 0
  
  if not finalState in XSEC_INFO:
    print "WARNING finalState {} not in XSEC_INFO".format(finalState)
    return 0
  
  fe = 1.0
  if filtereff_data != 'no_filter':
    if not (finalState in filtereff_data):
      print "WARNING finalState {} not in filtereff_data".format(finalState)
      return 0
    fe = filtereff_data[finalState]

  xsec = XSEC_INFO[finalState]['crossSection']
  nevents = norm_data[finalState]

  if fe == 0:
    print "WARNING for finalState {} fe == 0".format(finalState)
    return 0

  if xsec == 0:
    print "WARNING xsec for finalState {} == 0".format(finalState)
    return 0
    
  samplelumi = nevents/(xsec*fe)
  
  if samplelumi == 0:
    print "WARNING samplelumi for finalState {} == 0".format(finalState)
    return 0
    
  lumiweight = targetlumi/samplelumi

  if lumiweight == 0:
    print "WARNING final lumi weight == 0 for final State {}".format(finalState)  
    return 0
  
  return lumiweight

def total_weight(event,targetlumi,norm_data,filtereff_data, XSEC_INFO):
  lumiweight = lumi_weight(event,targetlumi,norm_data,filtereff_data, XSEC_INFO)
  all_other_weights = other_weights(event) 
  weight = all_other_weights * lumiweight
  return weight

def other_weights(event):
  other_list = [event['mc_weight'], event['pu_weight_unblind'], event['le_weight'], event['tr_weight_unblind'], event['hfor_weight'],event['bt_weight_vector'][0]]

  if any([x==0 for x in other_list]):
    print "WARNING other weights combined are null: {}".format(other_list)

  other_weights = reduce(lambda x,y:x*y,other_list)
  return other_weights

read_mini_branches = [
    'evt',
    'run',
    'lepton1_pdgid',
    'lepton1_isreal',
    'lepton1_pt',
    'lepton1_eta',
    'lepton1_phi',
    'lepton1_charge',
    'lepton2_pdgid',
    'lepton2_isreal',
    'lepton2_pt',
    'lepton2_eta',
    'lepton2_phi',
    'lepton2_charge',
    'nSignalTaus',
    'mt2',
    'metrel',
    'mll',
    'NL20',
    'NB20new',
    'NF30new',
    'mc_weight',
    'pu_weight_unblind',
    'le_weight',
    'tr_weight_unblind',
    'hfor_weight',
    'bt_weight_vector',
    'finalState',
    'jet_n',
    'jet_pt',
    'jet_eta',
    'jet_phi',
    'jet_E',
    'jet_det_eta',
    'jet_mv1',
    'jet_jvf',
]


import argparse
parser = argparse.ArgumentParser(description='Give Dilepon yields')
parser.add_argument('minifilename', type=str, help='mini ntuple filename')
parser.add_argument('eff_filename', type=str, help='filter efficiency filename')
parser.add_argument('xsec_filename', type=str, help='xsection filename')
parser.add_argument('model_name', type=str, help='model name')
parser.add_argument('outputfile', type=str, help='output file holding histfitter tree')
parser.add_argument('yieldsfile', type=str, help='file holding cumulative yields')
args = parser.parse_args()

import histfittree

def main():
  
  file = ROOT.TFile.Open(args.minifilename)
  events = ntuplereader.read(file,'none/minisusy',','.join(read_mini_branches))

  norm_histo = file.Get('none/stream_finalState_All')
  norm_data = {norm_histo.GetBinLowEdge(i+1):norm_histo.GetBinContent(i+1) for i in range(norm_histo.GetNbinsX()) 
                                          if norm_histo.GetBinContent(i+1) > 0}
  filtereff_data = {}
  if not args.eff_filename=='no_filter':
    filtereff_data = dict([(a(b) for a,b in zip((int,float),r)) for i,r in enumerate(csv.reader(open(args.eff_filename))) if i>0])
  else:
    filtereff_data = 'no_filter'  


  xsec_data = xsecinfo.xsec_info(args.xsec_filename,args.model_name)

  #file.Close()


  histfitfile = ROOT.TFile.Open(args.outputfile,'recreate')
  histfit_tree,histfit_arrays = histfittree.setup_tree()
  histfit_tree.SetDirectory(histfitfile)

  print 'processing {} events'.format( len(events))	


  #add total evt weights
  for e in events:
    lead_tlv = mktlv(e,'lepton1')
    sublead_tlv = mktlv(e,'lepton2')

    jets = zip(e['jet_E'],e['jet_pt'],e['jet_phi'],e['jet_det_eta'],e['jet_mv1'],e['jet_jvf'])
    clj = [j for j in jets if j[1]>20 and abs(j[3])<2.4 and j[4]<0.3511 and (abs(j[5])>0 or j[1]>50)]
    
    jet_tlvs = []
    for jet in clj:
    	tlv = ROOT.TLorentzVector()
    	tlv.SetPtEtaPhiE(jet[1],jet[3],jet[2],jet[0])
	jet_tlvs.append(tlv)

    totweight = total_weight(e,LUMI,norm_data,filtereff_data,xsec_data)
    lumiweight = lumi_weight(e,LUMI,norm_data,filtereff_data,xsec_data)
    otherweight = other_weights(e)


    GeVunit = 1000.

    histfit_arrays['run'][0]                 = e['run']
    histfit_arrays['evt'][0]                 = e['evt']
    histfit_arrays['otherwgts'][0]           = otherweight
    histfit_arrays['lumiwgt'][0]             = lumiweight


    histfit_arrays['lept1Pt'][0]	     = e['lepton1_pt']*GeVunit
    histfit_arrays['lept2Pt'][0] 	     = e['lepton2_pt']*GeVunit
    histfit_arrays['jet1Pt'][0] 	     = -1 if (len(clj)<1) else jet_tlvs[0].Pt()*GeVunit
    histfit_arrays['jet2Pt'][0] 	     = -1 if (len(clj)<2) else jet_tlvs[1].Pt()*GeVunit
    histfit_arrays['MT2'][0] 		     = e['mt2']*GeVunit

    histfit_arrays['isEE'][0]		     = (channel(e) == 'ee')
    histfit_arrays['isMUMU'][0] 	     = (channel(e) == 'mm')
    histfit_arrays['isEMU'][0] 		     = (channel(e) == 'em')
    histfit_arrays['isOS'][0]		     = (e['lepton1_charge']*e['lepton2_charge'] < 0)

    histfit_arrays['L2METrel'][0] 	     = e['metrel']*GeVunit
    histfit_arrays['L2Mll'][0] 		     = e['mll']*GeVunit
    
    
    relSigXSecErr = xsec_data[e['finalState']]['Tot_error']
    histfit_arrays['L2TotalWeight'][0] 	     = totweight 
    histfit_arrays['syst_XSUP'][0]          = 1+relSigXSecErr
    histfit_arrays['syst_XSDOWN'][0]        = 1-relSigXSecErr
    
    
    histfit_arrays['L2nCentralLightJets'][0] = e['NL20']
    histfit_arrays['L2nCentralBJets'][0]     = e['NB20new']
    histfit_arrays['L2nForwardJets'][0]      = e['NF30new']
    histfit_arrays['L2mJJ'][0] 		     = -1 if len(jet_tlvs)<2 else (jet_tlvs[0]+jet_tlvs[1]).M()*GeVunit
    histfit_arrays['L2dileptonpt'][0] 	     = (lead_tlv+sublead_tlv).Pt()*GeVunit
    histfit_arrays['L2dRLL'][0] 	     = lead_tlv.DeltaR(sublead_tlv)
    histfit_arrays['L2finalState'][0] 	     = e['finalState']

    histfit_tree.Fill()


  import writeYieldsQuery
  writeYieldsQuery.writeYields(histfit_tree,args.model_name,args.yieldsfile)
  
  histfitfile.Write()
  histfitfile.Close()
  
  



if __name__ == '__main__':
  main()
