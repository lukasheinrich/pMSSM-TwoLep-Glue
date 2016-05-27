import ROOT
def xsec_info(xsecfilename,modelName):
  f = ROOT.TFile.Open(xsecfilename)
  t = f.Get('SignalUncertainties')

  fields = [('modelName',int),('crossSection',float),('finalState',int),('Tot_error',float)]
  result = t.Query(':'.join(zip(*fields)[0]),"modelName == {}".format(modelName))

  data = [{f:fieldtype(row.GetField(i)) for i,(f,fieldtype) in enumerate(fields)} for row in result.GetRows()]
  dict_data = {row['finalState']:row for row in data}

  return dict_data
