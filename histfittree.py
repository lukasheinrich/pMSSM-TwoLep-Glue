import ROOT
import array

branch_defs = [  
  ('Float_t','lept1Pt'),
  ('Float_t','lept2Pt'),
  ('Float_t','jet1Pt'),
  ('Float_t','jet2Pt'),
  ('Float_t','MT2'),

  ('Bool_t','isEMU'),
  ('Bool_t','isMUMU'),
  ('Bool_t','isEE'),
  ('Bool_t','isOS'),

  ('Float_t','L2METrel'),
  ('Float_t','L2Mll'),
  ('Double_t','L2TotalWeight'),
  ('Int_t','L2nCentralLightJets'),
  ('Int_t','L2nCentralBJets'),
  ('Int_t','L2nForwardJets'),
  ('Float_t','L2mJJ'),
  ('Float_t','L2dileptonpt'),
  ('Float_t','L2dRLL'),
  ('Int_t','L2finalState'),
  ('Int_t','run'),
  ('Int_t','evt'),
  ('Double_t','otherwgts'),
  ('Double_t','lumiwgt'),

]

typemapping = {'Bool_t':'b', 'Double_t':'d', 'Float_t':'f', 'Int_t':'i'}
leafmapping = {'Bool_t':'O', 'Double_t':'D', 'Float_t':'F', 'Int_t':'I'}

def setup_tree():
  t = ROOT.TTree('DGemt100_120_160_CENTRAL','DGemt100_120_160_CENTRAL')
  arrays = {name:(array.array(typemapping[t],(0,)),'{}/{}'.format(name,leafmapping[t])) for t,name in branch_defs}
  for name,(arr,leaf) in arrays.iteritems():
    t.Branch(name,arr,leaf)
    t.SetBranchAddress(name,arr)

  return t,{name:arr for  name,(arr,leaf) in arrays.iteritems()}

