#!/usr/bin/env python

#  Created on: September 4, 2012
__author__ = "Sven Kreiss, Kyle Cranmer, Lukas Heinrich"
__version__ = "0.1"

import ROOT
# import pkg_resources
# ROOT.gROOT.ProcessLine('.L {}+'.format(pkg_resources.resource_filename('utils','data/loader.c')))



def flatten(e):
  for name,value in e.iteritems():
    if 'Buffer' in str(type(value)):
      e[name] = [value[i] for i in range(min(20,e[name.split('_',1)[0]+'_n']))]
  return e
       
def read(f, treeName, branchNames, max = None ):
   """ Generic function. Returns branches in tree and resolves all vectors into lists. """
   t = f.Get(treeName)
   branches = [(b,t.GetBranch(b)) for b in branchNames.split(",")]
   return [flatten({k:(b.GetEntry(i,1),getattr(t,k))[-1] for k,b in branches}) for i in xrange(t.GetEntries() if not max else max)]
