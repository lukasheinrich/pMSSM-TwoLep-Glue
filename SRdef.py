SRcuts = {}

SR1base = '(isOS && L2nCentralLightJets==0 && L2nCentralBJets==0 && L2nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && L2METrel>80000. && L2dileptonpt>80000.  && L2Mll<120000.)'

SRcuts['eeSR1'] = '({SR1base} && isEE && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR1base = SR1base)
SRcuts['emSR1'] = '({SR1base} && isEMU)'.format(SR1base = SR1base)
SRcuts['mmSR1'] = '({SR1base} && isMUMU && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR1base = SR1base)

SR2abase = '(isOS && L2nCentralLightJets==0 && L2nCentralBJets==0 && L2nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>90000. && L2Mll<170000)'

SRcuts['eeSR2a'] = '({SR2abase} && isEE && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR2abase = SR2abase)
SRcuts['emSR2a'] = '({SR2abase} && isEMU)'.format(SR2abase = SR2abase)
SRcuts['mmSR2a'] = '({SR2abase} && isMUMU && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR2abase = SR2abase)


SR2bbase = '(isOS && L2nCentralLightJets==0 && L2nCentralBJets==0 && L2nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>100000. )'

SRcuts['eeSR2b'] = '({SR2bbase} && isEE && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR2bbase = SR2bbase)
SRcuts['emSR2b'] = '({SR2bbase} && isEMU)'.format(SR2bbase = SR2bbase)
SRcuts['mmSR2b'] = '({SR2bbase} && isMUMU && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR2bbase = SR2bbase)


SR4abase = '(isOS && L2nCentralLightJets==0 && L2nCentralBJets==0 && L2nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>90000.)'

SRcuts['eeSR4a'] = '({SR4abase} && isEE && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR4abase = SR4abase)
SRcuts['emSR4a'] = '({SR4abase} && isEMU)'.format(SR4abase = SR4abase)
SRcuts['mmSR4a'] = '({SR4abase} && isMUMU && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR4abase = SR4abase)


SR4bbase = '(isOS && L2nCentralLightJets==0 && L2nCentralBJets==0 && L2nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>120000.)'

SRcuts['eeSR4b'] = '({SR4bbase} && isEE && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR4bbase = SR4bbase)
SRcuts['emSR4b'] = '({SR4bbase} && isEMU)'.format(SR4bbase = SR4bbase)
SRcuts['mmSR4b'] = '({SR4bbase} && isMUMU && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR4bbase = SR4bbase)


SR4cbase = '(isOS && L2nCentralLightJets==0 && L2nCentralBJets==0 && L2nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>150000.)'
SRcuts['eeSR4c'] = '({SR4cbase} && isEE && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR4cbase = SR4cbase)
SRcuts['emSR4c'] = '({SR4cbase} && isEMU)'.format(SR4cbase = SR4cbase)
SRcuts['mmSR4c'] = '({SR4cbase} && isMUMU && !(L2Mll>81187.6 && L2Mll<101187.6))'.format(SR4cbase = SR4cbase)


SR5abase = '((isEE || isMUMU) && isOS && lept1Pt>35000. && lept2Pt>20000. && L2nCentralLightJets>1 && L2nForwardJets==0 && L2nCentralBJets==0 && L2METrel>80000. && L2Mll>81187.6 && L2Mll<101187.6 && L2dileptonpt>80000. && L2dRLL>0.3 && L2dRLL<1.5 && L2mJJ>50000 && L2mJJ<100000 && jet1Pt>45000 && jet2Pt>45000)'

SRcuts['eeSR5a'] = '({SR5abase} && isEE)'.format(SR5abase = SR5abase)
SRcuts['emSR5a'] = '({SR5abase} && isEMU)'.format(SR5abase = SR5abase)
SRcuts['mmSR5a'] = '({SR5abase} && isMUMU)'.format(SR5abase = SR5abase)
