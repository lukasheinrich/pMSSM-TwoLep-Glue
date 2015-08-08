import xsecinfo
import csv
import glob

if __name__=='__main__':
  import sys

  allargs=sys.argv[1].split()
  dataset = allargs[0]
  finalstates = [int(x) for x in allargs[1].split(',')]
  dsid=dataset.split('.')[1]

  modelName=dataset.split('.')[2].split('_')[5]

  binoreqs = sum([open(x).readlines() for x in glob.glob('bino-*request.txt')],[])
  winoreqs = sum([open(x).readlines() for x in glob.glob('wino-*request.txt')],[])

  isBino=any(x for x in binoreqs if '.'+dsid+'.' in x)
  isWino=any(x for x in winoreqs if '.'+dsid+'.' in x)

  xsecfile = ''
  if isBino: xsecfile='bino-xsections.root'
  if isWino: xsecfile='wino-higgsino-xsections.root'

  effglob = [x for x in  glob.glob('*_effs/*') if '.{0}.'.format(dsid) in x]
  effarg = 'no_filter' if not effglob else effglob[0]

  xsec_data = xsecinfo.xsec_info(xsecfile,modelName)

  filtereff_data = {}
  if not effarg=='no_filter':
    filtereff_data = dict([(a(b) for a,b in zip((int,float),r)) for i,r in enumerate(csv.reader(open(effarg))) if i>0])
  else:
    filtereff_data = 'no_filter'  

  for x in finalstates:
    inxsec = (x in xsec_data.keys())
    ineff  = (effarg=='no_filter' or (x in filtereff_data.keys()))
    effnotnull = (effarg=='no_filter' or (ineff and filtereff_data[x]>0))
    print 'dsid: {} finalState: {} inxsec: {} ineff: {} effnotnull: {} fsnonnull: {}'.format(dsid,x,inxsec,ineff,effnotnull,x!=0)
