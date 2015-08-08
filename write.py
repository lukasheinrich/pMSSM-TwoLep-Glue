import ROOT
import numpy

def setup_tree(templatefilename):
  typemapping = {'Bool_t':'b', 'Double_t':'d', 'Float_t':'f', 'Int_t':'i'}


  f = ROOT.TFile.Open(templatefilename)
  t = f.Get('id_0')
  t.SetDirectory(0)
  f.Close()

  branch_data = dict([(b.GetName(),[l for l in b.GetListOfLeaves()][0].GetTypeName()) for b in t.GetListOfBranches()])

  arrays = {k:numpy.array((1,),dtype = typemapping[v]) for k,v in branch_data.iteritems()}
  
  for name,array in arrays.iteritems():
    t.SetBranchAddress(name,array)
  
  return t,arrays
