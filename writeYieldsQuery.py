import ROOT
import SRdef

def getchannelcount(tree,cuts):
  r = tree.Query('lumiwgt:L2finalState',cuts)
  selected_weights = [float(row.GetField(0)) for row in r.GetRows()]
  selected_finalstate = [float(row.GetField(1)) for row in r.GetRows()]
  n_null = len([(w,fs) for w,fs in zip(selected_weights,selected_finalstate) if w == 0])

  if n_null:
    print "WARNING: {}/{} selected events have lumi weight null".format(n_null,len(selected_weights))
    print "DEBUG: set of null weight fs:  {}".format(','.join(list(set([str(int(fs)) for w,fs in zip(selected_weights,selected_finalstate) if w ==0]))))
  return sum(selected_weights)
  
def formatcounts(counts):
  return 'ee: {ee}, mm: {mm}, em: {em}, sum: {sum}'.format(**counts)

def writeYields(tree,model,filename):
  ournames = ['SR-mT2a','SR-mT2b','SR-mT2c','SR-WWa','SR-WWb','SR-WWc','SR-Zjets']
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
