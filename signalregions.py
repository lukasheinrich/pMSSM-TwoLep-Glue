import ROOT
ROOT.gROOT.SetBatch(True)
import csv
import ntuplereader
import xsecinfo


LUMI = 20300.0
EL_MASS,MU_MASS = 0.510998,105.658367



def compose(*args):
  return lambda event: all(x(event) for x in args)

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
  

def count(events, weighted = True):
  return sum(e['total_weight'] if weighted else 1 for e in events)

def channel_counts(events, weighted = True):
    resolved =  {c:count(filter(lambda e:channel(e)==c,events),weighted) for c in ['ee','mm','em']}
    resolved.update(sum = sum(resolved.values()))
    return resolved
    
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


def total_weight(event,targetlumi,norm_data,filtereff_data, XSEC_INFO):
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

  if xsec == 0:
    print "WARNING xsec == 0"
    return 0
    
  samplelumi = nevents/(xsec*fe)
  
  if samplelumi == 0:
    print "WARNING samplelumi == 0"
    return 0
    

  lumiweight = targetlumi/samplelumi

  print "FS: {} FE: {} XSEC: {} NEV: {} LUMWGT: {}".format(finalState,fe,xsec,nevents,lumiweight)
    
  other_weights = event['mc_weight']* \
                  event['pu_weight_unblind']* \
                  event['le_weight']* \
                  event['tr_weight_unblind']* \
                  event['hfor_weight']* \
                  event['bt_weight_vector'][0]
  
  print "pileup: {}".format(event['pu_weight_unblind'])
  print "le_weight: {}".format(event['le_weight'])
  print "tr_weight_unblind: {}".format(event['tr_weight_unblind'])
  print "hfor_weight: {}".format(event['hfor_weight'])
  print "bt_weight_vector: {}".format(event['bt_weight_vector'][0])
  print "all other weights: {}".format(other_weights)
    
  weight = other_weights * lumiweight

  return weight


import argparse

parser = argparse.ArgumentParser(description='Give Dilepon yields')
parser.add_argument('minifilename', type=str, help='mini ntuple filename')
parser.add_argument('eff_filename', type=str, help='filter efficiency filename')
parser.add_argument('model_name', type=str, help='model name')
args = parser.parse_args()

def main():
  branches = [
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
  
  file = ROOT.TFile.Open(args.minifilename)
  events = ntuplereader.read(file,'none/minisusy',','.join(branches))


  print len(events)

  norm_histo = file.Get('none/stream_finalState_All')
  norm_data = {norm_histo.GetBinLowEdge(i+1):norm_histo.GetBinContent(i+1) for i in range(norm_histo.GetNbinsX()) 
                                          if norm_histo.GetBinContent(i+1) > 0}

  
  filtereff_data = {}
  if not args.eff_filename=='no_filter':
    filtereff_data = dict([(a(b) for a,b in zip((int,float),r)) for i,r in enumerate(csv.reader(open(args.eff_filename))) if i>0])
  else:
    filtereff_data = 'no_filter'  


  XSEC_INFO = xsecinfo.xsec_info('./xsections.root',args.model_name)

  #add total evt weights
  for e in events:
    e.update(total_weight = total_weight(e,LUMI,norm_data,filtereff_data,XSEC_INFO))
  
  cuts = [
    ('trig',  lambda e: True),
    ('tau',   lambda e:  e['nSignalTaus'] == 0),
    ('prompt',lambda e:  e['lepton1_isreal']==1.0 and e['lepton2_isreal']==1.0),
    ('pT',lambda e: e['lepton1_pt']>35 and e['lepton2_pt']>20),
    ('OS',lambda e: e['lepton1_charge']*e['lepton2_charge'] < 0),
  ]

  allcuts = zip(*cuts)[-1]

  
  def mT2_region(cut):    
    def selection(event):
      chan   = channel(event)
      zveto  = (abs(event['mll']-91.2) > 10) or (chan == 'em')
      metrel = event['metrel'] > 40
      mt2    = event['mt2'] > cut
      jetveto = event['NL20']==0 and event['NB20new']==0 and event['NF30new']==0
      return zveto and metrel and mt2 and jetveto
    return selection
  
  def SRWWa(event):
    chan   = channel(event)
    lead_tlv = mktlv(event,'lepton1')
    sublead_tlv = mktlv(event,'lepton2')

    zveto  = (abs(event['mll']-91.2) > 10) or (chan == 'em')
    jetveto = event['NL20']==0 and event['NB20new']==0 and event['NF30new']==0

    ptll = (lead_tlv+sublead_tlv).Pt() > 80
    metrel = event['metrel'] > 80

    mll = event['mll'] < 120
    delphi = lead_tlv.DeltaPhi(sublead_tlv) < 2.0
    return zveto and jetveto and ptll and metrel and mll and delphi
    

  def SRWWb(event):
    chan   = channel(event)
    lead_tlv = mktlv(event,'lepton1')
    sublead_tlv = mktlv(event,'lepton2')

    zveto  = (abs(event['mll']-91.2) > 10) or (chan == 'em')
    jetveto = event['NL20']==0 and event['NB20new']==0 and event['NF30new']==0

    mt2    = event['mt2'] > 90

    mll = event['mll'] < 170
    delphi = lead_tlv.DeltaPhi(sublead_tlv) < 2.0
    
    return zveto and jetveto and mt2 and mll and delphi

  def SRWWc(event):
    chan   = channel(event)
    lead_tlv = mktlv(event,'lepton1')
    sublead_tlv = mktlv(event,'lepton2')
    
    zveto  = (abs(event['mll']-91.2) > 10) or (chan == 'em')
    
    jetveto = event['NL20']==0 and event['NB20new']==0 and event['NF30new']==0

    mt2    = event['mt2'] > 100
    delphi = lead_tlv.DeltaPhi(sublead_tlv) < 2.0
    
    return zveto and jetveto and mt2 and delphi

  def SRZjets_decisions(event):
    chan   = channel(event)
    lead_tlv = mktlv(event,'lepton1')
    sublead_tlv = mktlv(event,'lepton2')
    
    jets = zip(event['jet_E'],event['jet_pt'],event['jet_phi'],event['jet_det_eta'],event['jet_mv1'],event['jet_jvf'])
    clj = [j for j in jets if j[1]>20 and abs(j[3])<2.4 and j[4]<0.3511 and (abs(j[5])>0 or j[1]>50)]
    zregion_jets = [j for j in clj if j[1]>45]

    zregion_jets_cut = len(zregion_jets)>=2
    if not zregion_jets_cut:
      return [False]

    tlv_leadjet = ROOT.TLorentzVector()
    tlv_leadjet.SetPtEtaPhiE(clj[0][1],clj[0][3],clj[0][2],clj[0][0])

    tlv_subleadjet = ROOT.TLorentzVector()
    tlv_subleadjet.SetPtEtaPhiE(clj[1][1],clj[1][3],clj[1][2],clj[1][0])
    
    zwindow  = (abs(event['mll']-91.2) < 10) and (chan != 'em')
    jetveto = event['NB20new']==0 and event['NF30new']==0

    mjj = 50 < (tlv_leadjet+tlv_subleadjet).M() < 100
    metrel = event['metrel'] > 80
    dRll = 0.3 < lead_tlv.DeltaR(sublead_tlv) < 1.5
    ptll = (lead_tlv+sublead_tlv).Pt() > 80
    
    return [zregion_jets_cut,jetveto,zwindow,mjj,metrel,dRll, ptll]

  def SRZjets(event):
    return all(SRZjets_decisions(event))

    
  SR_list = [('SRmT2a',mT2_region(90)),
             ('SRmT2b',mT2_region(120)),
             ('SRmT2c',mT2_region(150)),
             ('SRWWa',SRWWa),
             ('SRWWb',SRWWb),
             ('SRWWc',SRWWc),
             ('SRZjets',SRZjets)]

  preCuts_events = [(name, filter(compose(*zip(*cuts)[-1][0:i+1]),events)) for i,(name,selector) in enumerate(cuts) ]
  SR_events      = [(name, filter(compose(*(allcuts+(selector,))),events)) for name,selector in SR_list]
  
  weighted = True
  for name,pre_events in preCuts_events:
    print "{}: {}".format(name, channel_counts(pre_events,weighted).values())

  print '-=-=-=-=-=-=-=-=-='
  for name,sr_events in SR_events:
    print "{}: {}".format(name, channel_counts(sr_events,weighted).values())
              
  
  srcounts = [(name,count(sr_events,weighted)) for name,sr_events in SR_events]

  print 'Brian:'+'Model,'+','.join(str(x) for x in zip(*srcounts)[0])
  print 'Brian:'+args.model_name+','+','.join(str(x) for x in zip(*srcounts)[1])

  print "zjets"
  zjet_evts = filter(compose(*(allcuts+(SRZjets,))),events)
  for e in zjet_evts:
    print "channel: {}".format(channel(e))
    print total_weight(e,LUMI,norm_data,filtereff_data,XSEC_INFO)  

  decisions = [SRZjets_decisions(e) for e in events]

  for i,name in enumerate(['common cuts','central jets', 'jet veto', 'z window', 'mjj', 'metrel', 'dRll', 'ptLL']):
    print name+': {}'.format(channel_counts([e for dec,e in zip(decisions,events) if all(cut(e) for cut in allcuts) and all(dec[:i])]))

  def xcheck_jets(event):
    jets = zip(event['jet_E'],event['jet_pt'],event['jet_phi'],event['jet_det_eta'],event['jet_mv1'],event['jet_jvf'])
    clj = [j for j in jets if j[1]>20 and abs(j[3])<2.4 and j[4]<0.3511 and (abs(j[5])>0 or j[1]>50)]
    print 'me: {}, stockholm: {}, same: {}'.format(len(clj),event['NL20'], len(clj) == event['NL20'])

  #for e in events:
  #  xcheck_jets(e)

if __name__ == '__main__':
  main()
