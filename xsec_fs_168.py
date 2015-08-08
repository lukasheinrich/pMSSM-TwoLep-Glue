import ROOT
import sys
import glob

binoreqs = sum([open(x).readlines() for x in glob.glob('bino-*request.txt')],[])
winoreqs = sum([open(x).readlines() for x in glob.glob('wino-*request.txt')],[])

tag=sys.argv[1]
print tag

isBino=any(x for x in binoreqs if tag in x)
isWino=any(x for x in winoreqs if tag in x)

xsecfile = ''
if isBino: xsecfile='bino-xsections.root'
if isWino: xsecfile='wino-higgsino-xsections.root'



print "xsecfile: "+xsecfile
f = ROOT.TFile.Open(xsecfile)
import xsecinfo

model=sys.argv[1].split('.')[2].split('_')[5]

print model
info = xsecinfo.xsec_info(xsecfile,model)

print "{0} 168_in_info {1}".format(sys.argv[1],(168 in info))

