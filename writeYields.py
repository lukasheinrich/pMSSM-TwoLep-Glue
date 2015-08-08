import ROOT
import SRdef

def getchannelcount(tree,cuts):
  h = ROOT.TH1F('hist','hist',2,0,2)
  tree.Project('hist','isOS','{}*L2TotalWeight'.format(cuts))
  return h.GetSumOfWeights()
  
def formatcounts(counts):
  return 'ee: {ee}, mm: {mm}, em: {em}, sum: {sum}'.format(**counts)

def writeYields(tree,model,filename):
  ournames = ['SRmT2a','SRmT2b','SRmT2c','SRWWa','SRWWb','SRWWc','SRZjets']
  SRs = ['SR4a','SR4b','SR4c','SR1','SR2a','SR2b','SR5a']
  flav = ['ee','em','mm']

  channel_counts = {}
  for SR,ourname in zip(SRs,ournames):
    channel_counts[ourname] = {f:getchannelcount(tree,SRdef.SRcuts[f+SR]) for f in flav}
    channel_counts[ourname].update(sum = sum(channel_counts[ourname].values()))
    print "{}: {}".format(ourname,formatcounts(channel_counts[ourname]))


  with open(filename,'w') as yieldsfile:
    yieldsfile.write('Model'+','+','.join(ournames)+'\n')
    yieldsfile.write(str(model) +','+','.join([str(channel_counts[name]['sum']) for name in ournames])+'\n')
